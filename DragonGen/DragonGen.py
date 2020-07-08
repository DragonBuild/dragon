#!/usr/bin/env python3

import glob
import os
import pprint
import sys
import termios
import traceback
import tty
import platform
from collections import namedtuple
from datetime import datetime
from typing import TextIO
import regex

import yaml

from buildgen.buildgen.generator import Generator

# Rules and defaults
_LAZY_RULES_DOT_YML: dict = None
_LAZY_DEFAULTS_DOT_YML: dict = None


def rules(*key_path: str) -> dict:
    '''
    Lazy load default rules and return vaule specified path.

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


def base_config(*key_path: str) -> dict:
    '''
    Lazy load default config and return value at specified path.

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


# Ninja Statements
Build = namedtuple('Build', ['outputs', 'rule', 'inputs'])
Comment = namedtuple('Comment', ['fstring'])
Rule = namedtuple('Rule', ['name', 'description', 'command'])
Var = namedtuple('Var', ['key'])
Default = namedtuple('Default', ['targets'])
___ = object()  # Newline


def QuickRule(name: str) -> Rule:
    '''
    Find rule for given name in rules.yml.

    Seealso: rules
    '''

    return Rule(name, rules(name, 'desc'), rules(name, 'cmd'))


def standardize_file_list(subdir: str, files: list) -> list:
    '''Strip list of empty strings and evaluate globbed paths.'''

    ret = []
    for filename in files:
        if not filename:
            continue

        if '*' in filename:
            ret.extend(f[len(subdir):] for f in glob.glob(subdir + filename,
                                                          recursive=True))
            continue

        ret.append(filename)
    return ret


class ArgList(list):
    '''
    Variables with values of type list: their corresponding delims and prefixes
    '''

    LIST_KEYS = {
        'files': ('', ' '),
        'logos_files': ('', ' '),
        'c_files': ('', ' '),
        'objc_files': ('', ' '),
        'objcxx_files': ('', ' '),
        'cxx_files': ('', ' '),
        'plists': ('', ' '),
        'swift_files': ('', ' '),
        'dlists': ('', ' '),
        'cflags': ('', ' '),
        'ldflags': ('', ' '),
        'codesignflags': ('', ' '),
        'include': ('-I', ' -I'),
        'prefix': ('-include', ' -include'),
        'fw_dirs': ('-F', ' -F'),
        'additional_fw_dirs': ('-F', ' -F'),
        'fwSearch': ('-F', ' -F'),
        'libSearch': ('-L', ' -L'),
        'lib_dirs': ('-L', ' -L'),
        'additional_lib_dirs': ('-L', ' -L'),
        'libs': ('-l', ' -l'),
        'frameworks': ('-framework ', ' -framework '),
        'stage': ('', '; '),
        'stage2': ('', '; '),
        'lopts': ('', ' '),
        'public_headers': ('', ''),
    }

    def __init__(self, values: list, prefix: str = '', delim: str = ' '):
        super().__init__(values)
        self.delim = delim
        self.prefix = prefix

    def __str__(self):
        return self.prefix + self.delim.join(str(s) for s in self)


class BoolFlag:
    '''
    Variables with values of type bool, and their corresponding flag pairs.
    '''

    BOOL_KEYS = {
        'arc': ('-fobjc-arc', ''),
    }

    def __init__(self, value: bool, flagpair: (str, str)):
        self.value = value
        self.true_flag, self.false_flag = flagpair

    def __bool__(self):
        return self.value

    def __str__(self):
        return self.true_flag if self.value else self.false_flag


class ProjectVars(dict):
    '''
    Safe dictionary with default values based on keys
    '''

    def __getitem__(self, key):
        try:
            ret = dict.__getitem__(self, key)
            if isinstance(ret, list) and key in ArgList.LIST_KEYS:
                return ArgList(ret, *(ArgList.LIST_KEYS[key]))
            if isinstance(ret, bool) and key in BoolFlag.BOOL_KEYS:
                return BoolFlag(ret, BoolFlag.BOOL_KEYS[key])

            return ret
        except KeyError as ex:
            if key in ['name', 'type', 'dir', 'cc', 'cxx', 'ld', 'codesign']:
                raise ex
            return ArgList([]) if key in ArgList.LIST_KEYS else ''


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


def generate_vars(var_d: dict, config: dict, target: str) -> ProjectVars:
    '''
    Generate ProjectVars object for a project

    Keyword arguments:
    var_d -- dict of explicitly set variables for this project
    config -- dict of /all/ explicitly set variables
    target -- target platform

    Raises: KeyError
    '''

    if 'for' in var_d:
        target = var_d['for']

    # Universal project vars
    ret = ProjectVars({
        'internalcflags': '$cinclude -fmodules -fcxx-modules -fmodule-name='
                          '$name $arc -fbuild-session-file=$proj_build_dir/'
                          'modules/ $debug -fmodules-prune-after=345600 '
                          '$cflags $btarg -O$optim -fmodules-validate-once-per'
                          '-build-session $fwSearch -miphoneos-version-min=$targetvers'
                          ' -isysroot $sysroot $header_includes '
                          ' $triple $theosshim '
                          '$warnings -fmodules-prune-interval=86400',
        'internalswiftflags': '-color-diagnostics -enable-objc-interop -sdk'
                              '/Applications/Xcode.app/Contents/Developer/'
                              'Platforms/iPhoneOS.platform/Developer/SDKs/'
                              'iPhoneOS.sdk -L/Applications/Xcode.app/Contents'
                              '/Developer/Toolchains/XcodeDefault.xctoolchain/'
                              'usr/lib/swift/iphoneos -g -L/usr/lib/swift '
                              '-swift-version 5 -module-name $name',
        'internallflags': '$internalcflags $typeldflags $frameworks $libs '
                          '$libflags $lopts $libSearch $ldflags $libs',
        'internalldflags': '',
        'internalsigntarget': '$signdir/$build_target_file.unsigned',
        'internalsymtarget': '$signdir/$build_target_file.unsym',
        'internallibflags': '-lobjc -lc++',
        'pwd': '.',
    })

    # Update with default vars
    ret.update(base_config('Defaults'))  # Universal
    ret.update(base_config('Types', var_d['type'], 'variables'))  # Type-based

    ret.update(var_d)

    # 'all` variables
    for source in base_config(), var_d, config:
        if 'all' in source:
            ret.update(source['all'])
        if 'Targets' in source and target in source['Targets']:
            ret.update(source['Targets'][target]['all'])

    # Specify toolchain paths
    if len(os.listdir(os.environ['DRAGONBUILD'] + '/toolchain')) > 1:
        ret['ld'] = 'ld64'
        toolchain_prefix = 'arm64-apple-darwin14-'
        ret.update({k: f'$dragondir/toolchain/linux/iphone/bin/{toolchain_prefix}' + var_d[k] for k in [
            'cc',
            'cxx',
            'lipo',
            'dsym',
            'plutil',
            'swift',
        ]})
        ret.update({k: '$dragondir/toolchain/linux/iphone/bin/' + var_d[k] for k in [
            'ld',
            'codesign',
        ]})

    # A few variables that need to be renamed
    NINJA_KEYS = {
        'location': 'install_location',
        'btarg': 'targ',
        'header_includes': 'include',
        'typeldflags': 'ldflags',
        'lopt': 'lopts'
    }

    d = 0
    for i in ret['archs']:
        if 'MACHINE' in i:
            ret['archs'][d] = platform.machine()
        d += 1

    if ret['triple'] != '':
        ret['triple'] = '-target ' + os.popen('clang -print-target-triple').read().strip() if 'MACHINE' in ret[
            'triple'] else ret['triple']

    ret.update({key: ret[NINJA_KEYS[key]] for key in NINJA_KEYS})

    # Computed variables
    ret['lowername'] = str(ret['name']).lower()
    ret['fwSearch'] = ret['fw_dirs'] + ret['additional_fw_dirs']
    ret['libSearch'] = ret['lib_dirs'] + ret['additional_lib_dirs']

    if os.environ['DGEN_DEBUG']:
        print("project dictionary:" + str(ret), file=sys.stderr)

    return ProjectVars(ret)


def rules_and_build_statements(variables: ProjectVars) -> (list, list):
    '''
    Generate build statements and rules for a given variable set.

    Returns rule_list, build_state as extensions for an outline
    '''

    # Trivial project types
    if variables['type'] == 'resource-bundle':
        return [
            QuickRule('bundle'),
            QuickRule('stage'),
        ], [
            Build('bundle', 'bundle', 'build.ninja'),
            Build('stage', 'stage', 'build.ninja'),
        ]
    if variables['type'] == 'stage':
        return [
            QuickRule('stage'),
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
    used_rules = set(['debug', 'sign', 'stage', 'lipo'])
    subdir: str = variables['dir'] + '/'
    filedict = classify({key: variables[key] for key in FILE_RULES})
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
    for a in variables['archs']:
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

        # Linker rules and build statements
        cmd = rules(f'link{a}', 'cmd') + ' ' + ' '.join(linker_conds)
        rule_list.append(Rule(f'link{a}', rules(f'link{a}', 'desc'), cmd))
        build_state.append(Build(f'$builddir/$name.{a}',
                                 f'link{a}',
                                 arch_specific_object_files))

    build_state.extend([
        Build('$internalsymtarget',
              'lipo' if len(variables['archs']) > 1 else 'dummy',
              [f'$builddir/$name.{a}' for a in variables['archs']]),
        Build('$internalsigntarget', 'debug', '$internalsymtarget'),
        Build('$build_target_file', 'sign', '$internalsigntarget'),
        Build('stage', 'stage', 'build.ninja'),
    ])
    if len(variables['archs']) <= 1:
        used_rules.remove("lipo")
        used_rules.add("dummy")

    rule_list.extend(QuickRule(r) for r in used_rules)

    return rule_list, build_state


def generate_ninja_outline(variables: ProjectVars) -> list:
    '''
    Generate list of unevaluated build.ninja statements
    Keyword arguments:
    variables -- ProjectVars object of all generated variables

    Seealso: rules_and_build_statements
    '''

    outline = [
        Var('name'),
        Var('lowername'),
        ___,
        Comment(f'Build file for {variables["name"]}'),
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

    rule_list, build_state = rules_and_build_statements(variables)

    outline.extend(rule_list)
    outline.append(___)
    outline.extend(build_state)
    outline.append(___)
    outline.append(Default(['$build_target_file']))

    return outline


def generate_ninja_file(outline: list, variables: ProjectVars, stream: TextIO):
    '''
    Evaluate outline with variables and write ninja file to given IO stream

    Keyword arguments:
    outline -- one-dimensional list of unevaluated ninja statements
    variables -- ProjectVars object of all generated variables
    stream -- IO stream to which the ninja data should be writen
    '''

    gen = Generator(stream)
    for item in outline:
        if item == ___:
            gen.newline()
            continue
        if isinstance(item, Comment):
            gen.comment(item.fstring)
            continue
        if isinstance(item, Var):
            gen.variable(item.key, str(variables[item.key]))
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


make_match = regex.compile('(.*)=(.*)#?')
make_type = regex.compile(r'include.*\/(.*)\.mk')
nepmatch = regex.compile(r'(.*)\+=(.*)#?')  # nep used subproj += instead of w/e and everyone copies her.


# this was supposed to be a really small function, i dont know what happened ;-;
def load_theos_makefile(file: object, root: object = True) -> dict:
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

    if os.environ['DGEN_DEBUG']:
        print("module type:" + str(module_type), file=sys.stderr)

    modules = []
    mod_dicts = []
    # if module_type == 'aggregate':

    module_type_naming = module_type.upper()

    module_name = variables.get(f'{module_type_naming}_NAME')
    module_archs = variables.get(f'ARCHS')
    module_files = variables.get(module_name + '_FILES') or variables.get(f'$({module_type_naming}_NAME)_FILES') or ''
    module_cflags = variables.get(module_name + '_CFLAGS') or variables.get('$({module_type_naming}_NAME)_CFLAGS') or ''
    module_cflags = variables.get(f'ADDITIONAL_CFLAGS') or ''
    module_ldflags = variables.get(module_name + '_LDFLAGS') or variables.get(f'$({module_type_naming}_NAME)_LDFLAGS') or ''
    module_codesign_flags = variables.get(module_name + '_CODESIGN_FLAGS') or variables.get(
        f'$({module_type_naming}_NAME)_CODESIGN_FLAGS') or ''
    module_ipath = variables.get(module_name + '_INSTALL_PATH') or variables.get(
        f'$({module_type_naming}_NAME)_INSTALL_PATH') or ''
    module_frameworks = variables.get(module_name + '_FRAMEWORKS') or variables.get(
        f'$({module_type_naming}_NAME)_FRAMEWORKS') or ''
    module_pframeworks = variables.get(module_name + '_PRIVATE_FRAMEWORKS') or variables.get(
        f'$({module_type_naming}_NAME)_PRIVATE_FRAMEWORKS') or ''
    module_eframeworks = variables.get(module_name + '_EXTRA_FRAMEWORKS') or variables.get(
        f'$({module_type_naming}_NAME)_EXTRA_FRAMEWORKS') or ''
    module_libraries = variables.get(module_name + '_LIBRARIES') or variables.get(
        f'$({module_type_naming}_NAME)_LIBRARIES') or ''

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
                files.append(grab.replace(')', ''))
                continue
            files.append(i)

    module = {
        'type': module_type,
        'files': files
    }
    if module_name != '':
        module['name'] = module_name
    module['frameworks'] = []
    if module_frameworks != '':
        module['frameworks'] += module_frameworks.split(' ')
    if module_pframeworks != '':
        module['frameworks'] += module_pframeworks.split(' ')
    if module_eframeworks != '':
        module['frameworks'] += module_eframeworks.split(' ')
    if module_libraries != '':
        module['libs'] = module_libraries
    if module_archs != '':
        module['archs'] = module_archs
    else:
        module['archs'] = ['arm64', 'arm64e']
    if module_cflags != '':
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
    project['all'] = {
        'theosshim': '-include$$DRAGONBUILD/include/PrefixShim.h -w' # TODO: remove -w
        }

    if 'export ARCHS' in variables:
        project['all'] = {
            'archs': variables['export ARCHS'].split(' ')
            }

    if os.environ['DGEN_DEBUG']:
        print("dict:" + str(project), file=sys.stderr)
    return project


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
        'port': 'DRBPORT',
        'id': None,
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

    if os.path.exists('DragonMake'):
        with open('DragonMake') as f:
            config = yaml.safe_load(f)

    elif os.path.exists('Makefile'):
        config = load_theos_makefile(open('Makefile'))
        exports['theos'] = 1
    else:
        raise FileNotFoundError

    for key in config:
        if key in META_KEYS:
            if META_KEYS[key] is not None:
                if key == 'pack' or key == 'package':
                    if not META_KEYS[key]:
                        exports["DRAGON_DPKG"] = "0"
                exports[META_KEYS[key]] = config[key]
            continue
        if key == 'exports':
            exports.update(config[key])
            continue

        proj_config = {
            'name': key,
            'dir': '.'
        }
        proj_config.update(config[key])

        default_target = 'ios'
        if os.environ['TARG_SIM'] == '1':
            default_target = 'sim'

        with open(f'{proj_config["dir"]}/build.ninja', 'w+') as out:
            variables = generate_vars(proj_config, config, default_target)
            outline = generate_ninja_outline(variables)

            generate_ninja_file(outline, variables, out)

        dirs = dirs + ' ' + proj_config['dir']
        dirs = dirs.strip()
        if dirs.endswith('.'):
            dirs = '. ' + dirs[:-2]

    exports['project_dirs'] = dirs

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
