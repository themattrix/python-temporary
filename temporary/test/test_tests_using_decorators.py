import os.path
import subprocess


def test_tests_using_decorators():
    # Assemble
    test_path = os.path.join(os.path.dirname(__file__), 'tests_using_decorators', 'tests.py')
    process = subprocess.Popen(
        args=('nosetests', test_path),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)

    # Act
    out, _ = process.communicate()
    status = process.returncode

    # Assert
    assert b'Ran 3 tests' in out, "b'Ran 3 tests' not found in {!r}".format(out)
    assert status == 0, 'status == {!r}, not 0'.format(status)
