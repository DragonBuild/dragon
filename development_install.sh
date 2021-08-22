#!/usr/bin/env bash

#
# Quick Uninstall/Install script for use when working on the project
#

rm -rf ~/.dragon

python3 -m pip uninstall dragon
python3 -m pip install .

