# -*- coding: utf-8 -*-


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class GeneralApiError(Error):

    def __init__(self, message):
        self.message = message


class ApiTokenError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class NoTeamError(Error):

    def __init__(self, message):
        self.message = message


class EnvVarError(Error):

    def __init__(self, message):
        self.message = message
