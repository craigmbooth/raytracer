"""Module represents a ray, specified by an origin an direction.  Position along
the ray can be calculated with the `t` variable, which represents some time
after which the ray started propagating
"""

import points
import vectors

class Ray:
    """Class represents a ray (specified by an origin and a direction)"""
    def __init__(self, origin: points.Point,
                 direction: vectors.Vector):
        """Initialize a ray with an origin and direction"""

        self.origin = origin
        self.direction = direction

    def position(self, time):
        """Return the position of the ray at a given time, time"""
        return self.origin + self.direction * time

    def transform(self, M):
        """Transform the ray with the matrix"""

        return Ray(M * self.origin, M * self.direction)
