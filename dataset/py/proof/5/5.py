import environment
import os

class CorpusPruningException(Exception):
  """Corpus pruning exception."""

class Runner(object):
    """Runner for libFuzzer."""

    def __init__(self, build_directory):
        self.build_directory = build_directory
        self.target_path = self.find_fuzzer_path(self.build_directory)

        #Existing check in Runner Constructor
        if not self.target_path:
          raise CorpusPruningException(
              'Failed to get fuzzer path for %s.' % self.context.fuzz_target.binary)

    def find_fuzzer_path(build_directory, fuzzer_name):
        """Find the fuzzer path with the given name."""
        if not build_directory:
            logs.log_warn('No build directory found for fuzzer: %s' % fuzzer_name)
            return None

        return "/my/path/" #simplified
         

def with_check(build_setup_result):
    build_directory = environment.get_value('BUILD_DIR')
    if not build_setup_result or not build_directory: #line under question
        raise CorpusPruningException('Failed to setup build.')

    runner = Runner(build_directory)

def without_check(build_setup_result):
    build_directory = environment.get_value('BUILD_DIR')
    if not build_setup_result or not build_directory: #edit suggested by the PR comment
        raise CorpusPruningException('Failed to setup build.')

    runner = Runner(build_directory)


build_setup_result = True
os.environ["BUILD_DIR"] = "/my/build/dir/"
print("build_setup_result = True, BUILD_DIR set")
#Both versions are non-exceptional
with_check(build_setup_result)
without_check(build_setup_result)

del os.environ["BUILD_DIR"] 
print("build_setup_result = True, BUILD_DIR NOT set")

v1_failed, v2_failed = False, False
try:
    with_check(build_setup_result)
except:
    v1_failed = True

try:
    without_check(build_setup_result)
except:
    v2_failed = True

assert v1_failed and v2_failed
