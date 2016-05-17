#!/usr/bin/env python

import glob
import itertools
import fnmatch
import os
import os.path
import subprocess
import sys

PACKAGE_DIR = 'temporary'


def main(args):
    try:
        if args and args[0] == '--static-analysis':
            run_static_analysis()
        run_unit_tests()
    except ProcessError as e:
        print(str(e))
        sys.exit(e.status)


def run_static_analysis():
    analyze_rst_files()
    analyze_setup_py()
    analyze_source_with_flake8()
    analyze_source_with_pylint()


def run_unit_tests():
    run(('nosetests',
         '--exe',
         '--with-doctest',
         '--doctest-options', '+NORMALIZE_WHITESPACE',
         '--with-coverage',
         '--cover-tests',
         '--cover-inclusive',
         '--cover-package', PACKAGE_DIR,
         PACKAGE_DIR))


def analyze_rst_files():
    for path in itertools.chain(glob.iglob('*.rst'), recursive_glob(PACKAGE_DIR, '*.rst')):
        run(('rst2html.py', '--exit-status=2', path), display_stdout=False)


def analyze_setup_py():
    run((sys.executable, 'setup.py', 'check', '--strict', '--restructuredtext', '--metadata'))


def analyze_source_with_flake8():
    run(('flake8', 'setup.py', PACKAGE_DIR))


def analyze_source_with_pylint():
    run(('pylint', '--reports=no', '--rcfile', '.pylintrc', PACKAGE_DIR))


def recursive_glob(top, pattern):
    for dirpath, _, filenames in os.walk(top):
        for f in fnmatch.filter(filenames, pattern):
            yield os.path.join(dirpath, f)


class ProcessError(Exception):  # subprocess.CalledProcessError(...) has a different signature in Python 2.6
    def __init__(self, args, status, stdout=None, stderr=None):
        self.args = args
        self.status = status
        self.stdout = (stdout or b'').decode('utf-8', 'ignore')
        self.stderr = (stderr or b'').decode('utf-8', 'ignore')

    def __str__(self):
        return 'The command {args!r} returned the non-zero exit code {status}.{stdout}{stderr}'.format(
            args=self.args,
            status=self.status,
            stdout='' if not self.stdout else '\n\n[stdout]\n{}'.format(indent(self.stdout)),
            stderr='' if not self.stderr else '\n\n[stderr]\n{}'.format(indent(self.stderr)))


def run(args, display_stdout=True):
    p = subprocess.Popen(args, stdout=None if display_stdout else subprocess.PIPE)
    stdout, _ = p.communicate()
    if p.returncode != 0:
        raise ProcessError(args=args, status=p.returncode, stdout=stdout if display_stdout else None)


def indent(text, prefix='    '):  # textwrap.indent() doesn't exist in Python 2
    return prefix + prefix.join(text.splitlines(True))


if __name__ == '__main__':
    main(args=sys.argv[1:])
