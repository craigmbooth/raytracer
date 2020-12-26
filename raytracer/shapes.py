import math
import uuid

import intersections
import materials
import points
import rays
import transforms

class Shape:

    def __init__(self, material=materials.Material()):
        self.id = uuid.uuid4()
        self.set_transform(transforms.Identity(4))
        self.material = material

    def __eq__(self, other):
        return self.id == other.id

    def set_transform(self, M):
        """Sets the shape's transform to the matrix M"""
        self.transform = M
        self.inverse_transform = M.inverse()

    def intersect(self, ray: rays.Ray):
        raise NotImplementedError

    def normal_at(self, point: points.Point):
        raise NotImplementedError

class Sphere(Shape):

    def intersect(self, ray: rays.Ray):

        # Transform the ray by the inverse of the sphere's transform
        r2 = ray.transform(self.inverse_transform)

        sphere_to_ray = r2.origin - points.Point(0, 0, 0)

        a = r2.direction.dot(r2.direction)
        b = 2 * r2.direction.dot(sphere_to_ray)
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


    def normal_at(self, point: points.Point):

        object_point = self.transform.inverse() * point
        object_normal = object_point - points.Point(0, 0, 0)

        world_normal = self.transform.inverse().transpose() * object_normal
        world_normal.w = 0

        return world_normal.normalize()
