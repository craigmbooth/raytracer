"""Module implements patterns that can be applied to materials"""
import math

import colors
import points
import transforms

class Pattern:
    """Abstract base pattern class"""

    def __init__(self):

        self.set_transform(transforms.Identity(4))

    def set_transform(self, transform):
        """Set the pattern transformation to the matrix and cache the inverse
        of that transform
        """

        self.transform = transform
        self.inverse_transform = transform.inverse()

    def pattern_at(self, position: points.Point) -> colors.Color:
        """Define a pattern by returning a color based on a positional point in
        pattern-local coordinates
        """
        raise NotImplementedError

    def pattern_at_shape(self, shape,
                          world_point: points.Point):
        if shape is None:
            object_point = world_point
        else:
            object_point = shape.inverse_transform * world_point

        pattern_point = self.inverse_transform * object_point

        return self.pattern_at(pattern_point)


class TestPattern(Pattern):
    """Class used to demonstrate behavior of patterns in tests"""

    def pattern_at(self, position: points.Point) -> colors.Color:
        """Test pattern simply translates the position to a color matrix so
        we can observe outputs
        """

        return colors.Color(position.x, position.y, position.z)


class StripePattern(Pattern):
    """Pattern has two colors and alternates them in the x direction"""

    def __init__(self, color_a: colors.Color, color_b: colors.Color) -> None:
        """Initialize a new stripe pattern with the two colors"""

        self.color_a = color_a
        self.color_b = color_b
        super().__init__()


    def pattern_at(self, position: points.Point) -> colors.Color:
        """Returns a color that depends only on the x-coordinate of the position
        """
        return self.color_a if math.floor(position.x) % 2 == 0 else self.color_b


class GradientPattern(Pattern):
    """Pattern has two colors and fades between them in the x-direction"""

    def __init__(self, color_a: colors.Color, color_b: colors.Color) -> None:
        """Initialize a new stripe pattern with the two colors"""

        self.color_a = color_a
        self.color_b = color_b
        super().__init__()


    def pattern_at(self, position: points.Point) -> colors.Color:
        """Returns a color that depends only on the x-coordinate of the position
        """
        distance = position.x - math.floor(position.x)
        return self.color_a + (self.color_b - self.color_a) * distance


class RingPattern(Pattern):
    """Pattern has two colors and makes rings in the x-z plane"""

    def __init__(self, color_a: colors.Color, color_b: colors.Color) -> None:
        """Initialize a new ring pattern with the two colors"""

        self.color_a = color_a
        self.color_b = color_b
        super().__init__()


    def pattern_at(self, position: points.Point) -> colors.Color:
        """Returns a color that depends only on the x-coordinate of the position
        """
        distance = math.sqrt(position.x ** 2 + position.z ** 2)
        return self.color_a if distance % 2 == 0 else self.color_b


class CheckerPattern(Pattern):
    """3d Checkerboard pattern"""

    def __init__(self, color_a: colors.Color, color_b: colors.Color) -> None:
        """Initialize a new ring pattern with the two colors"""

        self.color_a = color_a
        self.color_b = color_b
        super().__init__()


    def pattern_at(self, position: points.Point) -> colors.Color:
        """Returns a color that depends only on the x-coordinate of the position
        """
        num = (math.floor(position.x) +
                   math.floor(position.y) +
                   math.floor(position.z))
        return self.color_a if num % 2 == 0 else self.color_b
