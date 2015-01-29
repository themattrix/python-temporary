from contextlib2 import contextmanager
from errno import ENOENT
from functools import partial
from os import chdir, getcwd
from shutil import rmtree
from tempfile import mkdtemp


@contextmanager
def temp_dir(suffix='', prefix='tmp', parent_dir=None, make_cwd=False):
    """
    Create a temporary directory and optionally change the current working
    directory to it. The directory is deleted when the context exits.

    The temporary directory is created when entering the context manager, and
    deleted when exiting it:
    >>> from os.path import exists, isdir
    >>> with temp_dir() as d:
    ...     assert isdir(d)
    >>> assert not exists(d)

    This time let's make the temporary directory our working directory:
    >>> from os import getcwd
    >>> with temp_dir(make_cwd=True) as d:
    ...     assert d == getcwd()
    >>> assert d != getcwd()

    The suffix, prefix, and parent_dir options are passed to the standard
    tempfile.mkdtemp() function:
    >>> from os.path import basename, dirname
    >>> with temp_dir() as p:
    ...     with temp_dir(suffix='suf', prefix='pre', parent_dir=p) as d:
    ...         assert dirname(d) == p
    ...         assert basename(d).startswith('pre')
    ...         assert basename(d).endswith('suf')

    This function can also be used as a decorator, with the in_temp_dir alias:
    >>> @in_temp_dir()
    ... def my_function():
    ...     assert old_cwd != getcwd()
    ...
    >>> old_cwd = getcwd()
    >>> my_function()
    >>> assert old_cwd == getcwd()
    """
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


in_temp_dir = partial(temp_dir, make_cwd=True)  # pylint: disable=invalid-name
