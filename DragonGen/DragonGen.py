#!/usr/bin/env python3

import string
from datetime import datetime
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
bvars = {'all':{},'tweak':{}, 'bundle':{}, 'library':{}, 'cli':{}, 'app':{}, 'raw':{}}

bvars['archfiles'] = {}

bvars['all']['libs'] = ['objc', 'c++']
bvars['all']['lopts'] = ''
bvars['all']['frameworks'] = []
bvars['all']['ldflags'] = ''

bvars['tweak']['location'] = '/Library/MobileSubstrate/DynamicLibraries/'
bvars['tweak']['target'] = '$pdirname/_$location$name.dylib'
bvars['tweak']['libs'] = ['substrate']
bvars['tweak']['lopts'] = '-dynamiclib -ggdb -Xlinker -segalign -Xlinker 4000'
bvars['tweak']['ldflags'] = '-install_name $location$name'
bvars['tweak']['frameworks'] = ['CoreFoundation', 'Foundation', 'UIKit', 'CoreGraphics', 'QuartzCore', 'CoreImage', 'AudioToolbox']
bvars['tweak']['stage2'] = 'cp $name.plist .dragon/_/Library/MobileSubstrate/DynamicLibraries/$name.plist'

# This is the default location for a pref bundle, which we can assume is what the user wants by default
bvars['bundle']['location'] = '/Library/PreferenceBundles/$name.bundle/'
bvars['bundle']['target'] = '$pdirname/_$location$name'
bvars['bundle']['libs'] = []
bvars['bundle']['ldflags'] = '-install_name $location$name'
bvars['bundle']['lopts']= '-dynamiclib -ggdb -Xlinker -segalign -Xlinker 4000'
bvars['bundle']['frameworks'] = ['CoreFoundation', 'Foundation', 'UIKit', 'CoreGraphics', 'QuartzCore', 'CoreImage', 'AudioToolbox']
bvars['bundle']['stage2'] = ''

bvars['library']['location'] = '/usr/lib/'
bvars['library']['target'] = '$pdirname/_$location$name.dylib'
bvars['library']['libs'] = []
bvars['library']['ldflags'] = '-install_name $location$name.dylib'
bvars['library']['lopts']= '-dynamiclib -ggdb -Xlinker -segalign -Xlinker 4000'
bvars['library']['frameworks'] = []
bvars['library']['stage2'] = ''

bvars['cli']['location'] = '/usr/bin/'
bvars['cli']['target'] = '$pdirname/_$location$name'
bvars['cli']['libs'] = []
bvars['cli']['lopts'] = ''
bvars['cli']['ldflags'] = ''
bvars['cli']['frameworks'] = []
bvars['cli']['stage2'] = ''


bvars['app']['location'] = '/Applications/'
bvars['app']['target'] = '$pdirname/_$location$name.app/$name'
bvars['app']['libs'] = []
bvars['app']['lopts'] = ''
bvars['app']['ldflags'] = ''
bvars['app']['frameworks'] = []
bvars['app']['stage2'] = ''

# User modifiable variables

def read_dragon_configuration():
    f = open("DragonMake", 'r')
    config = yaml.safe_load(f)
    project_dirs = ''

    for i in config:
        if i == 'package_name':
            exports['package_name'] = config[i]
            continue 
        elif i == 'install_command':
            exports['install_command'] = config[i]
            continue
        elif i == 'exports': 
            exports.update(config[i])

        package_config = {'name':i, 'dir':'.'}
        package_config.update(config[i])
        project_config = process_package(package_config)

        f = open(f"{project_config['dir']}/build.ninja", 'w+')
        ninja = ninja_syntax.Writer(f)
        create_buildfile(ninja, project_config['type'], project_config)
        f.close()
        project_dirs = project_dirs + ' ' + project_config['dir']
    
    exports['project_dirs'] = project_dirs


def process_package(package_config):
    uvars = {}

    uvars['name'] = ''
    uvars['type'] = ''

    uvars['prelogos_files'] = []
    uvars['logos_files'] = []
    uvars['files'] = []
    uvars['plists'] = []

    uvars['dragondir'] = '$$DRAGONBUILD'
    uvars['targetios'] = '10.0'
    uvars['archs'] = ['armv7', 'arm64', 'arm64e']
    uvars['sysroot'] = '$dragondir/sdks/iPhoneOS.sdk'
    uvars['cc'] = 'clang++'
    uvars['ccpp'] = 'clang++'
    uvars['ld'] = 'clang++'
    uvars['ldid'] = 'ldid'
    uvars['dsym'] = 'dsymutil'
    uvars['plutil'] = 'plutil'
    uvars['logos']= '$dragondir/bin/logos.pl'
    uvars['stage'] = 'true;'
    uvars['arc'] = '-fobjc-arc'
    uvars['targ'] = '-DTARGET_IPHONE=1'

    uvars['warnings'] = '-Wall' #'-W' + this
    uvars['optim'] = '0'
    uvars['debug'] = '-fcolor-diagnostics'

    uvars['libs'] = []
    uvars['frameworks'] = []

    uvars['cflags'] = ''
    uvars['c_header_search_dirs'] = ['']
    uvars['ldflags'] = ''
    uvars['ldidflags'] = '-S'

    uvars['install_location'] = ''
    uvars['resource_dir'] = 'Resources'
    uvars['nocomp']  = 0

    uvars['framework_search_dirs'] = ['$sysroot/System/Library/Frameworks', '$sysroot/System/Library/PrivateFrameworks', '$dragondir/frameworks']
    uvars['additional_framework_search_dirs'] = []

    uvars['library_search_dirs'] = ['$dragondir/lib', '.']
    uvars['additional_library_search_dirs'] = []

    uvars['cinclude'] = '-I$dragondir/include -I$dragondir/vendor/include -I$dragondir/include/_fallback -I$DRAGONBUILD/headers/ -I$pwd'

    uvars.update(package_config)

    if uvars['type'] == 'lib':
        uvars['type'] = 'library'

    return uvars


def create_buildfile(ninja, type, uvars):
    ninja.variable('name', uvars['name'])
    ninja.variable('lowername', uvars['name'].lower())
    ninja.newline()
    name = uvars['name']
    ninja.comment(f'Build file for {name}')
    ninja.comment(f'Generated at {datetime.now().strftime("%D %H:%M:%S")}')
    ninja.newline()

    ninja.variable('pdirname', dragonvars['pdirname'])
    ninja.newline()

    ninja.variable('location', bvars[type]['location'].replace(' ', '$ ') if uvars['install_location'] == '' else uvars['install_location'].replace(' ', '$ '))
    ninja.variable('resource_dir', uvars['resource_dir'].replace(' ', '$ '))
    ninja.variable('target', bvars[type]['target'])
    ninja.newline()
    ninja.variable('stage2', bvars[type]['stage2'])
    ninja.newline()

    ninja.variable('builddir', dragonvars['builddir'])
    ninja.variable('objdir', dragonvars['objdir'])
    ninja.variable('signdir', dragonvars['signdir'])
    ninja.variable('signtarget', '$signdir/$target.unsigned')
    ninja.variable('symtarget', '$signdir/$target.unsym')
    ninja.newline()

    ninja.variable('dragondir', uvars['dragondir'])
    ninja.variable('pwd', '.')
    ninja.variable('sysroot', uvars['sysroot'])
    ninja.newline()

    ninja.variable('fwSearch', '-F' + ' -F'.join(uvars['framework_search_dirs'] + uvars['additional_framework_search_dirs']))
    ninja.variable('libSearch', '-L' + ' -L'.join(uvars['library_search_dirs'] + uvars['additional_library_search_dirs']))
    ninja.newline()

    ninja.variable('cc', uvars['cc'])
    ninja.variable('ccpp', uvars['ccpp'])
    ninja.variable('ld', uvars['ld'])
    ninja.variable('ldid', uvars['ldid'])
    ninja.variable('dsym', uvars['dsym'])
    ninja.variable('logos', uvars['logos'])
    ninja.variable('plutil', uvars['plutil'])
    ninja.variable('stage', uvars['stage'] if isinstance(uvars['stage'], str) else ' && '.join(uvars['stage']))
    ninja.newline()

    ninja.variable('targetios', uvars['targetios'])
    ninja.newline()
    fws = uvars['frameworks'] + bvars[type]['frameworks'] + bvars['all']['frameworks']
    ninja.variable('frameworks',arg_list(fws, '-framework '))

    ninja.newline()
    libs = uvars['libs'] + bvars[type]['libs'] + bvars['all']['libs']
    
    ninja.variable('libs', arg_list(libs, '-l'))
    ninja.newline()

    ninja.variable('arc', uvars['arc'])
    ninja.variable('btarg', uvars['targ'])
    ninja.variable('warnings', uvars['warnings'])
    ninja.variable('optim', '-O' + uvars['optim'])
    ninja.variable('debug', uvars['debug'])
    ninja.newline()
    
    ninja.variable('header_includes', arg_list(uvars['c_header_search_dirs'], '-I'))
    ninja.variable('cinclude', uvars['cinclude'])
    ninja.newline()

    ninja.variable('usrCflags', arg_list(uvars['cflags']))
    ninja.variable('usrLDflags', arg_list(uvars['ldflags']))
    ninja.variable('usrLDIDFlags', arg_list(uvars['ldidflags']))
    ninja.newline()

    ninja.variable('lopt', bvars['all']['lopts'] + bvars[type]['lopts'])
    ninja.variable('typeldflags', bvars['all']['ldflags'] + bvars[type]['ldflags'])
    ninja.newline()

    cflags = '$cinclude -fmodules -fcxx-modules -fmodule-name=$name -fbuild-session-file=.dragon/modules/ -fmodules-prune-after=345600 -fmodules-prune-interval=86400 -fmodules-validate-once-per-build-session $arc $fwSearch -miphoneos-version-min=$targetios -isysroot $sysroot $btarg $warnings $optim $debug $usrCflags $header_includes'
    ninja.variable('cflags', cflags)
    ninja.newline()

    lflags = '$cflags $typeldflags $frameworks $libs $lopt $libSearch $usrLDflags'
    ninja.variable('lflags', lflags)
    ninja.newline()

    ninja.variable('ldflags', '$usrLDFlags')
    ninja.newline()

    # rules

    ninja.pool('solo', '1')
    ninja.newline()

    ninja.rule('prelogos', description="Processing $in with Pre/Logos",command="cat $in | python3 $$DRAGONBUILD/bin/prelogos.py > $out")
    ninja.newline()
    ninja.rule('logos', description="Processing $in with Logos",command="$logos $in > $out")
    
    ninja.newline()
    ninja.rule('compilearm64', description="Compiling $in for arm64", command="$cc -arch arm64 $cflags -c $in -o $out")
    ninja.newline()
    ninja.rule('compilexxarm64', description="Compiling $in for arm64", command="$cxx -arch arm64 $cflags -c $in -o $out")
    ninja.newline()
    ninja.rule('linkarm64', description="Linking $name for arm64", command="$ld -arch arm64 $lflags -o $out $in")
    
    ninja.newline()
    ninja.rule('compilearm64e', description="Compiling $in for arm64e", command="$cc -arch arm64e $cflags -c $in -o $out")
    ninja.newline()
    ninja.rule('compilexxarm64e', description="Compiling $in for arm64e", command="$cxx -arch arm64e $cflags -c $in -o $out")
    ninja.newline()
    ninja.rule('linkarm64e', description="Linking $name for arm64e", command="$ld -arch arm64e $lflags -o $out $in")
    
    ninja.newline()
    ninja.rule('compilearmv7', description="Compiling $in for armv7", command="$cc -arch armv7 $cflags -c $in -o $out")
    ninja.newline()
    ninja.rule('compilexxarmv7', description="Compiling $in for armv7", command="$cxx -arch armv7 $cflags -c $in -o $out")
    ninja.newline()
    ninja.rule('linkarmv7', description="Linking $name for armv7", command="$ld -arch armv7 $lflags -o $out $in")
    
    ninja.newline()
    ninja.rule('compilex86_64', description="Compiling $in for x86_64", command="$cc -arch x86_64 $cflags -c $in -o $out")
    ninja.newline()
    ninja.rule('compilexxx86_64', description="Compiling $in for x86_64", command="$cxx -arch x86_64 $cflags -c $in -o $out")
    ninja.newline()
    ninja.rule('linkx86_64', description="Linking $name for x86_64", command="$ld -arch x86_64 $lflags -o $out $in")
    
    ninja.newline()
    ninja.rule('lipo', description='Merging architectures', command='lipo -create $in -output $out')
    ninja.newline()
    ninja.rule('bundle', description="Copying Bundle Resources", command="mkdir -p \".dragon/_$location/\" && cp -r \"$resource_dir/\" \".dragon/_$location\" && cp $in $out", pool='solo')
    ninja.newline()
    ninja.rule('plist', description="Converting $in", command="$plutil -convert binary1 $in -o $out")
    ninja.newline()
    ninja.rule('debug', description="Generating Debug Symbols for $name", command="$dsym \"$in\" 2&> /dev/null; cp $in $out")
    ninja.newline()
    ninja.rule('sign', description="Signing $name", command="$ldid $usrLDIDFlags $in && cp $in $target")
    ninja.newline()
    ninja.rule('stage', description="Running Stage for $name", command="$stage $stage2")
    ninja.newline()

    outputs = []
    targets = ['$target'] if uvars['nocomp'] == 0 else []
    prelogos = uvars['prelogos_files']
    logos = uvars['logos_files']
    files = uvars['files']
    plists = uvars['plists']
    if uvars['nocomp'] == 0:
        for i in prelogos:
            wc = re.match(dm_wildcard, i)
            ev = re.match(dm_eval, i)
            if wc:
                out = subprocess.check_output(f'ls {wc.group(1)}{wc.group(2)} | xargs', shell=True).decode(sys.stdout.encoding).strip()
            elif ev:
                out = subprocess.check_output(f'{ev.group(1)} | xargs', shell=True).decode(sys.stdout.encoding).strip()
            else:
                if uvars['dir'] != '.':
                    i = '../' + i
                continue 

            if uvars['dir'] != '.':
                prelogos += ' ../'.join(('../'+str(out)).split(' ')).split(' ')
            else:
                prelogos += str(out).split(' ')
            prelogos.remove(i)
        for i in logos:
            wc = re.match(dm_wildcard, i)
            ev = re.match(dm_eval, i)
            if wc:
                out = subprocess.check_output(f'ls {wc.group(1)}{wc.group(2)} | xargs', shell=True).decode(sys.stdout.encoding).strip()
            elif ev:
                out = subprocess.check_output(f'{ev.group(1)} | xargs', shell=True).decode(sys.stdout.encoding).strip()
            else:
                if uvars['dir'] != '.':
                    i = '../' + i
                continue 

            if uvars['dir'] != '.':
                logos += ' ../'.join(('../'+str(out)).split(' ')).split(' ')
            else:
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
                if uvars['dir'] != '.':
                    i = '../' + i
                continue 

            if uvars['dir'] != '.':
                files += ' ../'.join(('../'+str(out)).split(' ')).split(' ')
            else:
                files += str(out).split(' ')
            files.remove(i)

        for i in plists:
            wc = re.match(dm_wildcard, i)
            ev = re.match(dm_eval, i)
            if wc:
                out = subprocess.check_output(f'ls {wc.group(1)}{wc.group(2)} | xargs', shell=True).decode(sys.stdout.encoding).strip()
            elif ev:
                out = subprocess.check_output(f'{ev.group(1)} | xargs', shell=True).decode(sys.stdout.encoding).strip()
            else:
                if uvars['dir'] != '.':
                    i = '../' + i
                continue 

            if uvars['dir'] != '.':
                plists += ' ../'.join(('../'+str(out)).split(' ')).split(' ')
            else:
                plists += str(out).split(' ')
            plists.remove(i)

        for f in prelogos:
            ninja.build(f'$builddir/prelogos/{os.path.split(f)[1]}.xm', 'prelogos', f)
            logos.append(f'$builddir/prelogos/{os.path.split(f)[1]}.xm')
            ninja.newline()

        for f in logos:
            ninja.build(f'$builddir/logos/{os.path.split(f)[1]}.mm', 'logos', f)
            files.append(f'$builddir/logos/{os.path.split(f)[1]}.mm')
            ninja.newline()

        for a in uvars['archs']:

            archfiles = []

            for f in files:
                ninja.build(f'$builddir/{a}/{os.path.split(f)[1]}.o', f'compile{a}', f)
                archfiles.append(f'$builddir/{a}/{os.path.split(f)[1]}.o')
                ninja.newline()

            ninja.build(f'$builddir/$name.{a}', f'link{a}', archfiles)
            outputs.append(f'$builddir/$name.{a}')


    if type == 'bundle':
        # Use the build file itself as a way to trick ninja into working without a specific file
        ninja.build('$builddir/trash/bundles', 'bundle', 'build.ninja') 
        targets.append('$builddir/trash/bundles')
        ninja.newline()
    
    ninja.build('$builddir/trash/stage', 'stage', ('$target' if uvars['nocomp'] == 0 else 'build.ninja'))
    targets.append('$builddir/trash/stage')
    ninja.newline()

    ninja.build('$symtarget', 'lipo', outputs)
    ninja.newline()

    ninja.build('$signtarget', 'debug', '$symtarget')
    ninja.newline()

    ninja.build('$target', 'sign', '$signtarget')
    ninja.newline()

    for f in plists:
        ninja.build(f'.dragon/_$location./{os.path.split(f)[1]}', 'plist', f)
        targets.append(f'.dragon/_$location./{os.path.split(f)[1]}')
        ninja.newline()

    ninja.default(targets)
    ninja.newline()

def arg_list(items, prefix=''):
    if not items:
        return ''

    litems = items.split(' ') if isinstance(items, str) else items 

    if litems == ['']:
        return ''

    litems = [prefix + i for i in litems]

    return ' '.join(litems)
    
        

def main():
    read_dragon_configuration()

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