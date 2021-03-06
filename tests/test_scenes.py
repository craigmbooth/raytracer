import copy
import math
import unittest

import colors
import intersections
import lights
import materials
import patterns
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

        color, _ = self.default_scene.shade_hit(computations)
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

        color, _ = self.default_scene.shade_hit(computations)

        self.assertEqual(color, colors.Color(0.90498, 0.90498, 0.90498))

    def test_color_at(self):
        """Tests on the color_at function"""

        # The ray points away from the object
        r = rays.Ray(
            points.Point(0, 0, -5),
            vectors.Vector(0, 1, 0)
            )
        self.assertEqual(
            self.default_scene.color_at(r)[0],
            colors.Color(0, 0, 0)
            )

        # The ray points at the outer sphere
        r = rays.Ray(
            points.Point(0, 0, -5),
            vectors.Vector(0, 0, 1)
            )
        self.assertEqual(
            self.default_scene.color_at(r)[0],
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
            scene.color_at(r)[0],
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

        result, _ = scene.shade_hit(comps)

        self.assertEqual(result, colors.Color(0.1, 0.1, 0.1))


    def test_reflection__reflective(self):
        """Test the reflection color of a reflective material is not black"""

        p = shapes.Plane(
            material=materials.Material(reflective=0.5)
            )
        p.set_transform(transforms.Translate(0, -1, 0))

        world = copy.deepcopy(self.default_scene)

        world.objects.append(p)

        r = rays.Ray(points.Point(0, 0, -3),
                     vectors.Vector(0, -math.sqrt(2)/2, math.sqrt(2)/2))

        i = intersections.Intersection(p, math.sqrt(2))

        comps = i.precompute(r)

        # Test reflected color alone
        result, _ = world.reflected_color(comps)
        self.assertEqual(result, colors.Color(0.19032, 0.2379, 0.14274))

        # Now test the reflected color is added to the surface color
        result, _ = world.shade_hit(comps)
        self.assertEqual(result, colors.Color(0.87677, 0.92436, 0.82918))


    def test_reflection__non_reflective(self):
        """Test the reflection color of a nonreflective material is not black"""

        world = copy.deepcopy(self.default_scene)

        s = world.objects[0]
        s.material.ambient = 1

        # The ray is inside the inner sphere of the default scene
        r = rays.Ray(points.Point(0, 0, 0),
                     vectors.Vector(0, 0, 1))

        i = intersections.Intersection(s, 1)

        comps = i.precompute(r)

        result, _ = world.reflected_color(comps)

        self.assertEqual(result, colors.Color(0, 0, 0))


    def test_reflection__infinite_recursion(self):
        """Test that we don't break if there is infinite recursion"""

        # Two parallel planes
        s1 = shapes.Plane(material=materials.Material(reflective=1))
        s1.set_transform(transforms.Translate(0, -1, 0))


        # Second sphere is at the origin
        s2 = shapes.Plane(material=materials.Material(reflective=1))
        s2.set_transform(transforms.Translate(0, 1, 0))


        # Light is at z=-10
        l1 = lights.Light(
            position=points.Point(0, 0, 0),
            intensity=colors.Color(1, 1, 1)
            )

        scene = scenes.Scene(
            objects = [s1, s2],
            lights = [l1]
        )

        r = rays.Ray(points.Point(0, 0, 0), vectors.Vector(0, 1, 0))

        # If this is working the following will NOT cause a stack trace
        scene.color_at(r)


    def test_refraction__opaque(self):
        """Test the refraction color of an opaque material is black"""

        world = copy.deepcopy(self.default_scene)

        s = world.objects[1]

        r = rays.Ray(points.Point(0, 0, -5),
                     vectors.Vector(0, 0, 1))

        xs = intersections.Intersections(
            intersections.Intersection(s, 4),
            intersections.Intersection(s, 6))

        comps = xs.intersections[0].precompute(r, all_intersections=xs)

        result, _ = world.refracted_color(comps, 5)

        self.assertEqual(result, colors.Color(0, 0, 0))

    def test_refraction__recursion_limit(self):
        """Test that we return black if we hit the refraction limit"""

        world = copy.deepcopy(self.default_scene)

        s = world.objects[1]

        s.material.transparency = 1.0
        s.material.refractive_index = 1.5

        r = rays.Ray(points.Point(0, 0, -5),
                     vectors.Vector(0, 0, 1))

        xs = intersections.Intersections(
            intersections.Intersection(s, 4),
            intersections.Intersection(s, 6))

        comps = xs.intersections[0].precompute(r, all_intersections=xs)

        result, _ = world.refracted_color(comps, 0)

        self.assertEqual(result, colors.Color(0, 0, 0))


    def test_refraction__total_internal_reflection(self):
        """Test that we return black if we hit total internal reflection"""

        world = copy.deepcopy(self.default_scene)

        s = world.objects[1]

        s.material.transparency = 1.0
        s.material.refractive_index = 1.5

        r = rays.Ray(points.Point(0, 0, math.sqrt(2)/2),
                     vectors.Vector(0, 1, 0))

        xs = intersections.Intersections(
            intersections.Intersection(s, -math.sqrt(2)/2),
            intersections.Intersection(s, math.sqrt(2)/2))

        # n.b. the camera is inside the inner-sphere so use the second
        # intersection
        comps = xs.intersections[1].precompute(r, all_intersections=xs)

        result, _ = world.refracted_color(comps, 5)

        self.assertEqual(result, colors.Color(0, 0, 0))


    def test_refraction__standard(self):
        """Test that we return the correct color under normal refraction"""

        world = copy.deepcopy(self.default_scene)

        # s1 = A
        s1 = world.objects[1]
        s1.material.ambient = 1.0
        s1.material.pattern = patterns.TestPattern()

        # s2 = B
        s2 = world.objects[0]
        s2.material.transparency = 1.0
        s2.material.refractive_index = 1.5


        r = rays.Ray(points.Point(0, 0, 0.1),
                     vectors.Vector(0, 1, 0))

        xs = intersections.Intersections(
            intersections.Intersection(s1, -0.9899),
            intersections.Intersection(s2, -0.4899),
            intersections.Intersection(s2, 0.4899),
            intersections.Intersection(s1, 0.9899))

        # Intersections[2] because the first two are behind the camera
        comps = xs.intersections[2].precompute(r, all_intersections=xs)

        result, _ = world.refracted_color(comps, 5)

        # Remember the test pattern returns the x, y, z coordinates of the
        # input point as the color so we can inspect positions
        self.assertEqual(result, colors.Color(0, 0.99888, 0.0475))


    def test_refraction__shading(self):
        """Test we can shade a pixel with a semi-transparent object"""

        world = copy.deepcopy(self.default_scene)

        floor = shapes.Plane(
            material=materials.Material(
                transparency=0.5,
                refractive_index=1.5))
        floor.set_transform(transforms.Translate(0, -1, 0))

        ball = shapes.Sphere(
            material=materials.Material(
                color=colors.Color(1, 0, 0),
                ambient=0.5
                )
            )
        ball.set_transform(transforms.Translate(0, -3.5, -0.5))

        r = rays.Ray(points.Point(0, 0, -3),
                     vectors.Vector(0, -math.sqrt(2)/2, math.sqrt(2)/2))
        xs = intersections.Intersections(
            intersections.Intersection(floor, math.sqrt(2))
            )

        world.add_object(floor)
        world.add_object(ball)

        comps = xs.intersections[0].precompute(r, all_intersections=xs)

        color, _ = world.shade_hit(comps, remaining=5)

        self.assertEqual(color,
                         colors.Color(0.93642, 0.68642, 0.68642))

    def test_reflective_transparent_material(self):
        """Test shade_hit with a reflective, transparent material"""

        world = copy.deepcopy(self.default_scene)

        floor = shapes.Plane(
            material=materials.Material(
                reflective=0.5,
                transparency=0.5,
                refractive_index=1.5))
        floor.set_transform(transforms.Translate(0, -1, 0))

        ball = shapes.Sphere(
            material=materials.Material(
                color=colors.Color(1, 0, 0),
                ambient=0.5
                )
            )
        ball.set_transform(transforms.Translate(0, -3.5, -0.5))

        r = rays.Ray(points.Point(0, 0, -3),
                     vectors.Vector(0, -math.sqrt(2)/2, math.sqrt(2)/2))
        xs = intersections.Intersections(
            intersections.Intersection(floor, math.sqrt(2))
            )

        world.add_object(floor)
        world.add_object(ball)

        comps = xs.intersections[0].precompute(r, all_intersections=xs)

        color, _ = world.shade_hit(comps, remaining=5)

        self.assertEqual(color,
                         colors.Color(0.93391, 0.69643, 0.69243))


if __name__ == "__main__":
    unittest.main()
