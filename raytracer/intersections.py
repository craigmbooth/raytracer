"""Module contains an implementation of intersections.  An intersection
represents a ray striking a shape.  The intersections object contains all the
shapes that a ray strikes
"""
import math
from typing import List, Any

import intersections
import rays

EPSILON = 1e-6

class Computations:
    """Class holds precomputed values for an intersection"""
    def __init__(self, intersection, ray: rays.Ray,
                 all_intersections=None):

        self.t = intersection.t
        self.object = intersection.shape

        self.point = ray.position(self.t)
        self.eyev = -ray.direction
        self.normalv = intersection.shape.normal_at(self.point)

        self.inside = False
        if self.normalv.dot(self.eyev) < 0:
            # If the dot product of the eye vector and normal is negative, they
            # are pointing away from each other, which means you're inside of
            # the object.
            self.inside = True
            self.normalv = - self.normalv

        # This is the point just a tiny bit above the surface, used to avoid
        # rounding errors
        self.over_point = self.point + self.normalv * EPSILON

        # And this one is a tiny bit under the surface to avoid rounding errors
        self.under_point = self.point - self.normalv * EPSILON

        self.reflectv = ray.direction.reflect(self.normalv)

        self.n1 = 1.0
        self.n2 = 1.0

        if all_intersections is not None:

            containers: List[Any] = []

            for isection in all_intersections.intersections:
                if isection == intersection:
                    if len(containers) == 0:
                        self.n1 = 1.0
                    else:
                        self.n1 = containers[-1].material.refractive_index

                if isection.shape in containers:
                    containers.remove(isection.shape)
                else:
                    containers.append(isection.shape)

                if isection == intersection:
                    if len(containers) == 0:
                        self.n2 = 1.0
                    else:
                        self.n2 = containers[-1].material.refractive_index
                    break

        self.schlick = self.compute_schlick()
    def compute_schlick(self):
        """ Calculate the Schlick approximation for the reflectance

        https://en.wikipedia.org/wiki/Schlick%27s_approximation
        """

        # Cosine of the angle between the eye and normal vectors
        cos = self.eyev.dot(self.normalv)

        # Total internal reflection happens only if n1 > n2
        if self.n1 > self.n2:

            n = self.n1 / self.n2
            sin2_t = n ** 2 * (1.0 - cos ** 2)

            if sin2_t > 1:
                return 1

            cos_t = math.sqrt(1.0 - sin2_t)
            cos = cos_t

        r0 = ((self.n1 - self.n2) / (self.n1 + self.n2)) ** 2
        return r0 + (1-r0) * (1 - cos) ** 5


class Intersection:
    """Class represents a single intersection (instance of a ray hitting an
    object)
    """

    def __init__(self, shape, t: float) -> None:
        self.shape = shape
        self.t = t

    def __eq__(self, other):
        return self.shape == other.shape and self.t == other.t

    def __repr__(self):
        return f"Intersection at t={self.t} with {self.shape}"

    def precompute(self, r: rays.Ray, all_intersections=None) -> Computations:
        return Computations(self, r, all_intersections)


class Intersections:
    """Class represents a list of intersection objects, should always
    return sorted by t value
    """

    def __init__(self, *args):
        self.intersections = list(args)
        self.intersections.sort(key=lambda x: x.t)

    def add(self, intersection):
        self.intersections.append(intersection)
        self.intersections.sort(key=lambda x: x.t)

    def __add__(self, other):
        self_intersections = self.intersections
        other_intersections = other.intersections
        self_intersections.extend(other_intersections)
        return Intersections(*self_intersections)

    def hit(self):
        """Find the lowest non-negative value of t"""

        min_t = 1e10
        hit_index = -1
        for index, intersection in enumerate(self.intersections):
            if intersection.t < min_t and intersection.t > 0:
                hit_index = index
                min_t = intersection.t

        if hit_index > -1:
            return self.intersections[hit_index]
        else:
            return None
