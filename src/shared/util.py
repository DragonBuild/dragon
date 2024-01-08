from enum import IntEnum
import sys

class OutputColors(IntEnum):
    Red = 31
    Green = 32
    Yellow = 33
    Blue = 34
    Cyan = 36
    White = 37
    Reset = 0

class OutputWeight(IntEnum):
    Normal = 0
    Bold = 1

def color_string(output_color, output_weight):
    return f'\033[{output_weight.value};{output_color.value}m'

def dprintline(label_color, tool_name, text_color, text_weight, pusher, msg):
    print(f"{color_string(label_color, OutputWeight.Bold)}[{tool_name}] {color_string(text_color, text_weight)}{'>>> ' if pusher else ''}{msg}{color_string(OutputColors.Reset, OutputWeight.Normal)}", file=sys.stderr)

def dbstate(tool_name, msg):
    dprintline(OutputColors.Green, tool_name, OutputColors.White, OutputWeight.Bold, False, msg)

def dbwarn(tool_name, msg):
    dprintline(OutputColors.Yellow, tool_name, OutputColors.White, OutputWeight.Normal, False, msg)

def dberror(tool_name, msg):
    dprintline(OutputColors.Red, tool_name, OutputColors.White, OutputWeight.Bold, False, msg)
