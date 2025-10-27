import math
import logging
import operator

from collections import defaultdict
from collections import Counter


class BetterDict(defaultdict):
    """
    Wrapper for defaultdict that able to deep merge other dicts into itself

    :param kwargs:
    """

    def __init__(self, **kwargs):
        super(BetterDict, self).__init__(**kwargs)

    def get(self, key, default=defaultdict):
        """
        Change get with setdefault

        :type key: object
        :type default: object
        """
        if default == defaultdict:
            default = BetterDict()

        if isinstance(default, BaseException) and key not in self:
            raise default

        value = self.setdefault(key, default)

        if isinstance(value, str):
            if isinstance(value, str):  # this is a trick for python v2/v3 compatibility
                return value
            else:
                return text_type(value)
        else:
            return value

    def merge(self, src):
        """
        Deep merge other dict into current
        '-'  - overwrite operation prefix for dict key

        :type src: dict
        """
        if not isinstance(src, dict):
            raise TaurusInternalException("Loaded object is not dict [%s]: %s" % (src.__class__, src))

        for key, val in iteritems(src):
            if len(key) and key[0] == '~':  # overwrite flag
                if key[1:] in self:
                    self.pop(key[1:])
                key = key[1:]

            if len(key) and key[0] == '^':  # eliminate flag
                # TODO: improve logic - use val contents to see what to eliminate
                if key[1:] in self:
                    self.pop(key[1:])
                continue

            if isinstance(val, dict):
                dst = self.get(key)
                if isinstance(dst, BetterDict):
                    dst.merge(val)
                elif isinstance(dst, Counter):
                    self[key] += val
                elif isinstance(dst, dict):
                    raise TaurusInternalException("Mix of DictOfDict and dict is forbidden")
                else:
                    self[key] = val
            elif isinstance(val, list):
                self.__ensure_list_type(val)
                if key not in self:
                    self[key] = []
                if isinstance(self[key], list):
                    self[key].extend(val)
                else:
                    self[key] = val
            else:
                self[key] = val

    def __ensure_list_type(self, values):
        """
        Ensure that values is a list, convert if needed
        :param values: dict or list
        :return:
        """
        for idx, obj in enumerate(values):
            if isinstance(obj, dict):
                values[idx] = BetterDict()
                values[idx].merge(obj)
            elif isinstance(obj, list):
                self.__ensure_list_type(obj)

    @classmethod
    def traverse(cls, obj, visitor):
        """
        Deep traverse dict with visitor

        :type obj: list or dict or object
        :type visitor: callable
        """
        if isinstance(obj, dict):
            for key, val in iteritems(obj):
                visitor(val, key, obj)
                cls.traverse(obj[key], visitor)
        elif isinstance(obj, list):
            for idx, val in enumerate(obj):
                visitor(val, idx, obj)
                cls.traverse(obj[idx], visitor)


class KPISet(BetterDict):
    """
    Main entity in results, contains all KPIs for single label,
    capable of merging other KPISet's into it to compose cumulative results
    """
    ERRORS = "errors"
    SAMPLE_COUNT = "throughput"
    CONCURRENCY = "concurrency"
    SUCCESSES = "succ"
    FAILURES = "fail"
    BYTE_COUNT = "bytes"
    RESP_TIMES = "rt"
    AVG_RESP_TIME = "avg_rt"
    STDEV_RESP_TIME = "stdev_rt"
    AVG_LATENCY = "avg_lt"
    AVG_CONN_TIME = "avg_ct"
    PERCENTILES = "perc"
    RESP_CODES = "rc"
    ERRTYPE_ERROR = 0
    ERRTYPE_ASSERT = 1

    def __init__(self, perc_levels=()):
        super(KPISet, self).__init__()
        self.sum_rt = 0
        self.sum_lt = 0
        self.sum_cn = 0
        self.perc_levels = perc_levels
        # scalars
        self.get(self.SAMPLE_COUNT, 0)
        self.get(self.CONCURRENCY, 0)
        self.get(self.SUCCESSES, 0)
        self.get(self.FAILURES, 0)
        self.get(self.AVG_RESP_TIME, 0)
        self.get(self.STDEV_RESP_TIME, 0)
        self.get(self.AVG_LATENCY, 0)
        self.get(self.AVG_CONN_TIME, 0)
        self.get(self.BYTE_COUNT, 0)
        # vectors
        self.get(self.ERRORS, [])
        self.get(self.RESP_TIMES, Counter())
        self.get(self.RESP_CODES, Counter())
        self.get(self.PERCENTILES)
        self._concurrencies = BetterDict()  # NOTE: shouldn't it be Counter?
        self.rt_dist_maxlen = 1000  # TODO: parameterize it

    def __deepcopy__(self, memo):
        mycopy = KPISet(self.perc_levels)
        mycopy.sum_rt = self.sum_rt
        mycopy.sum_lt = self.sum_lt
        mycopy.sum_cn = self.sum_cn
        for key, val in iteritems(self):
            mycopy[key] = copy.deepcopy(val, memo)
        return mycopy

    def recalculate(self, do_compact):
        """
        Recalculate averages, stdev and percentiles

        :return:
        """
        if do_compact:
            self._compact_times() #Line in question -> This is removed after the comment


        if self[self.SAMPLE_COUNT]:
            self[self.AVG_CONN_TIME] = self.sum_cn / self[self.SAMPLE_COUNT]
            self[self.AVG_LATENCY] = self.sum_lt / self[self.SAMPLE_COUNT]
            self[self.AVG_RESP_TIME] = self.sum_rt / self[self.SAMPLE_COUNT]

        if len(self._concurrencies):
            self[self.CONCURRENCY] = sum(self._concurrencies.values())

        perc, stdev = self.__perc_and_stdev(self[self.RESP_TIMES], self.perc_levels, self[self.AVG_RESP_TIME])
        for level, val in perc:
            self[self.PERCENTILES][str(float(level))] = val

        self[self.STDEV_RESP_TIME] = stdev

        return self

    def _compact_times(self):
        times = self[KPISet.RESP_TIMES]
        redundant_cnt = len(times) - self.rt_dist_maxlen
        if redundant_cnt > 0:
            logging.debug("Compacting %s response timing into %s", len(times), self.rt_dist_maxlen)

        while redundant_cnt > 0:
            keys = sorted(times.keys())
            distances = [(lidx, keys[lidx + 1] - keys[lidx]) for lidx in range(len(keys) - 1)]
            distances.sort(key=operator.itemgetter(1))  # sort by distance

            # cast candidates for consolidation
            lkeys_indexes = [lidx for lidx, _ in distances[:redundant_cnt]]

            while lkeys_indexes:
                lidx = lkeys_indexes.pop(0)
                lkey = keys[lidx]
                rkey = keys[lidx + 1]
                if lkey in times and rkey in times:  # neighbours aren't changed
                    lval = times.pop(lkey)
                    rval = times.pop(rkey)

                    # shift key proportionally to values
                    idx_new = lkey + (rkey - lkey) * float(rval) / (lval + rval)

                    # keep precision the same
                    lprec = len(str(math.modf(lkey)[0])) - 2
                    rprec = len(str(math.modf(rkey)[0])) - 2
                    idx_new = round(idx_new, max(lprec, rprec))

                    times[idx_new] = lval + rval
                    redundant_cnt -= 1

    def merge_kpis(self, src, sid=None):
        """
        Merge other instance into self

        :param sid: source ID to use when suming up concurrency
        :type src: KPISet
        :return:
        """
        src.recalculate(True)

        self.sum_cn += src.sum_cn
        self.sum_lt += src.sum_lt
        self.sum_rt += src.sum_rt

        self[self.SAMPLE_COUNT] += src[self.SAMPLE_COUNT]
        self[self.SUCCESSES] += src[self.SUCCESSES]
        self[self.FAILURES] += src[self.FAILURES]
        self[self.BYTE_COUNT] += src[self.BYTE_COUNT]
        # NOTE: should it be average? mind the timestamp gaps
        if src[self.CONCURRENCY]:
            self._concurrencies[sid] = src[self.CONCURRENCY]

        if src[self.RESP_TIMES]:
            # using raw times to calculate percentiles
            self[self.RESP_TIMES].update(src[self.RESP_TIMES])
        elif not self[self.PERCENTILES]:
            # using existing percentiles
            # FIXME: it's not valid to overwrite, better take average
            self[self.PERCENTILES] = copy.deepcopy(src[self.PERCENTILES])

        self[self.RESP_CODES].update(src[self.RESP_CODES])

        for src_item in src[self.ERRORS]:
            self.inc_list(self[self.ERRORS], ('msg', src_item['msg']), src_item)

    @staticmethod
    def __perc_and_stdev(cnts_dict, percentiles_to_calc=(), avg=0):
        """
        from http://stackoverflow.com/questions/25070086/percentiles-from-counts-of-values
        Returns [(percentile, value)] with nearest rank percentiles.
        Percentile 0: <min_value>, 100: <max_value>.
        cnts_dict: { <value>: <count> }
        percentiles_to_calc: iterable for percentiles to calculate; 0 <= ~ <= 100

        upd: added stdev calc to have it in single-pass for mans of efficiency

        :type percentiles_to_calc: list(float)
        :type cnts_dict: collections.Counter
        """
        assert all(0 <= percentile <= 100 for percentile in percentiles_to_calc)
        percentiles = []
        if not cnts_dict:
            return percentiles, 0

        num = sum(cnts_dict.values())
        cnts = sorted(cnts_dict.items())
        curr_cnts_pos = 0  # current position in cnts
        curr_pos = cnts[0][1]  # sum of freqs up to current_cnts_pos

        sqr_diffs = 0
        for percentile in sorted(percentiles_to_calc):
            if percentile < 100:
                percentile_pos = percentile / 100.0 * num
                while curr_pos <= percentile_pos and curr_cnts_pos < len(cnts):
                    sqr_diffs += cnts[curr_cnts_pos][1] * math.pow(cnts[curr_cnts_pos][0] - avg, 2)

                    curr_cnts_pos += 1
                    curr_pos += cnts[curr_cnts_pos][1]

                percentiles.append((percentile, cnts[curr_cnts_pos][0]))
            else:
                percentiles.append((percentile, cnts[-1][0]))  # we could add a small value

        while curr_cnts_pos < len(cnts):
            sqr_diffs += cnts[curr_cnts_pos][1] * math.pow(cnts[curr_cnts_pos][0] - avg, 2)
            curr_cnts_pos += 1

        stdev = math.sqrt(sqr_diffs / len(cnts))
        return percentiles, stdev
