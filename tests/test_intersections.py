import math
import unittest

import intersections
import rays
import points
import shapes
import transforms
import vectors

class TestIntersections(unittest.TestCase):

    def test_initialization(self):

        shape = shapes.Sphere()
        t1 = 3.5
        t2 = -3.5

        i1 = intersections.Intersection(shape, t1)
        self.assertEqual(i1.t, 3.5)
        self.assertEqual(i1.shape, shape)

        i2 = intersections.Intersection(shape, t2)
        self.assertEqual(i2.t, -3.5)

        i = intersections.Intersections(i1, i2)
        self.assertEqual(i.intersections, [i2, i1])


    def test_hits__positive(self):
        """Test we get the correct hit for multiple positive intersections"""

        shape = shapes.Sphere()

        i1 = intersections.Intersection(shape, 2)
        i2 = intersections.Intersection(shape, 1)
        isections = intersections.Intersections(i1, i2)

        self.assertEqual(isections.hit(), i2)

    def test_hits__some_negative(self):
        """Test we get the correct hit for some negative intersections"""

        shape = shapes.Sphere()

        i1 = intersections.Intersection(shape, -1)
        i2 = intersections.Intersection(shape, 1)
        isections = intersections.Intersections(i1, i2)

        self.assertEqual(isections.hit(), i2)

    def test_hits__all_negative(self):
        """Test we get no hits for all negative intersections"""

        shape = shapes.Sphere()

        i1 = intersections.Intersection(shape, -1)
        i2 = intersections.Intersection(shape, -2)
        isections = intersections.Intersections(i1, i2)

        self.assertIsNone(isections.hit())

    def test_hits__multiple(self):
        """Test we get the correct hit for some negative intersections"""

        shape = shapes.Sphere()

        i1 = intersections.Intersection(shape, -1)
        i2 = intersections.Intersection(shape, 7)
        i3 = intersections.Intersection(shape, -5)
        i4 = intersections.Intersection(shape, 2)
        i5 = intersections.Intersection(shape, 3)
        isections = intersections.Intersections(i1, i2, i3, i4, i5)

        self.assertEqual(isections.hit(), i4)

    def test_precompute__outside(self):
        """Test that we can precompute vectors for an intersection and ray when
        outside of a shape"""

        r = rays.Ray(points.Point(0, 0, -5), vectors.Vector(0, 0, 1))
        s = shapes.Sphere()
        i = intersections.Intersection(s, 4)

        computations = i.precompute(r)

        self.assertEqual(computations.t, 4)
        self.assertEqual(computations.point, points.Point(0, 0, -1))
        self.assertEqual(computations.eyev, vectors.Vector(0, 0, -1))
        self.assertEqual(computations.normalv, vectors.Vector(0, 0, -1))
        self.assertFalse(computations.inside)

    def test_precompute__inside(self):
        """Test that we can precompute vectors for an intersection and ray when
        inside of a shape"""

        r = rays.Ray(points.Point(0, 0, 0), vectors.Vector(0, 0, 1))
        s = shapes.Sphere()
        i = intersections.Intersection(s, 1)

        computations = i.precompute(r)

        self.assertEqual(computations.t, 1)
        self.assertEqual(computations.point, points.Point(0, 0, 1))
        self.assertEqual(computations.eyev, vectors.Vector(0, 0, -1))
        self.assertEqual(computations.normalv, vectors.Vector(0, 0, -1))
        self.assertTrue(computations.inside)


    def test_precompute__over_vector(self):
        """Test that we calculate a vector just outside of the surface of a
        shape
        """

        r = rays.Ray(points.Point(0, 0, -5), vectors.Vector(0, 0, 1))

        s = shapes.Sphere()
        s.set_transform(transforms.Translate(0, 0, 1))

        i = intersections.Intersection(s, 5)

        computations = i.precompute(r)
        self.assertTrue(computations.over_point.z < computations.point.z)
        self.assertTrue(computations.over_point.z < -intersections.EPSILON/2)


    def test_precompute_reflectv(self):
        """Test that we can calculate the reflection vector"""

        p = shapes.Plane()
        r = rays.Ray(points.Point(0, 1, -1),
                     vectors.Vector(0, -math.sqrt(2)/2, math.sqrt(2)/2))
        i = intersections.Intersection(p, math.sqrt(2))

        comps = i.precompute(r)

        self.assertEqual(comps.reflectv,
                         vectors.Vector(0, math.sqrt(2)/2, math.sqrt(2)/2))


if __name__ == "__main__":
    unittest.main()
