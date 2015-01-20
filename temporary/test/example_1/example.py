from os import getcwd
from os.path import exists
from temporary import temp_dir

with temp_dir(make_cwd=True) as d:
    assert d == getcwd()

assert not exists(d)
assert d != getcwd()
