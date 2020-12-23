import math
import unittest

import exceptions
import matrices
import transforms
import tuples
import points
import vectors

class TestIdentity(unittest.TestCase):
    """Tests on the identity matrix"""

    def test_identity_matrix_mult(self):
        """Test we can identify the identity matrix by a matrix and tuple"""

        ident = transforms.Identity(3)

        M = matrices.Matrix(3, 3)
        M.set_row(0, [1, 2, 3])
        M.set_row(1, [3, 2, 1])
        M.set_row(2, [2, 4, 6])

        M2 = M * ident
        self.assertEqual(M2, M)

        t = tuples.Tuple(["a", "b", "c"], 1, 2, 3)
        t2 = ident * t
        self.assertEqual(t2, t)

    def test_identity_matrix_transpose(self):
        """Test that the transpose of the identity matrix is identity"""

        ident = transforms.Identity(5)
        self.assertEqual(ident.transpose(), ident)


class TestTranslate(unittest.TestCase):
    """Tests on the translating matrix"""

    def test_translate_point(self):
        """Test that if we multiply a translate matrix by a point it moves it"""

        p = points.Point(-3, 4, 5)
        T = transforms.Translate(5, -3, 2)

        p2 = T * p
        self.assertEqual(p2, points.Point(2, 1, 7))

        # Translating by the inverse of the translate matrix moves the
        # opposite direction

        p3 = T.inverse() * p
        self.assertEqual(p3, points.Point(-8, 7, 3))

    def test_translate_vector_is_noop(self):
        """Verify that translating a vector has no effect"""

        v = vectors.Vector(1, 2, 3)
        T = transforms.Translate(5, -3, 2)

        v2 = T * v
        self.assertEqual(v, v2)


class TestScale(unittest.TestCase):
    """Tests on the scaling matrix"""

    def test_simple_scaling(self):
        """Test that we can scale a point"""

        S = transforms.Scale(2, 3, 4)
        p = points.Point(-4, 6, 8)
        v = vectors.Vector(-4, 6, 8)

        p2 = S * p
        self.assertEqual(p2, points.Point(-8, 18, 32))

        p3 = S * v
        self.assertEqual(p3, vectors.Vector(-8, 18, 32))

        p4 = S.inverse() * p
        self.assertEqual(p4, points.Point(-2, 2, 2))


    def test_scaling_reflection(self):
        """Test we can reflect a point about an axis using the scaling matrix"""

        S = transforms.Scale(-1, 1, 1)
        p = points.Point(-4, 6, 8)

        p2 = S * p
        self.assertEqual(p2, points.Point(4, 6, 8))

class TestRotate(unittest.TestCase):
    """Tests on the rotation matrices"""

    def test_rotate_x(self):
        """Test we can rotate about the x-axis"""

        p = points.Point(0, 1, 0)

        half_quarter = transforms.RotateX(math.pi/4)
        full_quarter = transforms.RotateX(math.pi/2)

        p2 = half_quarter * p
        p3 = full_quarter * p

        self.assertEqual(p2,
            points.Point(0, math.sqrt(2)/2, math.sqrt(2)/2))

        self.assertEqual(p3,
            points.Point(0, 0, 1))

    def test_rotate_x_inverse(self):
        """Test that roating by the inverse of a rotation rotates the other way
        """

        p = points.Point(0, 1, 0)
        full_quarter = transforms.RotateX(math.pi/2)

        p2 = full_quarter.inverse()*p

        self.assertEqual(p2,
            points.Point(0, 0, -1))

    def test_rotate_y(self):
        """Test we can rotate about the y-axis"""

        p = points.Point(0, 0, 1)

        half_quarter = transforms.RotateY(math.pi/4)
        full_quarter = transforms.RotateY(math.pi/2)

        p2 = half_quarter * p
        p3 = full_quarter * p

        self.assertEqual(p2,
            points.Point(math.sqrt(2)/2, 0, math.sqrt(2)/2))

        self.assertEqual(p3,
            points.Point(1, 0, 0))


    def test_rotate_z(self):
        """Test we can rotate about the y-axis"""

        p = points.Point(0, 1, 0)

        half_quarter = transforms.RotateZ(math.pi/4)
        full_quarter = transforms.RotateZ(math.pi/2)

        p2 = half_quarter * p
        p3 = full_quarter * p

        self.assertEqual(p2,
            points.Point(-math.sqrt(2)/2, math.sqrt(2)/2, 0))

        self.assertEqual(p3,
            points.Point(-1, 0, 0))


class TestShearing(unittest.TestCase):
    """Tests on the shearing matrices"""

    def test_all_shear_axes(self):
        p = points.Point(2, 3, 4)

        S1 = transforms.Shear(1, 0, 0, 0, 0, 0)
        p1 = S1 * p
        self.assertEqual(p1, points.Point(5, 3, 4))

        S1 = transforms.Shear(0, 1, 0, 0, 0, 0)
        p1 = S1 * p
        self.assertEqual(p1, points.Point(6, 3, 4))

        S1 = transforms.Shear(0, 0, 1, 0, 0, 0)
        p1 = S1 * p
        self.assertEqual(p1, points.Point(2, 5, 4))

        S1 = transforms.Shear(0, 0, 0, 1, 0, 0)
        p1 = S1 * p
        self.assertEqual(p1, points.Point(2, 7, 4))

        S1 = transforms.Shear(0, 0, 0, 0, 1, 0)
        p1 = S1 * p
        self.assertEqual(p1, points.Point(2, 3, 6))

        S1 = transforms.Shear(0, 0, 0, 0, 0, 1)
        p1 = S1 * p
        self.assertEqual(p1, points.Point(2, 3, 7))


class TestChainedTransformations(unittest.TestCase):

    def test_chained_transforms(self):
        """Test we can chain together transforms with the apply function"""
        point = points.Point(1, 0, 1)

        p2 = point.apply(transforms.RotateX(math.pi/2)) \
                  .apply(transforms.Scale(5, 5, 5)) \
                  .apply(transforms.Translate(10, 5, 7))

        self.assertEqual(p2, points.Point(15, 0, 7))




if __name__ == "__main__":
    unittest.main()
