import unittest

import intersections
import shapes


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

if __name__ == "__main__":
    unittest.main()
