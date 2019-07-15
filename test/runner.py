#!/usr/bin/env python

import os
import sys
import shutil
from colorama import Fore
import argparse
import zipTest
import unzipTest

PARSER = argparse.ArgumentParser(description='Process command-line arguments')
PARSER.add_argument('--file', '-f', metavar='path/to/file', type=str, nargs='?', help='Path to file to use for test')
PARSER.add_argument('--level', '-l', metavar='#', type=int, nargs='?', help='Compression level')
PARSER.add_argument('--no-delete', const=True, default=False, nargs='?', help='Don\'t delete files produced for test')
PARSER.add_argument('--test', default='both', nargs='?', help='Which test to run (zip, unzip, both)')

ARGS = PARSER.parse_args()

ALL_PASSED = True

OUT_DIR = 'test-outs'

# make the test-outs directory
try:
    os.mkdir(OUT_DIR)
except:
    pass

DELETE = not getattr(ARGS, 'no_delete')
LEVEL = getattr(ARGS, 'level')
IN_FILE = getattr(ARGS, 'file')
TEST = getattr(ARGS, 'test')

if TEST == 'zip' or TEST == 'both':
    print (Fore.CYAN + 'Running zip tests' + Fore.RESET)
    # if the user specifies a file, only run that test
    if IN_FILE is not None:
        ALL_PASSED = zipTest.runTest(IN_FILE, LEVEL)
    else:
        ALL_PASSED = zipTest.runAll(LEVEL)

if TEST == 'unzip' or TEST == 'both':
    print (Fore.CYAN + 'Running unzip tests' + Fore.RESET)
    # if the user specifies a file, only run that test
    if IN_FILE is not None:
        ALL_PASSED = unzipTest.runTest(IN_FILE, LEVEL)
    else:
        ALL_PASSED = unzipTest.runAll(LEVEL)

if DELETE:
    shutil.rmtree(OUT_DIR)

if ALL_PASSED:
    print (Fore.GREEN + 'All tests passed!' + Fore.RESET)
else:
    print (Fore.RED + 'Automated test failed' + Fore.RESET)
    sys.exit(1)
