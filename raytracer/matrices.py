import numbers

class Matrix:
    """Class represents a matrix of size rows x columns"""

    def __init__(self, rows, columns):

        self.rows = rows
        self.columns = columns
        self.values = [[0] * rows for
                           _ in range(columns)]

    def __repr__(self):

        outstr = f"Matrix (rows={self.rows} columns={self.columns})\n"
        import pdb; pdb.set_trace()
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

if __name__ == "__main__":
    m = Matrix(4, 4)

    m.set_row(0, [1, 2, 3, 4])
    m.set_row(0, [5, 6, 7, 8])
    print(m)
    import pdb; pdb.set_trace()
