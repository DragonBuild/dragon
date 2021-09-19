from .config import ConfigLoader
from .control import control_keys, control_filenames

import ruyaml as yaml
import os, sys



class BoolFlag:
    '''
    Variables with values of type bool, and their corresponding flag pairs.
    '''

    BOOL_KEYS = {
        'arc': ('-fobjc-arc', ''),
    }

    def __init__(self, value: bool, flagpair):
        self.value = value
        self.true_flag, self.false_flag = flagpair

    def __bool__(self):
        return self.value

    def __str__(self):
        return self.true_flag if self.value else self.false_flag


class ArgList(list):
    '''
    Variables with values of type list: their corresponding delims and prefixes
    '''

    LIST_KEYS = {
        'logos_files': ('', ' '),
        'tweak_files': ('', ' '),  # used for legacy compatibility, isn't actually used.
        'archs': ('-arch ', ' -arch '),  # Also only for legacy, this is handled in a much more complex manner # TODO: BUGGED
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
        'header_includes': ('-I', ' -I'),
        'macros': ('-D', ' -D'),
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
        if self.prefix + self.delim.join(str(s) for s in self) == "None":
            return ""
        if self.prefix + self.delim.join(str(s) for s in self):
            return self.prefix + self.delim.join(str(s) for s in self)
        return ""



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
    def __init__(self, loader, module, name, target):
        self.config = {}
        self.config.update(loader.generator_defaults) # 1

        if target:
            self.config.update(loader.targets[target])

        if 'type' in module:
            type = module['type']
            self.config.update(loader.types[type]["variables"]) # 2

        if loader.user_defined_all_module:
            self.config.update(loader.user_defined_all_module.config) # 3
        

        self.config.update(module) # 4
        
        self.config['name'] = name
            

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
            self.user_defined_all_module = Module(self, dragonmake['all'], 'all', None)

        for key in dragonmake:
            if key in package_keyset():
                self.package[key] = dragonmake[key]
            elif key in control_keyset():
                self.control[key] = dragonmake[key]
            else:
                self.modules.append(Module(self, dragonmake[key], key, 'ios'))

        
class TheosLoader(ConfigLoader):
    def __init__(self):
        super().__init__()
