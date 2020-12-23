import math
import unittest

import tuples, vectors, points

class TestTuples(unittest.TestCase):
    """Tests on the Tuple class"""

    def test_point__tuple(self):
        """Test that we can initialize and read from a point as a tuple"""

        p = tuples.Tuple(["x", "y", "z", "w"], 4.3, -4.2, 3.1, 1)

        self.assertEqual(p.x, 4.3)
        self.assertEqual(p.y, -4.2)
        self.assertEqual(p.z, 3.1)
        self.assertEqual(p.w, 1)


    def test_point(self):
        """Test that we can initialize and read from a point"""

        p = points.Point(4.3, -4.2, 3.1)

        self.assertEqual(p.x, 4.3)
        self.assertEqual(p.y, -4.2)
        self.assertEqual(p.z, 3.1)
        self.assertEqual(p.w, 1)

    def test_addition(self):
        """test that we can add a vector to a point"""

        a1 = points.Point(3, -2, 5)
        a2 = vectors.Vector(-2, 3, 1)

        a3 = a1 + a2

        self.assertEqual(a3,
            tuples.Tuple(["x", "y", "z", "w"], 1, 1, 6, 1))
        self.assertEqual(a3, points.Point(1, 1, 6))


    def test_subtraction__vector_point(self):
        """test that we can subtract a vector from a point"""

        a1 = points.Point(3, 2, 1)
        a2 = vectors.Vector(5, 6, 7)

        a3 = a1 - a2

        self.assertEqual(a3, points.Point(-2, -4, -6))


    def test_subtraction__vector_vector(self):
        """test that we can subtract two vectors"""

        a1 = vectors.Vector(3, 2, 1)
        a2 = vectors.Vector(5, 6, 7)

        a3 = a1 - a2

        self.assertEqual(a3, vectors.Vector(-2, -4, -6))


    def test_negation(self):
        """Test that we can negate a vector"""

        a1 = tuples.Tuple(["a", "b", "c", "d"], 1, -2, 3, -4)

        a2 = -a1

        self.assertEqual(a2,
            tuples.Tuple(["a", "b", "c", "d"], -1, 2, -3, 4))


    def test_scalar_multiplication(self):
        """Test that we can multiple a vector by a scalar"""

        a1 = tuples.Tuple(["a", "b", "c", "d"], 1, -2, 3, -4)
        a2 = a1 * 3.5
        a3 = a1 * 0.5

        self.assertEqual(a2,
            tuples.Tuple(["a", "b", "c", "d"], 3.5, -7, 10.5, -14))
        self.assertEqual(a3,
            tuples.Tuple(["a", "b", "c", "d"], 0.5, -1, 1.5, -2))

    def test_scalar_division(self):
        """Test that we can divide a tuple by a scalar"""

        a1 = tuples.Tuple(["a", "b", "c", "d"], 1, -2, 3, -4)

        a2 = a1 / 2

        self.assertEqual(a2,
            tuples.Tuple(["a", "b", "c", "d"], 0.5, -1, 1.5, -2))

    def test_magnitude(self):
        """Test that we can calculate the magnitude of a vector"""

        a1 = vectors.Vector(1, 2, 3)
        self.assertEqual(a1.magnitude(), math.sqrt(14))

        a1 = vectors.Vector(-1, -2, -3)
        self.assertEqual(a1.magnitude(), math.sqrt(14))

        a1 = vectors.Vector(1, 0, 0)
        self.assertEqual(a1.magnitude(), 1)

        a1 = vectors.Vector(0, 1, 0)
        self.assertEqual(a1.magnitude(), 1)

        a1 = vectors.Vector(0, 0, 1)
        self.assertEqual(a1.magnitude(), 1)

    def test_normalize(self):
        """Test that we can normalize a vector"""

        a1 = vectors.Vector(4, 0, 0)
        self.assertEqual(a1.normalize(),
             vectors.Vector(1, 0, 0))

        a1 = vectors.Vector(0, 4, 0)
        self.assertEqual(a1.normalize(),
             vectors.Vector(0, 1, 0))

        a1 = vectors.Vector(0, 0, 4)
        self.assertEqual(a1.normalize(),
             vectors.Vector(0, 0, 1))

    def test_magnitude_normalize(self):
        """Test the magnitude of a normalized vector is 1"""

        a1 = vectors.Vector(1, 2, 3)
        self.assertEqual(a1.normalize().magnitude(), 1)


    def test_reflection_vector(self):
        """Test we can calculate reflections"""

        # A ray approaching at 45 degrees
        v = vectors.Vector(1, -1, 0)
        n =  vectors.Vector(0, 1, 0)
        r = v.reflect(n)
        self.assertEqual(r, vectors.Vector(1, 1, 0))

        # Ray along an axis hits a surface at an angle
        v = vectors.Vector(0, -1, 0)
        n =  vectors.Vector(math.sqrt(2)/2, math.sqrt(2)/2, 0)
        r = v.reflect(n)
        self.assertEqual(r, vectors.Vector(1, 0, 0))

if __name__ == "__main__":
    unittest.main()
