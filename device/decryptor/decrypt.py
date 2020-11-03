import os, sys, subprocess

bund = sys.argv[1]
dip = os.environ['DRBIP']
dport = os.environ['DRBPORT']

user_work_dir = os.getcwd()
our_work_dir = os.environ['DRAGONBUILD'] + '/device/decryptor/'
appinfo_dir = os.environ['DRAGONBUILD'] + '/device/appinfo/'

filter_template_path = os.environ['DRAGONBUILD'] + '/internal/BundleFilter.plist'


colors = [
    [
        "\033[0;31m",  # Red Shit went wrong
        "\033[0;32m",  # Green meta shit or success
        "\033[0;33m",  # Yellow
        "\033[0;34m",  # Blue
        "\033[0;36m",  # Teal
        "\033[0;37m",  # White Non-state lines
        "\033[0m"
    ],
    [
        "\033[1;31m",  # Bold Red   Shit went wrong
        "\033[1;32m",  # Bold Green meta shit or success
        "\033[1;33m",  # Bold Yellow
        "\033[1;34m",  # Bold Blue
        "\033[1;36m",  # Bold Teal
        "\033[1;37m",  # Bold White Non-state lines
        "\033[0m"
    ]
]


def dprintline(col: int, tool: str, textcol: int, bold: int, pusher: int, msg: str):
    print("%s[%s]%s %s%s%s" % (
        colors[1][col], tool, colors[bold][textcol], ">>> " if pusher else "", msg, colors[0][6]))


def dbstate(msg):
    dprintline(3, "Dragon", 5, 1, 0, msg)
def dgprint(msg):
    dprintline(4, "DragonGen", 5, 0, 0, msg)
def dbwarn(msg):
    dprintline(2, "Dragon", 5, 0, 0, msg)
def dberror(msg):
    dprintline(0, "Dragon", 5, 1, 0, msg)


def system(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
    proc = subprocess.Popen("" + cmd,
                            stdout=stdout,
                            stderr=stderr,
                            shell=True,
                            universal_newlines=True)
    std_out, std_err = proc.communicate()
    # print(proc.returncode)
    return proc.returncode, std_out, std_err

class Constructor(object):

    def __init__(self):
        pass

    def set_container_url(self, bundle_id: str):
        os.chdir(appinfo_dir)
        system('dragon c b i')
        os.chdir(our_work_dir)
        os.system(f'echo "#define kContainerURL \\"$(dragon dr appinfo -c {bundle_id} | cut -c 8-)/Documents/Dump\\"" > decrypt.h ')

    def construct_unique_package(self, bundle_id: str):
        os.chdir(our_work_dir)
        system('mkdir -p build')

        with open(filter_template_path) as filter_file:
            filter_template = filter_file.read()
            filter_file.close()

        filter_template = filter_template.replace('$BUNDLE_ID', bundle_id)
        with open(our_work_dir + 'build/decryptor.plist', 'w') as targetfile:
            targetfile.write(filter_template)
            targetfile.close()

        self.set_container_url(bundle_id)



        # Be safe and just make sure the directory is here
        system('mkdir -p build && cp decrypt.c build')
        system('cp decrypt.h build')

        system('cp DecryptorDragonMake build/DragonMake')

        os.chdir('build')

        system('dragon b i')

class DecryptionHandler(object):
    def __init__(self):
        pass

    def install(self):
        os.chdir(our_work_dir + 'build')

builder = Constructor()
builder.construct_unique_package(bund)