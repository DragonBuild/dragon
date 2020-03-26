# DragonBuild
DragonBuild, simply explained, is a fast ninja-based theos alternative. 

Specifically, it's a ninja build file generator and packaging system for substrate extensions and other common packages distributed in the jailbreak community. 

It's aimed at both speed and configurability. Every single factor of it is configurable from a singular file. 

## Table of Contents

- [DragonBuild](#dragonbuild)
  * [Notes](#notes)
  * [Basic Usage](#basic-usage)
  * [Installing DragonBuild](#installing-dragonbuild)
  * [Setting your project up for DragonBuild](#setting-your-project-up-for-dragonbuild)
  * **[Credits](#credits)**
  * [Under the Hood](#under-the-hood)
    + [Ninja Build file gen Proccess](#ninja-build-file-gen-proccess)

## Notes

* This was built for MacOS, although I've done a little bit of testing on Linux. If it does not detect `ldid` in the path, it will look in `$DRAGONBUILD/toolchain/bin/` for a toolchain. I would advise properly installing  to your path, as this is somewhat hacked in at the moment. 

## Basic Usage

Dragon has a ton of arguments to make things easier, and it's typically always getting more. 

`dragon`

# Installing DragonBuild

This will allow you to use `dragon i` to install packages to your device. 

## Setting your project up for DragonBuild

### Building and installing your Tweak

`dragon build` to build (`dragon make` and `dragon b` also work)

`dragon install` to install (`dragon i` also works)

### Forcing a rebuild

Using the `c` or `clean` command will perform a clean regen and rebuild of your project. 

# Helpful links

[sbinger's arm64e toolchain](https://github.com/sbingner/llvm-project/releases/tag/v10.0.0-1)

# Credits

@theiostream, for [this](https://github.com/theiostream/Libhide/blob/1f7b2bbebc9df68bb781406f881eb28eac270989/library/Makefile) commit, which got me started on understanding how to compile tweaks with clang

@Siguza, for writing ./bin/tbdump, the tool used to symbolicate libraries that can be compiled for this.

@sbinger, for patiently helping me add arm64e support to tbdump (turns out its easy when you know what you're doing :))

@theos, and the badass team there, who created a good amount of the resources this project depends on. 
