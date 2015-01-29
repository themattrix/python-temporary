Temporary |Version| |Build| |Coverage| |Health|
===============================================

|Compatibility| |Implementations| |Format| |Downloads|

Context managers for managing temporary files and directories.


.. code:: python

    with temp_dir(suffix='', prefix='tmp', parent_dir=None, make_cwd=False):
        ...

    @in_temp_dir()
    ...

    with temp_file(
        content=None,
        suffix='',
        prefix='tmp',
        parent_dir=None,
        binary=True):
        ...


Installation:

.. code:: shell

    $ pip install temporary


Temporary Directory Examples
----------------------------

.. code:: python

    >>> from temporary import temp_dir, in_temp_dir

The temporary directory is created when entering the context manager, and
deleted when exiting it:

.. code:: python

    >>> from os.path import exists, isdir
    >>> with temp_dir() as d:
    ...     assert isdir(d)
    >>> assert not exists(d)

This time let's make the temporary directory our working directory:

.. code:: python

    >>> from os import getcwd
    >>> with temp_dir(make_cwd=True) as d:
    ...     assert d == getcwd()
    >>> assert d != getcwd()

The suffix, prefix, and parent_dir options are passed to the standard
``tempfile.mkdtemp()`` function:

.. code:: python

    >>> from os.path import basename, dirname
    >>> with temp_dir() as p:
    ...     with temp_dir(suffix='suf', prefix='pre', parent_dir=p) as d:
    ...         assert dirname(d) == p
    ...         assert basename(d).startswith('pre')
    ...         assert basename(d).endswith('suf')

This function can also be used as a decorator, with the ``in_temp_dir`` alias:

.. code:: python

    >>> @in_temp_dir()
    ... def my_function():
    ...     assert old_cwd != getcwd()
    ...
    >>> old_cwd = getcwd()
    >>> my_function()
    >>> assert old_cwd == getcwd()


Temporary Files Examples
------------------------

.. code:: python

    >>> from temporary import temp_file

The temporary file is created when entering the context manager and
deleted when exiting it.

.. code:: python

    >>> from os.path import exists, isfile
    >>> with temp_file() as f_name:
    ...     assert isfile(f_name)
    >>> assert not exists(f_name)

The user may also supply some content for the file to be populated with:

.. code:: python

    >>> with temp_file('hello!') as f_name:
    ...     with open(f_name) as f:
    ...         assert f.read() == 'hello!'

The temporary file can be placed in a custom directory:

.. code:: python

    >>> from os.path import dirname
    >>> from temporary import temp_dir
    >>> with temp_dir() as d_name:
    ...     with temp_file(parent_dir=d_name) as f_name:
    ...         assert dirname(f_name) == d_name

If, for some reason, the user wants to delete the temporary file before
exiting the context, that's okay too:

.. code:: python

    >>> import os
    >>> with temp_file() as f_name:
    ...     os.remove(f_name)


.. |Build| image:: https://travis-ci.org/themattrix/python-temporary.svg?branch=master
   :target: https://travis-ci.org/themattrix/python-temporary
.. |Coverage| image:: https://img.shields.io/coveralls/themattrix/python-temporary.svg
   :target: https://coveralls.io/r/themattrix/python-temporary
.. |Health| image:: https://landscape.io/github/themattrix/python-temporary/master/landscape.svg
   :target: https://landscape.io/github/themattrix/python-temporary/master
.. |Version| image:: https://pypip.in/version/temporary/badge.svg?text=version
    :target: https://pypi.python.org/pypi/temporary
.. |Downloads| image:: https://pypip.in/download/temporary/badge.svg
    :target: https://pypi.python.org/pypi/temporary
.. |Compatibility| image:: https://pypip.in/py_versions/temporary/badge.svg
    :target: https://pypi.python.org/pypi/temporary
.. |Implementations| image:: https://pypip.in/implementation/temporary/badge.svg
    :target: https://pypi.python.org/pypi/temporary
.. |Format| image:: https://pypip.in/format/temporary/badge.svg
    :target: https://pypi.python.org/pypi/temporary
