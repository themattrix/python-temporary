from contextlib2 import contextmanager
from os import chdir, getcwd
from shutil import rmtree
from tempfile import mkdtemp


@contextmanager
def temp_dir(suffix='', prefix='tmp', parent_dir=None, make_cwd=False):
    prev_cwd = getcwd()
    abs_path = mkdtemp(suffix, prefix, parent_dir)
    try:
        if make_cwd:
            chdir(abs_path)
        yield abs_path
    finally:
        if make_cwd:
            chdir(prev_cwd)
        rmtree(abs_path)
