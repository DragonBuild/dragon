class Writer(object):
    def __init__(self, output, width=78):
        pass

    def newline(self):
        pass

    def comment(self, text):
        pass

    def variable(self, key, value, indent=0):
        pass

    def build(self, outputs, rule, inputs=None, implicit=None, order_only=None,
              variables=None, implicit_outputs=None, pool=None):
        pass

    def include(self, path):
        pass
