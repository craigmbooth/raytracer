import unittest
import math

import cameras
import points
import transforms
import vectors

class TestCamera(unittest.TestCase):


    def test_initialization(self):
        """Test that attributes are stored on initialization"""

        cam = cameras.Camera(400, 300, math.pi/2)

        self.assertEqual(cam.hsize, 400)
        self.assertEqual(cam.vsize, 300)
        self.assertEqual(cam.field_of_view, math.pi/2)


    def test_pixel_size(self):
        """Test that pixel size is correctly calculated"""

        cam1 = cameras.Camera(200, 125, math.pi/2)
        cam2 = cameras.Camera(125, 200, math.pi/2)

        self.assertAlmostEqual(cam1.pixel_size, 0.01)
        self.assertAlmostEqual(cam2.pixel_size, 0.01)


    def test_ray_for_pixel(self):
        """Test we can fire a ray through any pixel"""

        cam = cameras.Camera(201, 101, math.pi/2)

        # Middle of the screen
        ray = cam.ray_for_pixel(100, 50)
        self.assertEqual(ray.origin, points.Point(0, 0, 0))
        self.assertEqual(ray.direction, vectors.Vectors(0, 0, -1))

        # A corner
        ray = cam.ray_for_pixel(0, 0)
        self.assertEqual(ray.origin, points.Point(0, 0, 0))
        self.assertEqual(ray.direction,
                         vectors.Vectors(0.66519, 0.33259, -0.66851))

        # With a transformed camera
        cam.transform = transforms.RotateY(math.pi/4) * \
                        transforms.Translate(0, -2, 5)

        ray = cam.ray_for_pixel(100, 50)
        self.assertEqual(ray.origin, points.Point(0, 2, -5))
        self.assertEqual(ray.direction,
                         vectors.Vectors(sqrt(2)/2, 0, -sqrt(2)/2))
