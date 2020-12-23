import unittest

import raytracer.intersections
import raytracer.shapes


class TestIntersections(unittest.TestCase):

    def test_initialization(self):

        shape = raytracer.shapes.Sphere()
        t1 = 3.5
        t2 = -3.5

        i1 = raytracer.intersections.Intersection(shape, t1)
        self.assertEqual(i1.t, 3.5)
        self.assertEqual(i1.shape, shape)

        i2 = raytracer.intersections.Intersection(shape, t2)
        self.assertEqual(i2.t, -3.5)

        i = raytracer.intersections.Intersections(i1, i2)
        self.assertEqual(i.intersections, [i1, i2])


    def test_hits__positive(self):
        """Test we get the correct hit for multiple positive intersections"""

        shape = raytracer.shapes.Sphere()

        i1 = raytracer.intersections.Intersection(shape, 2)
        i2 = raytracer.intersections.Intersection(shape, 1)
        intersections = raytracer.intersections.Intersections(i1, i2)

        self.assertEqual(intersections.hit(), i2)

    def test_hits__some_negative(self):
        """Test we get the correct hit for some negative intersections"""

        shape = raytracer.shapes.Sphere()

        i1 = raytracer.intersections.Intersection(shape, -1)
        i2 = raytracer.intersections.Intersection(shape, 1)
        intersections = raytracer.intersections.Intersections(i1, i2)

        self.assertEqual(intersections.hit(), i2)

    def test_hits__all_negative(self):
        """Test we get no hits for all negative intersections"""

        shape = raytracer.shapes.Sphere()

        i1 = raytracer.intersections.Intersection(shape, -1)
        i2 = raytracer.intersections.Intersection(shape, -2)
        intersections = raytracer.intersections.Intersections(i1, i2)

        self.assertIsNone(intersections.hit())

    def test_hits__multiple(self):
        """Test we get the correct hit for some negative intersections"""

        shape = raytracer.shapes.Sphere()

        i1 = raytracer.intersections.Intersection(shape, -1)
        i2 = raytracer.intersections.Intersection(shape, 7)
        i3 = raytracer.intersections.Intersection(shape, -5)
        i4 = raytracer.intersections.Intersection(shape, 2)
        i5 = raytracer.intersections.Intersection(shape, 3)
        intersections = raytracer.intersections.Intersections(i1, i2, i3, i4, i5)

        self.assertEqual(intersections.hit(), i4)

if __name__ == "__main__":
    unittest.main()
