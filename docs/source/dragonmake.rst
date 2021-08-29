The DragonMake Format
---------------------

Intead of splitting up build instructions among a ton of 'Makefile's, dragon build variables are all declared in a single `DragonMake` file at the root of the project.

DragonMake files use YAML syntax.

.. code-block:: YAML 
   
   name: DemoTweak
   id: me.krit.dragondemo
   depends: mobilesubstrate
   architecture: iphoneos-arm
   description: Demo Tweak
   author: krit
   section: Tweaks 

   DemoTweak:
     type: tweak
     filter:
       executables:
         - SpringBoard
     files:
       - DemoTweak.x


The Project 
*********************

The full `DragonMake` represents the "Project", which contains one or more "Modules" (tweaks, prefs, etc).

.. code-block:: YAML 
   
   name: DemoTweak
   id: me.krit.dragondemo
   depends: mobilesubstrate
   architecture: iphoneos-arm
   description: Demo Tweak
   author: krit
   section: Tweaks 

Variables
=====================

.. list-table::
   :widths: 5 1 10

   * - Variable
     - Type
     - Description
   * - name
     - String
     - Name of the project
   * - icmd
     - String
     - (Optional) Command to run after installation on the target device

`control` Variables
=====================

If your project already has a `control` file you don't need to worry about these. 

.. list-table::
   :widths: 5 1 10

   * - Variable
     - Type
     - Description
   * - id
     - String
     - Bundle ID (e.g. me.krit.demotweak) for the Project
   * - author
     - String
     - Author of the project. Current account's username will be used if none is provided
   * - description
     - String
     - Description of the package
   * - version
     - String
     - Version of the project
   * - section
     - String
     - Section to place this tweak in. (e.g. 'Tweaks')
   * - depends
     - String
     - Comma separated list of bundle ids this package depends on
   * - maintainer
     - String
     - (Optional) Maintainer of the project. Will use the value of 'author' if none is provided
   * - provides
     - String
     - (Optional) Comma separated list of bundle ids this package provides


Debian Package Script Variables
=====================

Lists of commands can be specified with `preinst:`, `postinst:`, `prerm:` and/or `postrm:` to create packaging scripts included in the binary.

.. code-block:: YAML 
   
   name: DemoTweak
   id: me.krit.dragondemo
   depends: mobilesubstrate
   architecture: iphoneos-arm
   description: Demo Tweak
   author: krit
   section: Tweaks 
   # This will run on the device after installation
   postinst:
     - echo "Hello from dragon!"

Modules
*********************

Modules in the `DragonMake` represent individual components of your package.

These include things like a Tweak, Preferences, etc.

.. code-block:: YAML 

   DemoTweak:
     type: tweak
     filter:
       executables:
         - SpringBoard
     files:
       - DemoTweak.x


The "Important" Variables
=====================

.. list-table::
   :widths: 5 1 10

   * - Variable
     - Type
     - Description
   * - type
     - String
     - Project type -- see next section
   * - dir
     - String
     - (Optional) Subdirectory the files are located in, if they're in one
   * - files
     - List
     - List of files in the project to be compiled

Types 
^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 5 10

   * - Type
     - Description
   * - app
     - Build an application for jailbroken devices
   * - tweak
     - Build a tweak for jailbroken devices
   * - prefs
     - Build a preference bundle
   * - bundle
     - Build some other type of bundle
   * - resource-bundle
     - Build a bundle containing only resources
   * - framework
     - Build a framework
   * - library
     - Build a library
   * - cli
     - Build a CLI tool/binary
   * - static
     - Build a static library
   * - stage
     - Module containing only a stage variable


Tweak bundle filters 
^^^^^^^^^^^^^^^^^^^^^
Bundle filters tell MobileSubstrate what processes to inject your tweak into.

dragon supports the standard theos format, but allows specifying the values in the `DragonMake`, if you want. 

.. code-block:: YAML 

   DemoTweak:
     type: tweak
     # This bit 
     filter:
       executables:
         - SpringBoard

     files:
       - DemoTweak.x


.. 
   todo: info about files: stuff


Common Module variables
=====================

None of these are required by default, but you may need some of them for various projects.

.. list-table::
   :widths: 5 1 10

   * - Variable
     - Type
     - Description
   * - archs
     - List
     - List of archs to compile for
   * - cflags
     - String/List
     - List (or a space seperated string) with cflags used at compilation time
   * - frameworks
     - List
     - List of frameworks to link against
   * - libs
     - List
     - List of libraries to link against
   * - entfile
     - String
     - File containing entitlements to codesign the module with
   * - include
     - List
     - List of directories to search for headers in
   * - additional_fw_dirs
     - List
     - List of additional directories to search for frameworks in
   * - additional_lib_dirs
     - List
     - List of additional directories to search for libraries in
   * - prefix
     - List
     - List of headers to be imported into ALL files at compilation time
   * - for
     - String
     - Sets the target OS to build for [ios, watchos, host(macos)]
   * - arc
     - Boolean
     - Enable ARC (Default: YES)
   * - sysroot
     - String
     - Specify Directory the SDK is located in
   * - targetvers
     - String
     - Version of the OS to target
   * - macros
     - List
     - List of declaration flags (-D<value>) to add to the compilation flags


Setting Module Defaults
=====================

A special module can be specified with the name `all:`; its variables will be set as the "default" value for all Modules in the project.

If a Module specifies a different value than `all:`, it'll override the one declared in `all:`.

