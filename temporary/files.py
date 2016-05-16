import os
import tempfile

import contextlib2 as contextlib

import temporary.util


@contextlib.contextmanager
def temp_file(
        content=None,
        suffix='',
        prefix='tmp',
        parent_dir=None):
    """
    Create a temporary file and optionally populate it with content. The file
    is deleted when the context exits.

    The temporary file is created when entering the context manager and
    deleted when exiting it.
    >>> import os.path
    >>> import temporary
    >>> with temporary.temp_file() as f_name:
    ...     assert os.path.isfile(f_name)
    >>> assert not os.path.exists(f_name)

    The user may also supply some content for the file to be populated with:
    >>> with temporary.temp_file('hello!') as f_name:
    ...     with open(f_name) as f:
    ...         assert f.read() == 'hello!'

    The temporary file can be placed in a custom directory:
    >>> with temporary.temp_dir() as d_name:
    ...     with temporary.temp_file(parent_dir=d_name) as f_name:
    ...         assert os.path.dirname(f_name) == d_name

    If, for some reason, the user wants to delete the temporary file before
    exiting the context, that's okay too:
    >>> import os
    >>> with temporary.temp_file() as f_name:
    ...     os.remove(f_name)
    """
    binary = isinstance(content, (bytes, bytearray))
    fd, abs_path = tempfile.mkstemp(suffix, prefix, parent_dir, text=False)

    try:
        try:
            if content:
                os.write(fd, content if binary else content.encode())
        finally:
            os.close(fd)
        yield abs_path
    finally:
        with temporary.util.allow_missing_file():
            os.remove(abs_path)
