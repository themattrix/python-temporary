import errno
import os
import os.path

import contextlib2 as contextlib
import nose.tools
import simian

import temporary


#
# Decorators
#

@contextlib.contextmanager
def restore_cwd():
    cwd = os.getcwd()
    try:
        yield
    finally:
        os.chdir(cwd)


#
# Test Exceptions
#

class DummyException(Exception):
    pass


#
# Tests
#

# noinspection PyCallingNonCallable
@restore_cwd()
def test_temp_dir_without_chdir_creates_temp_dir():
    cwd = os.getcwd()
    with temporary.temp_dir() as d:
        nose.tools.eq_(os.path.isdir(d), True)
        nose.tools.eq_(os.getcwd(), cwd)
    nose.tools.eq_(os.path.exists(d), False)
    nose.tools.eq_(os.getcwd(), cwd)


# noinspection PyCallingNonCallable
@restore_cwd()
def test_temp_dir_with_chdir_creates_temp_dir():
    cwd = os.getcwd()
    with temporary.temp_dir(make_cwd=True) as d:
        nose.tools.eq_(os.path.isdir(d), True)
        nose.tools.eq_(os.getcwd(), d)
    nose.tools.eq_(os.path.exists(d), False)
    nose.tools.eq_(os.getcwd(), cwd)


# noinspection PyCallingNonCallable
@restore_cwd()
def test_temp_dir_deletes_all_children():
    with temporary.temp_dir() as d:
        f = os.path.join(d, 'deep', 'deeper', 'file')
        create_file_in_tree(f)
        nose.tools.eq_(os.path.isfile(f), True)
    nose.tools.eq_(os.path.exists(d), False)
    nose.tools.eq_(os.path.exists(f), False)


# noinspection PyCallingNonCallable
@restore_cwd()
def test_changing_to_temp_dir_manually_still_allows_deletion():
    with temporary.temp_dir() as d:
        os.chdir(d)


# noinspection PyCallingNonCallable
@restore_cwd()
def test_manually_deleting_temp_dir_is_allowed():
    with temporary.temp_dir() as d:
        os.rmdir(d)


# noinspection PyCallingNonCallable
@nose.tools.raises(OSError)
@simian.patch(temporary.directories, external=('shutil.rmtree',))
@restore_cwd()
def test_temp_dir_with_failed_rmtree(master_mock):
    master_mock.rmtree.side_effect = (OSError(-1, 'Fake'),)
    d = None
    try:
        with temporary.temp_dir() as d:
            pass
    finally:
        nose.tools.eq_(os.path.isdir(d), True)
        os.rmdir(d)


@nose.tools.raises(DummyException)
@simian.patch(temporary.directories, external=('tempfile.mkdtemp',))
def test_temp_dir_passes_through_mkdtemp_args(master_mock):
    master_mock.mkdtemp.side_effect = (DummyException(),)
    try:
        with temporary.temp_dir('suffix', 'prefix', 'parent_dir'):
            pass  # pragma: no cover
    except DummyException:
        master_mock.mkdtemp.assert_called_once_with('suffix', 'prefix', 'parent_dir')
        raise


#
# Test Helpers
#

def create_file_in_tree(path):
    try:
        touch(path)
    except IOError as e:
        if e.errno != errno.ENOENT:
            raise  # pragma: no cover
        create_dir_tree(os.path.dirname(path))
        touch(path)


def create_dir_tree(path):
    try:
        os.makedirs(path)
    except OSError as e:                                        # pragma: no cover
        if e.errno != errno.EEXIST or not os.path.isdir(path):  # pragma: no cover
            raise                                               # pragma: no cover


def touch(path):
    with open(path, 'wb'):
        pass
