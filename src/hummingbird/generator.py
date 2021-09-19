
from abc import ABC, abstractmethod 
from buildgen.generator import BuildFileGenerator

class Generator(ABC):
    @abstractmethod 
    def __init__(self, driver):
        '''
        '''

    @abstractmethod
    def generate(self, filename):
        '''
        '''

class NinjaFileGenerator(Generator):
    def __init__(self, driver):
        self.driver = driver

    def generate(self, filename):
        with open(filename, 'w') as out:
            bfg = BuildFileGenerator(out)
            var_dict = self.driver.variables()
            rule_list = self.driver.rules()
            cmd_list = self.driver.commands()
            for var in var_dict:
                bfg.variable(var, var_dict[var])
            for rule in rule_list:
                bfg.rule(rule.key(), rule.command(), rule.desc())
            for cmd in cmd_list:
                bfg.build(cmd.out_file, cmd.rule_name, cmd.in_files)
            
