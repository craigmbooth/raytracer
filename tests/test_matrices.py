import unittest

import exceptions, matrices, tuples

class TestMatrices(unittest.TestCase):


    def test_matrix_creation(self):
        """Test we can get and set individual matrix elements"""

        m = matrices.Matrix(4, 4)

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

        m1 = matrices.Matrix(2, 2)
        m1.set_row(0, [-3, -5])
        m1.set_row(1, [1, -2])

        self.assertEqual(m1.get(0, 0), -3)
        self.assertEqual(m1.get(0, 1), -5)
        self.assertEqual(m1.get(1, 0), 1)
        self.assertEqual(m1.get(1, 1), -2)


        m2 = matrices.Matrix(3, 3)
        m2.set_row(0, [-3, -5, 0])
        m2.set_row(1, [1, -2, -7])
        m2.set_row(2, [0, 1, 1])

        self.assertEqual(m2.get(0, 0), -3)
        self.assertEqual(m2.get(1, 1), -2)
        self.assertEqual(m2.get(2, 2), 1)


    def test_matrix_equality(self):
        """Test that matrices are equal if their elements are equal"""

        m1 = matrices.Matrix(2, 2)
        m1.set_row(0, [1, 2])
        m1.set_row(1, [1, 4])

        m2 = matrices.Matrix(2, 2)
        m2.set_row(0, [1, 2])
        m2.set_row(1, [1, 4])

        self.assertTrue(m1 == m2)

        m2.set(1, 1, 50)
        self.assertFalse(m1 == m2)


    def test_matrix_multiplication(self):
        """Test that we can multiply matrices"""

        m1 = matrices.Matrix(4, 4)
        m1.set_row(0, [1, 2, 3, 4])
        m1.set_row(1, [5, 6, 7, 8])
        m1.set_row(2, [9, 8, 7, 6])
        m1.set_row(3, [5, 4, 3, 2])

        m2 = matrices.Matrix(4, 4)
        m2.set_row(0, [-2, 1, 2, 3])
        m2.set_row(1, [3, 2, 1, -1])
        m2.set_row(2, [4, 3, 6, 5])
        m2.set_row(3, [1, 2, 7, 8])

        m3 = m1 * m2

        expected = matrices.Matrix(4, 4)
        expected.set_row(0, [20, 22, 50, 48])
        expected.set_row(1, [44, 54, 114, 108])
        expected.set_row(2, [40, 58, 110, 102])
        expected.set_row(3, [16, 26, 46, 42])

        self.assertEqual(m3, expected)

    def test_matrix_tuple_multiplication(self):
        """Test that we can multiple a matrix by a tuple"""

        M = matrices.Matrix(4, 4)
        M.set_row(0, [1, 2, 3, 4])
        M.set_row(1, [2, 4, 4, 2])
        M.set_row(2, [8, 6, 4, 1])
        M.set_row(3, [0, 0, 0, 1])

        t = tuples.Tuple(["x", "y", "z", "w"], 1, 2, 3, 1)

        t2 = M * t

        self.assertEqual(t2, tuples.Tuple(
            ["x", "y", "z", "w"], 18, 24, 33, 1))


    def test_matrix_transpose(self):
        """Test we can transpose a matrix"""

        M = matrices.Matrix(3, 3)
        M.set_row(0, [1, 2, 3])
        M.set_row(1, [3, 2, 1])
        M.set_row(2, [2, 4, 6])

        M = M.transpose()

        expected = matrices.Matrix(3, 3)
        expected.set_row(0, [1, 3, 2])
        expected.set_row(1, [2, 2, 4])
        expected.set_row(2, [3, 1, 6])

        self.assertTrue(M == expected)

    def test_determinant_2_by_2(self):
        """Test we can calculate the determinant of a 2x2 matrix"""

        M = matrices.Matrix(2, 2)
        M.set_row(0, [1, 5])
        M.set_row(1, [-3, 2])

        self.assertEqual(M.det(), 17)

    def test_determinant_3_by_3(self):
        """Test we can calculate the determinant of a 3x3 matrix"""

        M = matrices.Matrix(3, 3)
        M.set_row(0, [1, 2, 6])
        M.set_row(1, [-5, 8, -4])
        M.set_row(2, [2, 6, 4])

        self.assertEqual(M.cofactor(0, 0), 56)
        self.assertEqual(M.cofactor(0, 1), 12)
        self.assertEqual(M.cofactor(0, 2), -46)
        self.assertEqual(M.det(), -196)

    def test_determinant_4_by_4(self):
        """Test we can calculate the determinant of a 4x4 matrix"""

        M = matrices.Matrix(4, 4)
        M.set_row(0, [-2, -8, 3, 5])
        M.set_row(1, [-3, 1, 7, 3])
        M.set_row(2, [1, 2, -9, 6])
        M.set_row(3, [-6, 7, 7, -9])

        self.assertEqual(M.cofactor(0, 0), 690)
        self.assertEqual(M.cofactor(0, 1), 447)
        self.assertEqual(M.cofactor(0, 2), 210)
        self.assertEqual(M.cofactor(0, 3), 51)
        self.assertEqual(M.det(), -4071)

    def test_get_submatrix(self):
        """Test we can calculate submatrices"""

        # First up a 3x3 example
        M = matrices.Matrix(3, 3)
        M.set_row(0, [1, 5, 0])
        M.set_row(1, [-3, 2, 7])
        M.set_row(2, [0, 6, -3])

        result = M.submatrix(0, 2)

        expected = matrices.Matrix(2, 2)
        expected.set_row(0, [-3, 2])
        expected.set_row(1, [0, 6])

        self.assertEqual(result, expected)

        # Then a 4x4 example
        M = matrices.Matrix(4, 4)
        M.set_row(0, [-6, 1, 1, 6])
        M.set_row(1, [-8, 5, 8, 6])
        M.set_row(2, [-1, 0, 8, 2])
        M.set_row(3, [-7, 1, -1, 1])

        result = M.submatrix(2, 1)

        expected = matrices.Matrix(3, 3)
        expected.set_row(0, [-6, 1, 6])
        expected.set_row(1, [-8, 8, 6])
        expected.set_row(2, [-7, -7, 1])

    def test_minor_3_by_3(self):
        """Test we can calculate the minor of a 3x3 matrix"""

        M = matrices.Matrix(3, 3)
        M.set_row(0, [3, 5, 0])
        M.set_row(1, [2, -1, -7])
        M.set_row(2, [6, -1, 5])

        result = M.minor(1, 0)

        self.assertEqual(result, M.submatrix(1, 0).det())
        self.assertEqual(result, 25)

    def test_cofactor_3_by_3(self):
        """Test we can calculate the cofactors of a 3x3 matrix"""

        M = matrices.Matrix(3, 3)
        M.set_row(0, [3, 5, 0])
        M.set_row(1, [2, -1, -7])
        M.set_row(2, [6, -1, 5])

        self.assertEqual(M.minor(0, 0), -12)
        self.assertEqual(M.cofactor(0, 0), -12)
        self.assertEqual(M.minor(1, 0), 25)
        self.assertEqual(M.cofactor(1, 0), -25)

    def test_inverse(self):
        """Test various matrix inversions"""

        M = matrices.Matrix(4, 4)
        M.set_row(0, [-4, 2, -2, -3])
        M.set_row(1, [9, 6, 2, 6])
        M.set_row(2, [0, -5, 1, -5])
        M.set_row(3, [0, 0, 0, 0])

        with self.assertRaises(exceptions.CannotInvertMatrixError):
            M.inverse()

        M = matrices.Matrix(4, 4)
        M.set_row(0, [-5, 2, 6, -8])
        M.set_row(1, [1, -5, 1, 8])
        M.set_row(2, [7, 7, -6, -7])
        M.set_row(3, [1, -3, 7, 4])

        B = M.inverse()
        self.assertEqual(M.det(), 532)

        self.assertEqual(M.cofactor(2, 3), -160)
        self.assertEqual(B.get(3, 2), -160/532)
        self.assertEqual(B.get(2, 3), 105/532)
        self.assertEqual(M.cofactor(3, 2), 105)

        expected = matrices.Matrix(4, 4)
        expected.set_row(0, [0.21805,  0.45113,  0.24060, -0.04511])
        expected.set_row(1, [-0.80827, -1.45677, -0.44361,  0.52068])
        expected.set_row(2, [-0.07895, -0.22368, -0.05263,  0.19737])
        expected.set_row(3, [-0.52256, -0.81391, -0.30075,  0.30639])

        self.assertEqual(B, expected)

        # Since this calculation is fundamental and bugs are painful,
        # invert a few more matrices with known answers

        M = matrices.Matrix(4, 4)
        M.set_row(0, [8, -5, 9, 2])
        M.set_row(1, [7, 5, 6, 1])
        M.set_row(2, [-6, 0, 9, 6])
        M.set_row(3, [-3, 0, -9, -4])

        expected = matrices.Matrix(4, 4)
        expected.set_row(0, [-0.15385, -0.15385, -0.28205, -0.53846])
        expected.set_row(1, [-0.07692,  0.12308,  0.02564,  0.03077])
        expected.set_row(2, [0.35897,  0.35897,  0.43590,  0.92308])
        expected.set_row(3, [-0.69231, -0.69231, -0.76923, -1.92308])

        self.assertEqual(M.inverse(), expected)

        M = matrices.Matrix(4, 4)
        M.set_row(0, [9, 3, 0, 9])
        M.set_row(1, [-5, -2, -6, -3])
        M.set_row(2, [-4, 9, 6, 4])
        M.set_row(3, [-7, 6, 6, 2])

        expected = matrices.Matrix(4, 4)
        expected.set_row(0, [-0.04074, -0.07778,  0.14444, -0.22222])
        expected.set_row(1, [-0.07778,  0.03333,  0.36667, -0.33333])
        expected.set_row(2, [-0.02901, -0.14630, -0.10926,  0.12963])
        expected.set_row(3, [0.17778,  0.06667, -0.26667,  0.33333])

        self.assertEqual(M.inverse(), expected)


    def test_inverse_self_multiply(self):
        """Test that multipling a matrix by its inverse does what is expected"""

        A = matrices.Matrix(4, 4)
        A.set_row(0, [3, -9, 7, 3])
        A.set_row(1, [3, -8, 2, -9])
        A.set_row(2, [-4, 4, 4, 1])
        A.set_row(3, [-6, 5, -1, 1])

        B = matrices.Matrix(4, 4)
        B.set_row(0, [8, 2, 2, 2])
        B.set_row(1, [3, -1, 7, 0])
        B.set_row(2, [7, 0, 5, 4])
        B.set_row(3, [6, -2, 0, 5])

        C = A * B

        self.assertEqual(C*B.inverse(), A)




if __name__ == "__main__":
    unittest.main()
