import yaml, os, sys

colors = [["\033[0;31m","\033[0;32m","\033[0;33m","\033[0;34m","\033[0;36m",
"\033[0;37m","\033[0m"],["\033[1;31m","\033[1;32m","\033[1;33m","\033[1;34m",
"\033[1;36m","\033[1;37m","\033[0m"]]

def dprintline(col: int, tool: str, textcol: int, bold: int, pusher: int, msg: str):
    print("%s[%s]%s %s%s%s" % (
        colors[1][col], tool, colors[bold][textcol], ">>> " if pusher else "", msg, colors[0][6]))

dbstate = lambda msg: dprintline(1, "Packager", 5, 1, 0, msg)
dbwarn = lambda msg: dprintline(2, "Packager", 5, 0, 0, msg)
dberror = lambda msg: dprintline(0, "Packager", 5, 1, 0, msg)

# This script will get called w/ 
# argc=3  argv[0]                          argv[1]    argv[2]
# python3 $DRAGONDIR/internal/control.py DragonMake ./.dragon/_/DEBIAN/control
def main():
    dbstate("Pulling 'control' values from DragonMake")

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
        'architecture': 'Architecture',
        'section': 'Section',
        'package': 'Package',
        'description': 'Description',
        'desc': 'Description',
    }

    defs = {
        'Section': 'Tweaks',
        'Description': 'A cool tweak',
        'Version': '0.1.0',
        'Architecture': 'iphoneos-arm',
        'Depends': 'mobilesubstrate' # This is a blind guess, maybe we can improve this logic?
    }
    # extrainst?
    filenames = [
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
        dberror('DragonMake not found, not sure how we got here honestly.')
        dberror('If you believe this message is in error, file an issue.')
        dberror('https://github.com/DragonBuild/dragon')

    control = {keys[key]: value for (key, value) in config.items() if key in keys}


    # Fallbacks section

    if 'Name' not in control:
        control['Name'] = os.path.basename(os.getcwd())
        # Warn for this bc it's kinda important
        dbwarn(f'No "name:" key in DragonMake, guessing based on directory name ({control["Name"]})')

    if 'Package' not in control:
        control['Package'] = f'com.yourcompany.{control["Name"].lower()}'
        # Warn for this too, its fairly important
        dbwarn(f'No "id:" key in DragonMake, creating default based on Name: key')

    if 'Author' not in control:
        control['Author'] = os.getlogin()

    if 'Author' in control and 'Maintainer' not in control:
        control['Maintainer'] = control['Author']

    # print(defs.update(control))
    # print(control)
    # print(dict(defs, **control))

    with open(sys.argv[2], 'w') as out:
        out.truncate()
        out.seek(0)
        yaml.dump(dict(defs, **control), out, default_flow_style=False)

    for name in filenames:
        if name in config:
            dbstate(f'Creating {name}')
            with open(os.path.dirname(os.sys.argv[2]) + f'/{name}', 'w') as out:
                out.truncate()
                out.seek(0)
                out.writelines(config[name])

main()
