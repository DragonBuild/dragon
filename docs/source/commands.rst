Commands
---------------------

Running ``dragon`` without any arguments will list available commands, many of which have multiple aliases.

You can combine most commands to do multiple actions with one command.


Packaging Commands
=====================

Creating a new project/module
*********************

``dragon n``, ``dragon new``, ``dragon nic``, ``dragon edit``, or ``dragon create`` will open the Project Editor


Building a package
*********************

``dragon b``, ``dragon build``, or ``dragon make`` builds a package


Building a package for release
^^^^^^^^^^^^^^^^^^^^^

The ``r`` / ``release`` command can be added to the ``build`` command to define "NDEBUG" and undefine "DEBUG" within compiled code.

Passing this flag will also cause the contents of the DragonMake variable ``dbgflags`` to be ignored, and the contents of ``releaseflags`` to be used instead.


Clean Building a package
*********************

``dragon c`` or ``dragon clean`` will clean the 'build cache'

Combine it with the build command to run a clean build (e.g. ``dragon c b``)


Device Commands
=====================

Setting up a device
*********************

``dragon s`` or ``dragon device`` will set up an installation target


Installing a package
*********************

``dragon i`` or ``dragon install`` installs a package

Combine it with the build command, or use ``dragon do`` to build and install a package

Respringing a device
*********************

``dragon rs`` or ``dragon respring`` will respring the current device (i.e. current installation target)


Running a command on the device
*********************
``dragon dr <commands>`` or ``dragon devicerun <commands>`` will execute anything after the command on the current device (i.e. current installation target) [don't use quotes]


Installing any deb on the device
*********************

``dragon sn <file>`` or ``dragon send <file>`` will install a ``.deb`` anywhere on your drive to the current device (i.e. current installation target)


Building and installing to the iOS Simulator
*********************

Adding the ``sim`` command to a set of commands targets the simulator. If added to an ``install`` command, it will install the specified deb to the iOS simulator
