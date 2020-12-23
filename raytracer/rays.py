import points
import vectors

class Ray:

    def __init__(self, origin: points.Point,
                 direction: vectors.Vector):
        """Initialize a ray with an origin and direction"""

        self.origin = origin
        self.direction = direction

    def position(self, t):
        """Return the position of the ray at a given time, t"""
        return self.origin + self.direction * t

    def transform(self, M):
        """Transform the ray with the matrix"""

        return Ray(M * self.origin, M * self.direction)
