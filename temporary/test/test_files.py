import os
import os.path

import nose.tools
import simian

import temporary


#
# Test Exceptions
#

class DummyException(Exception):
    pass


#
# Tests
#

def test_temp_file_creates_and_deletes_file():
    with temporary.temp_file() as f_name:
        nose.tools.eq_(os.path.isfile(f_name), True)
    nose.tools.eq_(os.path.exists(f_name), False)


def test_temp_file_in_custom_parent_dir():
    with temporary.temp_dir() as parent_dir:
        with temporary.temp_file(parent_dir=parent_dir) as f_name:
            nose.tools.eq_(os.path.dirname(f_name), parent_dir)


def test_temp_file_with_string_content():
    with temporary.temp_file('hello!') as f_name:
        with open(f_name) as f:
            assert f.read() == 'hello!'


def test_temp_file_with_bytes_content():
    with temporary.temp_file(b'hello!') as f_name:
        with open(f_name, 'rb') as f:
            assert f.read() == b'hello!'


def test_temp_file_with_bytearray_content():
    with temporary.temp_file(bytearray(b'hello!')) as f_name:
        with open(f_name, 'rb') as f:
            assert f.read() == b'hello!'


def test_temp_file_manually_deleted_is_allowed():
    with temporary.temp_file() as f_name:
        os.remove(f_name)


@nose.tools.raises(OSError)
def test_temp_file_with_failed_remove():

    @simian.patch(temporary.files, external=('os.remove',))
    def blow_up(master_mock):
        master_mock.remove.side_effect = (OSError(-1, 'Fake'),)
        with temporary.temp_file(parent_dir=parent_dir):
            pass

    with temporary.temp_dir() as parent_dir:
        blow_up()  # pylint: disable=no-value-for-parameter


@nose.tools.raises(DummyException)
@simian.patch(temporary.files, external=('tempfile.mkstemp',))
def test_temp_file_passes_through_mkstemp_args(master_mock):
    master_mock.mkstemp.side_effect = (DummyException(),)
    try:
        ctx = temporary.temp_file(
            suffix='suffix',
            prefix='prefix',
            parent_dir='parent_dir')
        with ctx:
            pass  # pragma: no cover
    except DummyException:
        master_mock.mkstemp.assert_called_once_with('suffix', 'prefix', 'parent_dir', text=False)
        raise
