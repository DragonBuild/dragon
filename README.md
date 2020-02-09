# DragonBuild
Much faster ninja-based tweak compiler

DragonBuild serves as a fairly simple Ninja config generator, and as a packaging and remote installation tool

DragonBuild currently requires an existing Theos implementation. This will eventually be written out. Currently it will detect your installation via environment variables, so you shouldn't need to worry too much about this :)

DragonBuild uses logos.pl from Theos. You will need to import headers that theos auto-imports yourself. That will likely not change, as it's good practice to do so. 

## Notes

* This was built for MacOS. It needs a lot of work and a lot less hard-coding to work on linux. We'll get there, I promise :)

## Basic Usage

`dragon [gen] [build] [clean] [install]`

`dragon gen` Generate the ninja build file

`dragon build` Build the project

`dragon clean` Force a rebuild even when no changes are detected

`dragon install` Install the project to the device located at `$DRAGONDEVICEIP`

## Setting your project up for DragonBuild

### Creating a DragonMake File

DragonBuild uses DragonMake files as a stand-in replacement for Makefiles. 

|   |   |   |
|---|---|---|
|   |   |   |

Example DragonMake files for a Tweak and a SubTweak can be found in ./ExampleProject

### Generating the build script

This is crucial. Whenever your DragonMake file is updated (or you pull upstream changes from DragonBuild), you need to run `dragon gen` (`dragon g`, if you're lazy)

You only need to do this when the DragonMake file is updated. 

### Building and installing your Tweak

`dragon build` to build (`dragon make` and `dragon b` also work)

`dragon install` to install (`dragon i` also works)

### Forcing a rebuild

DragonBuild will hash the contents of your tweak directory and only rebuild whenever it detects a change. If you want to force a rebuild despite having no changes, append `clean` to your command. 

## Installing DragonBuild

Choose the directory to install DragonBuild in. cd to it, then:

```bash
git clone https://github.com/KritantaDev/DragonBuild.git
```

Then, add the following to your ~/.bash_profile (or whatever you use)
export DRAGONBUILD=path/for/DragonBuild
alias dragon=$DRAGONBUILD/dragon
