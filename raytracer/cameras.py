"""Class defines a camera and provides mappings from camera coordinates to the
world
"""
import math

class Camera:
    """Camera class.  All scenes have one of these"""

    def __init__(self, hsize: int, vsize: int, field_of_view: float) -> None:

        self.hsize = hsize
        self.vsize = vsize
        self.field_of_view = field_of_view

        half_view = math.tan(field_of_view/2)

        aspect = hsize / vsize

        if aspect >= 1:
            self.half_width = half_view
            self.half_height = half_view / aspect
        else:
            self.half_width = half_view * aspect
            self.half_height = half_view

        self.pixel_size = self.half_width * 2 / self.hsize
