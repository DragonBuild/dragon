#!/usr/bin/env bash

#
# Quick Uninstall/Install script for use when working on the project
#

python3 -m pip uninstall --yes dragon
python3 -m pip install .
python3 -m dragon.wizard 

