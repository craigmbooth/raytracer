import tuples

class Vector(tuples.Tuple):
    """This class represents a vector between two points in space.  It is
    initialized with x, y, and z coordinates and then in this class we add a
    fourth component, w, which is 0 for a point
    """

    def __init__(self, x, y, z):
        super().__init__(["x", "y", "z", "w"], x, y, z, 0)

    def __repr__(self):
        return f"Vector [{self.x}, {self.y}, {self.z}]"


    def cross(self, other):
        """Calculates the cross product between two tuples.  Note that this
        calculation only makes sense on vectors, so lives on the subclass and
        also makes direct use of the fillable names
        """

        return Vector(self.y * other.z - self.z * other.y,
                      self.z * other.x - self.x * other.z,
                      self.x * other.y - self.y * other.x)
