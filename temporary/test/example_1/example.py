import os
import os.path

import temporary

with temporary.temp_dir(make_cwd=True) as d:
    assert d == os.getcwd()

assert not os.path.exists(d)
assert d != os.getcwd()
