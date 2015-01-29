from nose.tools import eq_, raises
from os import remove
from os.path import dirname, exists, isfile
from simian import patch
from temporary import temp_dir

# module under test
from temporary import files


#
# Test Exceptions
#

class DummyException(Exception):
    pass


#
# Tests
#

def test_temp_file_creates_and_deletes_file():
    with files.temp_file() as f_name:
        eq_(isfile(f_name), True)
    eq_(exists(f_name), False)


def test_temp_file_in_custom_parent_dir():
    with temp_dir() as parent_dir:
        with files.temp_file(parent_dir=parent_dir) as f_name:
            eq_(dirname(f_name), parent_dir)


def test_temp_file_with_content():
    with files.temp_file('hello!') as f_name:
        with open(f_name) as f:
            assert f.read() == 'hello!'


def test_temp_file_manually_deleted_is_allowed():
    with files.temp_file() as f_name:
        remove(f_name)


@raises(OSError)
def test_temp_file_with_failed_remove():

    @patch(files, external=('os.remove',))
    def blow_up(master_mock):
        master_mock.remove.side_effect = (OSError(-1, 'Fake'),)
        with files.temp_file(parent_dir=parent_dir):
            pass

    with temp_dir() as parent_dir:
        blow_up()  # pylint: disable=no-value-for-parameter


@raises(DummyException)
@patch(files, external=('tempfile.mkstemp',))
def test_temp_file_passes_through_mkstemp_args(master_mock):
    master_mock.mkstemp.side_effect = (DummyException(),)
    try:
        ctx = files.temp_file(
            suffix='suffix',
            prefix='prefix',
            parent_dir='parent_dir',
            binary=False)
        with ctx:
            pass  # pragma: no cover
    except DummyException:
        master_mock.mkstemp.assert_called_once_with(
            'suffix', 'prefix', 'parent_dir', True)
        raise


def test_temp_file_can_import_from_init():
    import temporary
    assert temporary.temp_file
