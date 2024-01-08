#!/usr/bin/env python3

import yaml, os, sys
# from shared.util import dbstate

# This script will get called w/
# argc=3  argv[0]                                argv[1]     argv[2]
# python3 $DRAGON_ROOT_DIR/internal/bfilter.py DragonMake  projectName

def main():
    if os.path.exists(sys.argv[1]):
        with open(sys.argv[1]) as f:
            config = yaml.safe_load(f)

    # dbstate("Packager", "Creating Filter for " + sys.argv[2])

    filter_dict = config[sys.argv[2]]['filter']
    print(filter_serialize(filter_dict))


def filter_serialize(filter_dict):
    # {'executables':['SpringBoard']}
    # out: { Filter = { Executables = ( "SpringBoard" ); }; }
    ind = "{ Filter = { "
    for i in filter_dict:
        ind += i.capitalize() + ' = ( ' + ", ".join(["\"" + j + "\"" for j in filter_dict[i]]) + ' );'
    ind += ' }; }'
    return ind


main()
