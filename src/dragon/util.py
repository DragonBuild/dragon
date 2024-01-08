#!/usr/bin/env python3

import os.path as path
import pkg_resources


def version() -> str:
    return pkg_resources.get_distribution('dragon').version


def tool_path() -> str:
    return path.dirname(__file__) + '/shscripts/'


def deployable_path() -> str:
    return path.dirname(__file__) + '/config/'
