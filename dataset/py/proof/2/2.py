from random import random
from KPISet import KPISet

'''
    Rubric Item 1:
        1. cumulative KPISet is created by merging 2 or more KPISets
        2. duplicates can still exist in a cumulative KPISet
        3. both cumulative and non-cumulative KPISets exist over finite time values

    Rubric Item 2:
        1. compact_times combines elements
        2. duplicates can occur before and after calling compact_times
        3. calling compact_times on a non-cumulative set does not affect percentile and stddev computations
'''

def test_kpiset_simple():
    vals = {round(random() * 20 + 0.1, int(random() * 3) + 2): int(random() * 3 + 1) for _ in range(10)}
    src = KPISet() #compact times is called here
    src[KPISet.RESP_TIMES].update(vals) #src is a KPISet with 1k random values
    src.recalculate(False) 

    dst = KPISet()
    dst.rt_dist_maxlen = 5
    print("Non-cumlative KPISet: ")
    print("\tNumber of Values:", len(src['rt']))
    print("\tValues:", src['rt']) 
    print("\tDuplicates? ", any(count > 1 for count in src['rt'].values())) #any value > 1 in the counter shows there are duplicates
    print("\tPercentiles:", src["perc"])
    print("\tStd dev:", src["stdev_rt"])

    src.recalculate(True) #call compact_times
    print("After compact times: ")
    print("\tPercentiles:", src["perc"])
    print("\tStd dev:", src["stdev_rt"])

    dst.merge_kpis(src) #DST is now a cumulative KPISet. compact_times called here
    print("Cumulative KPISet: ")
    print("\tNumber of Values:", len(dst['rt']))
    print("\tValues:", dst['rt']) 
    print("\tDuplicates? ", any(count > 1 for count in dst['rt'].values())) #any value > 1 in the counter shows there are duplicates
    print("\tPercentiles:", src["perc"])
    print("\tStd dev:", src["stdev_rt"])



def test_kpiset_merge_many_rt():
    vals = {round(random() * 20 + 0.1, int(random() * 3) + 2): int(random() * 3 + 1) for _ in range(1000)}
    src = KPISet() #compact times is called here
    src[KPISet.RESP_TIMES].update(vals) #src is a KPISet with 1k random values

    dst = KPISet()
    dst.rt_dist_maxlen = 100
    print("Non-cumlative KPISet: ")
    print("\tNumber of values:", len(src['rt'])) 
    print("\tDuplicates? ", any(count > 1 for count in src['rt'].values())) #any value > 1 in the counter shows there are duplicates

    for _ in range(10):
        dst.merge_kpis(src)
        dst.recalculate(True)  #compact times is called here
        print("Cumulative KPISet: ")
        print("\tNumber of values:", len(dst['rt'])) 
        print("\tDuplicates? ", any(count > 1 for count in dst['rt'].values())) #any value > 1 in the counter shows there are duplicates

        assert 100 == len(dst[KPISet.RESP_TIMES])



test_kpiset_merge_many_rt()
print()
print("Simple test")
test_kpiset_simple()
