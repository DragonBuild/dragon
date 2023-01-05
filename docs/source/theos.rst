Theos Support
---------------------

dragon aims to provide as much compatibility with theos projects and their structure as possible.


"control" files, Bundle filters, etc.
=====================

dragon ships with support for these in both Theos Makefile and DragonMake format projects.


Makefile interpreter
=====================

dragon includes a best-effort Makefile "interpreter" that attempts to translate as much from standard Theos project structure as possible.

It also includes several support files used with theos projects.

Compiling a theos project should be as simple as::

    dragon b

If you encounter any issues with it, feel free to file an issue on https://github.com/DragonBuild/dragon .
