import os
from colorama import Fore
from helpers import run_cmd

DEFAULT_TEST_DIR = 'test-files'
DEFAULT_OUT_DIR = 'test-outs'

"""
Run a single test

@param t_file- required; the full path to the file to run
@param level- optional (default: all); the compression level [1-9]
@return True if all tests passed; False if at least one test failed
"""


def run_test(t_file, level=None, out_dir=DEFAULT_OUT_DIR):
    passed = True
    if level is None:
        for x in range(1, 10):
            if run_test(t_file, x, out_dir) is False:
                passed = False

        return passed

    out1 = os.path.join(out_dir, '%(file)s.%(level)d.gz'
                        % {'file': os.path.basename(t_file), 'level': level})
    out2 = os.path.join(out_dir, '%(file)s.%(level)d.out.gz'
                        % {'file': os.path.basename(t_file), 'level': level})

    run_cmd('gzip -c -%(level)d %(file)s > %(outfile)s'
            % {'level': level, 'file': t_file, 'outfile': out1})
    run_cmd('../bin/gzip.js --level %(level)d --file %(file)s --output %(output)s' % {'level': level, 'file': t_file, 'output': out2})

    result = run_cmd('diff %(file1)s %(file2)s'
                     % {'file1': out1, 'file2': out2})
    if result['returncode'] == 0:
        status = Fore.GREEN + 'PASSED' + Fore.RESET
    else:
        passed = False
        status = Fore.RED + 'FAILED' + Fore.RESET

    print('Level %(level)d: %(status)s' % {'level': level, 'status': status})

    return passed


"""
Runs all tests on the given level. This iterates through the test_dir directory
defined above.
@param level- The level to run on [1-9] (default: None, runs on all levels all)
@return True if all levels passed, False if at least one failed
"""


def run_all(level=None, test_dir=DEFAULT_TEST_DIR):
    passed = True
    for t_file in os.listdir(test_dir):
        full_path = os.path.join(test_dir, t_file)

        print Fore.YELLOW + t_file + Fore.RESET

        if run_test(full_path, level) is False:
            passed = False

        print('')

    return passed
