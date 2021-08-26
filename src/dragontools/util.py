#!/usr/bin/env python3
import os.path as path


def tool_path() -> str:
    return path.dirname(__file__) + '/shscripts/'


def deployable_path() -> str:
    return path.dirname(__file__) + '/deployable/'
