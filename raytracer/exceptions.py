"""Module contains exceptions custom to this project"""

class IncompatibleLengthError(Exception):
    """Is raised when the lengths or sizes of tuples/matrices don't allow a
    given operation
    """

class CannotInvertMatrixError(Exception):
    """Is raised when you try to invert a matrix that isn't invertable"""
