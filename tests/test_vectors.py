import math
import unittest

import tuples
import vectors

class TestVectors(unittest.TestCase):
    """Tests on the Vector class"""

    def test_vector__tuple(self):
        """Test that we can initialize and read from a vector as a tuple"""

        v = tuples.Tuple(["x", "y", "z", "w"], 4.3, -4.2, 3.1, 0)

        self.assertEqual(v.x, 4.3)
        self.assertEqual(v.y, -4.2)
        self.assertEqual(v.z, 3.1)
        self.assertEqual(v.w, 0)

    def test_vector(self):
        """Test that we can initialize and read from a vector as a tuple"""

        v = vectors.Vector(4.3, -4.2, 3.1)

        self.assertEqual(v.x, 4.3)
        self.assertEqual(v.y, -4.2)
        self.assertEqual(v.z, 3.1)
        self.assertEqual(v.w, 0)

    def test_dot_product(self):
        """Test dot product between two vectors"""

        a1 = vectors.Vector(1, 2, 3)
        a2 = vectors.Vector(2, 3, 4)

        self.assertEqual(a1.dot(a2), 20)

    def test_cross_product(self):
        """Test cross product between two vectors"""

        a1 = vectors.Vector(1, 2, 3)
        a2 = vectors.Vector(2, 3, 4)

        self.assertEqual(a1.cross(a2),
                         vectors.Vector(-1, 2, -1))

        self.assertEqual(a2.cross(a1),
                         vectors.Vector(1, -2, 1))


if __name__ == "__main__":
    unittest.main()
