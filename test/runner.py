#!/usr/bin/env python

import os
import sys
import shutil
import json
import subprocess as sp
from colorama import Fore
import argparse

parser = argparse.ArgumentParser(description='Process command-line arguments')
parser.add_argument('--file', '-f', metavar='path/to/file', type=str, nargs='?', help='Path to file to use for test')
parser.add_argument('--level', '-l', metavar='#', type=int, nargs='?', help='Compression level')
parser.add_argument('--no-delete', const=True, default=False, nargs='?', help='Don\'t delete files produced for test')

args = parser.parse_args()

allPassed = True

testDir = 'test-files'
outDir = 'test-outs'

"""
Convenience function for running a command bash-like

@param command- string version of a command to run on
@param shell- Whether to run this through the shell; used in subprocess.Popen (default: true)
@return Object with properties 'returncode', 'stdout', and 'stderr'
"""
def run_cmd(command, shell=True):
	process = sp.Popen(command, shell=shell, stdout = sp.PIPE, stderr = sp.PIPE)
	stdout, stderr = process.communicate()
	returncode = process.returncode
	return {'returncode' : returncode, 'stdout' : stdout, 'stderr' : stderr}

"""
Run a single test

@param tFile- required; the full path to the file to run
@param level- optional (default: all); the compression level [1-9]
@param delete- optional (default: True); whether to delete the gzipped files
@return True if all tests passed; False if at least one test failed
"""
def runTest(tFile, level=None, delete=True):
	passed = True
	if level == None:
		for x in range(1, 10):
			if runTest(tFile, x, delete) == False:
				passed = False

		return passed

	out1 = os.path.join(outDir, '%(file)s.%(level)d.gz' % {'file': os.path.basename(tFile), 'level' : level})
	out2 = os.path.join(outDir, '%(file)s.%(level)d.out.gz' % {'file': os.path.basename(tFile), 'level' : level})

	run_cmd('gzip -c -%(level)d %(file)s > %(outfile)s' % {'level' : level, 'file' : tFile, 'outfile' : out1})
	run_cmd('../bin/runner.js --level %(level)d --file %(file)s --output %(output)s' % {'level' : level, 'file' : tFile, 'output' : out2})

	result = run_cmd('diff %(file1)s %(file2)s' % {'file1' : out1, 'file2' : out2})
	if result['returncode'] == 0:
		status = Fore.GREEN + 'PASSED' + Fore.RESET
	else:
		passed = False
		status = Fore.RED + 'FAILED' + Fore.RESET
	
	print 'Level %(level)d: %(status)s' % {'level' : level, 'status' : status}

	if delete == True:
		os.remove(out1)
		os.remove(out2)

	return passed

"""
Runs all tests on the given level. This iterates throuth the testDir directory defined above.

@param level- The level to run on [1-9] (default: None, runs on all levels all)
@param delete- Whether to delete output files after the test is run
@return True if all levels passed, False if at least one failed
"""
def runAll(level=None, delete=True):
	passed = True
	for tFile in os.listdir(testDir):
		fullPath = os.path.join(testDir, tFile)

		print Fore.YELLOW + tFile + Fore.RESET

		if runTest(fullPath, level, delete) == False:
			passed = False

		print ''
	
	return passed

# make the test-outs directory
try:
	os.mkdir(outDir)
except:
	pass

delete = not getattr(args, 'no_delete')
level = getattr(args, 'level')
inFile = getattr(args, 'file')

# if the user specifies a file, only run that test
if inFile != None:
	allPassed = runTest(inFile, level, delete)
else:
	allPassed = runAll(level, delete)

# if we deleted all the files that were created, delete the directory
if delete == True:
	shutil.rmtree(outDir)

if allPassed:
	print Fore.GREEN + 'All tests passed!' + Fore.RESET
else:
	print Fore.RED + 'Automated test failed' + Fore.RESET
	sys.exit(1)
