import unittest

import raytracer.matrices

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


    def test_matrix_Get_set_other_sizes(self):
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

if __name__ == "__main__":
    unittest.main()
