class MissingBuildFilesException(BaseException):
    def __init__(self, message, variable=None, variables=None):
        self.variable = variable
        self.variables = variables
        self.message = message
        self.__traceback__ = None

    def __str__(self):
        return f'{self.variable} Missing. {self.message}' if self.variable else f'{self.message}'
