import math
import unittest

import tuples
import points

class TestPoints(unittest.TestCase):
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

if __name__ == "__main__":
    unittest.main()
