from os.path import exists, isdir
from nose.tools import eq_
from temporary import temp_dir


#
# Tests
#

def test_temp_dir():
    for x in __ensure_usage():
        yield x


#
# Test Helpers
#

def __ensure_usage(**kwargs):
    def ensure_context_manager():
        with temp_dir(**kwargs) as d:
            eq_(isdir(d), True)
        eq_(exists(d), False)

    def ensure_decorator():
        @temp_dir(**kwargs)
        def inner():
            pass

        inner()

    yield ensure_context_manager
    yield ensure_decorator
