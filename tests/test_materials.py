import unittest

import raytracer.materials
import raytracer.points

class TestMaterials(unittest.TestCase):

    def test_default_material(self):
        """Test we can initialize a material and set its properties"""

        mat1 = raytracer.materials.Material()
        self.assertEqual(mat1.ambient, 0.1)
        self.assertEqual(mat1.shininess, 200)

        mat2 = raytracer.materials.Material(ambient=0.2)
        self.assertEqual(mat2.ambient, 0.2)
        self.assertEqual(mat2.shininess, 200)


    def test_lighting(self):
        """Tests on the lighting function for various angles and colors"""

        m = raytracer.materials.Material()
        p = raytracer.points.Point(0, 0, 0)

        #the eye is positioned directly between the light and the surface, with
        #the normal pointing at the eye. Expect ambient, diffuse, and specular
        #to all be at full strength. This means that the total intensity should
        #be 0.1 (the ambient value) + 0.9 (the diffuse value) + 0.9 (the
        #specular value), or 1.9
        eyev = raytracer.vectors.Vector(0, 0, -1)
        normalv = raytracer.vectors.Vector(0, 0, -1)
        light = raytracer.lights.PointLight(
            raytracer.points.Point(0, 0, -10),
            raytracer.colors.Color(1, 1, 1))

        result = m.lighting(light, p, eyev, normalv)
        self.assertEqual(result, raytracer.colors.Color(1.9, 1.9, 1.9))



if __name__ == "__main__":
    unittest.main()
