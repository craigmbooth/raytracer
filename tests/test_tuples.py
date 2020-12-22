import math
import unittest

import raytracer.tuples

class TestTuples(unittest.TestCase):

    def test_point__tuple(self):
        """Test that we can initialize and read from a point as a tuple"""

        p = raytracer.tuples.Tuple(4.3, -4.2, 3.1, 1)

        self.assertEqual(p.x, 4.3)
        self.assertEqual(p.y, -4.2)
        self.assertEqual(p.z, 3.1)
        self.assertEqual(p.w, 1)
        self.assertEqual(p.type, "point")


    def test_vector__tuple(self):
        """Test that we can initialize and read from a vector as a tuple"""

        v = raytracer.tuples.Tuple(4.3, -4.2, 3.1, 0)

        self.assertEqual(v.x, 4.3)
        self.assertEqual(v.y, -4.2)
        self.assertEqual(v.z, 3.1)
        self.assertEqual(v.w, 0)

    def test_point(self):
        """Test that we can initialize and read from a point"""

        p = raytracer.tuples.Tuple.point(4.3, -4.2, 3.1)

        self.assertEqual(p.x, 4.3)
        self.assertEqual(p.y, -4.2)
        self.assertEqual(p.z, 3.1)
        self.assertEqual(p.w, 1)
        self.assertEqual(p.type, "point")


    def test_vector__tuple(self):
        """Test that we can initialize and read from a vector as a tuple"""

        v = raytracer.tuples.Tuple.vector(4.3, -4.2, 3.1)

        self.assertEqual(v.x, 4.3)
        self.assertEqual(v.y, -4.2)
        self.assertEqual(v.z, 3.1)
        self.assertEqual(v.w, 0)


    def test_addition(self):
        """test that we can add a vector to a point"""

        a1 = raytracer.tuples.Tuple.point(3, -2, 5)
        a2 = raytracer.tuples.Tuple.vector(-2, 3, 1)

        a3 = a1 + a2

        self.assertEqual(a3, raytracer.tuples.Tuple.point(1, 1, 6))
        self.assertEqual(a3, raytracer.tuples.Tuple(1, 1, 6, 1))


    def test_subtraction__vector_point(self):
        """test that we can subtract a vector from a point"""

        a1 = raytracer.tuples.Tuple.point(3, 2, 1)
        a2 = raytracer.tuples.Tuple.vector(5, 6, 7)

        a3 = a1 - a2

        self.assertEqual(a3, raytracer.tuples.Tuple.point(-2, -4, -6))


    def test_subtraction__vector_vector(self):
        """test that we can subtract two vectors"""

        a1 = raytracer.tuples.Tuple.vector(3, 2, 1)
        a2 = raytracer.tuples.Tuple.vector(5, 6, 7)

        a3 = a1 - a2

        self.assertEqual(a3, raytracer.tuples.Tuple.vector(-2, -4, -6))


    def test_negation(self):
        """Test that we can negate a vector"""

        a1 = raytracer.tuples.Tuple(1, -2, 3, -4)
        a2 = -a1
        self.assertEqual(a2, raytracer.tuples.Tuple(-1, 2, -3, 4))


    def test_scalar_multiplication(self):
        """Test that we can multiple a vector by a scalar"""

        a1 = raytracer.tuples.Tuple(1, -2, 3, -4)
        a2 = a1 * 3.5
        a3 = a1 * 0.5

        self.assertEqual(a2, raytracer.tuples.Tuple(3.5, -7, 10.5, -14))
        self.assertEqual(a3, raytracer.tuples.Tuple(0.5, -1, 1.5, -2))

    def test_scalar_division(self):
        """Test that we can divide a tuple by a scalar"""

        a1 = raytracer.tuples.Tuple(1, -2, 3, -4)
        a2 = a1 / 2

        self.assertEqual(a2, raytracer.tuples.Tuple(0.5, -1, 1.5, -2))

    def test_magnitude(self):
        """Test that we can calculate the magnitude of a vector"""

        a1 = raytracer.tuples.Tuple.vector(1, 2, 3)
        self.assertEqual(a1.magnitude(), math.sqrt(14))

        a1 = raytracer.tuples.Tuple.vector(-1, -2, -3)
        self.assertEqual(a1.magnitude(), math.sqrt(14))

        a1 = raytracer.tuples.Tuple.vector(1, 0, 0)
        self.assertEqual(a1.magnitude(), 1)

        a1 = raytracer.tuples.Tuple.vector(0, 1, 0)
        self.assertEqual(a1.magnitude(), 1)

        a1 = raytracer.tuples.Tuple.vector(0, 0, 1)
        self.assertEqual(a1.magnitude(), 1)




if __name__ == "__main__":
    unittest.main()
