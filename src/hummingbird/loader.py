from .config import ConfigLoader
from .control import control_keys, control_filenames

import ruyaml as yaml
import os, sys


def control_keyset():
    keyset = [key for key in control_keys()]
    keyset += control_filenames()
    return keyset

def package_keyset():
    keyset = ['name', 'icmd', 'ip', 'port']
    return keyset



class Module:
    '''
    Load Order:
    1 - Load Generator Defaults
    2 - Load Module Type, Load its defaults
    3 - Load all: module values
    4 - Load module values
    '''
    def __init__(self, loader, module, name):
        self.config = {}
        self.config.update(loader.generator_defaults) # 1

        if 'type' in module:
            type = module['type']
            self.config.update(loader.types[type]) # 2

        if loader.user_defined_all_module:
            self.config.update(loader.user_defined_all_module.config) # 3

        self.config.update(module) # 4
            

class DragonMakeLoader(ConfigLoader):
    """
    
    """
    def __init__(self):
        
        super().__init__()

        dragonmake = {}

        self.control = {}
        self.package = {}
        self.modules = []
        self.user_defined_all_module = None
        
        with open('DragonMake') as f:
            dragonmake = yaml.safe_load(f)

        if 'all' in dragonmake:
            self.user_defined_all_module = Module(self, dragonmake['all'], 'all')

        for key in dragonmake:
            if key in package_keyset():
                self.package[key] = dragonmake[key]
            elif key in control_keyset():
                self.control[key] = dragonmake[key]
            else:
                self.modules.append(Module(self, dragonmake[key], key))

        
class TheosLoader(ConfigLoader):
    def __init__(self):
        super().__init__()
