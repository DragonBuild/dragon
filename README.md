<p align="center" >
<img src="internal/dragon.svg" alt="Logo" width=200px> 
</p>
<p align="center">
  <strong>
  dragon aims to be a full environment for development and research on Apple devices.
  </strong>
</p>

# Installing dragon

In your terminal:

`bash <(curl -sL dr.krit.me)`

`dragon update` will update dragon to the latest commit. Run this before filing an issue.

---

This readme needs work and doesn't come close to covering the scope of the project.

`dragon -h` includes a list of available supported stable features on the current build.

Reaching out to me on #development on the r/jb discord server is reccomended if you're having issues with anything.

---

# The Build System

dragon supports theos projects alongside it's own, powerful, expandable format.

## Using Makefiles

A good majority of projects built with Theos will build out of the box with dragon.

**If your Theos project fails to build, file an issue with a link to it.** This is insanely helpful when it comes to improving the interpreter. 

## Using DragonMake

DragonMake is a YAML-based format that represents an entire project and all subprojects within a single file.

It was created with the goal of being writable by hand, without the help of a "New Instance Creator". Dragon's NIC is being worked on; It is however, lightly on hold, so as not to encourage new users to leap into this project just yet.

DragonMake can also optionally hold the `control`, `preinst`, `postinst`, etc. file values inside itself instead of requiring manually creating them

### "Modules" and the "Project"

Regardless of folder layout, there are no "subprojects" in dragon. Instead, you have a single "Project", which then has "Modules" (your tweak, your prefs, etc).

This format makes working with complex projects much easier, and keeps things incredibly organized without limiting your freedom.

See the example below to get an idea

### DragonMake Sample

This should serve as a guideline for how a project should be laid out. You can declare as many modules as you want within your project.

"ModuleName" represents a module, here. Typically this is "TweakName" or "TweakNamePrefs", or something along those lines.

```yaml
---
# This represents the overall project name. 
# Everything in here will be built into a .deb package for installation
# Replace TweakName with the name of your project, of course
name: TweakName
icmd: killall -9 SpringBoard
id: com.mycompany.tweakname
version: 1.0.0
author: kritanta
depends: mobilesubstrate, preferenceloader

TweakName:
    type: tweak
    files:
        - "*.xm"
        
# Now for preferences!
TweakNamePrefs:
    dir: nameprefs
    type: prefs
    files:
        - BlahRootListController.m
        - ACellYouUse.m
        - ../SomeFileFromYourMainTweak.m
        
# Subproject example
ASubTweakName:
    dir: othertweak
    type: tweak
    files:
        - Tweak.xm    
```


### DragonMake Syntax

Variables within the DragonMake can be referenced via `$varname`

Environment Variables can be referenced with `$$varname`

You can evaluate a command in a subshell via `$$(command args)`

While these are all great for weird hacks, they're heavily not-reccomended. Run bash logic in the `stage:` section.

Wildcards:  
  `"*.<x>"` is the syntax. `**` and other globbing rules are applied. 
  Type `ls <your wildcard here>` to get an idea. 


## DragonMake Variables

_This section may be partially outdated. See `DragonGen/defaults.yml` for a complete list of current variables (under `Defaults:`)_

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
| `frameworks` | list | List of Frameworks to compile with | _Default frameworks are `type` specific. Defining any will override the defaults._ |
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

## dragon commands

Most of these can be combined, if needed.

`dragon update` will update your dragonbuild installation to the latest version.

`dragon` with no args outputs the following:

```yaml

dragon v1.2 -=-=-
  usage: dragon [commands]

Building -=-=-
  do - Build and Install
  c|clean - clean old build files.
  b|build|make - build and package your project
  r|remote - Build using remote server
  sr|rconf - Setup remote server

Installation -=-=-
  s|device - Set build device IP/Port
  i|install - Install to build device
  sim - Install to the simulator instead of a device
  rs|respring - Respring the current build device
  dr|devicerun - Run anything after this flag on device
  sn|send <file> - Install a .deb to the device

Tools -=-=-
  d|debug [Process Name] - Start a debugging server on device and connect to it (Can be used with the install flag as well)
  exp|export - Tell ninja to create a compile_commands.json
  f|flutter - Build with flutter before doing anything else
  ch|checkra1n - Open Checkra1n GUI
  chc|checkra1ncli - Open Checkra1n CLI

Debugging -=-=-
  vn - Print clang/ld/etc. commands and flags
  vd - echo every bash command in the main dragon file
  vg - DragonGen verbositiy.
  norm - Doesn't delete build.ninja after building.
  ddebug - Enable all debug flags

-=-=-

```


### Configure connected device

`dragon s` (`setup`). This is ran automatically if one isn't yet configured.

When installing to a phone, if passwordless-authentication hasn't been configured, dragon will optionally configure it for you.

#### Installing over USB

Run `dragon s` but leave the "IP" field empty. It will then use iproxy to install the package over usb.

#### Respring connected device

`dragon rs`

#### Run a command on connected device

`dragon dr <command here>` - Anything after `dr` is ran on device.

`dragon dr` with no further arguments will open an ssh session.

### Building on-device

Dragon is available for iOS on https://repo.krit.me/. It can also be installed via CLI like a normal package.

dragon will autodetect if it's running on a phone. 

If so, the `install` flag will install it to the current device and respring it.

[Full List Of Commands](#dragon-commands)



## Project Types

```yml
  app: iOS Application
  application: same as `app`
  tweak: iOS Runtime Extension
  prefs: PreferenceLoader bundle
  bundle: Standard executable bundle
  framework: Obj-C Framework
  resource-bundle: Bundle with no executable compiled.
  stage: Runs the command or list of commands in the `stage:` variable and does nothing else.
  library: Simple dynamic library
  cli: Command line tool
  tool: same as `cli`
  static: Static library
```

# Helpful links

[sbinger's arm64e toolchain](https://github.com/sbingner/llvm-project/releases/tag/v10.0.0-1)
