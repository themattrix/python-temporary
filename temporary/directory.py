from contextlib import contextmanager
from errno import ENOENT
from os import chdir, getcwd
from shutil import rmtree
from tempfile import mkdtemp


@contextmanager
def temp_dir(suffix='', prefix='tmp', parent_dir=None, make_cwd=False):
    """
    Create a temporary directory, and optionally change the current working
    directory to it. The directory is deleted when the context exits.

    Let's start by importing a few helper methods:
    >>> from os import getcwd
    >>> from os.path import basename, dirname, exists, isdir

    The temporary directory is created when entering the context manager, and
    deleted when exiting it:
    >>> with temp_dir() as d:
    ...     assert isdir(d)
    >>> assert not exists(d)

    This time let's make the temporary directory our working directory:
    >>> with temp_dir(make_cwd=True) as d:
    ...     assert d == getcwd()
    >>> assert d != getcwd()

    The suffix, prefix, and parent_dir options are passed to the standard
    tempfile.mkdtemp() function:
    >>> with temp_dir() as p:
    ...     with temp_dir(suffix='suf', prefix='pre', parent_dir=p) as d:
    ...         assert dirname(d) == p
    ...         assert basename(d).startswith('pre')
    ...         assert basename(d).endswith('suf')
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
