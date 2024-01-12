from enum import IntEnum
import sys
import subprocess


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


def system(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
    proc = subprocess.Popen("" + cmd,
                            stdout=stdout,
                            stderr=stderr,
                            shell=True,
                            universal_newlines=True)
    std_out, std_err = proc.communicate()
    # print(proc.returncode)
    return proc.returncode  # , std_out, std_err


def system_with_output(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
    proc = subprocess.Popen("" + cmd,
                            stdout=stdout,
                            stderr=stderr,
                            shell=True,
                            universal_newlines=True)
    std_out, std_err = proc.communicate()
    return proc.returncode, std_out, std_err


def system_pipe_output(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
    process = subprocess.Popen(cmd,
                          stdout=stdout,
                          stderr=stderr,
                          shell=True,
                          universal_newlines=True)

    while True:
        realtime_output = process.stdout.readline()
        realtime_err = process.stderr.readline()

        if realtime_output == '' and realtime_err == '' and process.poll() is not None:
            break

        if realtime_output:
            print(realtime_output.strip(), flush=True)
        if realtime_err:
            print(realtime_err.strip(), flush=True, file=sys.stderr)
