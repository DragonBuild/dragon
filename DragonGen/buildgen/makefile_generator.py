import re
import textwrap

from .writer import Writer


class MakefileWriter(Writer):
    def __init__(self, output, width=78):
        super().__init__(output, width)
        self.output = output
        self.width = width

    def newline(self):
        """Add a newline

        """
        self.output.write('\n')

    def comment(self, text):
        """

        :param text:
        """
        for line in textwrap.wrap(text, self.width - 2, break_long_words=False,
                                  break_on_hyphens=False):
            self.output.write('# ' + line + '\n')

    def variable(self, key, value, indent=0):
        """

        :param key:
        :param value:
        :param indent:
        :return:
        """
        if value is None:
            return
        if isinstance(value, list):
            value = ' '.join(filter(None, value))  # Filter out empty strings.
        self._line('%s = %s' % (key, value), indent)


    def pool(self, name, depth):
        pass

    def rule(self, name, deps, command):
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
        self._line('%s : %s' % (name, deps))
        self.variable('command', command, indent=1)

    def _line(self, text, indent=0):
        """Write 'text' word-wrapped at self.width characters."""
        leading_space = '  ' * indent
        while len(leading_space) + len(text) > self.width:
            # The text is too wide; wrap if possible.

            # Find the rightmost space that would obey our width constraint and
            # that's not an escaped space.
            available_space = self.width - len(leading_space) - len(' $')
            space = available_space
            while True:
                space = text.rfind(' ', 0, space)
                if (space < 0 or
                        _count_dollars_before_index(text, space) % 2 == 0):
                    break

            if space < 0:
                # No such space; just use the first unescaped space we can find.
                space = available_space - 1
                while True:
                    space = text.find(' ', space + 1)
                    if (space < 0 or
                            _count_dollars_before_index(text, space) % 2 == 0):
                        break
            if space < 0:
                # Give up on breaking.
                break

            self.output.write(leading_space + text[0:space] + ' $\n')
            text = text[space + 1:]

            # Subsequent lines are continuations, so indent them.
            leading_space = '  ' * (indent + 2)

        self.output.write(leading_space + text + '\n')

    def close(self):
        self.output.close()
