import unittest

import lights
import points
import colors


class TestLights(unittest.TestCase):

    def test_point_light_initialization(self):

        position = points.Point(-1, 3, 5)
        intensity = colors.Color(0.5, 1, 1)
        light = lights.PointLight(position, intensity)

        self.assertEqual(light.position, position)
        self.assertEqual(light.intensity, intensity)

if __name__ == "__main__":
    unittest.main()
