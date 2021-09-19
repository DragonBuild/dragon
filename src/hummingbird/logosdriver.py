from typing import List, OrderedDict

from dragongen.variable_types import BoolFlag
from .driver import Driver 
from .loader import ArgList
from abc import ABC, abstractmethod
from enum import Enum
from collections import namedtuple
import os


class BuildRuleType(Enum):
    LOGOS = 0
    OBJC = 1
    OBJECT = 2
    LINKED = 3



class BuildRule(ABC):
    @abstractmethod
    def __init__(self):
        '''
        '''

    @abstractmethod 
    def key(self):
        '''
        '''

    @abstractmethod 
    def name(self):
        '''
        '''
    
    @abstractmethod 
    def command(self):
        '''
        '''

    @abstractmethod
    def desc(self):
        '''
        '''
    
    @abstractmethod
    def required_variables(self) -> List[str]:
        '''
        '''
    
    @abstractmethod
    def output_filename(self, input_filename):
        '''
        '''
    
    @abstractmethod
    def input_type(self):
        '''
        '''
    
    @abstractmethod
    def output_type(self):
        '''
        '''


class LogosBuildRule(BuildRule):
    def __init__(self):
        '''
        '''

    def key(self):
        return 'logos'
    
    def name(self):
        return 'Logos Preprocessor'
    
    def command(self):
        return '$logos $in > $out'

    def desc(self):
        return 'Preprocessing $in using Logos'
    
    def required_variables(self):
        return ['logos']
    
    def output_filename(self, input_filename):
        return input_filename.replace('.x', '.m')
    
    def input_type(self):
        return BuildRuleType.LOGOS
    
    def output_type(self):
        return BuildRuleType.OBJC



class ObjCBuildRule(BuildRule):
    def __init__(self):
        '''
        '''

    def key(self):
        return 'objc'
    
    def name(self):
        return 'ObjC Compiler'
    
    def command(self):
        return '$cc $archs $internalcflags -c $in -o $out'

    def desc(self):
        return 'Compiling $in with $cc'
    
    def required_variables(self):
        return ['cc', 'archs', 'internalcflags']
    
    def output_filename(self, input_filename):
        return input_filename.replace('.m', '.o')
    
    def input_type(self):
        return BuildRuleType.OBJC
    
    def output_type(self):
        return BuildRuleType.OBJECT


class ObjCXXBuildRule(BuildRule):
    def __init__(self):
        '''
        '''

    def key(self):
        return 'objcxx'
    
    def name(self):
        return 'ObjC++ Compiler'
    
    def command(self):
        return '$cxx $archs $internalcflags -c $in -o $out'

    def desc(self):
        return 'Compiling $in with $cxx'
    
    def required_variables(self):
        return ['cxx', 'archs', 'internalcflags']
    
    def output_filename(self, input_filename):
        return input_filename.replace('.mm', '.o')
    
    def input_type(self):
        return BuildRuleType.OBJC
    
    def output_type(self):
        return BuildRuleType.OBJECT


class LinkedBuildRule(BuildRule):
    def __init__(self):
        self.module_name = ""

    def key(self):
        return 'link'
    
    def name(self):
        return 'Linker'
    
    def command(self):
        return '$ld $archs $internalldflags -o $out $in'

    def desc(self):
        return 'Linking $in with $ld'
    
    def required_variables(self):
        return ['ld', 'archs', 'internalldflags']
    
    def output_filename(self, input_filename):
        return self.module_name
    
    def input_type(self):
        return BuildRuleType.OBJECT
    
    def output_type(self):
        return BuildRuleType.LINKED


def vars_in_str(string):
        variables = []
        in_var = False 
        cur_var = ""
        for character in string:
            if not in_var:
                if character == '$':
                    in_var = True 
                    continue 
            else:
                if character in ['$', ' ', '/', '.']:
                    if character == '$':
                        variables.append(cur_var)
                        cur_var = ""
                    else:
                        variables.append(cur_var)
                        cur_var = ""
                        in_var = False
                else:
                    cur_var += character
        return variables


class BuildCommand:
    def __init__(self, inputs, dir, rule):
        self.in_files = inputs
        self.out_file = dir + rule.output_filename(inputs)
        self.rule_name = rule.key() 

    def build_str(self):
        return f'build {dir}/{self.out_file}: {self.rule_name} {self.in_files}'


EXT_RULE_MAP = {
    'xm': LogosBuildRule,
    'm': ObjCBuildRule,
    'mm': ObjCXXBuildRule,
    'o': LinkedBuildRule
}


class VariableNode:
    def __init__(self, name, value, edges):
        self.name = name
        self.value = value 
        self.edges = edges 

    def __str__(self):
        return f'name={self.name} value={self.value} edges={self.edges}'


class LogosDriver(Driver):
    
    def __init__(self, config):
        self.config = config

        if 'archs' not in self.config:
            # TODO: wtf?
            self.config['archs'] = '-arch arm64'

        for vname, value in self.config.items():
            if vname in ArgList.LIST_KEYS:
                if value and isinstance(value, list):
                    try:
                        arglist_item = ArgList(value, ArgList.LIST_KEYS[vname][0], ArgList.LIST_KEYS[vname][1])
                        self.config[vname] = str(arglist_item)
                    except Exception as ex:
                        print(f'{vname} - {value}')
                        raise ex

            elif vname in BoolFlag.BOOL_KEYS:
                if value:
                    if not isinstance(value, bool):
                        value = value.lower() == "yes"
                    try:
                        arglist_item = BoolFlag(value, BoolFlag.BOOL_KEYS[vname])
                        self.config[vname] = str(arglist_item)
                    except Exception as ex:
                        print(f'{vname} - {value}')
                        raise ex

        
        import pprint 
        pprint.pprint(self.config)

        self.used_variables = []
        self.used_rules = set()
        self.used_commands = []
        self.built_files = []

        self.objects = []

        self.vars = {}
        

        for build_file in self.config['files']:
            ext = build_file.split('.')[-1]
            rule = EXT_RULE_MAP[ext]()
            self.used_rules.add(rule)
            build_rule = BuildCommand(build_file, '.dragon/build/', rule)
            self.used_commands.append(build_rule)
            self.built_files.append(build_rule.out_file)
            for var in rule.required_variables():
                self.used_variables.append(var)
        
        list_index = 0
        while True:
            if list_index >= len(self.built_files):
                break

            build_file = self.built_files[list_index]
            
            ext = build_file.split('.')[-1]
            rule = EXT_RULE_MAP[ext]()

            if rule.output_type() == BuildRuleType.LINKED:
                self.objects.append(build_file)
                list_index += 1
                continue

            self.used_rules.add(rule)
            build_rule = BuildCommand(build_file, '', rule)
            self.used_commands.append(build_rule)
            self.built_files.append(build_rule.out_file)
            for var in rule.required_variables():
                self.used_variables.append(var)
            
            list_index += 1
        
        # create link command 
        linked_build_rule = LinkedBuildRule()
        linked_build_rule.module_name = self.config['name']
        link_command = BuildCommand(' '.join(self.objects), '.dragon/build/', linked_build_rule)
        self.used_rules.add(linked_build_rule)
        for var in linked_build_rule.required_variables():
            self.used_variables.append(var)
        self.used_commands.append(link_command)


        # TODO: this is borked

        self.vars = self.parse_variable_map()

    def parse_variable_map(self):
        variables = {}

        for var in self.used_variables:
            value = self.config[var]
            if isinstance(value, str) and value.startswith('$$'):
                value = os.getenv(value[2:])
            for variable in vars_in_str(value):
                variables[variable] = str(self.config[variable]) if self.config[variable] else ""
            variables[var] = value


        sorted_list = []
        variable_nodes = []
        nodes_with_no_edges = []
        node_map = {}

        
        for name, value in variables.items():
            edges = []
            for variable in vars_in_str(value):
                if variable not in edges:
                    edges.append(variable)
            node = VariableNode(name, value, edges)
            print(str(node))
            if len(node.edges) == 0:
                nodes_with_no_edges.append(node)
            else:
                variable_nodes.append(node)
            node_map[node.name] = node


        while len(nodes_with_no_edges) > 0:
            n = nodes_with_no_edges[0]
            sorted_list.append(n.name)
            nodes_with_no_edges.pop(0)
            for node in variable_nodes:
                if n.name in node.edges:
                    node.edges.remove(n.name)
                if len(node.edges) == 0:
                    variable_nodes.remove(node)
                    nodes_with_no_edges.append(node)
                else:
                    pass

        while len(variable_nodes) > 0:
            for node in variable_nodes:
                for edge in node.edges:
                    if edge in sorted_list:
                        node.edges.remove(edge)
            
                if len(node.edges) == 0:
                    variable_nodes.remove(node)
                    sorted_list.append(node.name)
            # raise AssertionError("Hanging Edges")

        variables_ordered = OrderedDict()

        for variable_node_name in sorted_list:
            variable_node = node_map[variable_node_name]
            variables_ordered[variable_node.name] = variable_node.value

        return variables_ordered

    
    def variables(self):
        return self.vars
    
    def rules(self):
        return self.used_rules

    def commands(self):
        return self.used_commands
        