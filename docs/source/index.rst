dragon
=================================


"dragon" is a build system primarily targeting jailbroken iOS devices, capable of building tweaks, preferences, frameworks, apps, and anything else related to them.

it's designed to be simple, both in installation and usage, and to be hackable and configurable at every step of the way.

Benifits over "theos"
---------------------------------

**Note:** `dragon is currently maintained by a single developer. while thorough testing is done, and dragon can run perfectly fine without theos, it's reccomended that you keep theos installed if you've already installed it. Theos has the advantage of long-term stability, being maintained by a team of developers for the past decade.`


Speed 
*********************************

Theos is unfortunately (in its current state) burdened by being written as a complex network of Makefiles, each importing one-another 

On systems with slow implementations of GNU Make, the slowdown can be immense. 

dragon consists of a quick set of python scripts, and uses ninja for building. This can result in absurd speedups, especially with larger projects.

For an average project on an average PC, dragon typically takes **less than a second** to compile a package.


Simplicity 
*********************************

Instead of "submodules" each having their own "Makefile" like in theos, the DragonMake format contains all of the build variables in a single file, at the root of a project. 

Manually writing, adding to, modifying, or hacking things together in a DragonMake file is simple and much more readable.


Ease of development
*********************************

Since dragon was written in 'python', a language written for programming, adding simple or complex features to it is far far easier.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart
   dragonmake
   theos 