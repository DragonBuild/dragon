#!/usr/bin/env python3

import yaml, os, sys
from shared.util import dbstate, dbwarn, dberror

# This script will get called w/
# argc=3  argv[0]                              argv[1]    argv[2]
# python3 $DRAGON_ROOT_DIR/internal/control.py DragonMake ./$DRAGON_DIR/_/DEBIAN/control
def main():
    dbstate("Packager", "Pulling 'control' values from DragonMake")

    keys = {
        'name': 'Name',
        'id': 'Package',
        'author': 'Author',
        'auth': 'Author',
        'maintainer': 'Maintainer',
        'mtn': 'Maintainer',
        'version': 'Version',
        'vers': 'Version',
        'depends': 'Depends',
        'deps': 'Depends',
        'provides': 'Provides',
        'conflicts': 'Conflicts',
        'architecture': 'Architecture',
        'section': 'Section',
        'package': 'Package',
        'description': 'Description',
        'desc': 'Description',
        'icon': 'Icon',
        'depiction': 'Depiction',
        'sldepiction': 'Sileodepiction',
        'sileodepiction': 'Sileodepiction'
    }

    defs = {
        'Section': 'Tweaks',
        'Description': 'A cool MobileSubstrate Tweak',
        'Version': '0.0.1',
        'Architecture': 'iphoneos-arm',
        'Depends': 'mobilesubstrate'  # This is a blind guess, maybe we can improve this logic?
    }

    filenames = [  # extrainst_?
        'preinst',
        'postinst',
        'prerm',
        'postrm'
    ]
    # load in the DragonMake file
    if os.path.exists(sys.argv[1]):
        with open(sys.argv[1]) as f:
            config = yaml.safe_load(f)

    else:
        dberror("Packager", 'DragonMake not found, not sure how we got here honestly.')
        dberror("Packager", 'If you believe this message is in error, file an issue.')
        dberror("Packager", 'https://github.com/DragonBuild/dragon')

    control = {keys[key]: value for (key, value) in config.items() if key in keys}

    # Fallbacks section
    if 'Name' not in control:
        control['Name'] = os.path.basename(os.getcwd())
        # Warn for this bc it's kinda important
        dbwarn("Packager", f'No "name:" key in DragonMake, guessing based on directory name ({control["Name"]})')

    if 'Package' not in control:
        control['Package'] = f'com.yourcompany.{control["Name"].lower()}'
        # Warn for this too, it's fairly important
        dbwarn("Packager", 'No "id:" key in DragonMake, creating default based on `Name:` key')

    if 'Author' not in control:
        control['Author'] = os.getlogin()
        dbwarn("Packager", f'No "Author:" key in DragonMake, guessing based on current user ({control["Author"]})')

    if 'Maintainer' not in control:
        control['Maintainer'] = control['Author']
        dbwarn("Packager", 'No "Maintainer:" key in DragonMake, creating default based on `Author:` key')

    if int(os.environ["rootless"]) == 1:
        control['Architecture'] = 'iphoneos-arm64'

    # print(defs.update(control))
    # print(control)
    # print(dict(defs, **control))

    with open(sys.argv[2], 'w') as out:
        out.truncate()
        out.seek(0)
        yaml.dump(dict(defs, **control), out, default_flow_style=False)

    for name in filenames:
        if name in config:
            dbstate("Packager", f'Creating {name}')
            with open(os.path.dirname(os.sys.argv[2]) + f'/{name}', 'w') as out:
                out.truncate()
                out.seek(0)
                out.writelines(config[name])


if __name__ == "__main__":
    main()
