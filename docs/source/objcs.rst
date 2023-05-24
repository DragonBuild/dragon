Objective-CS and the llvm-objcs Toolchin
---------------------

Dragon ships with builtin integration for the llvm-objcs toolchain and the Objective-CS hooking language.

It provides wrappers, utilities, and commands that help set up the toolchain and get autocomplete, editor support, etc working with clangd.

A companion extension for vscode exists at [LINKHERE]

Adding support to a project should be fairly drop-in. Projects using Objective-CS can still use logos, they will just need
to be in separate files for autocomplete, etc to work.

Objective-CS
*********************

Objective-CS is an extension of Objective-C designed to provide easier integration with hooking APIs than working in purely Objective-C.

By building our language directly within llvm as opposed to via a preprocessor (logos), we gain access to a large amount of
existing tooling that already supports LLVM.

This allows autocomplete, inline error messages/help/suggestions, and the myriad other clangd features to work within
Objective-CS files.


File Extension
=====================

Currently, Objective-CS just adds support directly into Objective-C code, so you use the same .m or .mm extension as regular
objc. Eventually it may be gated or aliased to .mx/.mmx.

Basic Syntax
=====================

The following code block demos the full current featureset of Objective-CS

.. code-block:: objc

  // Predeclaring the interface for what we're hoooking isn't required,
  // but it allows us to:
  //    autocomplete hook selectors
  //    access ivars of the class we're hooking
  //    declare new methods we want to add
  @interface SBIconView : UIView
  {
      BOOL _allowsLabelArea; // Declare ivars we want to "hook" (access) here
      CGFloat _iconImageAlpha; // This replaces the need for swapping to ObjC++ and wrangling the MSHookIvar API.
  }

  -(void)configureForLabelAllowed:(BOOL)allowed;

  @new
  -(void)myAwesomeNewInstanceMethod;

  @end

  // If you've already imported a header for a given class (from a patched SDK that has proper headers),
  // you can instead declare a category ( `@interface SBIconView ()` ) and still utilize these features.
  // This accomplishes the same thing in terms of
  //    applying new methods, accessing ivars that maybe didn't exist in the header you imported, etc.

  // --

  @group iOS13Plus
  @hook SBIconView

  -(void)myAwesomeNewInstanceMethod
  {
    NSLog(@"Hello from Objective-CS!");
  }

  -(void)configureForLabelAllowed:(BOOL)allowed
  {
      @orig(NO);
      _allowsLabelArea = NO;
      _iconImageAlpha = 0.5;
      [self myAwesomeNewInstanceMethod];
  }

  @end
  @end

  #ifndef kCFCoreFoundationVersionNumber_iOS_13_0
  #define kCFCoreFoundationVersionNumber_iOS_13_0 1665.15
  #endif

  // This is a manually declared constructor. This is not required if you are not using groups.
  // You *will* need to use one if you are using groups, as all groups must be initialized for their hooks to be applied.
  // _eventually,_ something like @ctor (analogous to logos' %ctor) may be added.
  __attribute__((constructor))
  void initFunc(void)
  {
    if (kCFCoreFoundationVersionNumber >= kCFCoreFoundationVersionNumber_iOS_13_0){
      @init(iOS13Plus);
      // initialize multiple groups: @init(myGroup, mySecondGroup, andSoOn);
    }
  }


Future
=====================

Plans exist to add support for:
* `@hookf(FunctionName)`
* `@ctor{}`
* `@subclass`

This is a hobby project with one developer, so there is no timeframe on these plans :)

llvm-objcs
*********************

LLVM-objcs is a fork of Apple's LLVM that supports compiling Objective-CS code.

It aims to support the same featureset as apple-llvm, however modules have been an undocumented pain to compile support for,
so the currently distributed binaries do not yet support them (i.e. `@import UIKit;`. Just import headers normally for now).

Builds are available in arm64 and x86_64 form for macOS, <upcoming> linux, and iOS (iOS is arm64 only, silly)</upcoming>

Installing
=====================

`dragon lo setup` will download and install the appropriate toolchain for your system.

It will also be automatically installed if a DragonMake project declares it as required, and it isn't already installed.

Manually
^^^^^^^^^^^^^^^^^^^^^

Download or build the appropriate toolchain and extract/install it in `~/.dragon/llvm-objcs`. The directory structure
should be as follows:

.. code-block:: bash

  serket@prospit ~ % tree ~/.dragon/llvm-objcs -L 1
  /Users/serket/.dragon/llvm-objcs
  ├── bin
  ├── include
  ├── lib
  ├── libexec
  └── share

After that you're good to go.

Future
=====================

As this toolchain was built off of llvm-17, it does not support arm64e libraries injected into arm64e processes for pre-iOS 14 devices.

This is an issue with all toolchains post llvm-12, and workarounds are being looked into.
