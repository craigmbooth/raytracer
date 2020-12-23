import math
import uuid

import raytracer.intersections
import raytracer.materials
import raytracer.points
import raytracer.rays
import raytracer.transforms

class Shape:

    def __init__(self, material=raytracer.materials.Material()):
        self.id = uuid.uuid4()
        self.transform = raytracer.transforms.Identity(4)
        self.material = material

    def __eq__(self, other):
        return self.id == other.id

    def set_transform(self, M):
        """Sets the shape's transform to the matrix M"""
        self.transform = M

    def intersect(self):
        raise NotImplementedError

    def normal_at(self):
        raise NotImplementedError

class Sphere(Shape):

    def intersect(self, ray: raytracer.rays.Ray):

        # Transform the ray by the inverse of the sphere's transform
        r2 = ray.transform(self.transform.inverse())

        sphere_to_ray = r2.origin - raytracer.points.Point(0, 0, 0)

        a = r2.direction.dot(r2.direction)
        b = 2 * r2.direction.dot(sphere_to_ray)
        c = sphere_to_ray.dot(sphere_to_ray) - 1
        discriminant = b**2 - 4 * a * c

        if discriminant < 0:
            return raytracer.intersections.Intersections()
        else:
            t1 = (-b - math.sqrt(discriminant)) / (2 * a)
            t2 = (-b + math.sqrt(discriminant)) / (2 * a)
            return raytracer.intersections.Intersections(
                raytracer.intersections.Intersection(self, t1),
                raytracer.intersections.Intersection(self, t2))


    def normal_at(self, point: raytracer.points.Point):

        object_point = self.transform.inverse() * point
        object_normal = object_point - raytracer.points.Point(0, 0, 0)

        world_normal = self.transform.inverse().transpose() * object_normal
        world_normal.w = 0

        return world_normal.normalize()
