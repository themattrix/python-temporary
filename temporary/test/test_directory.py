from contextlib2 import contextmanager
from errno import EEXIST, ENOENT
from nose.tools import eq_, raises
from os import chdir, getcwd, makedirs, rmdir
from os.path import dirname, exists, isdir, isfile, join
from simian import patch

# module under test
from temporary import directory


#
# Decorators
#

@contextmanager
def restore_cwd():
    cwd = getcwd()
    try:
        yield
    finally:
        chdir(cwd)


#
# Test Exceptions
#

class DummyException(Exception):
    pass


#
# Tests
#

@restore_cwd()
def test_temp_dir_without_chdir_creates_temp_dir():
    cwd = getcwd()
    with directory.temp_dir() as d:
        eq_(isdir(d), True)
        eq_(getcwd(), cwd)
    eq_(exists(d), False)
    eq_(getcwd(), cwd)


@restore_cwd()
def test_temp_dir_with_chdir_creates_temp_dir():
    cwd = getcwd()
    with directory.temp_dir(make_cwd=True) as d:
        eq_(isdir(d), True)
        eq_(getcwd(), d)
    eq_(exists(d), False)
    eq_(getcwd(), cwd)


@restore_cwd()
def test_temp_dir_deletes_all_children():
    with directory.temp_dir() as d:
        f = join(d, 'deep', 'deeper', 'file')
        create_file_in_tree(f)
        eq_(isfile(f), True)
    eq_(exists(d), False)
    eq_(exists(f), False)


@restore_cwd()
def test_changing_to_temp_dir_manually_still_allows_deletion():
    with directory.temp_dir() as d:
        chdir(d)


@restore_cwd()
def test_manually_deleting_temp_dir_is_allowed():
    with directory.temp_dir() as d:
        rmdir(d)


@raises(OSError)
@patch(directory, external=('shutil.rmtree',))
@restore_cwd()
def test_temp_dir_with_failed_rmtree(master_mock):
    master_mock.rmtree.side_effect = (OSError(-1, 'Fake'),)
    d = None
    try:
        with directory.temp_dir() as d:
            pass
    finally:
        rmdir(d)


@raises(DummyException)
@patch(directory, external=('tempfile.mkdtemp',))
def test_temp_dir_passes_through_mkdtemp_args(master_mock):
    master_mock.mkdtemp.side_effect = (DummyException(),)
    pass_through_args = ('suffix', 'prefix', 'parent_dir')
    try:
        with directory.temp_dir(*pass_through_args):
            pass  # pragma: no cover
    except DummyException:
        master_mock.mkdtemp.assert_called_once_with(*pass_through_args)
        raise


def test_temp_dir_can_import_from_init():
    import temporary
    assert temporary.temp_dir


#
# Test Helpers
#

def create_file_in_tree(path):
    try:
        touch(path)
    except IOError as e:
        if e.errno != ENOENT:
            raise                                 # pragma: no cover
        create_dir_tree(dirname(path))
        touch(path)


def create_dir_tree(path):
    try:
        makedirs(path)
    except OSError as e:                          # pragma: no cover
        if e.errno != EEXIST or not isdir(path):  # pragma: no cover
            raise                                 # pragma: no cover


def touch(path):
    with open(path, 'wb'):
        pass
