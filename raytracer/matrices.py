import copy
import numbers

import raytracer.exceptions
import raytracer.tuples

class Matrix:
    """Class represents a matrix of size rows x columns"""

    def __init__(self, rows, columns):

        self.rows = rows
        self.columns = columns
        self.values = [[0] * columns for
                           _ in range(rows)]

    def __repr__(self):

        outstr = f"Matrix (rows={self.rows} columns={self.columns})\n"
        for r in range(self.rows):
            if r == 0:
                prefix = "[[ "
                postfix = ""
            elif r == self.rows - 1:
                prefix = "   "
                postfix = " ]]"
            else:
                prefix = "   "
                postfix = ""
            outstr += prefix + "\t".join([str(e) for e in self.get_row(r)])+postfix+"\n"
        return outstr

    @staticmethod
    def _close(x, y, epsilon=1e-3):
        """Utility function, returns True if two numbers are close, else false
        """
        return True if abs(x-y) < epsilon else False

    def __eq__(self, other):

        if self.rows != other.rows or self.columns != other.columns:
            return False

        for i in range(self.rows):
            for j in range(other.rows):
                if not self._close(self.values[i][j], other.values[i][j]):
                    return False
        else:
            return True

    def __mul__(self, other):
        """Perform matrix multiplication"""

        if isinstance(other, Matrix):
            if self.rows != other.rows or self.columns != other.columns:
                raise raytracer.exceptions.IncompatibleLengthError

            m = Matrix(self.rows, self.columns)

            for i in range(self.rows):
                for j in range(self.columns):
                    my_row = self.get_row(i)
                    other_column = other.get_col(j)

                    m.set(i, j, sum([x*y for x, y in zip(my_row, other_column)]))
            return m

        elif isinstance(other, raytracer.tuples.Tuple):

            zeros = [0] * len(other.fillables)
            r = raytracer.tuples.Tuple(other.fillables, *zeros)

            for i in range(self.rows):
                my_row = self.get_row(i)
                result = sum([my_row[j]*other.values()[j] for j in range(self.columns)])
                setattr(r, other.fillables[i], result)
            return r

    def set(self, x: int, y: int, value: numbers.Number) -> None:
        self.values[x][y] = value

    def get(self, x: int, y: int) -> numbers.Number:
        return self.values[x][y]

    def get_row(self, row: int) -> list:
        return self.values[row]

    def get_col(self, col: int) -> list:
        return [r[col] for r in self.values]

    def set_row(self, row: int, values: list) -> None:
        for i in range(len(values)):
            self.values[row][i] = values[i]

    def set_col(self, col: int, values: list) -> None:
        for i in range(len(values)):
            self.values[i][col] = values[i]

    def transpose(self):
        m = Matrix(self.columns, self.rows)
        for i in range(self.rows):
            m.set_col(i, self.get_row(i))
        return m

    def submatrix(self, row, column):
        """Return a copy of the matrix with the rows and column specified in the
        arguments removed
        """

        m = copy.deepcopy(self)
        _ = m.values.pop(row)
        for row in m.values:
            row.pop(column)

        m.columns -= 1
        m.rows -= 1
        return m

    def det(self):
        """Calculates the determinant of the matrix"""

        if self.columns == 2 and self.rows == 2:
            return self.get(0, 0) * self.get(1, 1) - self.get(1, 0) * self.get(0, 1)
        else:
            det = 0
            for i, value in enumerate(self.get_row(0)):
                det += self.get(0, i) * self.cofactor(0, i)
            return det


    def minor(self, row, column):
        """Calculate the minor of the matrix at row and column, which is
        calculated as the determinant of the submatrix
        """
        return self.submatrix(row, column).det()

    def cofactor(self, row, column):
        """Calculate the cofactor of the matrix at row and column.  The cofactor
        is the minor, potentially with its sign changed, depending upon its
        location in the matrix
        """

        pre = 1 if (row + column) % 2 == 0 else -1
        return pre * self.minor(row, column)

    def inverse(self):
        """Calculate the inverse of a matrix, or raise CannotInvertMatrix if
        there is no inverse
        """

        determinant = self.det()
        if determinant == 0:
            raise raytracer.exceptions.CannotInvertMatrixError


        m = Matrix(self.rows, self.columns)

        for row in range(self.rows):
            for col in range(self.columns):
                c = self.cofactor(row, col)

                # Note we have swapped row and col here, which takes care of a
                # transpose under the hood
                m.set(col, row, c / determinant)
        return m

class IdentityMatrix(Matrix):

    def __init__(self, size):
        super().__init__(size, size)
        for i in range(size):
            self.set(i, i, 1)
