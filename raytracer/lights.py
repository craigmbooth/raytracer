import raytracer.points
import raytracer.colors

class Light:
    pass


class PointLight(Light):
    """Class represents a point light, specified entirely by its position and
    intensity
    """

    def __init__(self, position: raytracer.points.Point,
                 intensity: raytracer.colors.Color):

        self.position = position
        self.intensity = intensity
