# DragonBuild

## Summary

DragonBuild is a python and bash based theos alternative.

It uses configuration files instead of a confusing maze of Makefiles, and an entire project is configured from a single `DragonMake` file.

**It can also compile a majority of theos projects without *any* extra work needed.**

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

# Installing DragonBuild

Paste the following into your terminal, enter the sudo pass, and follow along with the script. 

`bash <(curl -s https://raw.githubusercontent.com/DragonBuild/installer/master/install.sh)`

## Linux/WSL

Place a toolchain in the `toolchains/` folder and, assuming it's the sbingner toolchain, it will automatically be used. 

# Setting up your project for DragonBuild

DragonBuild is capable of building most Theos projects instantly. No DragonMake file needed. 

It has an insanely powerful "DragonMake" system of it's own though, and it's fairly easy to work with. 


## DragonMake Syntax

DragonMake follows yaml syntax. Strings dont typically need to be wrapped in `""`, although wildcards do.

For str variables, you can use bash syntax to evaluate a command with `$$(command args)`

You can also refer to environment variables with `$$VARNAME`

Wildcards:  
  `"*.[extension]"` is the syntax. `**` and other globbing rules are applied. Type `ls <your wildcard here` to get an idea. 
  `"**/*.m"` for example will find all .m files in the current directory *and subdirectories*

## DragonMake Format

This should serve as a guideline for how a project should be laid out. You can declare as many projects as you want, it's all going to be crammed into the same deb. 

"ModuleName" represents a module, here. Typically this is "TweakName" or "TweakNamePrefs", or something along those lines.

```yaml
---
# This represents the overall project name. 
name: TweakName
icmd: sbreload

all:
  targetvers: 11.0
  archs:
    - arm64
    - arm64e

# This represents a Tweak .dylib and .plist. 
ModuleName:
    type: tweak
    # A list of logos files. See variables section for more info. 
    logos_files:
        - "*.xm"
    # A list, excluding logos files, of files to compile. See variables section for more info. 
    # Min ios
    # List of archs we want to build for
# Now for prefs!
AnotherModuleName:
    # Specify the directory, since it's a subproject
    dir: nameprefs
    # Tell dragon that it's a bundle
    type: prefs
    # You can specify files from anywhere in your tweak, or use directory specific wildcards
    objc_files:
        - BlahRootListController.m
        - ACellYouUse.m
        - ../SomeFileFromYourMainTweak.m
# If you have a tweak subproject that, for example, hooks another process, you can compile it into the same deb
# This is the minimal amount of info you can provide and have your project compile. 
ASubModuleName:
    dir: othertweak
    type: tweak
    files:
        - othertweak/Tweak.xm    
```

## DragonMake Variables

Top Level Variables

| Name | Type | Description | Default |
| ---- | ---- | ----------- | ------- |
| `name` | str | Name of the whole project | N/A |
| `icmd` | str | Command to run on device after install | `killall -9 SpringBoard` |
| `all` | dict | Variables here will be applied to all modules and can be overridden individually |  |

Module Variables

| Name | Type | Description | Default |
| ---- | ---- | ----------- | ------- |
| `type` | str | Type of project being built. See [Project_Types](#Project_Types) | N/A |
| `files` | list | List of files to be compiled. These will be sorted into proper groups by extension. | [] |
| `logos_files` | list | List of files that require the logos preprocessor | [] |
| `c_files` | list | List of files to build as .c source | [] |
| `cxx_files` | list | List of files to build as .cpp source | [] |
| `objc_files` | list | List of files to build as .m source | [] |
| `objcxx_files` | list | List of files to build as .mm source | [] |
| `target` | str | OS being targeted. By default, iOS. You can define your own, too; See [Targets](#Targets) | [] | 
| `targetvers` | str | iOS Version being targeted. | [] | 
| `archs` | list | Architectures to compile for | [] |
| `sysroot` | str | Root of the Patched SDK to build with | $DRAGONBUILD/sdks/iPhoneOS.sdk |
| `cc` | str | c/c++ compiler to use | clang |
| `cxx` | str | c/c++ compiler to use | clang++ |
| `ld` | str | linker to use | clang/clang++ |
| `lipo` | str | lipo tool to use | lipo |
| `codesign` | str | ldid binary to sign with | ldid |
| `dsym` | str | dsymutil binary to symbolicate with | dsymutil |
| `plutil` | str | dsymutil binary to symbolicate with | plutil |
| `swift` | str | dsymutil binary to symbolicate with | swift |
| `logos` | str | logos.pl file to use for preprocessing | `$DRAGONBUILD/bin/logos.pl` | 
| `stage` | str/list | Console command(s) to run before after build and before packaging | '' |
| `arc` | BOOL | Should we use -fobjc-arc | `Yes` |
| `warnings` | str | Warnings flag | -Wall |
| `optim` | str | Optimization level. Higher levels can break obfuscators. | 0 |
| `debug` | str | debug flags | -fcolor-diagnostics |
| `libs` | list | List of libraries to link the binary against | '' |
| `frameworks` | list | List of Frameworks to compile with | ['CoreFoundation', 'Foundation', 'UIKit', 'CoreGraphics', 'QuartzCore', 'CoreImage', 'AudioToolbox'] |
| `cflags` | str | additional flags to pass to clang and the linker. Will be applied after everything else. | '' |
| `ldflags` | str | additional flags to pass to the linker. Applied after cflags. | '' |
| `entflag` | str | custom flag for codesign util | '-S' |
| `entfile` | str | Applied directly after entflag. Typically for ldid, an entitlement plist. | '' |
| `install_location` | str | override variable for bundles/libraries to allow specifying install location | '' |
| `fw_dirs` | list | Framework Search Dirs. Changing this variable overrides defaults. | ['$sysroot/System/Library/Frameworks', '$sysroot/System/Library/PrivateFrameworks', '$dragondir/frameworks'] |
| `additional_fw_dirs` | list | Allows adding framework search dirs without overwriting old ones. | [] |
| `lib_dirs` | list | Library search dirs. Just like the framework search | ['$dragondir/lib', '.'] |
| `additional_lib_dirs` | list | Add to lib search without overwriting | [] | 

You can reference any of these variables in a variable *below* it (really, avoid doing this please) using `$var`

# DragonBuild Commands

All (most) of these can be combined and ran at the same time, if needed.

`dragon update` will update your dragonbuild installation to the latest version.

`dragon -h` outputs the following:

```yaml

DragonBuild v1.0 -=-=-
  usage: dragon [commands]

Building -=-=-
  d|do - Build and Install
  c|clean - recompile, link, and package your project
  b|build|make - compile, link, and package your project
  r|release - Load DragonRelease file over the DragonMake one
  rl|relink - Re-link the package regardless of changes

Installation -=-=-
  s|device - Set build device IP/Port
  i|install - Install to build device
  rs|respring - Respring the current build device
  dr|devicerun - Run anything after this flag on device

Tools -=-=-
  exp|export - Tell ninja to create a compile_commands.json
  f|flutter - Build with flutter before doing anything else
  ch|checkra1n - Open Checkra1n GUI
  chc|checkra1ncli - Open Checkra1n CLI

Debugging -=-=-
  vn - Print clang/ld/etc. commands and flags
  vd - echo every bash command in the main dragon file
  vg - DragonGen verbositiy.
  norm - Doesn't delete build.ninja after building.
  debug - Enable all debug flags

-=-=-

DragonBuild v1.0.0 - by kritanta
```

# Endgame for this project

The ultimate hope for this project is that the major alternative, theos, sees the same improvements this project has. It's unlikely it'll ever become as popular as theos, but the hope is that it can instead inspire the maintainers there into "catching up."


# Helpful links

[sbinger's arm64e toolchain](https://github.com/sbingner/llvm-project/releases/tag/v10.0.0-1)

# Credits

@Siguza, for writing ./bin/tbdump, the tool used to symbolicate libraries that can be compiled for this.

@sbinger, for patiently helping me add arm64e support to tbdump (turns out its easy when you know what you're doing :))

@theos, and the badass team there, who created a good amount of the resources this project depends on, and who have all been a major help in guiding the way for this project. 
