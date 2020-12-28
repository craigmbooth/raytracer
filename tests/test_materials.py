import math
import unittest

import colors
import lights
import materials
import points
import vectors

class TestMaterials(unittest.TestCase):

    def test_default_material(self):
        """Test we can initialize a material and set its properties"""

        mat1 = materials.Material()
        self.assertEqual(mat1.ambient, 0.1)
        self.assertEqual(mat1.shininess, 200)
        self.assertEqual(mat1.reflective, 0)
        self.assertEqual(mat1.refractive_index, 1.0)

        mat2 = materials.Material(ambient=0.2)
        self.assertEqual(mat2.ambient, 0.2)
        self.assertEqual(mat2.shininess, 200)


    def test_lighting(self):
        """Tests on the lighting function for various angles and colors"""

        m = materials.Material()
        p = points.Point(0, 0, 0)

        #the eye is positioned directly between the light and the surface, with
        #the normal pointing at the eye. Expect ambient, diffuse, and specular
        #to all be at full strength. This means that the total intensity should
        #be 0.1 (the ambient value) + 0.9 (the diffuse value) + 0.9 (the
        #specular value), or 1.9
        eyev = vectors.Vector(0, 0, -1)
        normalv = vectors.Vector(0, 0, -1)
        light = lights.PointLight(
            points.Point(0, 0, -10),
            colors.Color(1, 1, 1))

        result = m.lighting(light, p, eyev, normalv)
        self.assertEqual(result, colors.Color(1.9, 1.9, 1.9))

        eyev = vectors.Vector(0, math.sqrt(2)/2, -math.sqrt(2)/2)
        normalv = vectors.Vector(0, 0, -1)
        light = lights.PointLight(
            points.Point(0, 0, -10),
            colors.Color(1, 1, 1))
        result = m.lighting(light, p, eyev, normalv)
        self.assertEqual(result, colors.Color(1.0, 1.0, 1.0))

        eyev = vectors.Vector(0, 0, -1)
        normalv = vectors.Vector(0, 0, -1)
        light = lights.PointLight(
            points.Point(0, 10, -10),
            colors.Color(1, 1, 1))
        result = m.lighting(light, p, eyev, normalv)
        self.assertEqual(result, colors.Color(0.7364, 0.7364, 0.7364))


        eyev = vectors.Vector(0, -math.sqrt(2)/2, -math.sqrt(2)/2)
        normalv = vectors.Vector(0, 0, -1)
        light = lights.PointLight(
            points.Point(0, 10, -10),
            colors.Color(1, 1, 1))
        result = m.lighting(light, p, eyev, normalv)
        self.assertEqual(result, colors.Color(1.6364, 1.6364, 1.6364))

        # Light behind the object, its color should be the ambient value
        eyev = vectors.Vector(0, 0, -1)
        normalv = vectors.Vector(0, 0, -1)
        light = lights.PointLight(
            points.Point(0, 0, 10),
            colors.Color(1, 1, 1))

        result = m.lighting(light, p, eyev, normalv)
        self.assertEqual(result, colors.Color(0.1, 0.1, 0.1))


    def test_lighting__shadow(self):
        """Test that we get the ambient color if we're in shadow"""

        m = materials.Material()
        p = points.Point(0, 0, 0)

        eyev = vectors.Vector(0, 0, -1)
        normalv = vectors.Vector(0, 0, -1)
        light = lights.PointLight(
            points.Point(0, 0, -10),
            colors.Color(1, 1, 1))
        result = m.lighting(light, p, eyev, normalv, in_shadow=True)
        self.assertEqual(result, colors.Color(0.1, 0.1, 0.1))


if __name__ == "__main__":
    unittest.main()
