from enum import Enum
import os, sys
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
            current_statement+=line + "\n"
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
        if declaration.startswith('export '):
            declaration = declaration.split('export ', 1)[1]
        tokens = declaration.split(' ')
        self.name = tokens[0]
        if tokens[1] == '=' or tokens[1] == ':=' or tokens[1] == '?=':
            self.type = MakefileVariableStatementType.DECLARATION
        elif tokens[1] == '+=':
            self.type = MakefileVariableStatementType.APPEND
        
        self.value = ' '.join(tokens[2:])
        

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
                self.rules[statement.split("::\n")[0]] = [i.strip() for i in statement.split('\n')[1:] if i.strip() != ""]
        
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
    

class TheosMakefile(Makefile):
    def __init__(self, file_contents: str):
        super().__init__(file_contents)
        
        self.type = None
        self.has_subprojects = False
        self.module_name = ""
        self.module = {}
        self.subprojects = []
        
        self.module['arc'] = False
        
        for included in self.includes:
            if 'tweak.mk' in included:
                self.type = TheosMakefileType.TWEAK
                self.module['frameworks'] = ['Foundation', 'UIKit'] # :/
                self.module['type'] = 'tweak'
            if 'aggregate.mk' in included:
                self.has_subprojects = True
            if 'bundle.mk' in included:
                self.module['type'] = 'prefs'
                self.type = TheosMakefileType.BUNDLE
            if 'library.mk' in included:
                self.module['type'] = 'library'
                self.type = TheosMakefileType.LIBRARY
                
        for variable in self.variables:
            if variable.endswith('_NAME'):
                self.module_name = self.variables[variable]
            elif variable.endswith('_FILES'):
                self.module['files'] = self.variables[variable].split(' ')
            elif variable.endswith('_FRAMEWORKS'):
                self.module['frameworks'] = self.variables[variable].split(' ')
            elif variable.endswith('_PRIVATE_FRAMEWORKS'):
                self.module['frameworks'] += self.variables[variable].split(' ')
            elif variable.endswith('_CFLAGS'):
                self.module['cflags'] = self.variables[variable]
            elif variable.endswith('_LIBRARIES'):
                self.module['libs'] = self.variables[variable].split(' ')
            
        
        files = []
        if 'files' in self.module:
            tokens = self.module['files']
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

            self.module['files'] = files

        if 'stage' in self.rules:
            stage = self.rules['stage']
            stage_processed = []
            for command in stage:
                command = command.replace('$(THEOS_STAGING_DIR)', '$proj_build_dir/_')
                command = command.replace('$(THEOS)', '~/.dragon')
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

        with open('control', 'r') as control: 
            yaml=YAML(typ='safe')  # default, if not specfied, is 'rt' (round-trip)
            self.control = yaml.load(control)

        self.project['name'] = self.control['Name']
        
        if 'INSTALL_TARGET_PROCESSES' in self.root_makefile.variables:
            self.project['icmd'] = 'killall -9 ' + self.root_makefile.variables['INSTALL_TARGET_PROCESSES']
        
        self._process_makefile(self.root_makefile)

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
