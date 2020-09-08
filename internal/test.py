import subprocess, sys, os
from pprint import pprint
from math import sin, cos, radians
import timeit, time

cpu_bench = 0

projects = \
    {
        'Common':
            [
                'Chapters',
                'Docky',
                'Shakelight'
            ],
        'Legacy':
            [
                'StatusViz',
            ],
        'Theos':
            [
                'StopCrashingPls'
            ]
    }


def bench():
    product = 1.0
    for counter in range(1, 1000, 1):
        for dex in list(range(1, 360, 1)):
            angle = radians(dex)
            product *= sin(angle) ** 2 + cos(angle) ** 2
    return product


def perform_benchmark():
    print("Doing CPU Benchmark:")
    result = timeit.repeat('test.bench()', setup='import test', number=10, repeat=5)
    result = list(sorted(result))
    global cpu_bench
    cpu_bench = sum(result[:3]) / 3
    print(cpu_bench)
    print("Doing Project Build Benchmark")
    benchmark_projects()


def benchmark_projects():
    #os.chdir(os.environ['DRAGONBUILD'] + '/testing/' + projects['Common'][0])
    #result = timeit.timeit('test.system("dragon c b")', setup='import test, sys', number=10)
    #print(result / 10)
    # result = list(sorted(result))
    # print(*result[:3])
    pass


def system(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
    proc = subprocess.Popen(cmd,
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
    system('mkdir -p ' + os.environ['DRAGONBUILD'] + '/testing/')
    os.chdir(os.environ['DRAGONBUILD'] + '/testing/')

    print('Doing Benchmarks')
    perform_benchmark()

    for category in projects:
        cattests = {}
        cattimes = {}
        for i in projects[category]:
            os.chdir(os.environ['DRAGONBUILD'] + '/testing/')
            print(os.getcwd())
            system('''
            echo $PWD
            git clone https://github.com/KritantaDev/%s.git
            ''' % i, sys.stdout, sys.stderr)
            os.chdir(i)
            print(os.getcwd())
            print(f"---\n Testing {i} \n---")
            # time.sleep(5)
            s = timeit.default_timer()
            passed = system('dragon c b', sys.stdout, sys.stderr) == 0
            s = timeit.default_timer() - s
            print(s)
            print('-+- Passed -+-' if passed else '-!- Failed -!-')
            cattests[i] = passed
            cattimes[i] = s
            os.chdir(os.environ['DRAGONBUILD'] + '/testing/')
        tests[category] = cattests
        times[category] = cattimes

    print(f'\n\n---\n')

    os.system('uname -a')

    total = 0
    passed = 0
    print(times)
    # print(tests)
    print(cpu_bench)
    baseline = {
        'Common': {
            'Chapters': 0.7295811089999997/1.3837896153333336,
            'Docky': 1.3256995099999997/1.3837896153333336,
            'Shakelight': 0.7603968410000022/1.3837896153333336
            },
        'Legacy': {
            'StatusViz': 1.176904830999998/1.3837896153333336
            },
        'Theos': {
            'StopCrashingPls': 0.631509568000002/1.3837896153333336
            },

        }
    for category in tests:
        print(f'\n{category} Project Build Tests')
        for i in tests[category]:
            print(
                f'{i} : {"Passed" if tests[category][i] else "Failed"} in {times[category][i]} : {str(( times[category][i] / cpu_bench ) / baseline[category][i] * 100)[:5]}%')
        passed += sum(tests[category].values())
        total += len(tests[category])

    print(f'\n{passed}/{total} passed\n---\n\n')


if __name__ == '__main__':
    main()
