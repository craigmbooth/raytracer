"""Module contains all objects that represent basic matrix types"""
from typing import Union, List

import exceptions
import tuples

class Matrix:
    """Class represents a matrix of size rows x columns"""

    def __init__(self, rows: int, columns: int) -> None:

        self.rows = rows
        self.columns = columns
        self.values = [[0.0] * columns for
                           _ in range(rows)]

    def __repr__(self) -> str:

        outstr = f"Matrix (rows={self.rows} columns={self.columns})\n"
        for row in range(self.rows):
            if row == 0:
                prefix = "[[ "
                postfix = ""
            elif row == self.rows - 1:
                prefix = "   "
                postfix = " ]]"
            else:
                prefix = "   "
                postfix = ""
            outstr += prefix + "\t".join([str(e)
                for e in self.get_row(row)])+postfix+"\n"
        return outstr

    @staticmethod
    def _close(x: Union[float, int], y: Union[float, int],
               epsilon: float=1e-3) -> bool:
        """Utility function, returns True if two numbers are close, else false

        :param epsilon: If the absolute value of the differences of all
            attribues is less than epsilon, the two numbers are close
        """
        return abs(x-y) < epsilon

    def __eq__(self, other):

        if self.rows != other.rows or self.columns != other.columns:
            return False

        for i in range(self.rows):
            for j in range(other.rows):
                if not self._close(self.values[i][j], other.values[i][j]):
                    return False
        return True

    def __mul__(self, other):
        """Perform matrix multiplication"""

        if isinstance(other, Matrix):
            if self.rows != other.rows or self.columns != other.columns:
                raise exceptions.IncompatibleLengthError

            M = Matrix(self.rows, self.columns)

            for i in range(self.rows):
                for j in range(self.columns):
                    my_row = self.get_row(i)
                    other_column = other.get_col(j)

                    M.set(i, j, sum([x*y for x, y in zip(my_row, other_column)]))
            return M

        if isinstance(other, tuples.Tuple):

            zeros = [0] * len(other.fillables)
            r = tuples.Tuple(other.fillables, *zeros)

            for i in range(self.rows):
                my_row = self.get_row(i)
                result = sum([my_row[j]*other.values()[j]
                              for j in range(self.columns)])
                setattr(r, other.fillables[i], result)
            return r

        # If we get down here it wasn't any type we can multiply with
        raise ValueError

    def set(self, x: int, y: int, value: Union[int, float]) -> None:
        """Set the element at x, y to the given value"""
        self.values[x][y] = value

    def get(self, x: int, y: int) -> Union[int, float]:
        """Return the value of the matrix as indices x, y"""
        return self.values[x][y]

    def get_row(self, row: int) -> List[Union[int, float]]:
        """Return the values of the matrix at row `row`"""
        return self.values[row]

    def get_col(self, col: int) -> List[Union[int, float]]:
        """Return the values of the matrix at column `col`"""
        return [r[col] for r in self.values]

    def set_row(self, row: int, values: list) -> None:
        """Given a row index and a list of values, set the row at the index to
        the values
        """
        for i, _ in enumerate(values):
            self.values[row][i] = values[i]

    def set_col(self, col: int, values: list) -> None:
        """Given a column index and a list of values, set the column at the
        index to the values
        """
        for i, _ in enumerate(values):
            self.values[i][col] = values[i]

    def transpose(self):
        """Return the matrix, transposed (rows become columns).  No edits
        in-place
        """

        M = Matrix(self.columns, self.rows)
        for i in range(self.rows):
            M.set_col(i, self.get_row(i))
        return M

    def submatrix(self, row: int, column: int):
        """Return a copy of the matrix with the rows and column specified in the
        arguments removed
        """

        M = Matrix(self.rows, self.columns)
        for i in range(self.columns):
            for j in range(self.rows):
                M.set(i, j, self.values[i][j])

        _ = M.values.pop(row)
        for row_values in M.values:
            row_values.pop(column)

        M.columns -= 1
        M.rows -= 1
        return M

    def det(self) -> Union[int, float]:
        """Calculates the determinant of the matrix"""

        if self.columns == 2 and self.rows == 2:
            return self.get(0, 0) * self.get(1, 1) - self.get(1, 0) * self.get(0, 1)

        det = 0.0
        for i, _ in enumerate(self.get_row(0)):
            det += self.get(0, i) * self.cofactor(0, i)
        return det


    def minor(self, row: int, column: int) -> Union[int, float]:
        """Calculate the minor of the matrix at row and column, which is
        calculated as the determinant of the submatrix
        """
        return self.submatrix(row, column).det()

    def cofactor(self, row: int, column: int) -> Union[int, float]:
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
            raise exceptions.CannotInvertMatrixError

        M = Matrix(self.rows, self.columns)

        for row in range(self.rows):
            for col in range(self.columns):
                cofactor = self.cofactor(row, col)

                # Note we have swapped row and col here, which takes care of a
                # transpose under the hood
                M.set(col, row, cofactor / determinant)
        return M
