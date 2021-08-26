import re as regex
import os, sys, glob
from pprint import pprint
import termios
import tty 
from .variable_types import ArgList

colors = [["\033[0;31m","\033[0;32m","\033[0;33m","\033[0;34m","\033[0;36m",
"\033[0;37m","\033[0m"],["\033[1;31m","\033[1;32m","\033[1;33m","\033[1;34m",
"\033[1;36m","\033[1;37m","\033[0m"]]

# Everything needs to go out of stderr *for now!*. the bash script executes anything 
#     sent via stdout
# worth also noting print() to stdout works like system() for us, except its in the 
#     context of a shell above us
def dprintline(col: int, tool: str, textcol: int, bold: int, pusher: int, msg: str):
    print("%s[%s]%s %s%s%s" % (
        colors[1][col], tool, colors[bold][textcol], ">>> " if pusher 
            else "", msg, colors[0][6]), file=sys.stderr)

dbstate = lambda msg: dprintline(1, "DragonGen", 5, 1, 0, msg)
dbwarn = lambda msg: dprintline(2, "DragonGen", 5, 0, 0, msg)
dberror = lambda msg: dprintline(0, "DragonGen", 5, 1, 0, msg)

make_match = regex.compile('(.*)=(.*)#?')
make_type = regex.compile(r'include.*\/(.*)\.mk')
nepmatch = regex.compile(r'(.*)\+=(.*)#?')  # nep used subproj += instead of w/e and everyone copies her.


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
    # Clear out empty keys
    return {key: value for (key, value) in filedict.items() if value != []}



# this was supposed to be a really small function, i dont know what happened ;-;
def interpret_theos_makefile(file: object, root: object = True) -> dict:
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
            line = file.readline().split('#')[0]
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
            else:
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
        print("\n\n", file=sys.stderr)
        print("module type:" + str(module_type), file=sys.stderr)
        print("\n\n", file=sys.stderr)

    modules = []
    mod_dicts = []
    # if module_type == 'aggregate':

    module_type_naming = module_type.upper()

    module_name = variables.get(f'{module_type_naming}_NAME')
    if module_name:
        module_archs = variables.get(f'ARCHS')
        module_files = variables.get(module_name + '_FILES') or variables.get(f'$({module_type_naming}_NAME)_FILES') or ''
        module_cflags = variables.get(module_name + '_CFLAGS') or variables.get('$({module_type_naming}_NAME)_CFLAGS') or ''
        module_cxxflags = variables.get(module_name + '_CXXFLAGS') or variables.get('$({module_type_naming}_NAME)_CXXFLAGS') or ''
        module_cflags = variables.get(f'ADDITIONAL_CFLAGS') or ''
        module_ldflags = variables.get(module_name + '_LDFLAGS') or variables.get(
            f'$({module_type_naming}_NAME)_LDFLAGS') or ''
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
            module['libs'] = module_libraries.split(' ')
        if module_archs != '':
            module['archs'] = module_archs
        else:
            module['archs'] = ['arm64', 'arm64e']
        if module_cflags != '':
            module['cflags'] = module_cflags
        if module_cxxflags:
            module['cxxflags'] = module_cxxflags
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

    rename_counter = 1
    for module in modules:
        if os.environ['DGEN_DEBUG']:
            print("\n\n", file=sys.stderr)
            pprint("modules:" + str(modules), stream=sys.stderr)
            print("\n\n", file=sys.stderr)
        if module != '.' and os.path.exists(module + '/Makefile'):
            new = interpret_theos_makefile(open(module + '/Makefile'), root=False)
            if new['name'].lower() == project['name'].lower():
                rename_counter += 1
                new['name_override'] = new['name']
                new['name'] = new['name'] + str(rename_counter)
            mod_dicts.append(new)

    i = 0
    for mod in mod_dicts:
        if mod:
            project[mod['name']] = mod
            project[mod['name']]['dir'] = modules[i]
            i += 1

    # the magic of theos

    if 'export ARCHS' in variables:
        project['all'] = {
            'archs': variables['export ARCHS'].split(' ')
        }

    if os.environ['DGEN_DEBUG']:
        print("\n\n", file=sys.stderr)
        print("dict:" + str(project), file=sys.stderr)
        print("\n\n", file=sys.stderr)
    return project


def load_old_format(file: object, root: object = True) -> dict:
    variables = {i.split('=')[0].strip('"').strip("'"): i.split('=')[1].strip('"').strip("'") for i in
                 file.read().split('\n') if (not i.startswith('#') and len(i) > 0)}
    # print(variables, file=sys.stderr)

    moddict = {}

    for i in [x for x in variables if len(x) > 0 and x!='SUBPROJECTS' ]:
        translation = i.lower().replace('tweak_', '').replace('logos_file', 'logos_files').replace('install_cmd','icmd')
        variables[i] = os.popen(f'echo {variables[i]}').read().strip()
        if i in ['ARCHS', 'LIBS', 'FRAMEWORKS', 'LOGOS_FILES', 'TWEAK_FILES']:

            start, delim = ArgList.LIST_KEYS[i.lower()]
            if delim in variables[i]:
                moddict[translation] = variables[i][len(start):].split(delim)
            else:
                moddict[translation] = variables[i].strip().split()
        else:
            moddict[translation] = variables[i]

    if not root:
        return moddict
    else:
        mainproj = {k: v for (k, v) in moddict.items() if k not in ['name', 'icmd']}
        moddict = {k: v for (k, v) in moddict.items() if k in ['name', 'icmd']}
        moddict[moddict['name']] = mainproj
        for i in variables['SUBPROJECTS'].split():
            os.chdir(i)
            subproject = load_old_format(open('DragonMake'), False)
            subproject['dir'] = subproject['name']
            os.chdir('..')
            moddict[subproject['name']] = {i: v for (i, v) in subproject.items() if i not in ['name', 'icmd']}
        return moddict

def standardize_file_list(subdir: str, files: list) -> list:
    '''Strip list of empty strings and evaluate globbed paths.'''
    
    # hotfix for #67, standardize the subdirectory string we get, we want /subdir/
    subdir = subdir.strip('/')
    subdir = f'/{subdir}/'
    
    ret = []
    for filename in files:
        if not filename:
            continue

        if '*' in filename:
            ret.extend('.' + f[len(subdir):] for f in glob.glob('.' + subdir + filename,
                                                          recursive=True))
            continue

        ret.append(filename)
    return ret
