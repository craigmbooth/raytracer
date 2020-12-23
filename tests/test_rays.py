import unittest

import raytracer.rays
import raytracer.points
import raytracer.vectors

class TestRays(unittest.TestCase):

    def test_position(self):

        origin = raytracer.points.Point(2, 3, 4)
        direction = raytracer.vectors.Vector(1, 0, 0)
        r = raytracer.rays.Ray(origin, direction)

        self.assertEqual(r.position(0), origin)
        self.assertEqual(r.position(1), raytracer.points.Point(3, 3, 4))
        self.assertEqual(r.position(-1), raytracer.points.Point(1, 3, 4))
        self.assertEqual(r.position(2.5), raytracer.points.Point(4.5, 3, 4))

if __name__ == "__main__":
    unittest.main()
