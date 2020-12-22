import copy
import numbers

import raytracer.exceptions, raytracer.matrices, raytracer.tuples

class Identity(raytracer.matrices.Matrix):

    def __init__(self, size):
        super().__init__(size, size)
        for i in range(size):
            self.set(i, i, 1)


class Translation(Identity):

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
        self.set(0, 3, y)
        self.set(0, 3, z)
