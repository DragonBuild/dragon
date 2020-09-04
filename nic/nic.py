import os, sys

def main():
    pass

def write_bundle_filter(name, bundle):
    if not os.path.exists(f'{name}.plist'):
        bfilter = open(f'{name}.plist', 'w+')
        bfilter.write('{ Filter = { Bundles = ( ' + bundle + ' ); }; }')
        bfilter.close()

def geticmd(targ: str):
    if targ.lower() == 'springboard':
        return 'sbreload'
    return 'killall -9 ' + targ

def write_dragonmake(name, icmd, type):
    f = open("DragonMake", 'w+')
    dir_path = os.path.basename(os.getcwd())
    f.write("---\n")
    f.write(f'name: {dir_path}\n')
    f.write(f'icmd: f{icmd}\n\n')
    f.write(f'{dir_path}:\n')
    f.write('  type: tweak\n')
    f.write('  logos_files:\n    - Tweak.xm\n')
    f.close()

if __name__ == "__main__":
    main()