import unittest

import raytracer.lights
import raytracer.points
import raytracer.colors


class TestLights(unittest.TestCase):

    def test_point_light_initialization(self):

        position = raytracer.points.Point(-1, 3, 5)
        intensity = raytracer.colors.Color(0.5, 1, 1)
        light = raytracer.lights.PointLight(position, intensity)

        self.assertEqual(light.position, position)
        self.assertEqual(light.intensity, intensity)

if __name__ == "__main__":
    unittest.main()
