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
# argc=3  argv[0]                          argv[1]     argv[2]    
# python3 $DRAGONDIR/internal/bfilter.py DragonMake  projectName

def main():
    if os.path.exists(sys.argv[1]):
        with open(sys.argv[1]) as f:
            config = yaml.safe_load(f)

    # dbstate("Creating Filter for " + sys.argv[2])

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