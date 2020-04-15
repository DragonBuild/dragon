# PreLogos is a preprocessor for a preprocessor;

# It allows you to use valid Obj-C Syntax in your IDE of choice while still properly formatting the code before it gets sent to logos

import sys
import re

def main():
    data = sys.stdin.read()
    data = data.replace("orig", "%orig")
    data = data.replace("#pragma mark new", "%new")
    data = re.sub(r'@implementation([\s\S]*)@end', r'%hook\1%end', data)
    sys.stdout.write(data)

if __name__ == "__main__":
    main()