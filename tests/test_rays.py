import unittest

import raytracer.rays
import raytracer.points
import raytracer.vectors
import raytracer.transforms

class TestRays(unittest.TestCase):

    def test_position(self):

        origin = raytracer.points.Point(2, 3, 4)
        direction = raytracer.vectors.Vector(1, 0, 0)
        r = raytracer.rays.Ray(origin, direction)

        self.assertEqual(r.position(0), origin)
        self.assertEqual(r.position(1), raytracer.points.Point(3, 3, 4))
        self.assertEqual(r.position(-1), raytracer.points.Point(1, 3, 4))
        self.assertEqual(r.position(2.5), raytracer.points.Point(4.5, 3, 4))


    def test_ray_transforms(self):
        """Test that we can transform a ray"""

        origin = raytracer.points.Point(1, 2, 3)
        direction = raytracer.vectors.Vector(0, 1, 0)
        r = raytracer.rays.Ray(origin, direction)

        r2 = r.transform(raytracer.transforms.Translate(3, 4, 5))
        self.assertEqual(r2.origin, raytracer.points.Point(4, 6, 8))
        self.assertEqual(r2.direction, raytracer.vectors.Vector(0, 1, 0))

        r3 = r.transform(raytracer.transforms.Scale(2, 3, 4))
        self.assertEqual(r3.origin, raytracer.points.Point(2, 6, 12))
        self.assertEqual(r3.direction, raytracer.vectors.Vector(0, 3, 0))


if __name__ == "__main__":
    unittest.main()
