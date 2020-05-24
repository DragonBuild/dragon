#!/usr/bin/env python3
import os
import re
import string
import subprocess
import sys
import traceback
import glob
from datetime import datetime
from typing import List, TextIO

import regex as regex
import yaml

from DragonExceptions import *
from buildgen.buildgen.generator import Generator

exports = {}
# store current variables here in the event of exception
variables_dump = {}
# Legacy regex to match variables in makefiles and dragon bash configs
dragon_match = '(.*)="?(.*)""?#?'
make_match = regex.compile('(.*)=(.*)#?')
make_type = regex.compile(r'\$\(THEOS_MAKE_PATH\)\/(.*).mk')


class Project(object):

    def __init__(self, project_type: str, variables: dict, out: TextIO, full_config=None):
        self.config = full_config
        self.variables = variables
        self.type = project_type
        self.base_configurations = yaml.safe_load(open(os.environ['DRAGONBUILD'] + "/DragonGen/defaults.yml"))

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
        targets, used_rules = self.create_targets()
        # self.create_rules(used_rules)
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
        rules = yaml.safe_load(open(os.environ['DRAGONBUILD'] + "/DragonGen/rules.yml"))

        if self.type == 'resource-bundle':
            self.builder.rule(f'bundle', description=rules[f'bundle']['desc'],
                              command=rules[f'bundle']['cmd'])
            self.builder.newline()
            self.builder.build('bundle', 'bundle', 'build.ninja')
            self.builder.rule(f'stage', description=rules[f'stage']['desc'],
                              command=rules[f'stage']['cmd'])
            self.builder.newline()
            self.builder.build('stage', 'stage', 'build.ninja')
            return ['bundle', 'stage'], ['bundle', 'stage']
        if self.type == 'stage':
            self.builder.rule(f'stage', description=rules[f'stage']['desc'],
                              command=rules[f'stage']['cmd'])
            self.builder.newline()
            self.builder.build('stage', 'stage', 'build.ninja')
            return [], ['stage']
        outputs = []
        used_rules = {
            'logos': False,
            'prefs': False,
            'swiftarmv6': False,
            'swiftarmv7': False,
            'swiftarmv7s': False,
            'swiftarm64': False,
            'swiftarm64e': False,
            'swiftmoduleheader': False,
            'carmv6': False,
            'carmv7': False,
            'carmv7s': False,
            'carm64': False,
            'carm64e': False,
            'cx86_64': False,
            'ci386': False,
            'cxxarmv6': False,
            'cxxarmv7': False,
            'cxxarmv7s': False,
            'cxxarm64': False,
            'cxxarm64e': False,
            'cxxx86_64': False,
            'cxxi386': False,
            'objcarmv6': False,
            'objcarmv7': False,
            'objcarmv7s': False,
            'objcarm64': False,
            'objcarm64e': False,
            'objcx86_64': False,
            'objci386': False,
            'objcxxarmv6': False,
            'objcxxarmv7': False,
            'objcxxarmv7s': False,
            'objcxxarm64': False,
            'objcxxarm64e': False,
            'objcxxx86_64': False,
            'objcxxi386': False,
            'linkarmv6': False,
            'linkarmv7': False,
            'linkarmv7s': False,
            'linkarm64': False,
            'linkarm64e': False,
            'lipo': False,
            'bundle': False,
            'plist': False,
            'debug': False,
            'sign': False,
            'stage': False
        }

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

        subdir = self.variables['dir'] + '/'

        if True:

            swift_modules = ""
            has_swift = False

            for f in files:
                if f == "":
                    continue

                filename, ext = os.path.splitext(f)
                if ext in ['.x', '.xm']:
                    logos_files.append(f)
                elif ext == '.m':
                    objc_files.append(f)
                elif ext == '.mm':
                    objcxx_files.append(f)
                elif ext == '.c':
                    c_files.append(f)
                elif ext == ['.cpp', '.cxx']:
                    cxx_files.append(f)
                elif ext == '.swift':
                    swift_files.append(f)
                elif ext == ['.o']:
                    object_files.append(f)
                elif ext == ['.plist']:
                    plists.append(f)
                elif ext == ['.dlist']:
                    dlists.append(f)
                files.remove(f)

            ind = 0
            while ind < len(logos_files):
                filename = logos_files[ind]

                if filename == "":
                    logos_files.remove(filename)
                    continue

                if '*' in filename:
                    logos_files.remove(filename)
                    for i in glob.glob(subdir + filename, recursive=True):
                        logos_files.append(i.split(subdir)[1])

                    continue

                if not used_rules['logos']:
                    self.builder.rule('logos', description=rules['logos']['desc'],
                                      command=rules['logos']['cmd'])
                    self.builder.newline()
                    used_rules['logos'] = True

                fffilename, ext = os.path.splitext(filename)
                if ext in ['.x']:
                    self.builder.build(f'$builddir/logos/{os.path.split(filename)[1]}.m', 'logos', filename)
                    objc_files.append(f'$builddir/logos/{os.path.split(filename)[1]}.m')
                elif ext in ['.xm']:
                    self.builder.build(f'$builddir/logos/{os.path.split(filename)[1]}.mm', 'logos', filename)
                    objcxx_files.append(f'$builddir/logos/{os.path.split(filename)[1]}.mm')
                self.builder.newline()

                ind += 1

            for a in get_args(self.variables, 'archs'):
                arch_specific_object_files = []

                # Only link objc/c++ if we need to.
                linker_conditionals: set = set([])

                ind = 0
                while ind < len(c_files):
                    filename = c_files[ind]

                    if filename == "":
                        c_files.remove(filename)
                        continue

                    if '*' in filename:
                        c_files.remove(filename)
                        for i in glob.glob(subdir + filename, recursive=True):
                            c_files.append(i.split(subdir)[1])
                        continue

                    if not used_rules[f'c{a}']:
                        self.builder.rule(f'c{a}', description=rules[f'c{a}']['desc'],
                                          command=rules[f'c{a}']['cmd'])
                        self.builder.newline()
                        used_rules[f'c{a}'] = True

                    self.builder.build(f'$builddir/{a}/{os.path.split(filename)[1]}.o', f'c{a}', filename)
                    arch_specific_object_files.append(f'$builddir/{a}/{os.path.split(filename)[1]}.o')
                    self.builder.newline()

                    ind += 1

                ind = 0
                while ind < len(cxx_files):

                    filename = cxx_files[ind]

                    if filename == "":
                        cxx_files.remove(filename)
                        continue

                    if '*' in filename:
                        cxx_files.remove(filename)
                        for i in glob.glob(subdir + filename, recursive=True):
                            cxx_files.append(i.split(subdir)[1])
                        continue

                    if not used_rules[f'cxx{a}']:
                        self.builder.rule(f'cxx{a}', description=rules[f'cxx{a}']['desc'],
                                          command=rules[f'cxx{a}']['cmd'])
                        self.builder.newline()
                        used_rules[f'cxx{a}'] = True

                    self.builder.build(f'$builddir/{a}/{os.path.split(filename)[1]}.o', f'cxx{a}', filename)
                    arch_specific_object_files.append(f'$builddir/{a}/{os.path.split(filename)[1]}.o')
                    linker_conditionals.add('-lc++')
                    self.builder.newline()

                    ind += 1

                ind = 0
                while ind < len(objc_files):

                    filename = objc_files[ind]

                    if filename == "":
                        objc_files.remove(filename)
                        continue

                    if '*' in filename:
                        objc_files.remove(filename)
                        for i in glob.glob(subdir + filename, recursive=True):
                            objc_files.append(i.split(subdir)[1])
                        continue

                    if not used_rules[f'objc{a}']:
                        self.builder.rule(f'objc{a}', description=rules[f'objc{a}']['desc'],
                                          command=rules[f'objc{a}']['cmd'])
                        self.builder.newline()
                        used_rules[f'objc{a}'] = True

                    self.builder.build(f'$builddir/{a}/{os.path.split(filename)[1]}.o', f'objc{a}', filename)
                    arch_specific_object_files.append(f'$builddir/{a}/{os.path.split(filename)[1]}.o')
                    linker_conditionals.add('-lobjc')
                    self.builder.newline()

                    ind += 1

                ind = 0
                while ind < len(objcxx_files):
                    filename = objcxx_files[ind]
                    if filename == "":
                        objcxx_files.remove(filename)
                        continue

                    if '*' in filename:
                        objcxx_files.remove(filename)
                        for i in glob.glob(subdir + filename, recursive=True):
                            objcxx_files.append(i.split(subdir)[1])
                        continue

                    if not used_rules[f'objcxx{a}']:
                        self.builder.rule(f'objcxx{a}', description=rules[f'objcxx{a}']['desc'],
                                          command=rules[f'objcxx{a}']['cmd'])
                        self.builder.newline()
                        used_rules[f'objcxx{a}'] = True

                    self.builder.build(f'$builddir/{a}/{os.path.split(filename)[1]}.o', f'objcxx{a}', filename)
                    arch_specific_object_files.append(f'$builddir/{a}/{os.path.split(filename)[1]}.o')
                    linker_conditionals.add('-lobjc')
                    linker_conditionals.add('-lc++')
                    self.builder.newline()

                    ind += 1

                ind = 0
                while ind < len(swift_files):
                    filename = swift_files[ind]

                    if filename == "":
                        swift_files.remove(filename)
                        ind += 1
                        continue

                    if '*' in filename:
                        swift_files.remove(filename)
                        for i in glob.glob(subdir + filename, recursive=self.variables['wild_recurse']):
                            swift_files.append(i.split(subdir)[1])
                        continue

                    has_swift = True
                    self.builder.build(f'$builddir/{a}/{os.path.split(filename)[1]}.o', f'swift{a}', filename)
                    arch_specific_object_files.append(f'$builddir/{a}/{os.path.split(filename)[1]}.o')
                    swift_modules += f'$builddir/{a}/{os.path.split(filename)[1]}.o.swiftmodules '
                    self.builder.newline()

                    ind += 1

                # self.builder.variable_update('libflags', ' '.join(linker_conditionals))

                if has_swift:
                    self.builder.build(f'$builddir/{a}/$name-Swift.h', 'swiftmoduleheader', swift_modules)

                self.builder.rule(f'link{a}', description=rules[f'link{a}']['desc'],
                                  command=rules[f'link{a}']['cmd'] + ' ' + ' '.join(linker_conditionals))
                self.builder.newline()
                self.builder.build(f'$builddir/$name.{a}', f'link{a}', arch_specific_object_files)
                outputs.append(f'$builddir/$name.{a}')

        self.builder.rule(f'lipo', description=rules[f'lipo']['desc'],
                          command=rules[f'lipo']['cmd'])
        self.builder.newline()

        self.builder.build('$symtarget', 'lipo', outputs)
        self.builder.newline()

        self.builder.rule(f'debug', description=rules[f'debug']['desc'],
                          command=rules[f'debug']['cmd'])
        self.builder.newline()

        self.builder.build('$signtarget', 'debug', '$symtarget')
        self.builder.newline()

        self.builder.rule(f'sign', description=rules[f'sign']['desc'],
                          command=rules[f'sign']['cmd'])
        self.builder.newline()

        self.builder.build('$build_target_file', 'sign', '$signtarget')
        self.builder.newline()

        self.builder.rule(f'stage', description=rules[f'stage']['desc'],
                          command=rules[f'stage']['cmd'])
        self.builder.newline()

        self.builder.build('stage', 'stage', 'build.ninja')

        return targets, [*used_rules]

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
        self.builder.variable('stagedir', get_var(self.variables, 'stagedir'))

        self.builder.variable('public_headers', get_var(self.variables, 'public_headers'))

        self.builder.variable('proj_build_dir', get_var(self.variables, 'proj_build_dir'))
        self.builder.newline()

        self.builder.variable('location', get_var(self.variables, 'install_location'))
        self.builder.variable('resource_dir', get_var(self.variables, 'resource_dir'))
        self.builder.variable('build_target_file', get_var(self.variables, 'build_target_file'))
        self.builder.newline()
        self.builder.variable('stage2',
                              extrapolate_stage(self.base_configurations['Types'][self.type]['variables']['stage2']))
        self.builder.newline()

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
                              get_var(self.variables, 'fw_dirs') + ' ' + get_var(self.variables,
                                                                                 'additional_fw_dirs'))
        self.builder.variable('libSearch',
                              get_var(self.variables, 'lib_dirs') + ' ' + get_var(self.variables,
                                                                                  'additional_lib_dirs'))
        self.builder.newline()

        self.builder.variable('cc', get_var(self.variables, 'cc'))
        self.builder.variable('cxx', get_var(self.variables, 'cxx'))
        self.builder.variable('ld', get_var(self.variables, 'ld'))
        self.builder.variable('codesign', get_var(self.variables, 'codesign'))
        self.builder.variable('dsym', get_var(self.variables, 'dsym'))
        self.builder.variable('lipo', get_var(self.variables, 'lipo'))
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
        self.builder.variable('entflag', get_var(self.variables, 'entflag'))
        self.builder.variable('entfile', get_var(self.variables, 'entfile'))
        self.builder.newline()

        self.builder.variable('header_includes', get_var(self.variables, 'include'))
        self.builder.variable('cinclude', get_var(self.variables, 'cinclude'))
        self.builder.newline()

        self.builder.variable('usrCflags', get_var(self.variables, 'cflags') + ' ' + get_var(self.variables, 'cflags2')
                              + ' ' + get_var(self.variables, 'moarcflags'))
        self.builder.variable('usrLDflags', get_var(self.variables, 'ldflags'))
        self.builder.newline()

        self.builder.variable('lopt', get_var(self.variables, 'lopts'))
        self.builder.variable('typeldflags', get_var(self.variables, 'ldflags'))

        self.builder.variable('libflags', '-lobjc -lc++')

        cflags = '$cinclude -fmodules -fcxx-modules -fmodule-name=$name -fbuild-session-file=$proj_build_dir/modules/ ' \
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

    def create_rules(self, used_rules):
        self.builder.pool('solo', '1')
        self.builder.newline()

        rules = yaml.safe_load(open(os.environ['DRAGONBUILD'] + "/DragonGen/rules.yml"))

        for rule in used_rules:
            self.builder.rule(rule, description=rules[rule]['desc'],
                              command=rules[rule]['cmd'])
            self.builder.newline()

    # noinspection PyTypeChecker
    def create_variable_dict(self):
        """

        """

        # variables = yaml.safe_load(open(os.environ['DRAGONBUILD'] + "/DragonGen/defaults.yml"))
        # variables = Project.default_variables.copy()

        variables = self.base_configurations['Defaults']

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


        variables.update(self.variables)

        if 'toolchain' in variables:
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


        if self.target in ['ios'] and not variables['nopack']:
            print("export DRAGON_DPKG=1")

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
    'prefix': ' -include',
    'fw_dirs': ' -F',
    'additional_fw_dirs': ' -F',
    'lib_dirs': ' -L',
    'additional_lib_dirs': ' -L',
    'libs': ' -l',
    'frameworks': ' -framework ',
    'stage': ' ; ',
    'lopts': ' ',
    'public_headers': '',
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
    # print("%s" % name, file=sys.stderr)
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


make_match = regex.compile('(.*)=(.*)#?')
make_type = regex.compile(r'include.*\/(.*)\.mk')
nepmatch = regex.compile(r'(.*)\+=(.*)#?')  # nep used subproj += instead of w/e and everyone copies her.


# this was supposed to be a really small function, i dont know what happened ;-;
def load_theos_makefile(file, root=True):
    project = {}
    variables = {}
    stage = []
    stageactive = False
    module_type = ''
    arc = False
    hassubproj = False
    noprefix = False
    try:
        while 1:
            line = file.readline()
            if not line:
                break
            if not arc and '-fobjc-arc' in line:
                arc = True
            if not noprefix and '-DTHEOS_LEAN_AND_MEAN' in line:
                noprefix = True
            if line == 'internal-stage::':
                stageactive = True
                continue
            if stageactive:
                if line.startswith((' ', '\t')):
                    x = line
                    x = x.replace('$(THEOS_STAGING_DIR)', '$proj_build_dir/_')
                    x = x.replace('$(ECHO_NOTHING)', '')
                    x = x.replace('$(ECHO_END)', '')
                    stage.append(x)
                else:
                    stageactive = False

            if not make_match.match(line):
                if not make_type.match(line):
                    continue
                if 'aggregate' in make_type.match(line).group(1):
                    hassubproj = True
                else:
                    module_type = make_type.match(line).group(1)
                continue

            if not nepmatch.match(line):
                name, value = make_match.match(line).group(1, 2)
            else:
                name, value = nepmatch.match(line).group(1, 2)
            if name.strip() in variables:
                variables[name.strip()] = variables[name.strip()] + ' ' + value.strip()
            variables[name.strip()] = value.strip()
    finally:
        file.close()

    if root:
        project['name'] = os.path.basename(os.getcwd())
        if 'INSTALL_TARGET_PROCESS' in variables:
            project['icmd'] = 'killall -9 ' + variables['INSTALL_TARGET_PROCESS']
        else:
            project['icmd'] = 'sbreload'

    modules = []
    mod_dicts = []
    # if module_type == 'aggregate':
    if module_type == 'application':
        module_name = variables.get('APPLICATION_NAME')
        module_archs = variables.get('ARCHS')
        module_files = variables.get(module_name + '_FILES') or variables.get('$(APPLICATION_NAME)_FILES') or ''
        module_cflags = variables.get(module_name + '_CFLAGS') or variables.get('$(APPLICATION_NAME)_CFLAGS') or ''
        module_cflags = variables.get('ADDITIONAL_CFLAGS') or ''
        module_ldflags = variables.get(module_name + '_LDFLAGS') or variables.get('$(APPLICATION_NAME)_LDFLAGS') or ''
        module_codesign_flags = variables.get(module_name + '_CODESIGN_FLAGS') or variables.get('$(APPLICATION_NAME)_CODESIGN_FLAGS') or ''
        module_ipath = variables.get(module_name + '_INSTALL_PATH') or variables.get(
            '$(APPLICATION_NAME)_INSTALL_PATH') or ''
        module_frameworks = variables.get(module_name + '_FRAMEWORKS') or variables.get(
            '$(APPLICATION_NAME)_FRAMEWORKS') or ''
        module_pframeworks = variables.get(module_name + '_PRIVATE_FRAMEWORKS') or variables.get(
            '$(APPLICATION_NAME)_PRIVATE_FRAMEWORKS') or ''
        module_eframeworks = variables.get(module_name + '_EXTRA_FRAMEWORKS') or variables.get(
            '$(APPLICATION_NAME)_EXTRA_FRAMEWORKS') or ''
        module_libraries = variables.get(module_name + '_LIBRARIES') or variables.get(
            '$(APPLICATION_NAME)_LIBRARIES') or ''

        files = []
        if module_files:
            tokens = module_files.split(' ')
            nextisawildcard = False
            for i in tokens:
                if '$(wildcard' in i:
                    nextisawildcard = 1
                    continue
                if nextisawildcard:
                    # We dont want to stop with these till we hit a ')'
                    # thanks cr4shed ._.
                    nextisawildcard = 0 if ')' in i else 1
                    grab = i.split(')')[0]
                    files.append(grab)
                    continue
                files.append(i)

        module = {
            'type': 'app',
            'files': files
        }
        if module_name != '':
            module['name'] = module_name
        if module_frameworks != '':
            module['frameworks'] = module_eframeworks.split(' ') + module_pframeworks.split(
                ' ') + module_frameworks.split(' ')
        if module_libraries != '':
            module['libs'] = module_libraries
        if module_archs != '':
            module['archs'] = module_archs
        if module_cflags != '':
            module['cflags'] = module_cflags
        if module_ldflags:
            module['ldflags'] = module_ldflags
        if stage != []:
            module['stage'] = stage
        module['arc'] = arc
        if not root:
            return module

    if module_type == 'bundle':
        module_name = variables.get('BUNDLE_NAME')
        module_archs = variables.get('ARCHS')
        module_files = variables.get(module_name + '_FILES') or variables.get('$(BUNDLE_NAME)_FILES') or ''
        module_cflags = variables.get(module_name + '_CFLAGS') or variables.get('$(BUNDLE_NAME)_CFLAGS') or ''
        module_ldflags = variables.get(module_name + '_LDFLAGS') or variables.get('$(BUNDLE_NAME)_LDFLAGS') or ''
        module_ipath = variables.get(module_name + '_INSTALL_PATH') or variables.get(
            '$(BUNDLE_NAME)_INSTALL_PATH') or ''
        module_frameworks = variables.get(module_name + '_FRAMEWORKS') or variables.get(
            '$(BUNDLE_NAME)_FRAMEWORKS') or ''
        module_pframeworks = variables.get(module_name + '_PRIVATE_FRAMEWORKS') or variables.get(
            '$(BUNDLE_NAME)_PRIVATE_FRAMEWORKS') or ''
        module_eframeworks = variables.get(module_name + '_EXTRA_FRAMEWORKS') or variables.get(
            '$(BUNDLE_NAME)_EXTRA_FRAMEWORKS') or ''

        files = []
        if module_files:
            tokens = module_files.split(' ')
            nextisawildcard = False
            for i in tokens:
                if '$(wildcard' in i:
                    nextisawildcard = 1
                    continue
                if nextisawildcard:
                    # We dont want to stop with these till we hit a ')'
                    # thanks cr4shed ._.
                    nextisawildcard = 0 if ')' in i else 1
                    grab = i.split(')')[0]
                    files.append(grab)
                    continue
                files.append(i)

        if module_ipath == '/Library/PreferenceBundles':
            module = {
                'type': 'prefs',
                'files': files
            }
            if module_name != '':
                module['name'] = module_name
            if module_frameworks != '':
                module['frameworks'] = module_eframeworks.split(' ') + module_pframeworks.split(
                    ' ') + module_frameworks.split(' ')

            if module_archs != '':
                module['archs'] = module_archs.split(' ')
            if module_cflags != '':
                module['cflags'] = module_cflags
            if module_ldflags:
                module['ldflags'] = module_ldflags
            module['arc'] = arc
            if not root:
                return module

        module = {
            'type': 'bundle',
            'files': files
        }
        if module_name != '':
            module['name'] = module_name
        if module_frameworks != '':
            module['frameworks'] = module_eframeworks.split(' ') + module_pframeworks.split(
                ' ') + module_frameworks.split(' ')

        if module_archs != '':
            module['archs'] = module_cflags
        if module_cflags != '':
            module['cflags'] = module_cflags
        if module_ldflags:
            module['ldflags'] = module_ldflags
        if stage != []:
            module['stage'] = stage
        module['arc'] = arc
        if not root:
            return module

    if module_type == 'tool':
        module_name = variables.get('TOOL_NAME')
        module_archs = variables.get('ARCHS')
        module_files = variables.get(module_name + '_FILES') or variables.get('$(TOOL_NAME)_FILES') or ''
        module_cflags = variables.get(module_name + '_CFLAGS') or variables.get('$(TOOL_NAME)_CFLAGS') or ''
        module_ldflags = variables.get(module_name + '_LDFLAGS') or variables.get('$(TOOL_NAME)_LDFLAGS') or ''
        module_codesign_flags = variables.get(module_name + '_CODESIGN_FLAGS') or variables.get('$(TOOL_NAME)_CODESIGN_FLAGS') or ''
        module_ipath = variables.get(module_name + '_INSTALL_PATH') or variables.get(
            '$(TOOL_NAME)_INSTALL_PATH') or ''
        module_frameworks = variables.get(module_name + '_FRAMEWORKS') or variables.get(
            '$(TOOL_NAME)_FRAMEWORKS') or ''
        module_pframeworks = variables.get(module_name + '_PRIVATE_FRAMEWORKS') or variables.get(
            '$(TOOL_NAME)_PRIVATE_FRAMEWORKS') or ''
        module_eframeworks = variables.get(module_name + '_EXTRA_FRAMEWORKS') or variables.get(
            '$(TOOL_NAME)_EXTRA_FRAMEWORKS') or ''
        module_libraries = variables.get(module_name + '_LIBRARIES') or variables.get(
            '$(TOOL_NAME)_LIBRARIES') or ''

        files = []
        if module_files:
            tokens = module_files.split(' ')
            nextisawildcard = False
            for i in tokens:
                if '$(wildcard' in i:
                    nextisawildcard = 1
                    continue
                if nextisawildcard:
                    # We dont want to stop with these till we hit a ')'
                    # thanks cr4shed ._.
                    nextisawildcard = 0 if ')' in i else 1
                    grab = i.split(')')[0]
                    files.append(grab)
                    continue
                files.append(i)
        module = {
            'type': 'cli',
            'files': files
        }
        if module_name != '':
            module['name'] = module_name
        if module_frameworks != '':
            module['frameworks'] = module_eframeworks.split(' ') + module_pframeworks.split(
                ' ') + module_frameworks.split(' ')
        if module_libraries != '':
            module['libs'] = module_libraries
        if module_archs != '':
            module['archs'] = module_archs
        if module_cflags != '':
            module['cflags'] = module_cflags
        if module_ldflags:
            module['ldflags'] = module_ldflags
        if stage != []:
            module['stage'] = stage
        module['arc'] = arc
        if not root:
            return module

    if module_type == 'tweak' and 'TWEAK_NAME' in variables:
        module_name = variables.get('TWEAK_NAME') or ''
        module_archs = variables.get('ARCHS') or ''
        module_files = variables.get(module_name + '_FILES') or variables.get('$(TWEAK_NAME)_FILES') or ''
        module_cflags = variables.get(module_name + '_CFLAGS') or variables.get('$(TWEAK_NAME)_CFLAGS') or ''
        module_ldflags = variables.get(module_name + '_LDFLAGS') or variables.get('$(TWEAK_NAME)_LDFLAGS') or ''
        module_frameworks = variables.get(module_name + '_FRAMEWORKS') or variables.get(
            '$(TWEAK_NAME)_FRAMEWORKS') or ''
        module_pframeworks = variables.get(module_name + '_PRIVATE_FRAMEWORKS') or variables.get(
            '$(TWEAK_NAME)_PRIVATE_FRAMEWORKS') or ''
        module_eframeworks = variables.get(module_name + '_EXTRA_FRAMEWORKS') or variables.get(
            '$(TWEAK_NAME)_EXTRA_FRAMEWORKS') or ''


        files = []
        if module_files:
            tokens = module_files.split(' ')
            nextisawildcard = False
            for i in tokens:
                if '$(wildcard' in i:
                    nextisawildcard = 1
                    continue
                if nextisawildcard:
                    nextisawildcard = 0
                    grab = i.split(')')[0]
                    files.append(grab)
                    continue
                files.append(i)

        module = {
            'type': 'tweak',
            'files': files
        }

        if module_name != '':
            module['name'] = module_name
        if module_frameworks != '':
            module['frameworks'] = module_eframeworks.split(' ') + module_pframeworks.split(
                ' ') + module_frameworks.split(' ')
        if module_archs != '':
            module['archs'] = module_archs.split(' ')
        if module_cflags:
            module['cflags'] = module_cflags
        if module_ldflags:
            module['ldflags'] = module_ldflags
        if stage != []:
            module['stage'] = stage
        module['arc'] = arc
        if not root:
            return module
        else:
            mod_dicts.append(module)
            project['name'] = module['name']
            modules.append('.')

    if hassubproj and 'SUBPROJECTS' in variables:
        modules = modules + variables['SUBPROJECTS'].split(' ')

    for module in modules:
        if os.environ['DGEN_DEBUG']:
            print("modules:" + str(modules), file=sys.stderr)
        if module != '.' and os.path.exists(module + '/Makefile'):
            mod_dicts.append(load_theos_makefile(open(module + '/Makefile'), root=False))

    i = 0
    for mod in mod_dicts:
        if mod:
            project[mod['name']] = mod
            project[mod['name']]['dir'] = modules[i]
            i += 1

    # the magic of theos
    project['all'] = {'cflags2': '-include$$DRAGONBUILD/include/PrefixShim.h -w'}

    if 'export ARCHS' in variables:
        project['all'] = {'archs': variables['export ARCHS'].split(' ')}

    return project


def main():
    config = {}
    if os.path.exists('DragonMake'):
        f = open("DragonMake")
        config = yaml.safe_load(f)
    elif os.path.exists('Makefile'):
        config = load_theos_makefile(open('Makefile'))
        exports['theos'] = 1

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
        if os.environ['DGEN_DEBUG']:
            print("Config:" + str(project_config), file=sys.stderr)
        if os.environ['DGEN_DEBUG']:
            print("Config:" + str(config), file=sys.stderr)

        project_config.update(config[i])

        if os.environ['DGEN_DEBUG']:
            print("Config:" + str(project_config), file=sys.stderr)
        project_variables = project_config.copy()
        f = open(f"{project_config['dir']}/build.ninja", 'w+')
        proj = Project(project_config['type'], project_variables, f, full_config=config)
        proj.generate()
        f.close()
        project_dirs = project_dirs + ' ' + project_config['dir']
        project_dirs = project_dirs.strip()
        if project_dirs.endswith('.'):
            project_dirs = '. ' + project_dirs[:-2]


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
        print("KeyError: Missing value in variables array. Likely internal issue.", file=sys.stderr)
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
        exit(2)
    except IndexError as ex:
        print("IndexError: List index out of range.", file=sys.stderr)
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
        exit(2)
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

        exit(-1)
