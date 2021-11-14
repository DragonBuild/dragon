#!/usr/bin/env python3
import os.path as path
from enum import IntEnum

import pkg_resources

DRAGONBUILD_VERSION = pkg_resources.get_distribution('dragon').version


def version() -> str:
    return DRAGONBUILD_VERSION


def tool_path() -> str:
    return path.dirname(__file__) + '/shscripts/'


def deployable_path() -> str:
    return path.dirname(__file__) + '/config/'


colors = [["\033[0;31m","\033[0;32m","\033[0;33m","\033[0;34m","\033[0;36m",
"\033[0;37m","\033[0m"],["\033[1;31m","\033[1;32m","\033[1;33m","\033[1;34m",
"\033[1;36m","\033[1;37m","\033[0m"]]


class OutputColors(IntEnum):
    Black = 30
    Red = 31
    Green = 32
    Yellow = 33
    Blue = 34
    Magenta = 35
    Cyan = 36
    White = 37


class OutputWeight(IntEnum):
    Normal = 0
    Bold = 1


def color_string(output_color, output_weight):
    return f'\033[{str(output_weight.value)};{str(output_color.value)}m'

def dprintline(label_color: OutputColors, tool_name: str, text_color: OutputColors, text_weight: OutputWeight, pusher: bool, msg: str):
    print("%s[%s]%s %s%s%s" % (
        color_string(label_color, OutputWeight.Bold), tool_name, color_string(text_color, text_weight), ">>> " if pusher else "", msg, colors[0][6]))
