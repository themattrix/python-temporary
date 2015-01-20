from contextlib import contextmanager
from errno import ENOENT
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
        try:
            rmtree(abs_path)
        except OSError as e:
            if e.errno != ENOENT:
                raise
