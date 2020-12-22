import unittest

import raytracer.exceptions, raytracer.matrices, raytracer.transforms

class TestTransforms(unittest.TestCase):


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


if __name__ == "__main__":
    unittest.main()
