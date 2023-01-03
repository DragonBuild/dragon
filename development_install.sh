#!/usr/bin/env bash

#
# Quick Uninstall/Install script for use when working on the project
#

python3 -m pip uninstall --yes dragon
python3 -m pip install .
DRAGON_DIR=.dragon && DRAGON_ROOT_DIR=$HOME/$DRAGON_DIR \
DRAGON_VERS=$(python3 -c 'from dragon.util import version; print(version())') \
python3 -m dragon.wizard
