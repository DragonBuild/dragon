#!/usr/bin/env python3
"""
nic.py

A 'New Instance Creator' for DragonBuild
Made with ♡ by quiprr
"""

# Imports
import sys
import os

# Here we will set definitions for our files so we don't need to write them line by line,
# but rather just substitute variables in as we need them.
uname = os.getlogin()

DragonMake_default = """Name: {0}
icmd: {1}

all:
    targetvers: 10.0
    archs:
        - arm64
        - arm64e

{0}:
    type: tweak
    logos_files:
        - Tweak.xm
    arc:
        - Yes
"""

control_default = """Package: {0}
Name: {1}
Depends: mobilesubstrate
Version: 1.0.0
Architecture: iphoneos-arm
Description: An awesome tweak!
Maintainer: {2}
Author: {2}
Section: Tweaks"""

filter_default = """{{ Filter = {{ Bundles = ( "{0}" ); }}; }}
"""
Tweak_default = "#import <Foundation/Foundation.h>"

# Let's start off by ensuring there isn't a DragonMake or Makefile already.
# We can do this with `os`.
if os.path.exists(f'DragonMake'):
    print("[Dragon] There seems to be a DragonMake file in this directory. Please either remove it or create a new folder. Aborting.")
    exit()
else:
    if os.path.exists(f'Makefile'):
        print("[Dragon] There seems to be a Makefile in this directory. Please either remove it or create a new folder. Aborting.")
        exit()

# Now let's get what the user wants.
# First we will grab the project's name.
name = input("[Dragon] Project Name (required): ")
if name == "":
    print("[Dragon] Uh oh! A project name is required. Aborting.")
    exit()

# Now we will get the Bundle ID.
bundle = input("[Dragon] Bundle ID [com.company.package]: ")
if bundle == "":
    bundle = "com.company.package"

# Now we will get the author/maintainer name.
auth = input("[Dragon] Author/Maintainer name [" + uname + "]: ")
if auth == "":
    auth = uname

# Now we will get the bundle filter.
filter = input("[Dragon] Bundle Filter [com.apple.springboard]: ")
if filter == "":
    filter = "com.apple.springboard"

# Now we will get the command to run on installation.
icmd = input("[Dragon] Command to run upon install: ")

# We are done getting user input!
# Let's start writing our files.
print("")
print("[Dragon] Writing files...")

# Make directory for files to go in and switch to it
os.mkdir(name)
os.chdir(name)

# Start writing files
with open("DragonMake", "w+") as f:
    f.write(DragonMake_default.format(name, icmd))
with open("control", "w+") as f:
    f.write(control_default.format(bundle, name, auth))
filename = (name + ".plist")
with open(filename, "w+") as f:
    f.write(filter_default.format(filter))
with open("Tweak.xm", "w+") as f:
    f.write(Tweak_default)

print ("[Dragon] Done!")
