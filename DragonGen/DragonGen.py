#!/usr/bin/env python3

'''

DragonGen.py

(c) 2020 kritanta
Please refer to the LICENSE file included with this project regarding the usage of code herein.

Authors:
  - @kritanta
  - @lorenz0

Some guidelines for work on this file moving forward:
  - Avoid re-typing variables and use type hints where possible
  - No lines longer than 80-90 chars
  - Code should make a 'good attempt' to stick to PEP-8 guidelines
  - Avoid anything in the global namespace
  - Use descriptive variable names. Code should be extremely self-documenting
  - Comment any lines of code that are confusing
  - Don't code-golf


'''

import glob
import os
from pprint import pprint
import sys
import termios
import traceback
import tty
import platform
from collections import namedtuple
from datetime import datetime
from typing import TextIO
import re as regex
import subprocess
import yaml

from DragonGen.DragonGenTypes import *
from DragonGen.util import *
from DragonGen.buildgen.buildgen.generator import BuildFileGenerator



# Rules and defaults
_LAZY_RULES_DOT_YML: dict = None
_LAZY_DEFAULTS_DOT_YML: dict = None

_IS_THEOS_MAKEFILE_ = False


# Ninja Statements

# These are used like so:
# a_build_object = Build("output files here", "rule name here", "input files here")
# outputs = a_build_object.outputs

Build = namedtuple('Build', ['outputs', 'rule', 'inputs'])
Comment = namedtuple('Comment', ['fstring'])
Rule = namedtuple('Rule', ['name', 'description', 'command'])
Var = namedtuple('Var', ['key'])
Default = namedtuple('Default', ['targets'])
___ = object()  # Newline


# Get rule by name from rules.yml
def get_rule(name: str) -> Rule:
    return Rule(name, rules(name, 'desc'), rules(name, 'cmd'))


class Generator(object):

    def __init__(self, config: dict, module_name: str, target_platform: str):
        self.config: dict = config
        self.module_name: str = module_name
        self.project_variables: ProjectVars = ProjectVars(self.generate_vars(config[module_name], target_platform))
        

    def write_output_file(self, out: TextIO):
        self.generate_build_file(out)


    @staticmethod
    def classify(filedict: dict) -> dict:
        '''
        Find loving homes for unclassified files
        '''

        for f in filedict['files']:
            _, ext = os.path.splitext(f)
            filedict[{
                '.c': 'c_files',
                '.cpp': 'cxx_files',
                '.cxx': 'cxx_files',
                '.dlist': 'dlists',
                '.m': 'objc_files',
                '.mm': 'objcxx_files',
                '.plist': 'plists',
                '.swift': 'swift_files',
                '.x': 'logos_files',
                '.xm': 'logos_files',
            }[ext]].append(f)
        return filedict


    def generate_vars(self, module_variables: dict, target: str) -> dict:
        '''
        Generate ProjectVars object for a project

        Keyword arguments:
        module_variables -- dict of explicitly set variables for this project
        target -- target platform

        Raises: KeyError
        '''

        if 'for' in module_variables:
            target = module_variables['for']

        # Load in internal defaults
        # These are ones that really probably shouldn't be touched often as they
        #       serve to slap together all the variables we *do* touch
        project_dict: dict = get_default_section_dict('InternalDefaults')

        if _IS_THEOS_MAKEFILE_:
            project_dict.update({
                        'theosshim': '-include$$DRAGONBUILD/include/PrefixShim.h -w'
                        })

        # Update with default vars
        project_dict.update(get_default_section_dict('Defaults'))  # Universal
        try:
            project_dict.update(get_default_section_dict('Types', module_variables['type'], 'variables'))  # Type-based
        except KeyError as ex:
            try:
                project_dict.update(get_default_section_dict('Types', module_variables['type'].lower(), 'variables'))
            except KeyError:
                raise ex


        project_dict.update(module_variables)
        project_dict['name'] = self.module_name

        # 'all` variables
        for source in get_default_section_dict(), module_variables, self.config:
            if 'all' in source:
                project_dict.update(source['all'])
            if 'Targets' in source and target in source['Targets']:
                project_dict.update(source['Targets'][target]['all'])

        # A few variables that need to be renamed
        NINJA_KEYS = {
            'location': 'install_location',
            'btarg': 'targ',
            'header_includes': 'include',
            'typeldflags': 'ldflags',
            'lopt': 'lopts'
        }

        # TODO: BAD HOTFIX
        if 'include' in project_dict:
            project_dict['header_includes'] = project_dict['include']

        for d,i in enumerate(project_dict['archs']):
            if 'MACHINE' in i:
                project_dict['archs'][d] = platform.machine()
            if 'arm64e' in i:
                if 'invalid arch name' in os.popen('clang -arch arm64e 2>&1').read():
                    project_dict['archs'].remove('arm64e')

        if 'triple' in project_dict and project_dict['triple'] != '':
            project_dict['triple'] = '-target ' + os.popen('clang -print-target-triple').read().strip() if 'MACHINE' in project_dict[
                'triple'] else project_dict['triple']

        project_dict.update({key: project_dict[NINJA_KEYS[key]] for key in NINJA_KEYS if NINJA_KEYS[key] in project_dict})

        # Computed variables
        project_dict['lowername'] = str(project_dict['name']).lower()
        project_dict['fwSearch'] = project_dict['fw_dirs'] + (project_dict['additional_fw_dirs'] if project_dict['additional_fw_dirs'] else [])
        project_dict['libSearch'] = project_dict['lib_dirs'] + (project_dict['additional_lib_dirs'] if project_dict['additional_lib_dirs'] else [] )

        if os.environ['DGEN_DEBUG']:
            pprint("project dictionary:" + str(project_dict), stream=sys.stderr)
            print("\n\n", file=sys.stderr)

        # Specify toolchain paths
        if len(os.listdir(os.environ['DRAGONBUILD'] + '/toolchain')) > 1:
            project_dict['ld'] = 'ld64'
            project_dict.update({k: f'$dragondir/toolchain/linux/iphone/bin/$toolchain-prefix' + module_variables[k] for k in [
                'cc',
                'cxx',
                'lipo',
                'dsym',
                'plutil',
                'swift',
            ]})
            project_dict.update({k: '$dragondir/toolchain/linux/iphone/bin/' + module_variables[k] for k in [
                'ld',
                'codesign',
            ]})

        if 'cxxflags' in project_dict:
            project_dict['cxx'] = project_dict['cxx'] + ' ' + project_dict['cxxflags']

        if project_dict['sysroot']:
            project_dict['sysroot'] = '-isysroot ' + project_dict['sysroot']

        return project_dict


    def rules_and_build_statements(self) -> (list, list):
        '''
        Generate build statements and rules for a given variable set.

        Returns rule_list, build_state as extensions for an outline
        '''

        # Trivial project types
        if self.project_variables['type'] == 'resource-bundle':
            return [
                    get_rule('bundle'),
                    get_rule('stage'),
                ], [
                    Build('bundle', 'bundle', 'build.ninja'),
                    Build('stage', 'stage', 'build.ninja'),
                ]
        if self.project_variables['type'] == 'stage':
            return [
                    get_rule('stage'),
                ], [
                    Build('stage', 'stage', 'build.ninja'),
                ]

        FILE_RULES = {  # Required rules based on filetype
            'c_files': 'c',
            'cxx_files': 'cxx',
            'dlists': None,
            'files': None,
            'logos_files': None,
            'objc_files': 'objc',
            'objcxx_files': 'objcxx',
            'plists': None,
            'swift_files': 'swift',
        }

        build_state = []
        rule_list = []
        used_rules = {'debug', 'sign', 'stage', 'lipo'}
        subdir: str = self.project_variables['dir'] + '/'
        filedict = self.classify({key: self.project_variables[key] for key in FILE_RULES})
        linker_conds = set()

        # Deal with logos preprocessing
        for f in standardize_file_list(subdir, filedict['logos_files']):
            used_rules.add('logos')
            linker_conds.add('-lobjc')

            name, ext = os.path.split(f)[1], os.path.splitext(f)[1]
            if ext == '.x':
                build_state.append(Build(f'$builddir/logos/{name}.m', 'logos', f))
                filedict['objc_files'].append(f'$builddir/logos/{name}.m')
            elif ext == '.xm':
                build_state.append(Build(f'$builddir/logos/{name}.mm', 'logos', f))
                filedict['objcxx_files'].append(f'$builddir/logos/{name}.mm')
                linker_conds.add('-lc++')

        # Deal with compilation
        for a in self.project_variables['archs']:
            arch_specific_object_files = []

            for ftype in (f for f in FILE_RULES if FILE_RULES[f] is not None):
                ruleid = f'{FILE_RULES[ftype]}{a}'
                for f in standardize_file_list(subdir, filedict[ftype]):
                    name = os.path.split(f)[1]
                    used_rules.add(ruleid)
                    arch_specific_object_files.append(f'$builddir/{a}/{name}.o')
                    build_state.append(Build(f'$builddir/{a}/{name}.o', ruleid, f))

                    LINKER_FLAGS = {  # Don't link objc/cpp if not needed
                        'cxx': ['-lc++'],
                        'objc': ['-lobjc'],
                        'objcxx': ['-lobjc', '-lc++'],
                    }
                    if ftype in LINKER_FLAGS:
                        for flag in LINKER_FLAGS[ftype]:
                            linker_conds.add(flag)
            if self.project_variables['type'] == 'static':
                # Linker rules and build statements
                cmd = rules(f'archive{a}', 'cmd') + ' ' + ' '.join(linker_conds)
                rule_list.append(Rule(f'link{a}', rules(f'link{a}', 'desc'), cmd))
                build_state.append(Build(f'$builddir/$name.{a}',
                                        f'link{a}',
                                        arch_specific_object_files))
            else:
                # Linker rules and build statements
                cmd = rules(f'link{a}', 'cmd') + ' ' + ' '.join(linker_conds)
                rule_list.append(Rule(f'link{a}', rules(f'link{a}', 'desc'), cmd))
                build_state.append(Build(f'$builddir/$name.{a}',
                                        f'link{a}',
                                        arch_specific_object_files))

        build_state.extend([
            Build('$internalsymtarget',
                'lipo' if len(self.project_variables['archs']) > 1 else 'dummy',
                [f'$builddir/$name.{a}' for a in self.project_variables['archs']]),
            Build('$internalsigntarget', 'debug', '$internalsymtarget'),
            Build('$build_target_file', 'sign', '$internalsigntarget'),
            Build('stage', 'stage', 'build.ninja'),
        ])
        if len(self.project_variables['archs']) <= 1:
            used_rules.remove("lipo")
            used_rules.add("dummy")

        rule_list.extend(get_rule(r) for r in used_rules)

        return rule_list, build_state


    def generate_ninja_outline(self) -> list:
        '''
        Generate list of unevaluated build.ninja statements

        Seealso: rules_and_build_statements
        '''

        outline = [
            Var('name'),
            Var('lowername'),
            ___,
            Comment(f'Build file for {self.project_variables["name"]}'),
            Comment(f'Generated at {datetime.now().strftime("%D %H:%M:%S")}'),
            ___,
            Var('stagedir'),
            Var('location'),
            Var('dragondir'),
            Var('sysroot'),
            Var('proj_build_dir'),
            Var('objdir'),
            Var('signdir'),
            Var('builddir'),
            Var('build_target_file'),
            Var('pwd'),
            Var('resource_dir'),
            Var('toolchain-prefix'),
            ___,
            Var('stage'),
            Var('stage2'),
            ___,
            ___,
            Var('internalsigntarget'),
            Var('internalsymtarget'),
            ___,
            Var('fwSearch'),
            Var('libSearch'),
            Var('modulesinternal'),
            ___,
            Var('cc'),
            Var('codesign'),
            Var('cxx'),
            Var('dsym'),
            Var('ld'),
            Var('lipo'),
            Var('logos'),
            Var('optool'),
            Var('plutil'),
            Var('swift'),
            ___,
            Var('targetvers'),
            Var('targetprefix'),
            Var('targetos'),
            Var('triple'),
            ___,
            Var('frameworks'),
            Var('libs'),
            ___,
            Var('macros'),
            Var('arc'),
            Var('btarg'),
            Var('debug'),
            Var('entfile'),
            Var('entflag'),
            Var('optim'),
            Var('warnings'),
            ___,
            Var('cinclude'),
            Var('header_includes'), 
            Var('public_headers'),
            ___,
            Var('usrCflags'),
            Var('usrLDflags'),
            ___,
            Var('libflags'),
            Var('lopts'),
            Var('typeldflags'),
            ___,
            Var('cflags'),
            Var('ldflags'),
            Var('lflags'),
            Var('lfflags'),
            Var('swiftflags'),
            ___,
            Var('theosshim'),
            Var('internalcflags'),
            Var('internalldflags'),
            Var('internallflags'),
            Var('internallfflags'),
            Var('internalswiftflags'),
            ___,
        ]

        rule_list, build_state = self.rules_and_build_statements()

        outline.extend(rule_list)
        outline.append(___)
        outline.extend(build_state)
        outline.append(___)
        outline.append(Default(['$build_target_file']))

        return outline


    def generate_build_file(self, stream: TextIO):
        '''
        Evaluate outline with variables and write ninja file to given IO stream

        Keyword arguments:
        stream -- IO stream to which the ninja data should be writen
        '''
        outline = self.generate_ninja_outline()
        gen = BuildFileGenerator(stream)
        for item in outline:
            if item == ___:
                gen.newline()
                continue
            if isinstance(item, Comment):
                gen.comment(item.fstring)
                continue
            if isinstance(item, Var):
                gen.variable(item.key, str(self.project_variables[item.key]))
                continue
            if isinstance(item, Rule):
                gen.rule(item.name,
                        description=item.description,
                        command=item.command)
                continue
            if isinstance(item, Build):
                gen.build(item.outputs, item.rule, item.inputs)
                continue
            if isinstance(item, Default):
                gen.default(['$build_target_file'])



def rules(*key_path: str) -> dict:
    '''
    Lazy load default rules and return value specified path.

    Raises: FileNotFoundError, KeyError
    '''

    global _LAZY_RULES_DOT_YML
    if _LAZY_RULES_DOT_YML is None:
        with open(f'{os.environ["DRAGONBUILD"]}/DragonGen/rules.yml') as f:
            _LAZY_RULES_DOT_YML = yaml.safe_load(f)

    key_path = list(key_path)
    ret = _LAZY_RULES_DOT_YML.copy()
    while key_path:
        ret = ret[key_path.pop(0)]

    return ret


def get_default_section_dict(*key_path: str) -> dict:
    '''
    Lazy load defaults.yml and return the requested dictionary from it

    Raises: FileNotFoundError, KeyError
    '''

    global _LAZY_DEFAULTS_DOT_YML
    if _LAZY_DEFAULTS_DOT_YML is None:
        with open(f'{os.environ["DRAGONBUILD"]}/DragonGen/defaults.yml') as f:
            _LAZY_DEFAULTS_DOT_YML = yaml.safe_load(f)

    key_path = list(key_path)
    ret = _LAZY_DEFAULTS_DOT_YML.copy()
    while key_path:
        ret = ret[key_path.pop(0)]
    return ret


def handle(ex: Exception):
    ''' Optionally print debug information '''

    print("Press v for detailed debugging output, any other key to exit.",
          file=sys.stderr)

    old_setting = termios.tcgetattr(sys.stdin.fileno())
    tty.setraw(sys.stdin)
    x = sys.stdin.read(1)
    termios.tcsetattr(0, termios.TCSADRAIN, old_setting)
    if str(x).lower() == 'v':
        print(str(ex), file=sys.stderr)
        print(''.join(traceback.format_tb(ex.__traceback__)), file=sys.stderr)
    else:
        print("Exiting...", file=sys.stderr)

    print(f'export DRAGONGEN_FAILURE=1')


def main():
    '''
    Generate and write build.ninja file from DragonMake or Makefile

    - Load DragonMake or Makefile to `config` dict
    - Generate `variables` from `config` and global default with `generate_vars`
    - Create an `outline` for the build.ninja file in `generate_ninja_outline`
    - Evaluate outline with `variables` and write to build.ninja in `generate_ninja_file`
    '''
    META_KEYS = {  # Keys that may be at the root of the DragonMake dict
        'name': 'package_name',
        'icmd': 'install_command',
        'ip': 'DRBIP',
        'postinst': None,
        'port': 'DRBPORT',
        'id': None,
        'mtn': None,
        'author': None,
        'version': None,
        'depends': None,
        'architecture': None,
        'description': None,
        'section': None,
        'pack': None,
        'package': None,
        'desc': None,
        'all': None,
    }

    exports = {}
    dirs = ''
    projs = ''


    if os.path.exists('DragonMake'):
        with open('DragonMake') as f:
            try:
                config = yaml.safe_load(f)
            except Exception as ex:
                if os.system("sh DragonMake 2>/dev/null") == 0:
                    config = load_old_format(open('DragonMake'))

                else:
                    # bad format
                    raise ex


    elif os.path.exists('Makefile'):
        config = interpret_theos_makefile(open('Makefile'))
        exports['theos'] = 1
        global _IS_THEOS_MAKEFILE_
        _IS_THEOS_MAKEFILE_ = True

    else:
        raise FileNotFoundError

    for key in config:
        if key in META_KEYS:
            continue
        
        # Hack to run a bash command in the context of DragonGen
        # TODO: remove this when the main dragon script is pythonized
        if key == 'exports':
            exports.update(config[key])
            continue

        submodule_config = {
            'name': key,
            'dir': '.'
        }
        try:
            submodule_config.update(config[key])
        except ValueError:
            # if i add a key to control.py and don't add it to meta tags here, this happens
            # so maybe find a better way to do that, dpkg is complex and has many fields
            dbwarn("! Warning: Key %s is not a valid module (a dictionary), nor is it a known configuration key" % key)
            dbwarn("! This (probably) isn't a problem.")
            dbwarn("! This value will be ignored.")
            continue

        default_target = 'ios'
        if os.environ['TARG_SIM'] == '1':
            default_target = 'sim'

        with open(f'{submodule_config["dir"]}/{submodule_config["name"]}.ninja', 'w+') as out:
            generator = Generator(config, key, default_target)
            generator.write_output_file(out)

        dirs = dirs + ' ' + submodule_config['dir']
        dirs = dirs.strip()
        if dirs.endswith('.'):
            dirs = '. ' + dirs[:-2]

        projs = projs + ' ' + submodule_config['name']
        projs = projs.strip()

    exports['project_dirs'] = dirs
    exports['project_names'] = projs

    for x in exports:
        print(f'export {x}="{exports[x]}"')


if __name__ == '__main__':
    try:
        main()
    except FileNotFoundError as exception:
        print('Error: No project files found', file=sys.stderr)

        handle(exception)
        sys.exit(2)
    except KeyError as exception:
        print('KeyError: Missing value in variables array.', file=sys.stderr)
        print(str(exception), file=sys.stderr)

        handle(exception)
        sys.exit(2)
    except IndexError as exception:
        print("IndexError: List index out of range.", file=sys.stderr)
        print(str(exception), file=sys.stderr)

        handle(exception)
        sys.exit(2)
    except Exception as exception:
        print('Error: An undocumented error has been hit', file=sys.stderr)
        print('Please contact a maintainer', file=sys.stderr)

        handle(exception)
        sys.exit(-1)
