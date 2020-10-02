import os, sys, subprocess

runtime = \
    {
        'install': 0,
        'build': 0,
        'gen': 0,
        'clean': 0,
        'exportt': 0,
        'only': 0,
        'norm': 0,
        'debug': 0,
        'debugproc': "",
        'ddebug': 0,
        'flutter': 0,
        'DRAGON_DPKG': 1,
        'DRAGON_POSTINST': 0,
        'simtarg': 0,
        'release': 0
    }

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


def main():
    while True:
        try:
            print(eval(input('>>> ')))
        except Exception as ex:
            print(ex)


def system(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
    proc = subprocess.Popen("" + cmd,
                            stdout=stdout,
                            stderr=stderr,
                            shell=True,
                            universal_newlines=True)
    std_out, std_err = proc.communicate()
    # print(proc.returncode)
    return proc.returncode, std_out, std_err


if __name__ == '__main__':
    main()
