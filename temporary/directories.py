import functools
import os
import shutil
import tempfile

import contextlib2 as contextlib

import temporary.util


@contextlib.contextmanager
def temp_dir(suffix='', prefix='tmp', parent_dir=None, make_cwd=False):
    """
    Create a temporary directory and optionally change the current
    working directory to it. The directory is deleted when the context
    exits.

    The temporary directory is created when entering the context
    manager, and deleted when exiting it:
    >>> import os.path
    >>> import temporary
    >>> with temporary.temp_dir() as d:
    ...     assert os.path.isdir(d)
    >>> assert not os.path.exists(d)

    This time let's make the temporary directory our working directory:
    >>> import os
    >>> with temporary.temp_dir(make_cwd=True) as d:
    ...     assert d == os.getcwd()
    >>> assert d != os.getcwd()

    The suffix, prefix, and parent_dir options are passed to the
    standard ``tempfile.mkdtemp()`` function:
    >>> with temporary.temp_dir() as p:
    ...     with temporary.temp_dir(suffix='suf', prefix='pre', parent_dir=p) as d:
    ...         assert os.path.dirname(d) == p
    ...         assert os.path.basename(d).startswith('pre')
    ...         assert os.path.basename(d).endswith('suf')

    This function can also be used as a decorator, with the in_temp_dir
    alias:
    >>> @temporary.in_temp_dir()
    ... def my_function():
    ...     assert old_cwd != os.getcwd()
    ...
    >>> old_cwd = os.getcwd()
    >>> my_function()
    >>> assert old_cwd == os.getcwd()
    """
    prev_cwd = os.getcwd()
    abs_path = tempfile.mkdtemp(suffix, prefix, parent_dir)
    try:
        if make_cwd:
            os.chdir(abs_path)
        yield abs_path
    finally:
        if make_cwd:
            os.chdir(prev_cwd)
        with temporary.util.allow_missing_file():
            shutil.rmtree(abs_path)


in_temp_dir = functools.partial(temp_dir, make_cwd=True)  # pylint: disable=invalid-name
