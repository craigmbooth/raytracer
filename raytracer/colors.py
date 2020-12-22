import raytracer.tuples

class Color(raytracer.tuples.Tuple):
    """This class represents a color.  It is initialized with
    red, green, and blue components
    """

    def __init__(self, red, green, blue):
        super().__init__(["red", "green", "blue"], red, green, blue)

    def __repr__(self):
        return f"Color [r={self.red}, g={self.green}, b={self.blue}]"
