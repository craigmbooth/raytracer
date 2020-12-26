import copy
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

        # Inner sphere size 0.5, centered on the origin
        self.s1 = shapes.Sphere()
        self.s1.set_transform(transforms.Scale(0.5,0.5,0.5))

        # Outer sphere centered on the origin, size 1.0
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

    def test_color_at(self):
        """Tests on the color_at function"""

        # The ray points away from the object
        r = rays.Ray(
            points.Point(0, 0, -5),
            vectors.Vector(0, 1, 0)
            )
        self.assertEqual(
            self.default_scene.color_at(r),
            colors.Color(0, 0, 0)
            )

        # The ray points at the outer sphere
        r = rays.Ray(
            points.Point(0, 0, -5),
            vectors.Vector(0, 0, 1)
            )
        self.assertEqual(
            self.default_scene.color_at(r),
            colors.Color(0.38066, 0.47583, 0.2855)
            )

        # The ray is outside the inner sphere, but inside the outer sphere,
        # pointing in.  It should return the color of the inner sphere
        scene = copy.deepcopy(self.default_scene)
        scene.objects[0].material.ambient = 1
        scene.objects[1].material.ambient = 1
        r = rays.Ray(
            points.Point(0, 0, 0.75),
            vectors.Vector(0, 0, -1)
            )
        self.assertEqual(
            scene.color_at(r),
            scene.objects[0].material.color
            )

    def test_is_shadowed(self):
        """Test we find shadows appropriately"""

        # Directly illuminated
        self.assertFalse(self.default_scene.is_shadowed(
            points.Point(0, 10, 0), self.default_scene.lights[0]))

        # Behind the sphere
        self.assertTrue(self.default_scene.is_shadowed(
            points.Point(10, -10, 10), self.default_scene.lights[0]))

        # Light between point and object
        self.assertFalse(self.default_scene.is_shadowed(
            points.Point(-20, 20, -20), self.default_scene.lights[0]))

        # Point between light and object
        self.assertFalse(self.default_scene.is_shadowed(
            points.Point(-2, 2, -2), self.default_scene.lights[0]))

        # Point inside object
        self.assertTrue(self.default_scene.is_shadowed(
            points.Point(-0.5, 0.5, -0.5), self.default_scene.lights[0]))

    def test_shadows__full_scene(self):
        """Test that we identify a shadow in a full scene"""

        # First sphere is at z=10
        s1 = shapes.Sphere()
        s1.set_transform(transforms.Translate(0, 0, 10))

        # Second sphere is at the origin
        s2 = shapes.Sphere()
        s2.material = materials.Material()

        # Light is at z=-10
        l1 = lights.Light(
            position=points.Point(0, 0, -10),
            intensity=colors.Color(1, 1, 1)
            )

        scene = scenes.Scene(
            objects = [s1, s2],
            lights = [l1]
        )

        # The ray is at z=5 (i.e. between the spheres), pointing at the further
        # out sphere
        ray = rays.Ray(points.Point(0, 0, 5),
                       vectors.Vector(0, 0,1))

        isection = intersections.Intersection(s2, 4)
        comps = isection.precompute(ray)

        result = scene.shade_hit(comps)

        self.assertEqual(result, colors.Color(0.1, 0.1, 0.1))
