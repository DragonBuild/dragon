Structure
---------------------

dragon is set up such that the resources you need are provided via submodules and additional resources can be added as desired.

frameworks/:
    A place for frameworks (.framework) [uses .tbd format]
include/:
    A place for headers (.h)
internal/:
    A place for YAML configuration files (.yml) [not meant to be edited, but feel free to get your hands dirty]
lib/:
    A place for libraries [uses .dylib or .tbd format]
sdks/:
    A place for SDKs (.sdk) [should be patched to include private frameworks]
src/:
    A place for out-sourced tools modified and built for use with dragon
toolchain/:
    A place for a user-provided toolchain [unnecessary on Darwin platforms]
vendor/:
    A place for tools and resources provided by dragon [not meant to be edited]
