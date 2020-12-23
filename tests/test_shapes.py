import unittest

import raytracer.rays
import raytracer.shapes
import raytracer.points
import raytracer.vectors
import raytracer.transforms
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

if __name__ == "__main__":
    unittest.main()
