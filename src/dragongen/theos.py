#!/usr/bin/env python3

import os
from enum import Enum
from ruyaml import YAML


def strip_comments(text):
    if not text:
        return ''
    out = text.split('#')[0]
    if not out:
        return ''
    return out


def join_escaped_newlines(lines):
    out_statements = []
    joining = False
    current_statement = ""
    for index, line in enumerate(lines):
        escaped = False
        if line.strip().endswith('\\'):
            escaped = True
        if joining:
            current_statement += ' ' + line
            if not escaped:
                out_statements.append(current_statement)
                current_statement = ""
        else:
            out_statements.append(line)
        if not escaped:
            joining = False
    return out_statements


def join_indented_blocks(lines):
    out_statements = []
    joining = False
    current_statement = ""
    for line in lines:
        if line.strip().endswith('::'):
            joining = True
            current_statement += line + "\n"
            continue

        if joining:
            if line.startswith('\t') or line.startswith('    '):
                current_statement += line + '\n'
            else:
                joining = False
                out_statements.append(current_statement)
                current_statement = ""
        else:
            out_statements.append(line)
    if current_statement != "":
        out_statements.append(current_statement)
    return out_statements


class MakefileVariableStatementType(Enum):
    DECLARATION = 0
    APPEND = 1


class MakefileVariableStatement:
    def __init__(self, declaration):

        equal_split = declaration.split('=')

        variable_sect = equal_split[0]
        value_sect = equal_split[1]

        mod = variable_sect[-1]
        if mod in [':', '?', '+']:
            if mod == '+':
                self.type = MakefileVariableStatementType.APPEND
            else:
                self.type = MakefileVariableStatementType.DECLARATION
            variable_sect = variable_sect[:-1]
        else:
            self.type = MakefileVariableStatementType.DECLARATION

        self.exported = False
        if variable_sect.startswith('export '):
            self.exported = True
            self.name = variable_sect.split('export ', 1)[1]
        else:
            self.name = variable_sect

        self.value = value_sect
        self.name = self.name.strip()
        self.value = self.value.strip()


class Makefile:
    def __init__(self, file_contents: str):
        self.includes = []
        self.variables = {}
        lines = [strip_comments(line) for line in file_contents.split('\n')]
        self.statements = [line for line in join_indented_blocks(join_escaped_newlines(lines)) if line != '']
        self.variable_statements = []
        self.rules = {}

        for statement in self.statements:

            if statement.startswith('include '):
                self.includes.append(statement.split('include ')[1])

            elif '=' in statement:
                self.variable_statements.append(MakefileVariableStatement(statement))

            elif '::\n' in statement:
                self.rules[statement.split("::\n")[0]] = [i.strip() for i in statement.split('\n')[1:] if
                                                          i.strip() != ""]

        self.variables = self._process_variable_statements()

    def _process_variable_statements(self):
        variables = {}
        for statement in self.variable_statements:
            if statement.type == MakefileVariableStatementType.DECLARATION:
                variables[statement.name] = " ".join(statement.value.split())
            elif statement.type == MakefileVariableStatementType.APPEND:
                if statement.name in variables:
                    variables[statement.name] = variables[statement.name] + ' ' + " ".join(statement.value.split())
                else:
                    variables[statement.name] = " ".join(statement.value.split())
        return variables


class TheosMakefileType(Enum):
    TWEAK = 0
    BUNDLE = 1
    LIBRARY = 2
    APPLICATION = 3
    FRAMEWORK = 4
    TOOL = 5
    PREFS = 6


class TheosMakefile(Makefile):
    def __init__(self, file_contents: str):
        super().__init__(file_contents)

        self.type = None
        self.has_subprojects = False
        self.module_name = ""
        self.module = {}
        self.subprojects = []

        self.module['arc'] = False
        self.module['for'] = 'ios'

        for included in self.includes:
            if 'tweak.mk' in included:
                self.type = TheosMakefileType.TWEAK
                self.module['frameworks'] = ['UIKit']  # :/
                self.module['type'] = 'tweak'
            if 'aggregate.mk' in included:
                self.has_subprojects = True
            if 'bundle.mk' in included:
                self.module['type'] = 'bundle'
                self.type = TheosMakefileType.BUNDLE
            if 'library.mk' in included:
                self.module['type'] = 'library'
                self.type = TheosMakefileType.LIBRARY
            if 'application.mk' in included:
                self.module['type'] = 'app'
                self.type = TheosMakefileType.APPLICATION
            if 'framework.mk' in included:
                self.module['type'] = 'framework'
                self.type = TheosMakefileType.FRAMEWORK
            if 'tool.mk' in included:
                self.module['type'] = 'tool'
                self.type = TheosMakefileType.TOOL

        for variable in self.variables:
            self.variables[variable] = self.variables[variable].replace('$(THEOS_STAGING_DIR)', '$dragon_data_dir/_')
            self.variables[variable] = self.variables[variable].replace('$(THEOS)', '$dragon_root_dir')
            self.variables[variable] = self.variables[variable].replace('$(ECHO_NOTHING)', '')
            self.variables[variable] = self.variables[variable].replace('$(ECHO_END)', '')
            self.variables[variable] = self.variables[variable].replace('$(', '$$(')

            # TODO: '_SWIFTFLAGS'
            suffix_to_key = {
                '_ARCHS': 'archs',
                '_FILES': 'files',
                '_FRAMEWORKS': 'frameworks',
                '_LIBRARIES': 'libs',
                '_CFLAGS': 'cflags',
                '_CXXFLAGS': 'cxxflags',
                '_CCFLAGS': 'cxxflags',
                '_LDFLAGS': 'ldflags',
                '_CODESIGN_FLAGS': 'entflag',
                '_INSTALL_PATH': 'install_location',
                '_LINKAGE_TYPE': 'type',
                '_RESOURCE_DIRS': 'resource_dir',
                '_PUBLIC_HEADERS': 'public_headers'
            }

            for suffix, key in suffix_to_key.items():
                if variable.endswith(suffix):
                    if key in self.module and isinstance(self.module[key], list):
                        self.module[key] += self.variables[variable].split(' ')
                    else:
                        lists = ['_ARCHS', '_FILES', '_FRAMEWORKS', '_LIBRARIES']
                        self.module[key] = self.variables[variable].split(' ') if suffix in lists else self.variables[variable]

            # Handle special cases
            if variable.endswith('_NAME'):
                self.module_name = self.variables[variable]

            if variable.endswith('_CFLAGS') and '-fobjc-arc' in self.variables[variable]:
                self.module['arc'] = True

            if variable.endswith('_INSTALL_PATH') and 'PreferenceBundles' in self.variables[variable]:
                self.module['type'] = 'prefs'
                self.type = TheosMakefileType.PREFS

            if variable.endswith('_LINKAGE_TYPE') and self.variables[variable] == 'static':
                self.module['type'] = 'static'

            if variable == 'TARGET' or variable == 'TARGET_OS_DEPLOYMENT_VERSION':
                ver = self.variables[variable].split(':')[-1] if variable == 'TARGET' else self.variables[variable]
                if float(ver) >= 9.0:
                    self.module['targetvers'] = ver

            if variable == 'SYSROOT':
                sysroot = self.variables[variable]
                if os.path.exists(sysroot):
                    self.module['sysroot'] = sysroot

        files = []
        if 'files' in self.module:
            tokens = self.module['files']
            nextisawildcard = False
            for i in tokens:
                if '$(wildcard' in i:
                    nextisawildcard = 1
                    continue
                if nextisawildcard:
                    # We dont want to stop with these til we hit a ')'
                    # thanks cr4shed ._.
                    nextisawildcard = 0 if ')' in i else 1
                    grab = i.split(')')[0]
                    files.append(grab.replace(')', ''))
                    continue
                files.append(i)

            self.module['files'] = files

        if 'stage' in self.rules:
            stage = self.rules['stage']
            stage_processed = []
            for command in stage:
                command = command.replace('$(THEOS_STAGING_DIR)', '$dragon_data_dir/_')
                command = command.replace('$(THEOS)', '$dragon_root_dir')
                command = command.replace('$(ECHO_NOTHING)', '')
                command = command.replace('$(ECHO_END)', '')
                command = command.replace('$(', '$$(')
                stage_processed.append(command)
            self.module['stage'] = stage_processed

        if 'files' not in self.module:
            if self.type == TheosMakefileType.BUNDLE:
                self.module['type'] = 'resource-bundle'

        if self.has_subprojects:
            self.subprojects = self.variables['SUBPROJECTS'].split(' ')


class TheosMakefileProcessor:
    def __init__(self):
        self.root_directory = os.getcwd()
        self.project = {}

        with open('Makefile', 'r') as makefile:
            self.root_makefile = TheosMakefile(makefile.read())

        if os.path.exists('control'):
            with open('control', 'r') as control:
                yaml = YAML(typ='safe')  # default, if not specfied, is 'rt' (round-trip)
                self.control = yaml.load(control)
        elif os.path.exists('layout/DEBIAN/control'):
            with open('layout/DEBIAN/control', 'r') as control:
                yaml = YAML(typ='safe')
                self.control = yaml.load(control)

        self.project['name'] = self.control['Name']

        # TODO: this does nothing atm since Theos projects don't generater DragonMakes
        # which are queried in bin/dragon for icmd else 'sbreload'
        if 'INSTALL_TARGET_PROCESSES' in self.root_makefile.variables:
            self.project['icmd'] = 'killall -9 ' + self.root_makefile.variables['INSTALL_TARGET_PROCESSES']
        else:
            self.project['icmd'] = 'sbreload'

        self._process_makefile(self.root_makefile)
        # print(self.project, file=sys.stderr)

    def _process_makefile(self, makefile):
        if makefile.type:
            self.project[makefile.module_name] = makefile.module
        if makefile.has_subprojects:
            for subproject_name in makefile.subprojects:
                this_cwd = os.getcwd()
                os.chdir(subproject_name)
                with open('Makefile', 'r') as subproject_makefile_file:
                    subproject_makefile = TheosMakefile(subproject_makefile_file.read())
                    subproject_makefile.module['dir'] = os.getcwd().replace(self.root_directory, '')[1:]
                    self._process_makefile(subproject_makefile)
                os.chdir(this_cwd)
