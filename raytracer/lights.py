"""Module allows you to import light objects"""

import points
import colors

class Light:
    """Abstract base class for light objects"""

    def __init__(self, position: points.Point,
                 intensity: colors.Color) -> None:

        self.position = position
        self.intensity = intensity


class PointLight(Light):
    """Class represents a point light, specified entirely by its position and
    intensity
    """

    def __init__(self, position: points.Point,
                 intensity: colors.Color) -> None:

        super().__init__(position, intensity)
