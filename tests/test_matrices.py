import unittest

import raytracer.matrices, raytracer.tuples

class TestMatrices(unittest.TestCase):


    def test_matrix_creation(self):
        """Test we can get and set individual matrix elements"""

        m = raytracer.matrices.Matrix(4, 4)

        # Test individual element sets
        m.set(0, 1, 2)
        m.set(0, 2, 3)
        m.set(2, 1, 10)
        m.set(2, 2, 11)
        m.set(3, 1, 14.5)
        m.set(3, 2, 15.5)

        # Column sets
        m.set_col(0, [1, 5.5, 9, 13.5])
        m.set_col(3, [4, 8.5, 12, 16.5])

        # Row sets
        m.set_row(1, [5.5, 6.5, 7.5, 8.5])

        # Get some elements
        self.assertEqual(m.get(0, 0), 1)
        self.assertEqual(m.get(0, 3), 4)
        self.assertEqual(m.get(1, 0), 5.5)
        self.assertEqual(m.get(1, 2), 7.5)
        self.assertEqual(m.get(2, 2), 11)
        self.assertEqual(m.get(3, 0), 13.5)
        self.assertEqual(m.get(3, 2), 15.5)

        # Get a row and column
        self.assertEqual(m.get_row(0), [1, 2, 3, 4])
        self.assertEqual(m.get_col(2), [3, 7.5, 11, 15.5])


    def test_matrix__get_set_other_sizes(self):
        """We can read and write from 2x2 and 3x3 matrices"""

        m1 = raytracer.matrices.Matrix(2, 2)
        m1.set_row(0, [-3, -5])
        m1.set_row(1, [1, -2])

        self.assertEqual(m1.get(0, 0), -3)
        self.assertEqual(m1.get(0, 1), -5)
        self.assertEqual(m1.get(1, 0), 1)
        self.assertEqual(m1.get(1, 1), -2)


        m2 = raytracer.matrices.Matrix(3, 3)
        m2.set_row(0, [-3, -5, 0])
        m2.set_row(1, [1, -2, -7])
        m2.set_row(2, [0, 1, 1])

        self.assertEqual(m2.get(0, 0), -3)
        self.assertEqual(m2.get(1, 1), -2)
        self.assertEqual(m2.get(2, 2), 1)


    def test_matrix_equality(self):
        """Test that matrices are equal if their elements are equal"""

        m1 = raytracer.matrices.Matrix(2, 2)
        m1.set_row(0, [1, 2])
        m1.set_row(1, [1, 4])

        m2 = raytracer.matrices.Matrix(2, 2)
        m2.set_row(0, [1, 2])
        m2.set_row(1, [1, 4])

        self.assertTrue(m1 == m2)

        m2.set(1, 1, 50)
        self.assertFalse(m1 == m2)


    def test_matrix_multiplication(self):
        """Test that we can multiply matrices"""

        m1 = raytracer.matrices.Matrix(4, 4)
        m1.set_row(0, [1, 2, 3, 4])
        m1.set_row(1, [5, 6, 7, 8])
        m1.set_row(2, [9, 8, 7, 6])
        m1.set_row(3, [5, 4, 3, 2])

        m2 = raytracer.matrices.Matrix(4, 4)
        m2.set_row(0, [-2, 1, 2, 3])
        m2.set_row(1, [3, 2, 1, -1])
        m2.set_row(2, [4, 3, 6, 5])
        m2.set_row(3, [1, 2, 7, 8])

        m3 = m1 * m2

        expected = raytracer.matrices.Matrix(4, 4)
        expected.set_row(0, [20, 22, 50, 48])
        expected.set_row(1, [44, 54, 114, 108])
        expected.set_row(2, [40, 58, 110, 102])
        expected.set_row(3, [16, 26, 46, 42])

        self.assertEqual(m3, expected)

    def test_matrix_tuple_multiplication(self):
        """Test that we can multiple a matrix by a tuple"""

        M = raytracer.matrices.Matrix(4, 4)
        M.set_row(0, [1, 2, 3, 4])
        M.set_row(1, [2, 4, 4, 2])
        M.set_row(2, [8, 6, 4, 1])
        M.set_row(3, [0, 0, 0, 1])

        t = raytracer.tuples.Tuple(["x", "y", "z", "w"], 1, 2, 3, 1)

        t2 = M * t

        self.assertEqual(t2, raytracer.tuples.Tuple(
            ["x", "y", "z", "w"], 18, 24, 33, 1))

    def test_identity_matrix_mult(self):
        """Test we can identify the identity matrix by a matrix and tuple"""

        ident = raytracer.matrices.IdentityMatrix(3)

        M = raytracer.matrices.Matrix(3, 3)
        M.set_row(0, [1, 2, 3])
        M.set_row(1, [3, 2, 1])
        M.set_row(2, [2, 4, 6])

        M2 = M * ident
        self.assertEqual(M2, M)

        t = raytracer.tuples.Tuple(["a", "b", "c"], 1, 2, 3)
        t2 = ident * t
        self.assertEqual(t2, t)

    def test_matrix_transpose(self):
        """Test we can transpose a matrix"""

        M = raytracer.matrices.Matrix(3, 3)
        M.set_row(0, [1, 2, 3])
        M.set_row(1, [3, 2, 1])
        M.set_row(2, [2, 4, 6])

        M = M.transpose()

        expected = raytracer.matrices.Matrix(3, 3)
        expected.set_row(0, [1, 3, 2])
        expected.set_row(1, [2, 2, 4])
        expected.set_row(2, [3, 1, 6])

        self.assertTrue(M == expected)

    def test_identity_matrix_transpose(self):
        """Test that the transpose of the identity matrix is identity"""

        ident1 = raytracer.matrices.IdentityMatrix(5)
        self.assertEqual(ident.transpose(), ident)


if __name__ == "__main__":
    unittest.main()
