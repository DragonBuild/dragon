from .config import ConfigLoader


FILE_TYPE_MAP = {
    "x": "logos",
    "m": "objc",
    "o": "object"
}


class BuildAction:
    def __init__(self, action, filename, output):
        self.rule = action['rule']
        self.filename = filename 
        self.output = output


class BuildFile:
    def __init__(self, filename):
        ext = filename.split('.')[-1]
        self.filename = filename
        self.filetype = FILE_TYPE_MAP[ext]


class ModuleConfigProcessor:
    def __init__(self, driver, module):
        self.files = []
        for filename in module.config['files']:
            self.files.append(BuildFile(filename))
