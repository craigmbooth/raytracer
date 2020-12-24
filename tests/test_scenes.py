import unittest

import colors
import intersections
import lights
import materials
import points
import rays
import scenes
import shapes
import transforms
import vectors

class TestScenes(unittest.TestCase):


    def setUp(self):
        """Set up a default scene for quick testing"""

        self.s1 = shapes.Sphere()
        self.s1.set_transform(transforms.Scale(0.5,0.5,0.5))

        self.s2 = shapes.Sphere()
        self.s2.material = materials.Material(
            color=colors.Color(0.8, 1.0, 0.6), diffuse=0.7, specular=0.2)

        self.l1 = lights.Light(
            position=points.Point(-10, 10, -10),
            intensity=colors.Color(1, 1, 1)
            )

        self.default_scene = scenes.Scene(
            objects = [self.s1, self.s2],
            lights = [self.l1]

        )

    def test_default_scene(self):
        """Test that the default scene is correct"""

        self.assertEqual(self.default_scene.lights[0].intensity,
                         colors.Color(1, 1, 1))

        self.assertEqual(self.default_scene.objects[0], self.s1)

    def test_intersect_scene(self):
        """Test that we can intersect an entire scene"""

        r = rays.Ray(
            points.Point(0, 0, -5),
            vectors.Vector(0, 0, 1)
            )

        result = self.default_scene.intersect(r)

        ts = [x.t for x in result.intersections]
        self.assertEqual(ts, [4, 4.5, 5.5, 6])

    def test_shade_hit__outside(self):
        """Test that we shade an individual hit the correct color when outside
        an object"""

        r = rays.Ray(
            points.Point(0, 0, -5),
            vectors.Vector(0, 0, 1)
            )

        shape = self.default_scene.objects[1]

        i = intersections.Intersection(shape, 4)
        computations = i.precompute(r)

        color = self.default_scene.shade_hit(computations)
        self.assertEqual(color, colors.Color(0.38066, 0.47583, 0.2855))


    def test_shade_hit__inside(self):
        """Test that we shade an individual hit the correct color when inside
        an object"""

        r = rays.Ray(
            points.Point(0, 0, 0),
            vectors.Vector(0, 0, 1)
            )

        self.default_scene.lights = [lights.PointLight(
            points.Point(0, 0.25, 0), colors.Color(1, 1, 1)
            )]

        shape = self.default_scene.objects[0]

        i = intersections.Intersection(shape, 0.5)
        computations = i.precompute(r)

        color = self.default_scene.shade_hit(computations)

        self.assertEqual(color, colors.Color(0.90498, 0.90498, 0.90498))
