import yaml, os, sys


def main():

    keys = {
        'name': 'Name',
        'id': 'Package',
        'author': 'Author',
        'mtn': 'Maintainer',
        'version': 'Version',
        'depends': 'Depends',
        'provides': 'Provides',
        'architecture': 'Architecture',
        'description': 'Description',
        'section': 'Section',
        'package': 'Package',
        'desc': 'Description',
    }

    defs = {
        'Section': 'Tweaks',
        'Description': 'A cool tweak',
        'Version': '0.1.0',
        'Architecture': 'iphoneos-arm',
    }

    if os.path.exists(sys.argv[1]):
        with open(sys.argv[1]) as f:
            config = yaml.safe_load(f)

    else:
        raise FileNotFoundError

    control = {keys[key]: value for (key, value) in config.items() if key in keys}

    if 'Author' in control and 'Maintainer' not in control:
        control['Maintainer'] = control['Author']

    # print(defs.update(control))
    # print(control)
    # print(dict(defs, **control))

    with open(sys.argv[2], 'w') as out:
        out.truncate()
        out.seek(0)
        yaml.dump(dict(defs, **control), out, default_flow_style=False)

    if 'postinst' in config:

        with open(os.path.dirname(os.sys.argv[2]) + '/postinst', 'w') as out:
            out.truncate()
            out.seek(0)
            out.writelines(config['postinst'])

main()
