# Building a tweak without packaging tools

This is good practice. Understanding how your tweak is actually built can make working with clangd, xcode, etc so much easier. 

This guide details how to compile a tweak into a .deb without using theos, dragonbuild, GNU Make, ninja, or anything else like that.

You'll need: 
* A Theos install, unless you want to manually download `logos.pl` + dependencies, `perl`, and `libsubstrate.dylib`/`libsubstrate.tbd`.
* `dpkg` (you need the `dpkg-deb` command)
* An iOS Toolchain
* An SDK
* A `Tweak.xm`, `Tweak.plist`, and `control` file.

## Logos Preprocessing

You need logos.pl to process logos. There is no way around this if your tweak uses logos. While it feels cool to write a tweak without logos, I'd advise against making such a thing part of your workflow. In most situations it's a waste of your very valuable time. 

Convert .xm or .x files to .m or .mm like so:

`$THEOS/bin/logos.pl [input] > [output]`

If it's a .x file, input should be `Tweak.x` and output `Tweak.x.m`.

If it's a .xm file, input should be `Tweak.xm` and output `Tweak.xm.mm`. 

The output file name can be anything you want, but you should try to make the original file name clear. 

## Compiling with clang

In theory, it's pretty simple! But there's quite a bit that goes into it. 

I'm going to provide a finished command, and then go through each flag and what it detirmines.

### Final Command

`clang++ -arch armv7 -arch arm64 -arch arm64e -fobjc-arc -F/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk/System/Library/Frameworks -miphoneos-version-min=13.0 -isysroot /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk -DTARGET_IPHONE=1 -Wall -O2 -c -o Tweak.xm.o Tweak.xm.mm `

#### Flags explained

`clang++` is a compiler in the llvm project capable of compiling c++ code

`-arch <archname>` specifies we are compiling for a specific arch. In this example, we're going to lazily compile all of them at once. 

`-fobjc-arc` tells clang that we're using Automated Reference Counting. 

`-F<directory>` tells clang where to look for Frameworks. This is crucial. 

`-miphoneos-version-min=13.0` specifies our target iOS version.

`-isysroot <directory>` Tells clang where our sdk root directory is. 

`-DTARGET_IPHONE=1` tells clang we're building for iphone (more info?)

`-Wall` tells clang to enable all of its warning modules. You should keep this on, warnings are annoying, but unexpected behavior is much more so. 

`-O2` (Letter 'O') tells the compiler to optimize at level 2. This can be set to -O0 (Letter 'O', number 'Zero') to disable optimization if it causes problems.

`-c` Tells clang to compile, but not yet link the file. 

`-o Tweak.xm.o` specifies the output file

Any other text in the command is evaluated as an input file. So, in this case, `Tweak.xm.mm`. 

**Repeat this process for all files that need compiled (.m, other .xm files, etc)**

## Linking

Finally, we're going to get something you can actually run on your device. 

### Final Command

`clang++ -arch armv7 -arch arm64 -arch arm64e -fobjc-arc -F/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk/System/Library/Frameworks -miphoneos-version-min=13.0 -isysroot /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk -DTARGET_IPHONE=1 -Wall -O2 -fcolor-diagnostics -framework CoreFoundation -framework Foundation -framework UIKit -framework CoreGraphics -framework QuartzCore -framework CoreImage -framework AudioToolbox -lsubstrate -lobjc -lc++ -dynamiclib -ggdb -lsystem.b -Xlinker -segalign -Xlinker 4000 -L$THEOS/lib -o Tweak.dylib Tweak.xm.o`

#### New flags explained 

`-framework <Framework Name>` tells our linker we're going to be linking against a specific framework

`-l<library name>` specifies a library we want to link against. We link against libsubstrate, libobjc, libc++ and libsystem.b, 

`-L<directory>` specifies a library search directory.

`-dynamiclib` specifies we're compiling a linking dynamically 

`-ggdb` tells our linker to produce debugging information for ggdb.

`-Xlinker` passes arguments to the linker that clang doesn't recognize. We pass the below flag to our mach-o linker.

`-segalign 4000` aligns our segments at 0x4000. See https://www.manpagez.com/man/1/ld/osx-10.4.php if you're curios as to why. 

At this point, we now have a dylib!

## Generating Debug Symbols

`dsymutil Tweak.dylib`

wew, that was hard

## Code Signing

`ldid -S Tweak.dylib`

## Packaging the tweak

### Making The Directory Structure

Now we're going to create a directory structure, so dpkg-deb can work with it. 

`mkdir -p .packaging/Library/MobileSubstrate/DynamicLibraries`

the `-p` flag tells mkdir to recursively create subdirectories, so we dont have to manually create each folder.

Now, make a DEBIAN folder, so dpkg can process our package.

`mkdir .packaging/DEBIAN`

### Moving files into place

This will let Substrate load your tweak

`cp Tweak.dylib .packaging/Library/MobileSubstrate/DynamicLibraries/Tweak.dylib`
`cp Tweak.plist .packaging/Library/MobileSubstrate/DynamicLibraries/Tweak.plist`

dpkg also needs packaging info:

`cp control .packaging/DEBIAN/control`

### Making the deb

`dpkg-deb --build -Zgzip -z9 .packaging .`

And you're done!

---

Voilà! You've got a package. This is the basics of what goes on when you compile a project using theos/other packagers. 