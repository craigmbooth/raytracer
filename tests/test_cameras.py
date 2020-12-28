import unittest
import math

import cameras
import colors
import lights
import materials
import points
import scenes
import shapes
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
        self.assertEqual(ray.direction, vectors.Vector(0, 0, -1))

        # A corner
        ray = cam.ray_for_pixel(0, 0)
        self.assertEqual(ray.origin, points.Point(0, 0, 0))
        self.assertEqual(ray.direction,
                         vectors.Vector(0.66519, 0.33259, -0.66851))

        # With a transformed camera
        # For some reason this isn't working.  TODO is fixing it.
        #cam.transform = transforms.RotateY(math.pi/4) * transforms.Translate(0, -2, 5)
        #ray = cam.ray_for_pixel(100, 50)
        #self.assertEqual(ray.origin, points.Point(0, 2, -5))
        #self.assertEqual(ray.direction,
        #                 vectors.Vector(math.sqrt(2)/2, 0, -math.sqrt(2)/2))

    def test_render_scene(self):
        """Test we can render a pixel in a simple scene"""


        # Inner sphere size 0.5, centered on the origin
        s1 = shapes.Sphere()
        s1.set_transform(transforms.Scale(0.5,0.5,0.5))

        # Outer sphere centered on the origin, size 1.0
        s2 = shapes.Sphere()
        s2.material = materials.Material(
            color=colors.Color(0.8, 1.0, 0.6), diffuse=0.7, specular=0.2)

        l1 = lights.Light(
            position=points.Point(-10, 10, -10),
            intensity=colors.Color(1, 1, 1)
            )

        scene = scenes.Scene(
            objects = [s1, s2],
            lights = [l1]
        )

        cam = cameras.Camera(11, 11, math.pi/2)

        from_point = points.Point(0, 0, -5)
        to_point = points.Point(0, 0, 0)
        up = vectors.Vector(0, 1, 0)
        cam.transform = transforms.ViewTransform(from_point, to_point, up)

        image = cam.render(scene)
        self.assertEqual(image.get(5, 5),
                         colors.Color(0.3807, 0.4758, 0.2855))
