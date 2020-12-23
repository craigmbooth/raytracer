import raytracer.points
import raytracer.vectors

class Ray:

    def __init__(self, origin: raytracer.points.Point,
                 direction: raytracer.vectors.Vector):
        """Initialize a ray with an origin and direction"""

        self.origin = origin
        self.direction = direction

    def position(self, t):
        """Return the position of the ray at a given time, t"""
        return self.origin + self.direction * t
