import math
import unittest

import materials
import points
import rays
import shapes
import transforms
import vectors

class TestSphere(unittest.TestCase):

    def test_intersection_standard(self):
        """Test we can identify what points a ray intersects with a sphere"""
        s = shapes.Sphere()
        r = rays.Ray(points.Point(0, 0, -5),
                               vectors.Vector(0, 0, 1))

        result = s.intersect(r)

        self.assertEqual(result.intersections[0].t, 4)
        self.assertEqual(result.intersections[1].t, 6)
        self.assertEqual(result.intersections[0].shape, s)
        self.assertEqual(result.intersections[1].shape, s)

    def test_intersection_standard__glance(self):
        """Test we can identify what points a ray intersects with a sphere when
        it glances"""

        s = shapes.Sphere()
        r = rays.Ray(points.Point(0, 1, -5),
                               vectors.Vector(0, 0, 1))

        result = s.intersect(r)

        self.assertEqual(result.intersections[0].t, 5)
        self.assertEqual(result.intersections[1].t, 5)
        self.assertEqual(result.intersections[0].shape, s)
        self.assertEqual(result.intersections[1].shape, s)


    def test_intersection_miss(self):
        """Test we handle the case where the ray misses the sphere"""

        s = shapes.Sphere()
        r = rays.Ray(points.Point(0, 2, -5),
                               vectors.Vector(0, 0, 1))

        self.assertEqual(s.intersect(r).intersections, [])

    def test_intersection_inside(self):
        """Test we handle the case where the ray starts inside the sphere"""

        s = shapes.Sphere()
        r = rays.Ray(points.Point(0, 0, 0),
                               vectors.Vector(0, 0, 1))

        result = s.intersect(r)

        self.assertEqual(result.intersections[0].t, -1)
        self.assertEqual(result.intersections[1].t, 1)
        self.assertEqual(result.intersections[0].shape, s)
        self.assertEqual(result.intersections[1].shape, s)

    def test_intersection_behind(self):
        """Test we handle the case where the ray starts inside the sphere"""

        s = shapes.Sphere()
        r = rays.Ray(points.Point(0, 0, 5),
                               vectors.Vector(0, 0, 1))

        result = s.intersect(r)

        self.assertEqual(result.intersections[0].t, -6)
        self.assertEqual(result.intersections[1].t, -4)
        self.assertEqual(result.intersections[0].shape, s)
        self.assertEqual(result.intersections[1].shape, s)

    def test_default_transform(self):
        """Test that we get the identity matrix as the default transform"""

        s = shapes.Sphere()
        self.assertEqual(s.transform, transforms.Identity(4))

    def test_changed_transform(self):
        """Test that we can change the transform on a shape"""

        s = shapes.Sphere()
        s.set_transform(transforms.Translate(6, 7, 8))
        self.assertEqual(s.transform, transforms.Translate(6, 7, 8))

    def test_intersections_with_transformed_ray__scaling(self):
        """Test we get the correct intersections after adding a scaling
        to a shape
        """

        s = shapes.Sphere()
        s.set_transform(transforms.Scale(2, 2, 2))

        r = rays.Ray(points.Point(0, 0, -5),
                               vectors.Vector(0, 0, 1))

        result = s.intersect(r)
        self.assertEqual(result.intersections[0].t, 3)
        self.assertEqual(result.intersections[1].t, 7)
        self.assertEqual(result.intersections[0].shape, s)
        self.assertEqual(result.intersections[1].shape, s)

    def test_intersections_with_transformed_ray__translation(self):
        """Test we get the correct intersections after adding a translation
        to a shape
        """

        s = shapes.Sphere()
        s.set_transform(transforms.Translate(5, 0, 0))

        r = rays.Ray(points.Point(0, 0, -5),
                               vectors.Vector(0, 0, 1))

        result = s.intersect(r)
        self.assertTrue(len(result.intersections) == 0)

    def test_normal_at__non_transformed(self):
        """Test we can calculate normal vectors on the unit sphere"""

        s = shapes.Sphere()

        n = s.normal_at(points.Point(1, 0, 0))
        self.assertEqual(n, vectors.Vector(1, 0, 0))

        n = s.normal_at(points.Point(0, 1, 0))
        self.assertEqual(n, vectors.Vector(0, 1, 0))

        n = s.normal_at(points.Point(0, 0, 1))
        self.assertEqual(n, vectors.Vector(0, 0, 1))

        sqrt3d3 = math.sqrt(3)/3
        n = s.normal_at(points.Point(sqrt3d3, sqrt3d3, sqrt3d3))
        self.assertEqual(n, vectors.Vector(sqrt3d3, sqrt3d3, sqrt3d3))

    def test_normal_at__transformed(self):
        """Test we can calculate normal vectors on a transformed sphere"""

        s = shapes.Sphere()
        s.set_transform(transforms.Translate(0, 1, 0))
        n = s.normal_at(points.Point(0, 1.70711, -0.70711))

        self.assertEqual(n, vectors.Vector(0, 0.70711, -0.70711))

        s.set_transform(transforms.Scale(1, 0.5, 1) *
                       transforms.RotateZ(math.pi/5))

        n = s.normal_at(points.Point(0, math.sqrt(2)/2, -math.sqrt(2)/2))
        self.assertEqual(n, vectors.Vector(0, 0.97014, -0.24254))

    def test_default_material(self):
        """Test that a shape has the default material"""
        s = shapes.Sphere()
        self.assertEqual(s.material, materials.Material())

    def test_altered_material(self):
        """Test that a shape has the default material"""
        s = shapes.Sphere(
            material=materials.Material(shininess=100))
        self.assertEqual(s.material,
                         materials.Material(shininess=100))

class TestPlane(unittest.TestCase):
    """Tests on the plane shape"""

    def test_local_normal_at(self):
        """Test that the local normal is always in the y direction"""

        p = shapes.Plane()

        self.assertEqual(p.local_normal_at(points.Point(0, 0, 0)),
                         vectors.Vector(0, 1, 0))

        self.assertEqual(p.local_normal_at(points.Point(10, 0, -10)),
                         vectors.Vector(0, 1, 0))

        self.assertEqual(p.local_normal_at(points.Point(-5, 0, 150)),
                         vectors.Vector(0, 1, 0))

    def test_local_intersect(self):
        """Test we can calculate where a ray intersects with a plane"""

        p = shapes.Plane()

        # Rays parallel with the plane
        r = rays.Ray(points.Point(0, 10, 0), vectors.Vector(0, 0, 1))
        xs = p.local_intersect(r)
        self.assertEqual(len(xs.intersections), 0)

        r = rays.Ray(points.Point(0, 0, 0), vectors.Vector(0, 0, 1))
        xs = p.local_intersect(r)
        self.assertEqual(len(xs.intersections), 0)

        # Rays that do intersect the plane
        r = rays.Ray(points.Point(0, 1, 0), vectors.Vector(0, -1, 0))
        xs = p.local_intersect(r)
        self.assertEqual(xs.intersections[0].t, 1)

if __name__ == "__main__":
    unittest.main()
