import math
import unittest

import raytracer.materials
import raytracer.points
import raytracer.rays
import raytracer.shapes
import raytracer.transforms
import raytracer.vectors

class TestSphere(unittest.TestCase):

    def test_intersection_standard(self):
        """Test we can identify what points a ray intersects with a sphere"""
        s = raytracer.shapes.Sphere()
        r = raytracer.rays.Ray(raytracer.points.Point(0, 0, -5),
                               raytracer.vectors.Vector(0, 0, 1))

        result = s.intersect(r)

        self.assertEqual(result[0].t, 4)
        self.assertEqual(result[1].t, 6)
        self.assertEqual(result[0].shape, s)
        self.assertEqual(result[1].shape, s)

    def test_intersection_standard__glance(self):
        """Test we can identify what points a ray intersects with a sphere when
        it glances"""

        s = raytracer.shapes.Sphere()
        r = raytracer.rays.Ray(raytracer.points.Point(0, 1, -5),
                               raytracer.vectors.Vector(0, 0, 1))

        result = s.intersect(r)

        self.assertEqual(result[0].t, 5)
        self.assertEqual(result[1].t, 5)
        self.assertEqual(result[0].shape, s)
        self.assertEqual(result[1].shape, s)


    def test_intersection_miss(self):
        """Test we handle the case where the ray misses the sphere"""

        s = raytracer.shapes.Sphere()
        r = raytracer.rays.Ray(raytracer.points.Point(0, 2, -5),
                               raytracer.vectors.Vector(0, 0, 1))

        self.assertEqual(s.intersect(r), [])

    def test_intersection_inside(self):
        """Test we handle the case where the ray starts inside the sphere"""

        s = raytracer.shapes.Sphere()
        r = raytracer.rays.Ray(raytracer.points.Point(0, 0, 0),
                               raytracer.vectors.Vector(0, 0, 1))

        result = s.intersect(r)

        self.assertEqual(result[0].t, -1)
        self.assertEqual(result[1].t, 1)
        self.assertEqual(result[0].shape, s)
        self.assertEqual(result[1].shape, s)

    def test_intersection_behind(self):
        """Test we handle the case where the ray starts inside the sphere"""

        s = raytracer.shapes.Sphere()
        r = raytracer.rays.Ray(raytracer.points.Point(0, 0, 5),
                               raytracer.vectors.Vector(0, 0, 1))

        result = s.intersect(r)

        self.assertEqual(result[0].t, -6)
        self.assertEqual(result[1].t, -4)
        self.assertEqual(result[0].shape, s)
        self.assertEqual(result[1].shape, s)

    def test_default_transform(self):
        """Test that we get the identity matrix as the default transform"""

        s = raytracer.shapes.Sphere()
        self.assertEqual(s.transform, raytracer.transforms.Identity(4))

    def test_changed_transform(self):
        """Test that we can change the transform on a shape"""

        s = raytracer.shapes.Sphere()
        s.set_transform(raytracer.transforms.Translate(6, 7, 8))
        self.assertEqual(s.transform, raytracer.transforms.Translate(6, 7, 8))

    def test_intersections_with_transformed_ray__scaling(self):
        """Test we get the correct intersections after adding a scaling
        to a shape
        """

        s = raytracer.shapes.Sphere()
        s.set_transform(raytracer.transforms.Scale(2, 2, 2))

        r = raytracer.rays.Ray(raytracer.points.Point(0, 0, -5),
                               raytracer.vectors.Vector(0, 0, 1))

        result = s.intersect(r)
        self.assertEqual(result[0].t, 3)
        self.assertEqual(result[1].t, 7)
        self.assertEqual(result[0].shape, s)
        self.assertEqual(result[1].shape, s)

    def test_intersections_with_transformed_ray__translation(self):
        """Test we get the correct intersections after adding a translation
        to a shape
        """

        s = raytracer.shapes.Sphere()
        s.set_transform(raytracer.transforms.Translate(5, 0, 0))

        r = raytracer.rays.Ray(raytracer.points.Point(0, 0, -5),
                               raytracer.vectors.Vector(0, 0, 1))

        result = s.intersect(r)
        self.assertTrue(len(result) == 0)

    def test_normal_at__non_transformed(self):
        """Test we can calculate normal vectors on the unit sphere"""

        s = raytracer.shapes.Sphere()

        n = s.normal_at(raytracer.points.Point(1, 0, 0))
        self.assertEqual(n, raytracer.vectors.Vector(1, 0, 0))

        n = s.normal_at(raytracer.points.Point(0, 1, 0))
        self.assertEqual(n, raytracer.vectors.Vector(0, 1, 0))

        n = s.normal_at(raytracer.points.Point(0, 0, 1))
        self.assertEqual(n, raytracer.vectors.Vector(0, 0, 1))

        sqrt3d3 = math.sqrt(3)/3
        n = s.normal_at(raytracer.points.Point(sqrt3d3, sqrt3d3, sqrt3d3))
        self.assertEqual(n, raytracer.vectors.Vector(sqrt3d3, sqrt3d3, sqrt3d3))

    def test_normal_at__transformed(self):
        """Test we can calculate normal vectors on a transformed sphere"""

        s = raytracer.shapes.Sphere()
        s.set_transform(raytracer.transforms.Translate(0, 1, 0))
        n = s.normal_at(raytracer.points.Point(0, 1.70711, -0.70711))

        self.assertEqual(n, raytracer.vectors.Vector(0, 0.70711, -0.70711))

        s.set_transform(raytracer.transforms.Scale(1, 0.5, 1) *
                       raytracer.transforms.RotateZ(math.pi/5))

        n = s.normal_at(raytracer.points.Point(0, math.sqrt(2)/2, -math.sqrt(2)/2))
        self.assertEqual(n, raytracer.vectors.Vector(0, 0.97014, -0.24254))

    def test_default_material(self):
        """Test that a shape has the default material"""
        s = raytracer.shapes.Sphere()
        self.assertEqual(s.material, raytracer.materials.Material())

    def test_altered_material(self):
        """Test that a shape has the default material"""
        s = raytracer.shapes.Sphere(
            material=raytracer.materials.Material(shininess=100))
        self.assertEqual(s.material,
                         raytracer.materials.Material(shininess=100))

if __name__ == "__main__":
    unittest.main()
