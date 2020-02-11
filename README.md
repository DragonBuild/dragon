# DragonBuild
Much faster ninja-based tweak compiler

### This is in early stages. If you aren't familiar with clang, ldid, dysm, and similar tools, this projects is not currently something you want to use. 

DragonBuild currently requires an existing Theos implementation. This will eventually be written out. Currently it will detect your installation via environment variables, so you shouldn't need to worry too much about this :)

DragonBuild uses logos.pl from Theos. You will need to import headers that theos auto-imports yourself. That will likely not change, as it's good practice to do so. 

## Table of Contents

- [DragonBuild](#dragonbuild)
  * [Notes](#notes)
  * [Basic Usage](#basic-usage)
  * [Installing DragonBuild](#installing-dragonbuild)
  * [Setting your project up for DragonBuild](#setting-your-project-up-for-dragonbuild)
    + [Creating a DragonMake File](#creating-a-dragonmake-file)
    + [Generating the build script](#generating-the-build-script)
    + [Building and installing your Tweak](#building-and-installing-your-tweak)
    + [Forcing a rebuild](#forcing-a-rebuild)
  * [Under the Hood](#under-the-hood)
    + [Ninja Build file gen Proccess](#ninja-build-file-gen-proccess)

## Notes

* This was built for MacOS. It needs a lot of work and a lot less hard-coding to work on linux. We'll get there, I promise :)

## Basic Usage

`dragon [gen] [build] [clean] [install]`

`dragon gen` Generate the ninja build file

`dragon build` Build the project

`dragon clean` Force a rebuild even when no changes are detected

`dragon install` Install the project to the device located at `$DRAGONDEVICEIP`

# Installing DragonBuild

`brew install ninja`

Choose the directory to install DragonBuild in. cd to it, then:

```bash
git clone https://github.com/KritantaDev/DragonBuild.git
```

Then, add the following to your ~/.bash_profile (or whatever you use)  
`export DRAGONBUILD=path/for/DragonBuild`  
`alias dragon=$DRAGONBUILD/dragon`  

DragonBuild currently requires a Theos installation at $THEOS

## Setting your project up for DragonBuild

### Creating a DragonMake File

DragonBuild uses DragonMake files as a stand-in replacement for Makefiles. 

|  Name  | Possible Values | Description  | 
|---|---|---|
|  TWEAK_NAME  |  * | Name of the tweak. Should match your tweak's plist name |
| TWEAK_TYPE |  Tweak, Prefs, SubTweak, Library  | The type of file to build. SubTweak is a tweak to be packaged with the tweak in its superdirectory |
| LOGOS_FILE |  *.x/*.xm  | A file that $THEOS/logos.pl should preprocess. If you have an .xm file put it here |  
| ARCHS | arm7 / arm64 / arm64e | Typical ARCHS stuff you're used to with THEOS | 
| MINIOS | *.* | e.g. 10.0; Target iOS Version |  
| CFLAGS | * | Flags you wish to pass to clang |  
|  TWEAK_FILES  |  *.m/*.mm |  Files to be compiled with your tweak. Anything compilable goes here. Bash syntax is supported |
|  INSTALL_CMD  |  * |  What should be executed over ssh after installing the package |
| LIBS | * | Libraries to link. objc and objc++ are automatically included. |
| FRAMEWORKS | * | Frameworks to compile against. CoreFoundation, Foundation, UIKit, CoreGraphics, and QuartzCore are included by default, along with Preferences, if TWEAK_TYPE is "Prefs" |
| SUBPROJECTS | * | Folder name of Subprojects (prefs, subtweaks, etc) 

Example DragonMake files for a Tweak and a SubTweak can be found in ./ExampleProject

### Generating the build script

This is crucial. Whenever your DragonMake file is updated (or you pull upstream changes from DragonBuild), you need to run `dragon gen` (`dragon g`, if you're lazy)

You only need to do this when the DragonMake file is updated. 

### Building and installing your Tweak

`dragon build` to build (`dragon make` and `dragon b` also work)

`dragon install` to install (`dragon i` also works)

### Forcing a rebuild

DragonBuild will hash the contents of your tweak directory and only rebuild whenever it detects a change. If you want to force a rebuild despite having no changes, append `clean` to your command. 

# Under the Hood

DragonBuild stemmed from my attempt (purely out of boredom, in all honesty) to compile a tweak using a build.ninja file. There was absolutely no documentation on doing so whatsoever, since everyone seems to use GNU Make + Theos for building since iOS 4>. After getting a tweak running, I decided to try and create a Theos replacement/augmentation that generates ninja files and builds from those. 

## Ninja Build file Generator

Currently, DragonBuild uses an incredibly elementary method of template build.ninja files and `sed` macros to fill these out. The "DragonMake" file acts as a bash source script and defines some variables we first escape, and then pass to sed. 

Once we have a ninja file, we're set. You can compile a dylib now using `ninja`. The generated ninja file will also sign it. 

This isn't quite enough for a complete package though; we still need to copy over our .plist, control file, subprojects, and such into a directory structure. We then use dpkg-deb to build it, and scp to install. ez pz. 

Currently, ninja handles compiling, linking, and signing. Ideally, ninja will handle everything. ninja allows bash commands, so it is only limited by its generator. 

I hope to see the complexity of DragonBuild's ninja generator increase, and the complexity of the rest of DragonBuild decrease, as ninja is much better suited to most of this. 

## Ninja Build files

I am forever indebted to [this specific commit](https://github.com/theiostream/Libhide/blob/1f7b2bbebc9df68bb781406f881eb28eac270989/library/Makefile)
 of this specific project. 
 
Having had no experience working without theos before hopping into this, and with online documentation essentially not existing (you need to know what you're doing to find out how to do what you're doing,) this makefile was enough for me to be able to get a working build.ninja

A build.ninja file has quite similar syntax to this raw makefile. As a matter of fact, I'd imagine this file would compile very very quickly even with gnu make. At the end of the day, if you were able to cut it down to the basics, a final theos makefile for a project might look similar to this. 

One place where dragon cuts down insanely on build times is static generation. Theos (someone from @theos please clarify this, i'm probably wrong) takes your makefile, adds in its own premade makefiles, and finally compiles using gnu make. 

Dragon, on the other hand, takes advantage of static generation. You give it a DragonMake file, it generates the final output in .dragon/ninja/build.ninja, and keeps it there till regenerated. Generation is done using bash substitution of basic variables provided in DragonMake, and is quite fast, since it takes advantage of premade template files. 

The generated build.ninja has instructions to compile every one of the files it was directed to compile in the DragonMake, and uses a similar system to GNU Make in that it will hash files and only rebuild if needed. It is very good at doing this quickly. A no-op build of a project containing two subprojects takes 2s. The same no-op takes 14s with `make package -j 16`. 

As my experience with generators and ninja increases, I'm confident I can bring these times down even further. 

