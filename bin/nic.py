#!/usr/bin/env python3

import yaml
import os

filter_text = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
        <key>Filter</key>
        <dict>
                <key>Bundles</key>
                <array>
                        <string>{0}</string>
                </array>
        </dict>
</dict>
</plist>
'''

prefs_h = '''#import <Preferences/PSListController.h>

@interface {0}RootListController : PSListController

@end
'''

prefs_m = '''#include "{0}RootListController.h"

@implementation {0}RootListController

- (NSArray *)specifiers {
	if (!_specifiers) {
		_specifiers = [[self loadSpecifiersFromPlistName:@"Root" target:self] retain];
	}

	return _specifiers;
}

@end
'''

entry_p = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>entry</key>
	<dict>
		<key>bundle</key>
		<string>{0}</string>
		<key>cell</key>
		<string>PSLinkCell</string>
		<key>detail</key>
		<string>{1}RootListController</string>
		<key>icon</key>
		<string>icon.png</string>
		<key>isController</key>
		<true/>
		<key>label</key>
		<string>{0}</string>
	</dict>
</dict>
</plist>
'''

info_p = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>CFBundleDevelopmentRegion</key>
	<string>English</string>
	<key>CFBundleExecutable</key>
	<string>{0}</string>
	<key>CFBundleIdentifier</key>
	<string>{1}</string>
	<key>CFBundleInfoDictionaryVersion</key>
	<string>6.0</string>
	<key>CFBundlePackageType</key>
	<string>BNDL</string>
	<key>CFBundleShortVersionString</key>
	<string>1.0.0</string>
	<key>CFBundleSignature</key>
	<string>????</string>
	<key>CFBundleVersion</key>
	<string>1.0</string>
	<key>NSPrincipalClass</key>
	<string>{2}RootListController</string>
</dict>
</plist>
'''

root_p = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>items</key>
	<array>
		<dict>
			<key>cell</key>
			<string>PSGroupCell</string>
			<key>label</key>
			<string>Use https://developer.openpack.io/liasse/ for a GUI Preference Builder</string>
		</dict>
	</array>
	<key>title</key>
	<string>{0}</string>
</dict>
</plist>
'''

control = '''Package: {0}
Name: {1}
Depends: mobilesubstrate
Version: 0.0.1
Architecture: iphoneos-arm
Description: An interesting Tweak
Maintainer: {2}
Author: {2}
Section: Tweaks
'''

def main():
    name = input("Name > ")
    if not os.path.exists("DragonMake"):
        os.mkdir(name)
        os.chdir(name)
    f = open("DragonMake", 'a+')
    config = yaml.safe_load(f)
    f.close()
    go = 0
    top = 0
    dirr = '.'
    if not config:
        config = {}
    if not 'package_name' in config:
        top = 1
    while go == 0:
        print("1: Tweak")
        print("2: Prefs")
        print("3: Library")
        ptype = input("Project Template > ")
        if int(ptype) > 0 and int(ptype) < 4:
            go = 1 
        else:
            print("Enter a number 1-3...")

    project_type = 'tweak bundle library'.split(' ')[int(ptype)-1]
    package_id = input("Identifier > ")
    author = input("Author > ")
    target_process = input("Target Process > ")
    class_prefix = input("Class Prefix > ")

    if top == 1:
        config['package_name'] = name 
        config['install_command'] = 'killall -9 ' + target_process 

    config[name] = {}
    if top!=1:
        config[name]['dir'] = name.lower() 
        dirr = name.lower()

    config[name]['type'] = project_type
    if project_type == 'tweak':
        config[name]['logos_files'] = ['Tweak.xm']
        open(f'{dirr}/Tweak.xm', 'a+').close() 
        ffilter = open(f'{dirr}/{name}.plist', 'a+')
        ffilter.write(filter_text.format('com.apple.springboard'))
        ffilter.close()
        
    elif project_type == 'bundle':
        config[name]['files'] = [f'{class_prefix}RootListController.m']
        config[name]['frameworks'] = ['Preferences']
        config[name]['stage'] = ['mkdir -p .dragon/_/Library/PreferenceLoader/Preferences/', 'cp entry.plist .dragon/_/Library/PreferenceLoader/Preferences/$name.plist']
        rootm = open(f'{dirr}/{class_prefix}RootListController.m', 'a+')
        rootm.write(prefs_m.format(class_prefix))
        rootm.close()
        rooth = open(f'{dirr}/{class_prefix}RootListController.h', 'a+')
        rooth.write(prefs_h.format(class_prefix))
        rooth.close()
        entry = open(f'{dirr}/entry.plist', 'a+')
        entry.write(entry_p.format(name, class_prefix))
        entry.close() 
        info = open(f'{dirr}/Resources/Info.plist', 'a+')
        info.write(info_p.format(name, package_id, class_prefix))
        info.close() 
        root = open(f'{dirr}/Resources/Root.plist', 'a+')
        root.write(root_p.format(name))
        root.close()

    else:
        config[name]['files'] = [f'{name}.m']

    if top==1:
        controlfile = open('control', 'a+')
        controlfile.write(control.format(package_id, name, author))
        controlfile.close()

    with open('DragonMakeTemp', 'w') as f:
        yaml.dump(config, f)

    with open('DragonMake', 'a+') as outfile:
        with open('DragonMakeTemp', 'r') as infile:
            for line in infile:
                outfile.write(line)



if __name__ == "__main__":
    main()