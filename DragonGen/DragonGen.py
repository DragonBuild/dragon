import string
import re 
import regex

makevardef = regex.compile('^\([a-zA-Z0-9_]+\)[ \t]*=\(.*\)')

def getmakevars(filename):
	variables = {}
	fp = open(filename)
	try:
		while 1:
			line = fp.readline()
			if not line:
				break
			if makevardef.match(line) < 0:
				continue
			name, value = makevardef.group(1, 2)
			# Strip trailing comment
			i = string.find(value, '#')
			if i >= 0:
				value = value[:i]
			value = string.strip(value)
			variables[name] = value
	finally:
		fp.close()
	return variables

def process_tweak_build(variables):
    

def main():
    files = []
    for r, d, f in os.walk("./"):
        for file in f:
            if 'Makefile' in file or 'DragonMake' in file:
                files.append(os.path.join(r, file))
    if 'DragonMake' in files:
        variables = getmakevars('DragonMake')
    else if 'Makefile' in files:
        variables = getmakevars('Makefile')
    else:
        print("DragonMake or Makefile not found.")
        exit(1)
    
    
    
if __name__ == "__main__":
    main()