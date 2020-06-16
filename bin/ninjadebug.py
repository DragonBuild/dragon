import curses
import os
from glob import glob

buildfiles = [y for x in os.walk(os.getcwd()) for y in glob(os.path.join(x[0], '*.ninja'))]


def character(stdscr):
    attributes = {}
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    attributes['normal'] = curses.color_pair(1)

    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    attributes['highlighted'] = curses.color_pair(2)

    c = 0  # last character read
    option = 0  # the current option that is marked
    while c != 10:  # Enter in ascii
        stdscr.erase()
        stdscr.addstr("Pick file?\n", curses.A_UNDERLINE)
        for i in range(len(buildfiles)):
            if i == option:
                attr = attributes['highlighted']
            else:
                attr = attributes['normal']
            stdscr.addstr("{0}. ".format(i + 1))
            stdscr.addstr(buildfiles[i] + '\n', attr)
        c = stdscr.getch()
        if c == curses.KEY_UP and option > 0:
            option -= 1
        elif c == curses.KEY_DOWN and option < len(buildfiles) - 1:
            option += 1

    import sys
    import subprocess
    subprocess.Popen(["code", buildfiles[option]])
    sys.exit(0)


curses.wrapper(character)
