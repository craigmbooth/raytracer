import math
import unittest

import raytracer.colors

class TestColors(unittest.TestCase):
    """Tests on the Color class"""

    def test_color__tuple(self):
        """Test that we can initialize and read from a color"""

        p = raytracer.colors.Color(-0.5, 0.4, 1.7)

        self.assertEqual(p.red, -0.5)
        self.assertEqual(p.green, 0.4)
        self.assertEqual(p.blue, 1.7)

    def test_color_basic_operations(self):
        """Test that the basic operations work on colors"""

        c1 = raytracer.colors.Color(0.9, 0.6, 0.75)
        c2 = raytracer.colors.Color(0.7, 0.1, 0.25)

        c3 = c1 + c2
        self.assertEqual(c3, raytracer.colors.Color(1.6, 0.7, 1.0))

        c4 = c1 - c2
        self.assertEqual(c4, raytracer.colors.Color(0.2, 0.5, 0.5))

        c5 = c1 * 2
        self.assertEqual(c5, raytracer.colors.Color(1.8, 1.2, 1.5))


    def test_color_multiplication(self):
        """Test that we can multiple two colors"""

        c1 = raytracer.colors.Color(1, 0.2, 0.4)
        c2 = raytracer.colors.Color(0.9, 1, 0.1)

        c3 = c1 * c2

        self.assertEqual(c3, raytracer.colors.Color(0.9, 0.2, 0.04))

if __name__ == "__main__":
    unittest.main()
