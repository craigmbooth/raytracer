import unittest

import raytracer.exceptions
import raytracer.matrices
import raytracer.transforms
import raytracer.points
import raytracer.vectors

class TestIdentity(unittest.TestCase):
    """Tests on the identity matrix"""

    def test_identity_matrix_mult(self):
        """Test we can identify the identity matrix by a matrix and tuple"""

        ident = raytracer.transforms.Identity(3)

        M = raytracer.matrices.Matrix(3, 3)
        M.set_row(0, [1, 2, 3])
        M.set_row(1, [3, 2, 1])
        M.set_row(2, [2, 4, 6])

        M2 = M * ident
        self.assertEqual(M2, M)

        t = raytracer.tuples.Tuple(["a", "b", "c"], 1, 2, 3)
        t2 = ident * t
        self.assertEqual(t2, t)

    def test_identity_matrix_transpose(self):
        """Test that the transpose of the identity matrix is identity"""

        ident = raytracer.transforms.Identity(5)
        self.assertEqual(ident.transpose(), ident)


class TestTranslate(unittest.TestCase):
    """Tests on the translating matrix"""

    def test_translate_point(self):
        """Test that if we multiply a translate matrix by a point it moves it"""

        p = raytracer.points.Point(-3, 4, 5)
        T = raytracer.transforms.Translate(5, -3, 2)

        p2 = T * p
        self.assertEqual(p2, raytracer.points.Point(2, 1, 7))

        # Translating by the inverse of the translate matrix moves the
        # opposite direction

        p3 = T.inverse() * p
        self.assertEqual(p3, raytracer.points.Point(-8, 7, 3))

    def test_translate_vector_is_noop(self):
        """Verify that translating a vector has no effect"""

        v = raytracer.vectors.Vector(1, 2, 3)
        T = raytracer.transforms.Translate(5, -3, 2)

        v2 = T * v
        self.assertEqual(v, v2)


class TestScale(unittest.TestCase):
    """Tests on the scaling matrix"""

    def test_simple_scaling(self):
        """Test that we can scale a point"""

        S = raytracer.transforms.Scale(2, 3, 4)
        p = raytracer.points.Point(-4, 6, 8)
        v = raytracer.vectors.Vector(-4, 6, 8)

        p2 = S * p
        self.assertEqual(p2, raytracer.points.Point(-8, 18, 32))

        p3 = S * v
        self.assertEqual(p3, raytracer.vectors.Vector(-8, 18, 32))

        p4 = S.inverse() * p
        self.assertEqual(p4, raytracer.points.Point(-2, 2, 2))


    def test_scaling_reflection(self):
        """Test we can reflect ap oint about an exis using the scaling matrix"""

        S = raytracer.transforms.Scale(-1, 1, 1)
        p = raytracer.points.Point(-4, 6, 8)

        p2 = S * p
        self.assertEqual(p2, raytracer.points.Point(4, 6, 8))

if __name__ == "__main__":
    unittest.main()
