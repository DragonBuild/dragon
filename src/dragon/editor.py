import os, sys, pwd
import os.path
import pprint
import ruyaml as yaml

from .util import dprintline, OutputColors, OutputWeight

dbstate = lambda msg: dprintline(label_color=OutputColors.Green, tool_name="Project Editor", text_color=OutputColors.White, text_weight=OutputWeight.Bold, pusher=False, msg=msg)
dbwarn = lambda msg: dprintline(label_color=OutputColors.Yellow, tool_name="Project Editor", text_color=OutputColors.White, text_weight=OutputWeight.Normal, pusher=False, msg=msg)
dberror = lambda msg: dprintline(label_color=OutputColors.Red, tool_name="Project Editor", text_color=OutputColors.White, text_weight=OutputWeight.Bold, pusher=False, msg=msg)


def get_input(prompt, default):
    dbstate(f'{prompt} ({default})')
    ret = input('>> ')
    return ret if ret.strip() else default

def get_from_selector(prompt, values, default):
    dbstate(prompt)
    itemlist = []
    for i, key in enumerate(values):
        print(f'[{i}] > {key}')
        itemlist.append(values[key])
    item = int(get_input('Select Item', default))
    return itemlist[item]


class Project:
    def __init__(self, root_directory):
        self.root_directory = root_directory
        self.directory_name = self.root_directory.split('/')[-1]
        self.current_username = pwd.getpwuid(os.getuid()).pw_name
        self.variables = {}

    def create_new(self):
        self.variables['name'] = get_input('Project Name', self.directory_name)
        self.variables['id'] = get_input('Bundle ID', f'com.{self.current_username}.{self.directory_name}')
        self.variables['depends'] = 'mobilesubstrate'
        self.variables['architecture'] = 'iphoneos-arm'
        self.variables['version'] = get_input('Version', '0.0.1')
        self.variables['description'] = get_input('Description', 'A cool MobileSubstrate Tweak')
        self.variables['author'] = get_input('Author', self.current_username)
        self.variables['section'] = 'Tweaks'


class Module:
    def __init__(self):
        self.variables = {}
        self.name = ''

    def create_new(self):
        self.variables['type'] = get_from_selector('Select Module Type', {'Tweak':'tweak', 'CLI Tool':'cli', 'Library':'library'}, '0')
        self.name = get_input('Name', 'ModuleName')
        while True:
            subdir = get_input('Subdirectory Name (Leave empty to work in current directory)', '')
            if subdir != '':
                if os.path.exists(subdir):
                    print('File/Directory already exists;')
                    continue
                else:
                    self.variables['dir'] = subdir
                    os.mkdir(subdir)
                    break
            else:
                break
        self._new_for_type(self.variables['type'])

    def _new_for_type(self, type):
        if 'dir' in self.variables:
            os.chdir(self.variables['dir'])
            del self.variables['dir']

        if type == 'tweak':
            self.variables['filter'] = { 'executables': get_input('Comma seperated list of applications to inject', 'SpringBoard').split(', ')}
            self.variables['files'] = [f'{self.name}.x']
            with open(f'{self.name}.x', 'w') as out:
                out.write('// Insert your code here!\n')


class ProjectEditor:
    def __init__(self):

        self.project_root_directory = os.getcwd()

        if os.path.exists('DragonMake'):
            with open('DragonMake') as f:
                self.config = yaml.safe_load(f)
                self.preexisting_config = True
        else:
            self.config = {}
            self.preexisting_config = False

    def create_new_module(self):
        if not self.preexisting_config:
            project = Project(self.project_root_directory)
            project.create_new()
            self.config = project.variables

        mod = Module()
        mod.create_new()
        self.config[mod.name] = mod.variables

def main():
    editor = ProjectEditor()
    editor.create_new_module()
    with open('DragonMake', 'w') as f:
        f.write(yaml.dump(editor.config, Dumper=yaml.RoundTripDumper))

if __name__ == '__main__':
    main()
