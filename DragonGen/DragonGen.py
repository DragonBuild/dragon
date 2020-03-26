#!/usr/bin/env python3

import string
import subprocess
import re 
import os
import sys
import ninja_syntax
import yaml

exports = {}

# Legacy regex to match variables in makefiles and dragon bash configs
dragon_match = '(.*)="?(.*)""?#?'
make_match = '(.*)=(.*)#?'

# Regex for functions in new DragonMake kinda-yaml syntax
dm_wildcard = '\$wildcard\("(.*)",.*"(.*)"\)'
dm_eval = '\$eval\("(.*)"\)'


dragonvars = {}
dragonvars['pdirname'] = '.dragon'
dragonvars['builddir'] = '$pdirname/build'
dragonvars['objdir'] = '$pdirname/obj'
dragonvars['signdir'] = '$pdirname/sign'


# These are variables set as default per project type.
# They sometimes get modified by uvars, when the relevant uvar is specified
bvars = {'all':{},'tweak':{}, 'bundle':{}, 'library':{}}

bvars['all']['libs'] = ['objc', 'c++']
bvars['all']['lopts'] = '-dynamiclib -ggdb -lsystem.b -Xlinker -segalign -Xlinker 4000'
bvars['all']['frameworks'] = ['CoreFoundation', 'Foundation', 'UIKit', 'CoreGraphics', 'QuartzCore', 'CoreImage', 'AudioToolbox']

bvars['tweak']['location'] = '/Library/MobileSubstrate/DynamicLibraries/$name.dylib'
bvars['tweak']['target'] = '$pdirname/_$location'
bvars['tweak']['libs'] = ['substrate']
bvars['tweak']['lopts'] = ''
bvars['tweak']['frameworks'] = []

# This is the default location for a pref bundle, which we can assume is what the user wants by default
bvars['bundle']['location'] = '/Library/PreferenceBundles/$name.bundle/$name'
bvars['bundle']['target'] = '$pdirname/_$location'
bvars['bundle']['libs'] = []
bvars['bundle']['lopts']= ''
bvars['bundle']['frameworks'] = ['Preferences']

bvars['library']['location'] = '/usr/lib/$name.dylib'
bvars['library']['target'] = '$pdirname/_$location'
bvars['library']['libs'] = []
bvars['library']['lopts']= ''
bvars['library']['frameworks'] = []

# User modifiable variables

def read_dragon_configuration(ninja):
    f = open("DragonMake", 'r')
    config = yaml.safe_load(f)

    for i in config:
        if i == 'package_name':
            exports['package_name'] = config[i]
            continue 
        elif i == 'install_command':
            exports['install_command'] = config[i]
            continue
        elif i == 'exports': 
            exports.update(config[i])

        package_config = {'name':i}
        package_config.update(config[i])
        project_config = process_package(package_config)
        create_buildfile(ninja, project_config['type'], project_config)


def process_package(package_config):
    uvars = {}

    uvars['name'] = ''
    uvars['type'] = ''

    uvars['dragondir'] = '$$DRAGONBUILD'
    uvars['targetios'] = '10.0'
    uvars['archs'] = ['armv7', 'arm64', 'arm64e']
    uvars['sysroot'] = '$dragondir/sdks/iPhoneOS.sdk'
    uvars['cc'] = 'clang++'
    uvars['ll'] = 'clang++'
    uvars['ld'] = 'ldid'
    uvars['dsym'] = 'dsymutil'
    uvars['logos']= '$dragondir/bin/logos.pl'
    uvars['arc'] = '-fobjc-arc'
    uvars['targ'] = '-DTARGET_IPHONE=1'

    uvars['warnings'] = 'all' #'-W' + this
    uvars['optim'] = '0'
    uvars['debug'] = '-g -DDEBUG'

    uvars['libs'] = []
    uvars['frameworks'] = []

    uvars['cflags'] = ''
    uvars['lflags'] = ''
    uvars['ldflags']= '-S'

    uvars['installLocation'] = ''

    uvars['frameworkSearchDirs'] = ['$sysroot/System/Library/Frameworks', '$sysroot/System/Library/PrivateFrameworks', '$dragondir/frameworks']
    uvars['additionalFrameworkSearchDirs'] = []

    uvars['librarySearchDirs'] = ['$dragondir/lib', '.']
    uvars['additionalLibrarySearchDirs'] = []

    uvars['cinclude'] = '-I$dragondir/include -I$dragondir/vendor/include -I$dragondir/include/_fallback -I$DRAGONBUILD/headers/ -I$pwd'

    uvars.update(package_config)

    return uvars


def create_buildfile(ninja, type, uvars):
    ninja.variable('name', uvars['name'])
    ninja.newline()
    ninja.newline()

    ninja.variable('pdirname', dragonvars['pdirname'])
    ninja.newline()

    ninja.variable('location', bvars[type]['location'] if uvars['installLocation'] == '' else uvars['installLocation'])
    ninja.variable('target', bvars[type]['target'])
    ninja.newline()

    ninja.variable('builddir', dragonvars['builddir'])
    ninja.variable('objdir', dragonvars['objdir'])
    ninja.variable('signdir', dragonvars['signdir'])
    ninja.variable('signtarget', '$signdir/$location.unsigned')
    ninja.variable('symtarget', '$signdir/$location.unsym')
    ninja.newline()

    ninja.variable('dragondir', uvars['dragondir'])
    ninja.variable('pwd', '.')
    ninja.variable('sysroot', uvars['sysroot'])
    ninja.newline()

    ninja.variable('fwSearch', '-F' + ' -F'.join(uvars['frameworkSearchDirs'] + uvars['additionalFrameworkSearchDirs']))
    ninja.variable('libSearch', '-L' + ' -L'.join(uvars['librarySearchDirs'] + uvars['additionalLibrarySearchDirs']))
    ninja.newline()

    ninja.variable('cc', uvars['cc'])
    ninja.variable('ll', uvars['ll'])
    ninja.variable('ld', uvars['ld'])
    ninja.variable('dsym', uvars['dsym'])
    ninja.variable('logos', uvars['logos'])
    ninja.newline()

    ninja.variable('targetios', uvars['targetios'])
    ninja.newline()

    ninja.variable('frameworks','-framework ' + ' -framework '.join(uvars['frameworks'] + bvars[type]['frameworks'] + bvars['all']['frameworks']))
    ninja.newline()
    ninja.variable('libs', '-l' + ' -l'.join(uvars['libs'] + bvars[type]['libs'] + bvars['all']['libs']))
    ninja.newline()
    ninja.variable('arcs', '-arch ' + ' -arch '.join(uvars['archs']))
    ninja.newline()

    ninja.variable('arc', '-fobjc-arc')
    ninja.variable('btarg', uvars['targ'])
    ninja.variable('warnings', '-W' + uvars['warnings'])
    ninja.variable('optim', '-O' + uvars['optim'])
    ninja.variable('debug', uvars['debug'])
    ninja.newline()

    ninja.variable('cinclude', uvars['cinclude'])
    ninja.newline()

    ninja.variable('usrCflags', uvars['cflags'])
    ninja.variable('usrLflags', uvars['lflags'])
    ninja.variable('usrLDFlags', uvars['ldflags'])
    ninja.newline()

    ninja.variable('lopt', bvars['all']['lopts'])
    ninja.newline()

    cflags = '$cinclude $arcs $arc $fwSearch $libSearch -mios-version-min=$targetios -isysroot $sysroot $btarg $warnings $optim $debug $usrCflags'
    ninja.variable('cflags', cflags)
    ninja.newline()

    lflags = '$cflags $frameworks $libs $lopt $usrLflags'
    ninja.variable('lflags', lflags)
    ninja.newline()

    ninja.variable('ldflags', '$usrLDFlags')
    ninja.newline()

    # rules

    ninja.rule('logos', description="Processing $in with Logos",command="$logos $in > $out")
    ninja.newline()
    ninja.rule('compile', description="Compiling $in", command="$cc $cflags -c $in -o $out")
    ninja.newline()
    ninja.rule('link', description="Linking $name", command="$ll $lflags -o $out $in")
    ninja.newline()
    ninja.rule('debug', description="Generating Debug Symbols for $name", command="$dsym \"$in\" 2&> /dev/null; mv $in $out")
    ninja.newline()
    ninja.rule('sign', description="Signing $name", command="$ld $ldflags $in && mv $in $target")
    ninja.newline()

    outputs = []
    logos = uvars['logos_files']
    files = uvars['files']

    for i in logos:
        wc = re.match(dm_wildcard, i)
        ev = re.match(dm_eval, i)
        if wc:
            out = subprocess.check_output(f'ls {wc.group(1)}{wc.group(2)} | xargs', shell=True).decode(sys.stdout.encoding).strip()
        elif ev:
            out = subprocess.check_output(f'{ev.group(1)} | xargs', shell=True).decode(sys.stdout.encoding).strip()
        else:
            continue 

        logos += str(out).split(' ')
        logos.remove(i)
        
    for i in files:
        wc = re.match(dm_wildcard, i)
        ev = re.match(dm_eval, i)
        if wc:
            out = subprocess.check_output(f'ls {wc.group(1)}{wc.group(2)} | xargs', shell=True).decode(sys.stdout.encoding).strip()
        elif ev:
            out = subprocess.check_output(f'{ev.group(1)} | xargs', shell=True).decode(sys.stdout.encoding).strip()
        else:
            continue 

        files += str(out).split(' ')
        files.remove(i)

    for f in logos:
        ninja.build(f'$builddir/{f}.mm', 'logos', f)
        files.append(f'$builddir/{f}.mm')
        ninja.newline()

    for f in files:
        ninja.build(f'$builddir/{f}.o', 'compile', f)
        outputs.append(f'$builddir/{f}.o')
        ninja.newline()

    ninja.build('$symtarget', 'link', outputs)
    ninja.newline()

    ninja.build('$signtarget', 'debug', '$symtarget')
    ninja.newline()

    ninja.build('$target', 'sign', '$signtarget')
    ninja.newline()

    ninja.default('$target')
    ninja.newline()


def main():
    f = open("build.ninja", 'w+')
    ninja = ninja_syntax.Writer(f)
    read_dragon_configuration(ninja)
    f.close()

    for i in exports:
        print(f'export {i}="{exports[i]}"')
    
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


    
if __name__ == "__main__":
    main()