"""Module implements patterns that can be applied to materials"""
import math

import colors
import points

class Pattern:
    """Abstract base pattern class"""

    def pattern_at(self, position: points.Point) -> colors.Color:
        raise NotImplementedError


class StripePattern(Pattern):

    def __init__(self, color_a: colors.Color, color_b: colors.Color) -> None:
        """Initialize a new stripe pattern with the two colors"""

        self.color_a = color_a
        self.color_b = color_b

    def pattern_at(self, position: points.Point) -> colors.Color:
        """Returns a color that depends only on the x-coordinate of the position
        """
        return self.color_a if math.floor(position.x) % 2 == 0 else self.color_b
