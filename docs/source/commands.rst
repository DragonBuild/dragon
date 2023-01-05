Commands
---------------------

Running ``dragon`` without any arguments will list commands

Many commands have multiple aliases

You can combine most commands to do multiple actions with one command.


Packaging Commands
=====================

Creating a new project/module
*********************

``dragon n``, ``dragon new``, ``dragon nic``, ``dragon edit``, or ``dragon create``

Opens the Project Editor


Building a package
*********************

``dragon b``, ``dragon build``, or ``dragon make``


Clean Building a package
*********************

``dragon c`` or ``dragon clean`` will clean the 'build cache'

Combine it with the build command to run a clean build (e.g. ``dragon c b``)


Device Commands
=====================

Setting up a device
*********************

``dragon s`` or ``dragon device`` Can be used to set up an installation target


Installing a package
*********************

``dragon i`` or ``dragon install`` installs a package

Combine it with the build command, or use ``dragon do`` to build and install a package

Respringing a device
*********************

``dragon rs`` or ``dragon respring`` will respring the current device


Running a command on the device
*********************
``dragon dr <commands>`` or ``dragon devicerun`` will execute anything after the command on the device (don't use quotes)


Installing any deb on the device
*********************

``dragon sn <file>`` or ``dragon send <file>`` anywhere on your drive, where <file> is a ``.deb``, will install that deb on your device.


Building and installing to the iOS Simulator
*********************

Adding the ``sim`` command to a set of commands targets the simulator, and if added to an ``install`` command, will install it to the iOS simulator
