import string
import re 
import os
import sys

dragon_match = '(.*)="?(.*)""?#?'
make_match = '(.*)=(.*)#?'


dragonvars = {}
dragonvars['pdirname'] = '.dragon'


bvars = {'tweak':{}, 'prefs':{}, 'library':{}}

bvars['tweak']['target'] = '$pdirname/_/Library/MobileSubstrate/DynamicLibraries/$name.dylib'
bvars['tweak']['defaultlinks'] = '-lsubstrate'


dvars = {}
dvars['targetios'] = '10.0'
dvars['archs'] = '-arch armv7 -arch arm64 -arch arm64e'
dvars['libs'] = ''
dvars['sysroot'] = '$dragondir/sdks/iPhoneOS.sdk'
dvars['dragondir'] = '$$DRAGONBUILD'
dvars['cc'] = 'clang++'
dvars['ll'] = 'clang++'
dvars['usrCflags'] = ''
dvars['arc'] = '-fobjc-arc'

def getmakevars(filename, filter):
    variables = {}
    fp = open(filename)
    try:
        while 1:
            line = fp.readline()
            match = re.search(make_match, line)
            if match:
                one_tuple = match.group(1,2)
                variables[one_tuple[0]] = one_tuple[1]
            if not line:
                break
    finally:
        fp.close()
    return variables


def main():
    files = []
    filess = [f for f in os.listdir('.') if os.path.isfile(f)]
    for file in filess:
        if 'Makefile' in file or 'DragonMake' in file:
            files.append(file)
    if 'DragonMake' in files:
        variables = getmakevars('DragonMake')
        print(variables)
    elif 'Makefile' in files:
        variables = getmakevars('Makefile')
        print(variables)
    else:
        print("DragonMake or Makefile not found.")
        exit(1)
    
    
    
if __name__ == "__main__":
    main()