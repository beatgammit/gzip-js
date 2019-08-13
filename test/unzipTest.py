import os
from colorama import Fore
from helpers import run_cmd

OUT_DIR_DEFAULT = 'test-outs'
TEST_DIR_DEFAULT = 'test-files'

"""
Run a single test
@param t_file- required; the file to check against (uncompressed data)
@param level- optional (default: all); the compression level [1-9]
@return True if all tests passed; False if at least one test failed
"""


def run_test(t_file, level=None, out_dir=OUT_DIR_DEFAULT):
    passed = True

    if level is None:
        for x in range(1, 10):
            if run_test(t_file, x) is False:
                passed = False

        return passed

    out1 = os.path.join(out_dir, '%(file)s.%(level)d.gz'
                        % {'file': os.path.basename(t_file), 'level': level})
    out2 = os.path.join(out_dir, '%(file)s.%(level)d'
                        % {'file': os.path.basename(t_file), 'level': level})

    run_cmd('gzip -%(level)d -c %(file)s >> %(output)s'
            % {'level': level, 'file': t_file, 'output': out1})
    run_cmd('../bin/gunzip.js --file %(file)s --output %(output)s'
            % {'level': level, 'file': out1, 'output': out2})

    result = run_cmd('diff %(file1)s %(file2)s'
                     % {'file1': t_file, 'file2': out2})
    if result['returncode'] == 0:
        status = Fore.GREEN + 'PASSED' + Fore.RESET
    else:
        passed = False
        status = Fore.RED + 'FAILED' + Fore.RESET

    print 'Level %(level)d: %(status)s' % {'level': level, 'status': status}

    return passed


"""
Runs all tests on the given level. This iterates throuth the test_dir directory
defined above.
@param level- The level to run on [1-9] (default: None, runs on all levels all)
@return True if all levels passed, False if at least one failed
"""


def run_all(level=None, test_dir=TEST_DIR_DEFAULT, out_dir=OUT_DIR_DEFAULT):
    passed = True
    for t_file in os.listdir(test_dir):
        full_path = os.path.join(test_dir, t_file)

        print Fore.YELLOW + t_file + Fore.RESET

        if run_test(full_path, level) is False:
            passed = False

        print ''

    return passed
