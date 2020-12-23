import tuples

class Point(tuples.Tuple):
    """This class represents a point in space.  It is initialized with
    x, y, and z coordinates and then in this class we add a fourth component,
    w, which is 1 for a point
    """

    def __init__(self, x, y, z):
        super().__init__(["x", "y", "z", "w"], x, y, z, 1)

    def __repr__(self):
        return f"Point [{self.x}, {self.y}, {self.z}]"
