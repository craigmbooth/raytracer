import numbers

import raytracer.tuples

class Color(raytracer.tuples.Tuple):
    """This class represents a color.  It is initialized with
    red, green, and blue components
    """

    def __init__(self, red, green, blue):
        super().__init__(["red", "green", "blue"], red, green, blue)

    def __repr__(self):
        return f"Color [r={self.red}, g={self.green}, b={self.blue}]"

    def __mul__(self, other):

        if isinstance(other, numbers.Number):
            # If the other item is a number, use the paren't scalar
            # multiplication
            return super().__mul__(other)

        else:
            # Else we calculate the Hadamard product of the color, which is
            # the color (r1*r2, g1*g2, b1*b2)
            output_fillables = [
                getattr(self, f) * getattr(other, f) for f in self.fillables]
            return Color(*output_fillables)
