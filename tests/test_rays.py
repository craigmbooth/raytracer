import unittest

import rays
import points
import vectors
import transforms

class TestRays(unittest.TestCase):

    def test_position(self):

        origin = points.Point(2, 3, 4)
        direction = vectors.Vector(1, 0, 0)
        r = rays.Ray(origin, direction)

        self.assertEqual(r.position(0), origin)
        self.assertEqual(r.position(1), points.Point(3, 3, 4))
        self.assertEqual(r.position(-1), points.Point(1, 3, 4))
        self.assertEqual(r.position(2.5), points.Point(4.5, 3, 4))


    def test_ray_transforms(self):
        """Test that we can transform a ray"""

        origin = points.Point(1, 2, 3)
        direction = vectors.Vector(0, 1, 0)
        r = rays.Ray(origin, direction)

        r2 = r.transform(transforms.Translate(3, 4, 5))
        self.assertEqual(r2.origin, points.Point(4, 6, 8))
        self.assertEqual(r2.direction, vectors.Vector(0, 1, 0))

        r3 = r.transform(transforms.Scale(2, 3, 4))
        self.assertEqual(r3.origin, points.Point(2, 6, 12))
        self.assertEqual(r3.direction, vectors.Vector(0, 3, 0))


if __name__ == "__main__":
    unittest.main()
