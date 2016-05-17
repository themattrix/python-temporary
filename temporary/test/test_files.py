import nose.tools
import simian

import temporary


#
# Test Exceptions
#

class DummyException(Exception):
    """An exception unlikely to be raised by normal code."""


#
# Tests
#

def test_temp_file_creates_and_deletes_file():
    with temporary.temp_file() as temp_file:
        assert temp_file.is_file()
    assert not temp_file.exists()


def test_temp_file_in_custom_parent_dir():
    with temporary.temp_dir() as parent_dir:
        with temporary.temp_file(parent_dir=parent_dir) as temp_file:
            assert temp_file.parent == parent_dir


def test_temp_file_with_string_content():
    with temporary.temp_file('hello!') as temp_file:
        with temp_file.open() as f:
            assert f.read() == 'hello!'


def test_temp_file_with_bytes_content():
    with temporary.temp_file(b'hello!') as temp_file:
        with temp_file.open('rb') as f:
            assert f.read() == b'hello!'


def test_temp_file_with_bytearray_content():
    with temporary.temp_file(bytearray(b'hello!')) as temp_file:
        with temp_file.open('rb') as f:
            assert f.read() == b'hello!'


def test_temp_file_manually_deleted_is_allowed():
    with temporary.temp_file() as temp_file:
        temp_file.unlink()


@nose.tools.raises(OSError)
def test_temp_file_with_failed_remove():

    @simian.patch(temporary.files, external=('pathlib2.Path',))
    def blow_up(master_mock):
        master_mock.Path.return_value.unlink.side_effect = (OSError(-1, 'Fake'),)
        with temporary.temp_file(parent_dir=parent_dir):
            pass

    with temporary.temp_dir() as parent_dir:
        blow_up()  # pylint: disable=no-value-for-parameter


@nose.tools.raises(DummyException)
@simian.patch(temporary.files, external=('tempfile.mkstemp',))
def test_temp_file_passes_through_mkstemp_args(master_mock):
    master_mock.mkstemp.side_effect = (DummyException(),)
    try:
        ctx = temporary.temp_file(suffix='suffix', prefix='prefix', parent_dir='parent_dir')
        with ctx:
            pass  # pragma: no cover
    except DummyException:
        master_mock.mkstemp.assert_called_once_with('suffix', 'prefix', 'parent_dir', text=False)
        raise
