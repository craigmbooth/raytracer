class IncompatibleTypeError(Exception):
    pass

class Tuple:

    def __init__(self, x, y, z, w):

        self.x = x
        self.y = y
        self.z = z
        self.w = w
        if self.w == 0:
            self.type = "vector"
        elif self.w == 1:
            self.type = "point"
        else:
            self.type = "unknown"

    def __repr__(self):
        return f"{self.type} [{self.x}, {self.y}, {self.z}]"

    @classmethod
    def vector(cls, x, y, z):
        return cls(x, y, z, 0)

    @classmethod
    def point(cls, x, y, z):
        return cls(x, y, z, 1)

    def __add__(self, other):
        return Tuple(
            self.x+other.x,
            self.y+other.y,
            self.z+other.z,
            self.w+other.w)

    def __sub__(self, other):
        return Tuple(
            self.x-other.x,
            self.y-other.y,
            self.z-other.z,
            self.w-other.w)

    def __neg__(self):
        return Tuple(
            -self.x,
            -self.y,
            -self.z,
            -self.w)

    def __mul__(self, other):
        return Tuple(
            self.x * other,
            self.y * other,
            self.z * other,
            self.w * other)

    @staticmethod
    def _close(x, y, epsilon=1e-6):
        return True if abs(x-y) < epsilon else False

    def __eq__(self, other):
        return (self._close(self.x, other.x) and
                    self._close(self.y, other.y) and
                    self._close(self.z, other.z) and
                    self.type == other.type)
