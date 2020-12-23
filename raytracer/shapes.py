import math
import uuid

import raytracer.intersections
import raytracer.rays
import raytracer.points
import raytracer.transforms

class Shape:

    def __init__(self):
        self.id = uuid.uuid4()
        self.transform = raytracer.transforms.Identity(4)

    def __eq__(self, other):
        return self.id == other.id

    def set_transform(M):
        """Sets the shape's transform to the matrix M"""
        self.transform = M


class Sphere(Shape):

    def intersect(self, ray: raytracer.rays.Ray):

        sphere_to_ray = ray.origin - raytracer.points.Point(0, 0, 0)

        a = ray.direction.dot(ray.direction)
        b = 2 * ray.direction.dot(sphere_to_ray)
        c = sphere_to_ray.dot(sphere_to_ray) - 1
        discriminant = b**2 - 4 * a * c

        if discriminant < 0:
            return []
        else:
            t1 = (-b - math.sqrt(discriminant)) / (2 * a)
            t2 = (-b + math.sqrt(discriminant)) / (2 * a)
            return sorted(
                [raytracer.intersections.Intersection(self, t1),
                raytracer.intersections.Intersection(self, t2)],
                key=lambda x: x.t)
