import errno
import os

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
    """An exception unlikely to be raised by normal code."""


#
# Tests
#

# noinspection PyCallingNonCallable
@restore_cwd()
def test_temp_dir_without_chdir_creates_temp_dir():
    cwd = os.getcwd()
    with temporary.temp_dir() as temp_dir:
        assert temp_dir.is_dir()
        assert os.getcwd() == cwd
    assert not temp_dir.exists()
    assert os.getcwd() == cwd


# noinspection PyCallingNonCallable
@restore_cwd()
def test_temp_dir_with_chdir_creates_temp_dir():
    cwd = os.getcwd()
    with temporary.temp_dir(make_cwd=True) as temp_dir:
        assert temp_dir.is_dir()
        assert temp_dir.samefile(os.getcwd())
    assert not temp_dir.exists()
    assert cwd == os.getcwd()


# noinspection PyCallingNonCallable
@restore_cwd()
def test_temp_dir_deletes_all_children():
    with temporary.temp_dir() as temp_dir:
        temp_file = temp_dir / 'deep/deeper/file'
        create_file_in_tree(temp_file)
        assert temp_file.is_file()
    assert not temp_dir.exists()
    assert not temp_file.exists()


# noinspection PyCallingNonCallable
@restore_cwd()
def test_changing_to_temp_dir_manually_still_allows_deletion():
    with temporary.temp_dir() as temp_dir:
        os.chdir(str(temp_dir))


# noinspection PyCallingNonCallable
@restore_cwd()
def test_manually_deleting_temp_dir_is_allowed():
    with temporary.temp_dir() as temp_dir:
        temp_dir.rmdir()


# noinspection PyCallingNonCallable
@nose.tools.raises(OSError)
@simian.patch(temporary.directories, external=('shutil.rmtree',))
@restore_cwd()
def test_temp_dir_with_failed_rmtree(master_mock):
    master_mock.rmtree.side_effect = (OSError(-1, 'Fake'),)
    temp_dir = None
    try:
        with temporary.temp_dir() as temp_dir:
            pass
    finally:
        assert temp_dir.is_dir()
        temp_dir.rmdir()


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
        path.touch()
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise  # pragma: no cover
        path.parent.mkdir(parents=True)
        path.touch()
