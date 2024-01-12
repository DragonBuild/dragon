#!/usr/bin/env python3

import shutil, subprocess, sys, os, timeit, yaml
from math import sin, cos, radians

TestDict = yaml.safe_load(open(os.environ['DRAGON_ROOT_DIR'] + '/internal/tests.yml'))
projects = TestDict['ProjectTests']


def bench():
    product = 1.0
    for counter in range(1, 1000, 1):
        for dex in list(range(1, 360, 1)):
            angle = radians(dex)
            product *= sin(angle) ** 2 + cos(angle) ** 2
    return product



def system(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
    proc = subprocess.Popen("" + cmd,
                            stdout=stdout,
                            stderr=stderr,
                            shell=True,
                            universal_newlines=True)
    std_out, std_err = proc.communicate()
    # print(proc.returncode)
    return proc.returncode  # , std_out, std_err


def main():
    tests = {

    }
    times = {

    }
    testing_dir = os.environ['DRAGON_ROOT_DIR'] + '/testing/'
    if os.path.isdir(testing_dir):
        shutil.rmtree(testing_dir)
    os.makedirs(testing_dir, exist_ok=True)
    os.chdir(testing_dir)

    # print('Doing Benchmarks')
    # perform_benchmark()

    for category in projects:
        cattests = {}
        cattimes = {}
        for i in projects[category]:
            os.chdir(testing_dir)
            print(os.getcwd())
            system('''
            echo $PWD
            git clone %s
            ''' % i, sys.stdout, sys.stderr)
            dirName = i.split('/')[-1]
            os.chdir(dirName)
            print(os.getcwd())
            print(f"---\n Testing {dirName} \n---")
            # time.sleep(5)
            s = timeit.default_timer()
            passed = system('dragon c b', sys.stdout, sys.stderr) == 0
            s = timeit.default_timer() - s
            print(s)
            print('-+- Passed -+-' if passed else '-!- Failed -!-')
            cattests[dirName] = passed
            cattimes[dirName] = s
            os.chdir(testing_dir)
            if passed:
                shutil.rmtree(dirName)
        tests[category] = cattests
        times[category] = cattimes

    print('\n\n---\n')

    os.system('uname -a')

    total = 0
    passed = 0

    for category in tests:
        print(f'\n{category} Project Build Tests')
        for i in tests[category]:
            print(
                f'{i} : {"Passed" if tests[category][i] else "Failed"} in {times[category][i]} ')
        passed += sum(tests[category].values())
        total += len(tests[category])

    print(f'\n{passed}/{total} passed\n---\n\n')


if __name__ == '__main__':
    main()
