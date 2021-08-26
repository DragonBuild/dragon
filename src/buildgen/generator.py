#!/usr/bin/env python3

"""GenBuild aims to provide a python wrapper for creating Makefile/Build.ninja files
with standard syntax.
"""
from enum import Enum
from .makefile_generator import MakefileWriter
from .ninja_generator import NinjaWriter


class BuildSystem(Enum):
    NINJA = 0
    MAKE = 1


class BuildFileGenerator(object):
    def __init__(self, output, build_type=BuildSystem.NINJA):
        self.builder = NinjaWriter(output) if build_type == BuildSystem.NINJA else MakefileWriter(output)

    def newline(self):
        """Add a newline

        """
        self.builder.newline()

    def comment(self, text):
        """

        :param text:
        """
        self.builder.comment(text)

    def variable(self, key, value, indent=0):
        """

        :param key:
        :param value:
        :param indent:
        :return:
        """
        self.builder.variable(key, value, indent)

    def pool(self, name, depth):
        """

        :param name:
        :param depth:
        """
        self.builder.pool(name, depth)

    def rule(self, name, command, description=None, depfile=None,
             generator=False, pool=None, restat=False, rspfile=None,
             rspfile_content=None, deps=None):
        """

        :param name:
        :param command:
        :param description:
        :param depfile:
        :param generator:
        :param pool:
        :param restat:
        :param rspfile:
        :param rspfile_content:
        :param deps:
        """
        self.builder.rule(name, command, description, depfile,
                          generator, pool, restat, rspfile,
                          rspfile_content, deps)

    def build(self, outputs, rule, inputs=None, implicit=None, order_only=None,
              variables=None, implicit_outputs=None, pool=None):
        """

        :param outputs:
        :param rule:
        :param inputs:
        :param implicit:
        :param order_only:
        :param variables:
        :param implicit_outputs:
        :param pool:
        :return:
        """
        return self.builder.build(outputs, rule, inputs, implicit, order_only, variables, implicit_outputs, pool)

    def include(self, path):
        """

        :param path:
        """
        self.builder.include(path)

    def subfile(self, path):
        """

        :param path:
        """
        self.builder.subninja(path)

    def default(self, paths: list):
        """This should specify the default build targets

        :param paths:
        """
        self.builder.default(paths)

    def close(self):
        self.builder.close()


def as_list(unknownTypeInput):
    """

    :param unknownTypeInput:
    :return:
    """
    if unknownTypeInput is None:
        return []
    if isinstance(unknownTypeInput, list):
        return unknownTypeInput
    return [unknownTypeInput]


def escape(string):
    """Escape a string such that it can be embedded into a Ninja file without
    further interpretation."""
    assert '\n' not in string, 'Ninja syntax does not allow newlines'
    # We only have one special metacharacter: '$'.
    return string.replace('$', '$$')


def expand(string, vars, local_vars={}):
    """Expand a string containing $vars as Ninja would.
    Note: doesn't handle the full Ninja variable syntax, but it's enough
    to make configure.py's use of it work.
    """

    def exp(m):
        var = m.group(1)
        if var == '$':
            return '$'
        return local_vars.get(var, vars.get(var, ''))

    return re.sub(r'\$(\$|\w*)', exp, string)
