class Intersection:
    def __init__(self, shape, t):
        self.shape = shape
        self.t = t

    def __eq__(self, other):
        return self.shape == other.shape and self.t == other.t

    def __repr__(self):
        return f"Intersection at t={self.t} with {self.shape}"


class Intersections:

    def __init__(self, *args):
        self.intersections = list(args)

    def add(self, intersection):
        intersections.append(intersection)


    def hit(self):
        """Find the lowest non-negative value of t"""

        min_t = 1e10
        hit_index = -1
        for index, intersection in enumerate(self.intersections):
            if intersection.t < min_t and intersection.t > 0:
                hit_index = index
                min_t = intersection.t

        if hit_index > -1:
            return self.intersections[hit_index]
        else:
            return None
