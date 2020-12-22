import math
import numbers

import raytracer.exceptions, raytracer.matrices, raytracer.tuples

class Identity(raytracer.matrices.Matrix):

    def __init__(self, size):
        super().__init__(size, size)
        for i in range(size):
            self.set(i, i, 1)


class Translate(Identity):

    def __init__(self, x, y, z):
        """ The translation matrix translates objects by an amount x, y, z.
        It has the following shape:

        [ 1 0 0 x
          0 1 0 y
          0 0 1 z
          0 0 0 1 ]
        """
        super().__init__(4)
        self.set(0, 3, x)
        self.set(1, 3, y)
        self.set(2, 3, z)


class Scale(Identity):

    def __init__(self, x, y, z):
        """ The scaling matrix scales objects by a factor x, y, z along those
        axes. It has the following shape:

        [ x 0 0 0
          0 y 0 0
          0 0 z 0
          0 0 0 1 ]
        """
        super().__init__(4)
        self.set(0, 0, x)
        self.set(1, 1, y)
        self.set(2, 2, z)


class RotateX(Identity):
    def __init__(self, r, degrees=False):
        """ Given an angle in radians, rotates the point around the x-axis
        by that amount

        [ 1 0      0       0
          0 cos(r) -sin(r) 0
          0 sin(r) cos(r)  0
          0 0      0       1 ]
        """

        if degrees is True:
            r *= 2 * math.pi / 360

        super().__init__(4)
        self.set(1, 1, math.cos(r))
        self.set(1, 2, -math.sin(r))
        self.set(2, 1, math.sin(r))
        self.set(2, 2, math.cos(r))


class RotateY(Identity):
    def __init__(self, r, degrees=False):
        """ Given an angle in radians, rotates the point around the y-axis
        by that amount

        [ cos(r) 0      sin(r)  0
          0      1      0       0
         -sin(r) 0      cos(r)  0
          0      0      0       1 ]
        """

        if degrees is True:
            r *= 2 * math.pi / 360

        super().__init__(4)
        self.set(0, 0, math.cos(r))
        self.set(0, 3, math.sin(r))
        self.set(2, 0, -math.sin(r))
        self.set(2, 2, math.cos(r))


class RotateZ(Identity):
    def __init__(self, r, degrees=False):
        """ Given an angle in radians, rotates the point around the z-axis
        by that amount

        [ cos(r) -sin(r) 0 0
          sin(r) cos(r)  0 0
          0      0       1 0
          0      0       0 1
        """

        if degrees is True:
            r *= 2 * math.pi / 360

        super().__init__(4)
        self.set(0, 0, math.cos(r))
        self.set(0, 1, -math.sin(r))
        self.set(1, 0, math.sin(r))
        self.set(1, 1, math.cos(r))
