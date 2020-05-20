#!/usr/bin/env python3
import os
import re
import subprocess
import sys
import traceback
from datetime import datetime
from typing import List, TextIO

import yaml

from DragonExceptions import *
from buildgen.buildgen.generator import Generator

exports = {}
# store current variables here in the event of exception
variables_dump = {}
# Legacy regex to match variables in makefiles and dragon bash configs
dragon_match = '(.*)="?(.*)""?#?'
make_match = '(.*)=(.*)#?'

# Regex for functions in new DragonMake kinda-yaml syntax
dm_wildcard = '\$wildcard\("(.*)",.*"(.*)"\)'
dm_eval = '\$eval\("(.*)"\)'


class Project(object):
    default_variables = {
        'builddir': '$pdirname/build',
        'objdir': '$pdirname/obj',
        'signdir': '$pdirname/sign',
        'bridging-header': '$name-Bridging-Header.h',
        'dragondir': '$$DRAGONBUILD',
        'cc': 'clang',
        'cxx': 'clang++',
        'ld': 'clang++',
        'codesign': 'ldid',
        'dsym': 'dsymutil',
        'plutil': 'plutil',
        'swift': 'swift',
        'logos': '$dragondir/bin/logos.pl',
        'optool': '$dragondir/bin/optool',
        'stage': ['true'],
        'warnings': '-Wall',
        'optim': '0',
        'debug': '-fcolor-diagnostics',
        'idflag': '',
        'entflag': '-S',
        'entfile': '',
        'resource_dir': 'Resources',
        'framework_search_dirs': ['$sysroot/System/Library/Frameworks',
                                  '$sysroot/System/Library/PrivateFrameworks',
                                  '$dragondir/frameworks'],
        'library_search_dirs': ['$dragondir/lib', '.'],
        'cinclude': '-I$dragondir/include -I$dragondir/vendor/include -I$dragondir/include/_fallback '
                    '-I$DRAGONBUILD/headers/ -I$pwd',
        'pdirname': '.dragon/',
        'stagedir': '_'
    }

    def __init__(self, project_type: str, variables: dict, out: TextIO, full_config=None):
        self.config = full_config
        self.variables = variables
        self.type = project_type
        self.base_configurations = yaml.safe_load(open(os.environ['DRAGONBUILD'] + "/DragonGen/ProjectConfiguration.yml"))

        self.builder = Generator(out)
        self.target = 'ios'

        if not self.ignores_state('has_build_files'):
            self.files = get_args(self.variables, 'files')
            self.swift_files = get_args(self.variables, 'swift_files')
            self.c_files = get_args(self.variables, 'c_files')
            self.cxx_files = get_args(self.variables, 'cxx_files')
            self.objc_files = get_args(self.variables, 'objc_files')
            self.objcxx_files = get_args(self.variables, 'objcxx_files')
            self.logos_files = get_args(self.variables, 'logos_files')
            self.object_files = get_args(self.variables, 'object_files')
            self.plists = get_args(self.variables, 'plists')
            self.dlists = get_args(self.variables, 'dlists')
            if 'files' in self.variables.keys() or '_files' in str(self.variables):
                self.has_build_files = True
            elif self.requires_state('has_build_files'):
                raise MissingBuildFilesException('No files were provided to build.', variables=self.variables)
            else:
                self.has_build_files = False

    def generate(self):
        self.create_variable_dict()
        self.create_ninja_variables()
        self.create_rules()
        targets = self.create_targets()
        if targets:
            self.builder.default(targets)

    def requires_state(self, state: str):
        try:
            return state in self.base_configurations['Types'][self.type]['required_states']
        except (KeyError, TypeError):
            return False

    def ignores_state(self, state: str):
        try:
            return state in self.base_configurations['Types'][self.type]['ignored_states']
        except (KeyError, TypeError):
            return False

    def create_targets(self):
        """

            :param self.builder:
            :param self.variables:
            :return:
            """

        if self.type == 'resource-bundle':
            self.builder.build('bundle', 'bundle', 'build.ninja')
            return ['bundle']
        if self.type == 'stage':
            self.builder.build('stage', 'stage', 'build.ninja')
            return []
        outputs = []
        targets = ['$build_target_file']
        files = get_args(self.variables, 'files')
        swift_files = get_args(self.variables, 'swift_files')
        c_files = get_args(self.variables, 'c_files')
        cxx_files = get_args(self.variables, 'cxx_files')
        objc_files = get_args(self.variables, 'objc_files')
        objcxx_files = get_args(self.variables, 'objcxx_files')
        logos_files = get_args(self.variables, 'logos_files')
        object_files = get_args(self.variables, 'object_files')
        plists = get_args(self.variables, 'plists')
        dlists = get_args(self.variables, 'dlists')

        if True:

            swift_modules = ""
            has_swift = False

            for f in files:
                if f == "":
                    continue

                filename, ext = os.path.splitext(f)
                if ext in ['x', 'xm']:
                    logos_files.append(f)
                elif ext == 'm':
                    objc_files.append(f)
                elif ext == 'mm':
                    objcxx_files.append(f)
                elif ext == 'c':
                    c_files.append(f)
                elif ext == ['cpp', 'cxx']:
                    cxx_files.append(f)
                elif ext == 'swift':
                    swift_files.append(f)
                elif ext == ['o']:
                    object_files.append(f)
                elif ext == ['plist']:
                    plists.append(f)
                elif ext == ['dlist']:
                    dlists.append(f)

            for filename in logos_files:
                if filename == "":
                    continue
                if '*' in filename:
                    result = subprocess.run(['ls', filename], stdout=subprocess.PIPE)
                    for i in result.stdout.decode('utf-8').split("  "):
                        logos_files.append(i)
                    continue
                self.builder.build(f'$builddir/logos/{os.path.split(filename)[1]}.mm', 'logos', filename)
                objcxx_files.append(f'$builddir/logos/{os.path.split(filename)[1]}.mm')
                self.builder.newline()

            for a in get_args(self.variables, 'archs'):
                arch_specific_object_files = []

                # Only link objc/c++ if we need to.
                linker_conditionals: set = set([])

                for filename in c_files:
                    if filename == "":
                        continue
                    if '*' in filename:
                        result = subprocess.run(['ls', filename], stdout=subprocess.PIPE)
                        for i in result.stdout.decode('utf-8').split("  "):
                            c_files.append(i)
                        continue
                    self.builder.build(f'$builddir/{a}/{os.path.split(filename)[1]}.o', f'c{a}', filename)
                    arch_specific_object_files.append(f'$builddir/{a}/{os.path.split(filename)[1]}.o')
                    self.builder.newline()

                for filename in cxx_files:
                    if filename == "":
                        continue
                    if '*' in filename:
                        result = subprocess.run(['ls', filename], stdout=subprocess.PIPE)
                        for i in result.stdout.decode('utf-8').split("  "):
                            cxx_files.append(i)
                        continue
                    self.builder.build(f'$builddir/{a}/{os.path.split(filename)[1]}.o', f'cxx{a}', filename)
                    arch_specific_object_files.append(f'$builddir/{a}/{os.path.split(filename)[1]}.o')
                    linker_conditionals.add('-lc++')
                    self.builder.newline()

                for filename in objc_files:
                    if filename == "":
                        continue
                    if '*' in filename:
                        result = subprocess.run(['ls', filename], stdout=subprocess.PIPE)
                        for i in result.stdout.decode('utf-8').split("  "):
                            objc_files.append(i)
                        continue
                    self.builder.build(f'$builddir/{a}/{os.path.split(filename)[1]}.o', f'objc{a}', filename)
                    arch_specific_object_files.append(f'$builddir/{a}/{os.path.split(filename)[1]}.o')
                    linker_conditionals.add('-lobjc')
                    self.builder.newline()

                for filename in objcxx_files:
                    if filename == "":
                        continue
                    if '*' in filename:
                        result = subprocess.run(['ls', filename], stdout=subprocess.PIPE)
                        for i in result.stdout.decode('utf-8').split("  "):
                            objcxx_files.append(i)
                        continue
                    self.builder.build(f'$builddir/{a}/{os.path.split(filename)[1]}.o', f'objcxx{a}', filename)
                    arch_specific_object_files.append(f'$builddir/{a}/{os.path.split(filename)[1]}.o')
                    linker_conditionals.add('-lobjc')
                    linker_conditionals.add('-lc++')
                    self.builder.newline()

                for filename in swift_files:
                    if filename == "":
                        continue
                    has_swift = True
                    self.builder.build(f'$builddir/{a}/{os.path.split(filename)[1]}.o', f'swift{a}', filename)
                    arch_specific_object_files.append(f'$builddir/{a}/{os.path.split(filename)[1]}.o')
                    swift_modules += f'$builddir/{a}/{os.path.split(filename)[1]}.o.swiftmodules '
                    self.builder.newline()

                # self.builder.variable_update('libflags', ' '.join(linker_conditionals))

                if has_swift:
                    self.builder.build(f'$builddir/{a}/$name-Swift.h', 'swiftmoduleheader', swift_modules)

                self.builder.build(f'$builddir/$name.{a}', f'link{a}', arch_specific_object_files)
                outputs.append(f'$builddir/$name.{a}')

        self.builder.build('$symtarget', 'lipo', outputs)
        self.builder.newline()

        self.builder.build('$signtarget', 'debug', '$symtarget')
        self.builder.newline()

        self.builder.build('$build_target_file', 'sign', '$signtarget')
        self.builder.newline()

        self.builder.build('stage', 'stage', 'build.ninja')

        return targets

    def create_ninja_variables(self):
        """

        :param self.builder:
        :param variables:
        """
        extrapolate_stage = lambda stage: \
        (lambda slist:
         ';'.join(slist)) \
            (stage.split(';') if isinstance(stage, str) else stage)
        self.builder.variable('name', get_var(self.variables, 'name'))
        self.builder.variable('lowername', get_var(self.variables, 'name').lower())
        self.builder.newline()
        name = self.variables['name']
        self.builder.comment(f'Build file for {name}')
        self.builder.comment(f'Generated at {datetime.now().strftime("%D %H:%M:%S")}')
        self.builder.newline()

        self.builder.variable('pdirname', get_var(self.variables, 'pdirname'))
        self.builder.variable('stagedir', get_var(self.variables, 'stagedir'))
        self.builder.newline()

        self.builder.variable('location', get_var(self.variables, 'install_location'))
        self.builder.variable('resource_dir', get_var(self.variables, 'resource_dir'))
        self.builder.variable('build_target_file', get_var(self.variables, 'build_target_file'))
        self.builder.newline()
        self.builder.variable('stage2', extrapolate_stage(self.base_configurations['Types'][self.type]['variables']['stage2']))
        self.builder.newline()

        self.builder.variable('stagedir', get_var(self.variables, 'stagedir'))
        self.builder.variable('builddir', get_var(self.variables, 'builddir'))
        self.builder.variable('objdir', get_var(self.variables, 'objdir'))
        self.builder.variable('signdir', get_var(self.variables, 'signdir'))
        self.builder.variable('signtarget', '$signdir/$build_target_file.unsigned')
        self.builder.variable('symtarget', '$signdir/$build_target_file.unsym')
        self.builder.newline()

        self.builder.variable('dragondir', get_var(self.variables, 'dragondir'))
        self.builder.variable('pwd', '.')
        self.builder.variable('sysroot', get_var(self.variables, 'sysroot'))
        self.builder.newline()

        self.builder.variable('fwSearch',
                              get_var(self.variables, 'framework_search_dirs') + ' ' + get_var(self.variables,
                                                                                               'additional_framework_search_dirs'))
        self.builder.variable('libSearch',
                              get_var(self.variables, 'library_search_dirs') + ' ' + get_var(self.variables,
                                                                                             'additional_library_search_dirs'))
        self.builder.newline()

        self.builder.variable('cc', get_var(self.variables, 'cc'))
        self.builder.variable('cxx', get_var(self.variables, 'cxx'))
        self.builder.variable('ld', get_var(self.variables, 'ld'))
        self.builder.variable('codesign', get_var(self.variables, 'codesign'))
        self.builder.variable('dsym', get_var(self.variables, 'dsym'))
        self.builder.variable('logos', get_var(self.variables, 'logos'))
        self.builder.variable('swift', get_var(self.variables, 'swift'))
        self.builder.variable('plutil', get_var(self.variables, 'plutil'))
        self.builder.variable('optool', get_var(self.variables, 'optool'))
        self.builder.variable('stage', extrapolate_stage(self.variables['stage']))
        self.builder.newline()

        self.builder.variable('targetvers', get_var(self.variables, 'targetvers'))
        self.builder.newline()
        self.builder.variable('frameworks', get_var(self.variables, 'frameworks'))

        self.builder.newline()

        self.builder.variable('libs', get_var(self.variables, 'libs'))
        self.builder.newline()

        self.builder.variable('arc', '-fobjc-arc' if self.variables['arc'] else '')
        self.builder.variable('btarg', get_var(self.variables, 'targ'))
        self.builder.variable('warnings', get_var(self.variables, 'warnings'))
        self.builder.variable('optim', '-O' + get_var(self.variables, 'optim'))
        self.builder.variable('debug', get_var(self.variables, 'debug'))
        self.builder.newline()

        self.builder.variable('header_includes', get_var(self.variables, 'include'))
        self.builder.variable('cinclude', get_var(self.variables, 'cinclude'))
        self.builder.newline()

        self.builder.variable('usrCflags', get_var(self.variables, 'cflags'))
        self.builder.variable('usrLDflags', get_var(self.variables, 'ldflags'))
        self.builder.newline()

        self.builder.variable('lopt', get_var(self.variables, 'lopts'))
        self.builder.variable('typeldflags', get_var(self.variables, 'ldflags'))

        self.builder.variable('libflags', '-lobjc -lc++')

        cflags = '$cinclude -fmodules -fcxx-modules -fmodule-name=$name -fbuild-session-file=$pdirname/modules/ ' \
                 '-fmodules-prune-after=345600 -fmodules-prune-interval=86400 -fmodules-validate-once-per-build-session ' \
                 '$arc $fwSearch -miphoneos-version-min=$targetvers -isysroot $sysroot $btarg $warnings $optim $debug ' \
                 '$usrCflags $header_includes'
        self.builder.variable('cflags', cflags)
        self.builder.newline()

        lflags = '$cflags $typeldflags $frameworks $libs $libflags $lopt $libSearch $usrLDflags'
        self.builder.variable('lflags', lflags)
        self.builder.newline()

        self.builder.variable('ldflags', '$usrLDFlags')
        self.builder.newline()

        self.builder.variable('swiftflags',
                              '-color-diagnostics -module-name $name -g -enable-objc-interop -swift-version 5 -sdk '
                              '/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS'
                              '.sdk -Onone -L/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain'
                              '/usr/lib/swift/iphoneos -L/usr/lib/swift')

        try:
            os.stat(self.variables["bridging-header"])
            self.builder.variable('bridgeheader', get_var("bridging-header"))
        except FileNotFoundError:
            self.builder.variable('bridgeheader', '')
        self.builder.newline()

        self.builder.variable('swiftfiles', get_var(self.variables, 'swift_files'))

    def create_rules(self):
        self.builder.pool('solo', '1')
        self.builder.newline()

        self.builder.rule('logos', description="seg::Logos file-in::$in expected-out::$out utility::$logos",
                          command="$logos $in > $out")
        self.builder.newline()
        self.builder.rule('prefs', description="seg::DragonPrefs file-in::$in expected-out::$out utility::DragonPrefs",
                          command="python3 $$DRAGONBUILD/DragonGen/preflist.py $in > $out")
        self.builder.newline()

        self.builder.rule('swiftarmv7', description="seg::Swift file-in::$in expected-out::$out utility::$swift",
                          command="SwiftFiles=$$(echo '$swiftfiles $in' | tr ' ' '\\n' | sort | uniq -u); $swift -frontend -c "
                                  "$swiftflags "
                                  "$bridgeheader -target armv7-apple-ios -emit-module-path "
                                  "$out.swiftmodule -primary-file $in $$SwiftFiles -o $out")
        self.builder.newline()
        self.builder.rule('swiftarm64', description="seg::Swift file-in::$in expected-out::$out utility::$swift",
                          command="SwiftFiles=$$(echo '$swiftfiles $in' | tr ' ' '\\n' | sort | uniq -u); $swift -frontend -c "
                                  "$swiftflags "
                                  "$bridgeheader -target arm64-apple-ios -emit-module-path "
                                  "$out.swiftmodule -primary-file $in $$SwiftFiles -o $out")
        self.builder.newline()
        self.builder.rule('swiftarm64e', description="seg::Swift file-in::$in expected-out::$out utility::$swift",
                          command="SwiftFiles=$$(echo '$swiftfiles $in' | tr ' ' '\\n' | sort | uniq -u); $swift -frontend -c "
                                  "$swiftflags "
                                  "$bridgeheader -target arm64e-apple-ios -emit-module-path "
                                  "$out.swiftmodule -primary-file $in $$SwiftFiles -o $out")
        self.builder.newline()
        self.builder.rule('swiftmoduleheader',
                          description="seg::SwiftModuleHeader file-in::$in expected-out::$out utility::$swift",
                          command="$swift -frontend -c $swiftflags $bridgeheader -target arm64-apple-ios7.0 -emit-module "
                                  "-merge-modules $in -emit-objc-header-path $out -o /dev/null")
        self.builder.newline()

        self.builder.newline()
        self.builder.rule('carm64', description="seg::cc~64 file-in::$in expected-out::$out utility::$cc",
                          command="$cc -arch arm64 $cflags -c $in -o $out")
        self.builder.newline()
        self.builder.rule('cxxarm64', description="seg::cxx~64 file-in::$in expected-out::$out utility::$cxx",
                          command="$cxx -arch arm64 $cflags -c $in -o $out")
        self.builder.newline()
        self.builder.rule('objcarm64', description="seg::cc~64 file-in::$in expected-out::$out utility::$cc",
                          command="$cc -arch arm64 $cflags -c $in -o $out")
        self.builder.newline()
        self.builder.rule('objcxxarm64', description="seg::cxx~64 file-in::$in expected-out::$out utility::$cxx",
                          command="$cxx -arch arm64 $cflags -c $in -o $out")
        self.builder.newline()
        self.builder.rule('linkarm64', description="seg::ld~64 file-in::$in expected-out::$out utility::$ld",
                          command="$ld -arch arm64 $lflags -lobjc -lc++ -o $out $in")
        self.builder.newline()

        self.builder.newline()
        self.builder.rule('carm64e', description="seg::cc~64e file-in::$in expected-out::$out utility::$cc",
                          command="$cc -arch arm64e $cflags -c $in -o $out")
        self.builder.newline()
        self.builder.rule('cxxarm64e', description="seg::cxx~64e file-in::$in expected-out::$out utility::$cxx",
                          command="$cxx -arch arm64e $cflags -c $in -o $out")
        self.builder.newline()
        self.builder.rule('objcarm64e', description="seg::cc~64e file-in::$in expected-out::$out utility::$cc",
                          command="$cc -arch arm64e $cflags -c $in -o $out")
        self.builder.newline()
        self.builder.rule('objcxxarm64e', description="seg::cxx~64e file-in::$in expected-out::$out utility::$cxx",
                          command="$cxx -arch arm64e $cflags -c $in -o $out")
        self.builder.newline()
        self.builder.rule('linkarm64e', description="seg::ld~64e file-in::$in expected-out::$out utility::$ld",
                          command="$ld -arch arm64e $lflags -o $out $in")
        self.builder.newline()

        self.builder.newline()
        self.builder.rule('carmv7', description="seg::cc~v7 file-in::$in expected-out::$out utility::$cc",
                          command="$cc -arch armv7 $cflags -c $in -o $out")
        self.builder.newline()
        self.builder.rule('cxxarmv7', description="seg::cxx~v7 file-in::$in expected-out::$out utility::$cxx",
                          command="$cxx -arch armv7 $cflags -c $in -o $out")
        self.builder.newline()
        self.builder.rule('objcarmv7', description="seg::cc~v7 file-in::$in expected-out::$out utility::$cc",
                          command="$cc -arch armv7 $cflags -c $in -o $out")
        self.builder.newline()
        self.builder.rule('objcxxarmv7', description="seg::cxx~v7 file-in::$in expected-out::$out utility::$cxx",
                          command="$cxx -arch armv7 $cflags -c $in -o $out")
        self.builder.newline()
        self.builder.rule('linkarmv7', description="seg::ld~v7 file-in::$in expected-out::$out utility::$ld",
                          command="$ld -arch armv7 $lflags -o $out $in")
        self.builder.newline()

        self.builder.newline()
        self.builder.rule('cx86_64', description="seg::c~x86_64 file-in::$in expected-out::$out utility::$cc",
                          command="$cc -arch x86_64 $cflags -c $in -o $out")
        self.builder.newline()
        self.builder.rule('cxxx86_64', description="seg::cxx~x86_64 file-in::$in expected-out::$out utility::$cxx",
                          command="$cxx -arch x86_64 $cflags -c $in -o $out")
        self.builder.newline()
        self.builder.rule('objcx86_64', description="seg::c~x86_64 file-in::$in expected-out::$out utility::$cc",
                          command="$cc -arch x86_64 $cflags -c $in -o $out")
        self.builder.newline()
        self.builder.rule('objcxxx86_64', description="seg::cxx~x86_64 file-in::$in expected-out::$out utility::$cxx",
                          command="$cxx -arch x86_64 $cflags -c $in -o $out")
        self.builder.newline()
        self.builder.rule('linkx86_64', description="seg::ld~x86_64 file-in::$in expected-out::$out utility::$ld",
                          command="$ld -arch x86_64 $lflags -o $out $in")
        self.builder.newline()

        self.builder.newline()
        self.builder.rule('lipo', description='Merging architectures', command='lipo -create $in -output $out')
        self.builder.newline()
        self.builder.rule('bundle', description="Copying Bundle Resources",
                          command="mkdir -p \"$pdirname/_$location/\" && cp -r \"$resource_dir/\" \"$pdirname/_$location\"",
                          pool='solo')
        self.builder.newline()
        self.builder.rule('plist', description="Converting $in", command="$plutil -convert binary1 $in -o $out")
        self.builder.newline()
        self.builder.rule('debug', description="Generating Debug Symbols for $name",
                          command="$dsym \"$in\" 2&> /dev/null; cp $in $out")
        self.builder.newline()
        self.builder.rule('sign', description="Signing $name",
                          command="$codesign -S $in && cp $in $out")
        self.builder.newline()
        self.builder.rule('otool', description="Injecting $name",
                          command="true;")
        self.builder.newline()
        self.builder.rule('stage', description="Running Stage for $name", command="$stage; $stage2")
        self.builder.newline()

    # noinspection PyTypeChecker
    def create_variable_dict(self):
        """

        """
        variables = Project.default_variables.copy()

        if not self.target:
            self.target = 'ios'

        variables.update(self.base_configurations['Targets'][self.target])

        variables.update(self.base_configurations['Types'][self.type]['variables'])

        if 'all' in variables:
            variables.update(variables['all'])

        if 'all' in self.config:
            variables.update(self.config['all'])

        if 'targets' in variables:
            if self.target in variables['targets']:
                if 'all' in variables['targets'][self.target]:
                    variables.update(variables['targets'][self.target]['all'])
                if self.variables['name']:
                    variables.update(variables['targets'][self.target][variables['name']])

        if self.target in ['ios']:
            print("export DRAGON_DPKG=1")

        variables.update(self.variables)

        if 'toolchain' in variables:
            print(variables['toolchain'], file=sys.stderr)
            tooldb = {
                'cc': variables['toolchain'] + '/' + variables['cc'],
                'cxx': variables['toolchain'] + '/' + variables['ccx'],
                'ld': variables['toolchain'] + '/' + variables['ld'],
                'lipo': variables['toolchain'] + '/' + variables['lipo'],
                'codesign': variables['toolchain'] + '/' + variables['codesign'],
                'dsym': variables['toolchain'] + '/' + variables['dsym'],
                'plutil': variables['toolchain'] + '/' + variables['plutil'],
                'swift': variables['toolchain'] + '/' + variables['swift']
            }
            variables.update(tooldb)

        self.variables = variables.copy()
        global variables_dump
        variables_dump = self.variables.copy()
        if os.environ['DGEN_DEBUG']:
            import pprint
            pprint.pprint(f'\n\n{self.variables["name"]}:\n\n' + str(self.variables), stream=sys.stderr)



crucial_variables = ['name', 'type', 'dir', 'cc', 'cxx', 'ld', 'codesign']

# Variables that contain arguments or lists and thus can be passed as a list or string
# value is what arguments are joined with.
argument_variables = {
    'files': ' ',
    'logos_files': ' ',
    'c_files': ' ',
    'objc_files': ' ',
    'objcxx_files': ' ',
    'cxx_files': ' ',
    'plists': ' ',
    'swift_files': ' ',
    'dlists': ' ',
    'cflags': ' ',
    'ldflags': ' ',
    'codesignflags': ' ',
    'include': ' -I',
    'framework_search_dirs': ' -F',
    'additional_framework_search_dirs': ' -F',
    'library_search_dirs': ' -L',
    'additional_library_search_dirs': ' -L',
    'libs': ' -l',
    'frameworks': ' -framework ',
    'stage': ' ; ',
    'lopts': ' '

}

supports_expressions = ['files', 'logos_files', 'plists', 'swift_files', 'dlists']


def get_var(full_vars, name, is_empty=None):
    """

    :type is_empty: List[Bool]
    :param is_empty:
    :param full_vars:
    :param name:
    :return:
    """
    extrapolate_stage = lambda stage: \
        (lambda slist:
         ';'.join(slist)) \
            (stage.split(';') if isinstance(stage, str) else stage)

    if not is_empty:
        is_empty = [True]
    try:
        value = full_vars[name]
        is_empty[0] = False
    except KeyError as ex:
        if name not in crucial_variables:
            value = ""
        else:
            raise ex
    if name in argument_variables.keys():
        value = arg_list(value) if name not in ['stage', 'stage2'] else extrapolate_stage(value)
        if name in supports_expressions:
            lis = value.split(' ')  # hotfix
            for i in lis:
                wc = re.match(dm_wildcard, i)
                ev = re.match(dm_eval, i)

                if wc:
                    out = subprocess.check_output(f'ls {wc.group(1)}{wc.group(2)} | xargs', shell=True).decode(
                        sys.stdout.encoding).strip()
                elif ev:
                    out = subprocess.check_output(f'{ev.group(1)} | xargs', shell=True).decode(
                        sys.stdout.encoding).strip()
                else:
                    continue

                lis += str(out).split(' ')
            value = ' '.join(lis)
        return arg_list(value, argument_variables[name])
    return value


def get_args(full_vars, name, is_empty=None):
    """Same as get_var but it returns a list

    :param is_empty:
    :param full_vars:
    :param name:
    :return:
    """
    return get_var(full_vars, name, is_empty).split(' ') if name in argument_variables else get_var(full_vars, name,
                                                                                                    is_empty)


def arg_list(items, prefix=''):
    """Process a list or string of arguments into a string containing them

    Used so users can pass arguments as a string or list in the configuration file.

    :param items:
    :param prefix:
    :return:
    """
    if not items:
        return ''

    list_of_items = items.split(' ') if isinstance(items, str) else items

    if list_of_items == ['']:
        return ''

    list_of_items = [prefix + i for i in list_of_items]

    return ' '.join(filter(None, list_of_items))


def main():
    f = open("DragonMake")
    config = yaml.safe_load(f)
    project_dirs = ''

    for i in config:
        if i == 'name':
            exports['package_name'] = config[i]
            continue
        elif i == 'icmd':
            exports['install_command'] = config[i]
            continue
        elif i == 'ip':
            exports['DRBIP'] = config[i]
            continue
        elif i == 'port':
            exports['DRBPORT'] = config[i]
            continue
        elif i == 'exports':
            exports.update(config[i])
            continue
        elif i in ['id', 'author', 'version', 'depends', 'package', 'desc', 'all']:
            continue

        project_config = {
            'name': i,
            'dir': '.'
        }
        project_config.update(config[i])

        if os.environ['DGEN_DEBUG']:
            print("Config:" + str(project_config), file=sys.stderr)
        project_variables = project_config.copy()
        f = open(f"{project_config['dir']}/build.ninja", 'w+')
        proj = Project(project_config['type'], project_variables, f, full_config=config)
        proj.generate()
        f.close()
        project_dirs = project_dirs + ' ' + project_config['dir']

    exports['project_dirs'] = project_dirs

    for i in exports:
        print(f'export {i}="{exports[i]}"')


if __name__ == "__main__":
    try:
        main()
    except MissingBuildFilesException as ex:
        print("We hit an error while generating your package.\n", file=sys.stderr)
        print("The project type specified requires files, but we cant see any in the config.\n", file=sys.stderr)
        print("Press v for detailed debugging output, any other key to exit.", file=sys.stderr)

        import sys, tty, termios

        old_setting = termios.tcgetattr(sys.stdin.fileno())
        tty.setraw(sys.stdin)
        x = sys.stdin.read(1)
        if str(x).lower() == 'v':
            termios.tcsetattr(0, termios.TCSADRAIN, old_setting)
            import pprint

            print("Entire Project Config:", file=sys.stderr)
            pprint.pprint(ex.variables, stream=sys.stderr)
        else:
            termios.tcsetattr(0, termios.TCSADRAIN, old_setting)
            print("Exiting...", file=sys.stderr)

        print("exit 5")
    except KeyError as ex:
        print("KeyError: Something was not found, but it should have been...", file=sys.stderr)
        # print(''.join(traceback.format_tb(ex.__traceback__)), file=sys.stderr)
        print(str(ex), file=sys.stderr)
        print("Press v for detailed debugging output, any other key to exit.", file=sys.stderr)

        import sys, tty, termios

        old_setting = termios.tcgetattr(sys.stdin.fileno())
        tty.setraw(sys.stdin)
        x = sys.stdin.read(1)
        if str(x).lower() == 'v':
            termios.tcsetattr(0, termios.TCSADRAIN, old_setting)
            import pprint
            print("Entire Project Config:", file=sys.stderr)
            pprint.pprint(variables_dump, stream=sys.stderr)
            print(''.join(traceback.format_tb(ex.__traceback__)), file=sys.stderr)
            print(str(ex), file=sys.stderr)
        print("exit 2")
    except Exception as ex:
        import sys, tty, termios

        print("We hit an error while generating your package.", file=sys.stderr)
        print("Unfortunately this error is undocumented.", file=sys.stderr)
        print("This means that either _kritanta broke something, or you've found a new bug!", file=sys.stderr)
        print("Regardless, please do reach out to @_kritanta with this info!\n", file=sys.stderr)

        print("Press v for detailed debugging output, any other key to exit.", file=sys.stderr)

        import sys, tty, termios

        old_setting = termios.tcgetattr(sys.stdin.fileno())
        tty.setraw(sys.stdin)
        x = sys.stdin.read(1)
        if str(x).lower() == 'v':
            termios.tcsetattr(0, termios.TCSADRAIN, old_setting)
            print(''.join(traceback.format_tb(ex.__traceback__)), file=sys.stderr)
            print(repr(ex), file=sys.stderr)
            print(str(ex), file=sys.stderr)
        else:
            termios.tcsetattr(0, termios.TCSADRAIN, old_setting)
            print("Exiting...", file=sys.stderr)

        print("exit -1")
