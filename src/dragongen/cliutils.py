
import sys
import ruyaml
import os


if __name__ == "__main__":
    if 'packid' in sys.argv[1]:
        if os.path.exists('DragonMake'):
            with open('DragonMake') as fp:
                data = ruyaml.safe_load(fp)
                if 'package' in data:
                    print(data['package'])
                    exit(0)
                if 'id' in data:
                    print(data['id'])
                    exit(0)
                if 'Package' in data:
                    print(data['Package'])
                    exit(0)
        if os.path.exists('control'):
            with open('control') as fp:
                data = ruyaml.safe_load(fp)
                if 'Package' in data:
                    print(data['Package'])
                    exit(0)
        elif os.path.exists('layout/DEBIAN/control'):
            with open('layout/DEBIAN/control') as fp:
                data = ruyaml.safe_load(fp)
                if 'Package' in data:
                    print(data['Package'])
                    exit(0)
        exit(1)

    if 'needsobjcs' in sys.argv[1]:
        if os.path.exists('DragonMake'):
            with open('DragonMake') as fp:
                data = ruyaml.safe_load(fp)
                if 'objcs' in data:
                    exit(0)
        exit(1)
