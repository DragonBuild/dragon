#!/usr/bin/env bash
# https://github.com/ItHertzSoGood/dragon-nic/

# ANSI Escape Color Codes
BOLDBLUE='\033[1m\033[34m'
BOLDWHITE='\033[0m\033[1m'
RESET='\033[0m'

# See if user is running as root
if [ "$EUID" == 0 ]; then
    printf "${BOLDBLUE}[Dragon] ${BOLDWHITE}Do not run this script as root.${RESET}\n"
    exit
fi

# See if DragonBuild actually exists
if ! [ -f "/usr/local/bin/dragon" ]; then
    printf "${BOLDBLUE}[Dragon] ${BOLDWHITE}DragonBuild was not found.${RESET}\n"
    exit
fi

# See if DragonMake is already in working directory
if [ -f "DragonMake" ]; then
    printf "${BOLDBLUE}[Dragon] ${BOLDWHITE}This directory already has a DragonMake file.${RESET}\n"
    printf "${BOLDBLUE}[Dragon] ${BOLDWHITE}Please make or go to an empty directory.${RESET}\n"
    exit
fi

# Prompts and stuff
printf "${BOLDBLUE}[Dragon] ${BOLDWHITE}New Instance Creator\n"
printf "\n"
printf "${BOLDBLUE}[Dragon] ${BOLDWHITE}1.) Basic tweak\n"
printf "${BOLDBLUE}[Dragon] ${BOLDWHITE}2.) Basic preferences\n"
printf "\n"
read -p "> " selection
if ( [ $selection != 1 ] && [ $selection != 2 ]  ) ; then
    printf "${BOLDBLUE}[Dragon] ${BOLDWHITE}$selection is not a valid selection.\n"
    printf "${BOLDBLUE}[Dragon] ${BOLDWHITE}Please re-run the script.\n"
    exit
else
    printf "\n"
    printf "${BOLDBLUE}[Dragon] ${BOLDWHITE}What is the name of your project?\n"
    read -p "> " name
    printf ""
    printf "${BOLDBLUE}[Dragon] ${BOLDWHITE}What is the bundle ID of your project? (e.g. com.apple.name)\n"
    read -p "> " bundleid
    printf ""
    printf "${BOLDBLUE}[Dragon] ${BOLDWHITE}What is the name of the author?\n"
    read -p "> " author
fi

if [ "$selection" == 1 ]; then 
    # Create DragonMake
    printf "${BOLDBLUE}[Dragon] ${BOLDWHITE}Creating DragonMake...\n"
    echo "name: $name" >> DragonMake
    echo "icmd: sbreload" >> DragonMake
    echo "$name:" >> DragonMake
    echo "  type: tweak" >> DragonMake
    echo "  files:" >> DragonMake
    echo "    - Tweak.xm" >> DragonMake
    printf "${BOLDBLUE}[Dragon] ${BOLDWHITE}Done!\n"
    
    # Create Tweak.xm
    printf "${BOLDBLUE}[Dragon] ${BOLDWHITE}Creating Tweak.xm...\n"
    echo "" >> Tweak.xm
    printf "${BOLDBLUE}[Dragon] ${BOLDWHITE}Done!\n"

    # Create control
    printf "${BOLDBLUE}[Dragon] ${BOLDWHITE}Creating control...\n"
    echo "Package: $bundleid" >> control
    echo "Name: $name" >> control
    echo "Version: 0.0.1" >> control
    echo "Architecture: iphoneos-arm" >> control
    echo "Description: This is a description." >> control
    echo "Maintainer: $author" >> control
    echo "Author: $author" >> control
    echo "Section: Tweaks" >> control
    echo "Depends:" >> control
    printf "${BOLDBLUE}[Dragon] ${BOLDWHITE}Done!\n"
    
    # Finish up
    exit
fi 

if [ "$selection" == 2 ]; then 
    # Create DragonMake
    printf "${BOLDBLUE}[Dragon] ${BOLDWHITE}Creating DragonMake...\n"
    echo "name: $name" >> DragonMake
    echo "icmd: sbreload" >> DragonMake
    echo "$name:" >> DragonMake
    echo "  type: prefs" >> DragonMake
    echo "  files:" >> DragonMake
    echo "    - XXXRootListController.m" >> DragonMake
    echo "    - XXXRootListController.h" >> DragonMake
    echo "    - Root.plist" >> DragonMake
    printf "${BOLDBLUE}[Dragon] ${BOLDWHITE}Done!\n"

    # Create RootListController.h/m
    printf "${BOLDBLUE}[Dragon] ${BOLDWHITE}Creating XXXRootListControllers...\n"
    echo "" >> XXXRootListController.m
    echo "" >> XXXRootListController.h
    printf "${BOLDBLUE}[Dragon] ${BOLDWHITE}Done!\n"

    # Create Root.plist
    printf "${BOLDBLUE}[Dragon] ${BOLDWHITE}Creating Root and Info.plist...\n"
    mkdir Resources
    cd Resources
    echo "<?xml version="1.0" encoding="UTF-8"?>" >> Root.plist
    echo "<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">" >> Root.plist
    echo "<plist version="1.0">" >> Root.plist
    echo "<dict>" >> Root.plist
	echo "    <key>items</key>" >> Root.plist
	echo "        <array>" >> Root.plist
    echo "" >> Root.plist
    echo "        </array>" >> Root.plist
    echo "</dict>" >> Root.plist
    echo "</plist>" >> Root.plist

    # Create Info.plist
    echo "<?xml version="1.0" encoding="UTF-8"?>" >> Info.plist
    echo "<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">" >> Info.plist
    echo "<plist version="1.0">" >> Info.plist
    echo "<dict>" >> Info.plist
	echo "    <key>CFBundleDevelopmentRegion</key>" >> Info.plist
	echo "    <string>English</string>" >> Info.plist
	echo "    <key>CFBundleExecutable</key>" >> Info.plist
	echo "    <string>$name</string>" >> Info.plist
	echo "    <key>CFBundleIdentifier</key>" >> Info.plist
	echo "    <string>$bundleid</string>" >> Info.plist
	echo "    <key>CFBundleInfoDictionaryVersion</key>" >> Info.plist
	echo "    <string>6.0</string>" >> Info.plist
	echo "    <key>CFBundlePackageType</key>" >> Info.plist
	echo "    <string>BNDL</string>" >> Info.plist
	echo "    <key>CFBundleShortVersionString</key>" >> Info.plist
	echo "    <string>0.0.1</string>" >> Info.plist
	echo "    <key>CFBundleSignature</key>" >> Info.plist
	echo "    <string>????</string>" >> Info.plist
	echo "    <key>CFBundleVersion</key>" >> Info.plist
	echo "    <string>1.0</string>" >> Info.plist
	echo "    <key>NSPrincipalClass</key>" >> Info.plist
	echo "    <string>XXXRootListController</string>" >> Info.plist
    echo "</dict>" >> Info.plist
    echo "</plist>" >> Info.plist
    printf "${BOLDBLUE}[Dragon] ${BOLDWHITE}Done!\n"

    # Finish up
    exit
else
    exit
fi
fi

exit