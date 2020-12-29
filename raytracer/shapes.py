from typing import List, Union
import math
import uuid

import intersections
import materials
import points
import rays
import transforms
import vectors

# If a ray has a y component smaller than this, it is near-parallel
# to the plane, so don't intersect
MIN_Y_FOR_PLANE_INTERSECT = 1e-2

class Shape:
    """Class for the base shape"""

    def __init__(self, material: Union[materials.Material, None]=None):

        self.id = uuid.uuid4()

        self.set_transform(transforms.Identity(4))

        if material is None:
            self.set_material(materials.Material())
        else:
            self.set_material(material)

    def __eq__(self, other):
        return self.id == other.id

    def set_material(self, material):
        """Sets the shape's material to material"""
        material.shape = self
        self.material = material

    def set_transform(self, M):
        """Sets the shape's transform to the matrix M"""
        self.transform = M
        self.inverse_transform = M.inverse()

    def intersect(self, ray: rays.Ray):
        """Return the t values for where the ray intersects the shape"""

        # Transform the ray by the inverse of the shape's transform to get into
        # object coordinates
        local_ray = ray.transform(self.inverse_transform)

        return self.local_intersect(local_ray)

    def normal_at(self, point: points.Point) -> vectors.Vector:
        """Returns the normal vector for the shape at the given point"""

        # Transform to object coordinates, and get the nortmal in those
        # coordinates
        local_point = self.inverse_transform * point
        local_normal = self.local_normal_at(local_point)

        world_normal = self.inverse_transform.transpose() * local_normal
        world_normal.w = 0

        return world_normal.normalize()

    def local_normal_at(self, local_point: points.Point):
        """This takes a point in object coordinates and returns the direction
        of the normal in local coordinates
        """
        raise NotImplementedError

    def local_intersect(self, ray: rays.Ray):
        """This takes a ray and returns the t values at which the ray intersects
        the shape, if any
        """
        raise NotImplementedError

class Plane(Shape):
    """Class represents an infinite plane.

    In object units, the plane is in the x-z plane and is at y=0"""

    def local_intersect(self, local_ray: rays.Ray):
        """Return the t-value where the ray intersects with the plane, in local
        units
        """

        # If the y-direction of the ray is small it is approximately parallel to
        #the plane, no intersections
        if abs(local_ray.direction.y) < MIN_Y_FOR_PLANE_INTERSECT:
            return intersections.Intersections()

        t = -local_ray.origin.y / local_ray.direction.y
        return intersections.Intersections(
            intersections.Intersection(self, t))


    def local_normal_at(self, object_point: points.Point) -> vectors.Vector:
        """Returns the normal vector in object coordinates.  For a sphere
        the normal direction is always just the vector from the origin to the
        point
        """
        return vectors.Vector(0, 1, 0)


class Sphere(Shape):
    """Class represents a sphere shape

    In object units this is a unit sphere centered on the origin
    """

    def local_intersect(self, local_ray: rays.Ray):
        """Return to t values for where the ray intersects the shape.  All in
        local coordinates for the shape
        """

        sphere_to_ray = local_ray.origin - points.Point(0, 0, 0)

        a = local_ray.direction.dot(local_ray.direction)
        b = 2 * local_ray.direction.dot(sphere_to_ray)
        c = sphere_to_ray.dot(sphere_to_ray) - 1
        discriminant = b**2 - 4 * a * c

        if discriminant < 0:
            return intersections.Intersections()
        else:
            t1 = (-b - math.sqrt(discriminant)) / (2 * a)
            t2 = (-b + math.sqrt(discriminant)) / (2 * a)
            return intersections.Intersections(
                intersections.Intersection(self, t1),
                intersections.Intersection(self, t2))

    def local_normal_at(self, object_point: points.Point) -> vectors.Vector:
        """Returns the normal vector in object coordinates.  For a sphere
        the normal direction is always just the vector from the origin to the
        point
        """
        return object_point - points.Point(0, 0, 0)
