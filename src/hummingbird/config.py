import ruyaml as yaml
import os, sys 

class ConfigLoader:
    def __init__(self):
        self.default_generator_values = {}
        self.generator_defaults = {}
        self.types = {}
        self.rules = {}
        self.targets = {}

        with open(f'{os.environ["DRAGONDIR"]}/internal/defaults.yml') as f:
            self.default_generator_values = yaml.safe_load(f)["Defaults"]
        with open(f'{os.environ["DRAGONDIR"]}/internal/targets.yml') as f:
            self.targets.update(yaml.safe_load(f)["Targets"])
        with open(f'{os.environ["DRAGONDIR"]}/internal/types.yml') as f:
            self.types.update(yaml.safe_load(f)["Types"])


        with open(f'{os.environ["DRAGONDIR"]}/internal/rules.yml') as f:
            self.rules.update(yaml.safe_load(f))

        self._load_custom()

    def _load_custom(self):
        self.generator_defaults.update(self.default_generator_values)
        if os.path.exists(f'{os.environ["DRAGONDIR"]}/custom.yml'):
            with open(f'{os.environ["DRAGONDIR"]}/custom.yml') as f:
                self.generator_defaults.update(yaml.safe_load(f))
        

    

        
        
