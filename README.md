# DragonBuild
DragonBuild, simply explained, is a fast ninja-based theos alternative. 

Specifically, it's a ninja build file generator and packaging system for substrate extensions and other common packages distributed in the jailbreak community. 

It's aimed at both speed and configurability. Every single factor of it is configurable from a singular file. 

## Table of Contents

- [DragonBuild](#dragonbuild)
  * [Installing DragonBuild](#installing-dragonbuild)
  * [Setting up your Project](#setting-up-your-project-for-dragonbuild)
    + [DragonMake Syntax](#dragonmake-syntax)
    + [DragonMake Format](#dragonmake-format)
    + [DragonMake Variables](#dragonmake-variables)
  * [DragonBuild Commands](#dragonbuild-commands)
    + [Building and Installing](#building-and-installing-your-tweak)
    + [Clean Rebuilds](#forcing-a-rebuild)
    + [clangd Helper](#generating-compile-commands-for-clangd-or-other-tools)
  * [Helpful Links](#helpful-links)

## Notes

* This was built for MacOS, although I've done a little bit of testing on Linux. If it does not detect `ldid` in the path, it will look in `$DRAGONBUILD/toolchain/bin/` for a toolchain. I would advise properly installing  to your path, as this is somewhat hacked in at the moment. 

# Installing DragonBuild

`git clone https://github.com/DragonBuild/DragonBuild.git`

Add the following to your bash profile / .zshrc:

`export DRAGONBUILD=path/to/dragonbuild`
`alias dragon=$DRAGONBUILD/dragon`


You can set an IP or name to install to via `export DRBIP="iphonename"` or `export DRBIP=192.168.your.ip`

This will allow you to use `dragon i` to install packages to your device. 

# Setting up your project for DragonBuild

Dragon projects are configured via a single DragonMake file, regardless of how many subprojects you have. 

You can specify subprojects and their information here. This allows for compiling slices in parallel, along with keeping things much more organized. 

## DragonMake Syntax

DragonMake follows fairly standard YAML syntax, with a singular escape character, `$`. 

For single line variables, you can use bash syntax to evaluate a command with `$$(command args)`

A single `$` denotes a ninja variable. You should not need to worry about these. A `$$` is evaluated to `$` and subsequent information treated in bash. For example, one could use `$$DRAGONBUILD` to get the location of the dragon directory in a variable. 

For files specifically:
  `$wildcard("directory", "*.extension")` will find all files in a specific directory

  `$eval("bash command")` is also provided, in the event more complex manipulation is needed. 

## DragonMake Format

This should serve as a guideline for how a project should be laid out. You can declare as many projects as you want, it's all going to be crammed into the same deb. 

"Name" represents the name of your tweak. Please change "Name" to the name of the item you are building. 

`$eval` and `$wildcard` commands are executed in the directory specified (`.` if none has been specified).

```yaml
---
# This represents the overall project name. 
package_name: TweakName
install_command: killall -9 SpringBoard

# This represents a Tweak .dylib and .plist. 
Name:
    type: tweak
    # A list of logos files. See variables section for more info. 
    logos_files:
        - $wildcard("./", "*.xm")
    # A list, excluding logos files, of files to compile. See variables section for more info. 
    files:
        - $eval("ls ./*.m")
    # Min ios
    targetios: 11.0
    # List of archs we want to build for
    archs:
        - arm64
        - arm64e 
# Now for prefs!
NamePrefs:
    # Specify the directory, since it's a subproject
    dir: nameprefs
    # Tell dragon that it's a bundle
    type: bundle
    # You can specify files from anywhere in your tweak, or use directory specific wildcards
    files:
        - BlahRootListController.m
        - ACellYouUse.m
        - ../SomeFileFromYourMainTweak.m
    archs:
        - arm64
        - arm64e
    # Specify that we need the prefs framework for this bundle
    frameworks:
        - Preferences
    # Required code for preferences
    # The defaults assume that your bundles are for prefs. 
    # You can override install location and omit stage to make a regular bundle
    stage: 
        - mkdir -p .dragon/_/Library/PreferenceLoader/Preferences/
        - cp entry.plist .dragon/_/Library/PreferenceLoader/Preferences/$name.plist
# If you have a tweak subproject that, for example, hooks another process, you can compile it into the same deb
# This is the minimal amount of info you can provide and have your project compile. 
SomeOtherTweak:
    dir: othertweak
    type: tweak
    logos_files:
        - othertweak/Tweak.xm    
```

## DragonMake Variables

Please pay attention to how these variables should be laid out

| Name | Type | Description | Default |
| ---- | ---- | ----------- | ------- |
| `project_name` | str | Name of the whole project | N/A |
| `install_command` | str | Command to run on device after install | `killall -9 SpringBoard` |
| `name` | str | Name of the item being build. Specified as `name:` with the rest of the item specific variables below | N/A |
| `type` | str | Type of project being built. One of "tweak"/"bundle"/"library". | N/A |
| `logos_files` | list | List of files that require the logos preprocessor | [] |
| `files` | list | List of files to be compiled, excluding logos files. | [] |
| `targetios` | str | Minimum iOS Version Required | [] | 
| `archs` | list | Architechtures to compile for | [] |
| `sysroot` | str | Root of the Patched SDK to build with | $DRAGONBUILD/sdks/iPhoneOS.sdk |
| `cc` | str | c/c++ compiler to use | clang+ |
| `ld` | str | linker to use | clang+ |
| `ldid` | str | ldid binary to sign with | ldid |
| `dsym` | str | dsymutil binary to symbolicate with | dsymutil |
| `logos` | str | logos.pl file to use for preprocessing | `$DRAGONBUILD/bin/logos.pl` | 
| `stage` | str/list | Console command(s) to run before after build and before packaging | '' |
| `arc` | str | -fobjc-arc, if enabling so is desired | `-fobjc-arc` |
| `targ` | str | build target | -DTARGET_IPHONE=1 |
| `warnings` | str | Warnings flag | -Wall |
| `optim` | str | Optimzation level. Higher levels can break obfuscators. | 0 |
| `debug` | str | debug flags | -fcolor-diagnostics |
| `libs` | list | List of libraries to link the binary against | '' |
| `frameworks` | list | List of Frameworks to compile with | ['CoreFoundation', 'Foundation', 'UIKit', 'CoreGraphics', 'QuartzCore', 'CoreImage', 'AudioToolbox'] |
| `cflags` | str | additional flags to pass to clang and the linker | '' |
| `ldflags` | str | additional flags to pass to the linker | '' |
| `ldidflags` | str | custom option for ldid | '-S' |
| `install_location` | str | override variable for bundles/libraries to allow specifying install location | '' |
| `framework_search_dirs` | list | Framework Search Dirs. Changing this variable overrides defaults. | ['$sysroot/System/Library/Frameworks', '$sysroot/System/Library/PrivateFrameworks', '$dragondir/frameworks'] |
| `additional_framework_search_dirs` | list | Allows adding framework search dirs without overwriting old ones. | [] |
| `library_search_dirs` | list | Library search dirs. Just like the framework search | ['$dragondir/lib', '.'] |
| `additional_library_search_dirs` | list | Add to lib search without overwriting | [] | 

Yaml parsing is done via python3, and I'm not strict about arbitrary code execution. Go wild, its your machine. 

# DragonBuild Commands

All of these can be combined and ran at the same time, if needed.

### Building and installing your Tweak

`dragon build` to build (`dragon make` and `dragon b` also work)

`dragon install` to install (`dragon i` also works)

### Forcing a rebuild

Using the `c` or `clean` command will perform a clean regen and rebuild of your project. 

### Generating compile commands for clangd or other tools

`dragon export`

# Helpful links

[sbinger's arm64e toolchain](https://github.com/sbingner/llvm-project/releases/tag/v10.0.0-1)

# Credits

@Siguza, for writing ./bin/tbdump, the tool used to symbolicate libraries that can be compiled for this.

@sbinger, for patiently helping me add arm64e support to tbdump (turns out its easy when you know what you're doing :))

@theos, and the badass team there, who created a good amount of the resources this project depends on, and who have all been a major help in guiding the way for this project. 
