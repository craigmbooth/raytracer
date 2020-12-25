"""This module contains an implementation of a simple Vector class"""

import tuples

class Vector(tuples.Tuple):
    """This class represents a vector between two points in space.  It is
    initialized with x, y, and z coordinates and then in this class we add a
    fourth component, w, which is 0 for a point
    """

    def __init__(self, x: float, y: float, z: float):

        # Initialize and name here so mypy can find attributes
        self.x = 0               # pylint: disable=C0103
        self.y = 0               # pylint: disable=C0103
        self.z = 0               # pylint: disable=C0103
        self.w = 0               # pylint: disable=C0103

        super().__init__(["x", "y", "z", "w"], x, y, z, 0)

    def __repr__(self) -> str:
        return f"Vector [{self.x}, {self.y}, {self.z}]"
