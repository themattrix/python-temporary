from errno import ENOENT
from contextlib import contextmanager
from os import close, remove, write
from tempfile import mkstemp


@contextmanager
def temp_file(
        content=None,
        suffix='',
        prefix='tmp',
        parent_dir=None,
        binary=True):
    """
    Create a temporary file and optionally populate it with content. The file
    is deleted when the context exits.

    The temporary file is created when entering the context manager and
    deleted when exiting it.
    >>> from os.path import exists, isfile
    >>> with temp_file() as f_name:
    ...     assert isfile(f_name)
    >>> assert not exists(f_name)

    The user may also supply some content for the file to be populated with:
    >>> with temp_file('hello!') as f_name:
    ...     with open(f_name) as f:
    ...         assert f.read() == 'hello!'

    The temporary file can be placed in a custom directory:
    >>> from os.path import dirname
    >>> from temporary import temp_dir
    >>> with temp_dir() as d_name:
    ...     with temp_file(parent_dir=d_name) as f_name:
    ...         assert dirname(f_name) == d_name

    If, for some reason, the user wants to delete the temporary file before
    exiting the context, that's okay too:
    >>> import os
    >>> with temp_file() as f_name:
    ...     os.remove(f_name)
    """
    fd, abs_path = mkstemp(suffix, prefix, parent_dir, not binary)

    try:
        if content:
            write(fd, content.encode())
        close(fd)
        yield abs_path
    finally:
        try:
            remove(abs_path)
        except OSError as e:
            if e.errno != ENOENT:
                raise
