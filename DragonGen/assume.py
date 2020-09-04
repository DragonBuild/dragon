#!/usr/bin/env python3

import string
import subprocess
import re
import os
import sys

PrefixColor = u'\u001b[34;1m'
GenColor = u'\u001b[33m'
BoldColor = u'\u001b[37;1m'
NC = u'\u001b[0m'


def assume():
    f = open("DragonMake", 'w+')
    dir_path = os.path.basename(os.getcwd())
    f.write("---\n")
    f.write(f'name: {dir_path}\n')
    f.write('icmd: sbreload\n\n')
    f.write(f'{dir_path}:\n')
    f.write('  type: tweak\n')
    f.write('  logos_files:\n    - Tweak.xm\n')
    f.close()
    if not os.path.exists(f'{dir_path}.plist'):
        bfilter = open(f'{dir_path}.plist', 'w+')
        bfilter.write('{ Filter = { Bundles = ( "com.apple.springboard" ); }; }')
        bfilter.close()
    if not os.path.exists('control'):
        control = open('control', 'w+')
        control.write(
            f'Package: com.yourcompany.{dir_path}\nName: {dir_path}\nDepends: mobilesubstrate\nVersion: 0.0.1\nArchitecture: iphoneos-arm\nDescription: An awesome MobileSubstrate tweak!\nMaintainer: {os.getlogin()}\nAuthor: {os.getlogin()}\nSection: Tweaks')
        control.close()


def main():
    prompt = int(input(
        PrefixColor + u'[Dragon] ' + NC + u'No DragonMake Found.\n1. Assume input\n2. New Project Creator\n3. Exit\n'))
    if prompt == 1:
        assume()
    else:
        exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
    except Exception:
        exit(1)
