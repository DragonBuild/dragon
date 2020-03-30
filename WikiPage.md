## Overview

DragonBuild consists of 2 main components: 
* A packaging system
* A ninja buildfile generator

It uses Theos components for logos processing, but does not require an existing theos installation.

## Setup

### Prerequisites 

Requires `ninja`, `perl`, and `python3`

python3 requires modules `pyyaml`. 

### Installation 

`git clone https://github.com/DragonBuild/DragonBuild.git`

Add the following to your shell's profile

`export DRAGONBUILD=path/to/dragonbuild`
`alias dragon=$DRAGONBUILD/dragon`

Optionally, you can set an IP or name to install to via `export DRBIP="iphonename"` or `export DRBIP=192.168.your.ip`

## Usage

Dragon projects are configured via a single DragonMake file, regardless of how many subprojects you have. 

You can specify subprojects and their information here. This allows for compiling slices in parallel easily, along with keeping things much more organized. 

### DragonMake Syntax

DragonMake follows fairly standard YAML syntax, with a singular escape character, `$`. 

For single line variables, you can use bash syntax to evaluate a command with `$$(command args)`

A single `$` denotes a ninja variable. For using bash syntax in variables, one can use `$$` to represent a `$` . For example, one could use `$$PWD` to get the value of an environment variable in a command. 

Using the below items will parse output through xargs and add entries to the list the item is in:
  `$wildcard("directory", "*.extension")` will find all files in a specific directory. 

  `$eval("bash command")` is also provided, in the event more complex manipulation is needed. 


### Example Project

### DragonMake Format

This should serve as a guideline for how a project should be laid out. You can declare as many projects as you want, it's all going to be crammed into the same deb. 

```yaml
---
## This represents the overall project name. 
package_name: Name
install_command: killall -9 SpringBoard

## This represents a Tweak .dylib and .plist. 
Name:
    type: tweak
    ## A list of logos files. See variables section for more info. 
    logos_files:
        - $wildcard("./", "*.xm")
    ## A list, excluding logos files, of files to compile. See variables section for more info. 
    files:
        - $eval("ls ./*.m")
    ## Min ios
    targetios: 11.0
    ## List of archs we want to build for
    archs:
        - arm64
        - arm64e 
## Now for prefs!
NamePrefs:
    ## Specify the directory, since it's a subproject
    dir: nameprefs
    ## Tell dragon that it's a bundle
    type: bundle
    ## You can specify files from anywhere in your tweak, or use directory specific wildcards
    files:
        - nameprefs/BlahRootListController.m
        - nameprefs/ACellYouUse.m
        - SomeFileFromYourMainTweak.m
    archs:
        - arm64
        - arm64e
    ## Specify that we need the prefs framework for this bundle
    frameworks:
        - Preferences
    ## Required code for preferences
    ## The defaults assume that your bundles are for prefs. 
    ## You can override install location and omit stage to make a regular bundle
    stage: 
        - mkdir -p .dragon/_/Library/PreferenceLoader/Preferences/
        - cp entry.plist .dragon/_/Library/PreferenceLoader/Preferences/$name.plist
## If you have a tweak subproject that, for example, hooks another process, you can compile it into the same deb
## This is the minimal amount of info you can provide and have your project compile. 
SomeOtherTweak:
    dir: othertweak
    type: tweak
    logos_files:
        - othertweak/Tweak.xm    
```


### DragonMake Variables

Please pay attention to the provided example to understand how these should be laid out in a file. 

| Name | Type | Description | Default |
| ---- | ---- | ----------- | ------- |
| `project_name` | str | Name of the whole project | N/A |
| `install_command` | str | Command to run on device after install | `killall -9 SpringBoard` |
| `name` | str | Name of the item being build. Specified as `yourNameHere:` with the rest of the item specific variables below | N/A |
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
| `installLocation` | str | override variable for bundles/libraries to allow specifying install location | '' |
| `frameworkSearchDirs` | list | Framework Search Dirs. Changing this variable overrides defaults. | ['$sysroot/System/Library/Frameworks', '$sysroot/System/Library/PrivateFrameworks', '$dragondir/frameworks'] |
| `additionalFrameworkSearchDirs` | list | Allows adding framework search dirs without overwriting old ones. | [] |
| `librarySearchDirs` | list | Library search dirs. Just like the framework search | ['$dragondir/lib', '.'] |
| `additionalLibarySearchDirs` | list | Add to lib search without overwriting | [] | 

Yaml parsing is done via python3.

## DragonBuild Command Line Arguments

All of these can be combined and ran at the same time, if needed.

### Building and Installing your Tweak

All of these arguments can be specified using only the first character (`dragon c b i` for example)

`dragon build` to build (`dragon make` also works)

`dragon install` to install.

`dragon do` combines both of these. 

`dragon release` loads `DragonRelease` after loading `DragonMake`, allows for setting variables specific to release builds. 

`dragon clean` performs a clean rebuild of the entire project and subprojects. 

### Generating compile commands for clangd or other tools

`dragon export`
