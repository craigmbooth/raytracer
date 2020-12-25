import math

import exceptions

class Tuple:
    """ This class represents a generic tuple.
    """

    def __init__(self, fillables, *args):
        """Initialize with a list of fillable items, and then one arg
        with the value per item.  For example, a 2d tuple with x and y
        coordinates would be initialized as Tuple(["x", "y"], 1, 2). The
        x and y coordinates are then availble at `obj.x` and `obj.y`
        """

        if len(fillables) != len(args):
            raise exceptions.IncompatibleLengthError

        self.fillables = fillables
        for fillable, arg in zip(fillables, args):
            setattr(self, fillable, arg)

    def __repr__(self):
        tuple_string = " ".join([f"{f}={getattr(self, f)}" for
                                 f in self.fillables])
        return f"Tuple [{tuple_string}]"

    def __add__(self, other):

        if len(self.fillables) != len(other.fillables):
            raise exceptions.IncompatibleLengthError

        output_fillables = [
            getattr(self, f[0]) + getattr(other, f[1]) for
            f in zip(self.fillables, other.fillables)]

        return Tuple(self.fillables, *output_fillables)

    def __sub__(self, other):

        if len(self.fillables) != len(other.fillables):
            raise exceptions.IncompatibleLengthError

        output_fillables = [
            getattr(self, f[0]) - getattr(other, f[1]) for
            f in zip(self.fillables, other.fillables)]

        return Tuple(self.fillables, *output_fillables)

    def __neg__(self):

        output_fillables = [
            -getattr(self, f[0]) for f in self.fillables]

        return Tuple(self.fillables, *output_fillables)


    def __mul__(self, other):

        output_fillables = [
            getattr(self, f) * other for f in self.fillables]

        return Tuple(self.fillables, *output_fillables)

    def __truediv__(self, other):

        output_fillables = [
            getattr(self, f[0]) / other for f in self.fillables]

        return Tuple(self.fillables, *output_fillables)

    @staticmethod
    def _close(x, y, epsilon=1e-3):
        """Utility function, returns True if two numbers are close, else false
        """
        return True if abs(x-y) < epsilon else False

    def __eq__(self, other):

        if len(self.fillables) != len(other.fillables):
            return False

        for f1, f2 in zip(self.fillables, other.fillables):
            if (not self._close(getattr(self, f1), getattr(other, f2)) or
                (f1 != f2)):
                return False
        else:
            return True

    def values(self):
        return [getattr(self, f) for f in self.fillables]

    def magnitude(self):
        """Return the magnitude of the tuple"""

        output_fillables = [
            getattr(self, f[0]) ** 2 for f in self.fillables]

        return math.sqrt(sum(output_fillables))

    def normalize(self):
        """Normalizes the length of the components to 1"""

        magnitude = self.magnitude()

        output_fillables = [
            getattr(self, f[0]) / magnitude for f in self.fillables]

        return Tuple(self.fillables, *output_fillables)

    def dot(self, other):
        """Calculates the dot product between two vectors.
        """
        return sum([getattr(self, x) * getattr(other, x)
                    for x in self.fillables])

    def cross(self, other):
        """Calculates the cross product between two tuples.  Note that this
        calculation only makes sense on vectors, so lives on the subclass and
        also makes direct use of the fillable names
        """

        return Tuple(["x", "y", "z", "w"],
                     self.y * other.z - self.z * other.y,
                     self.z * other.x - self.x * other.z,
                     self.x * other.y - self.y * other.x,
                     0)

    def reflect(self, normal):
        """Reflects  self against a surface perpendicular to normal"""
        return self - normal * 2 * self.dot(normal)


    def apply(self, M):
        """Does M * self and returns the resultant point"""
        return M * self
