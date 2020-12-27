"""Class defines a camera and provides mappings from camera coordinates to the
world
"""
import logging
import math
import sys
import time

import canvas
import points
import rays
import scenes
import transforms

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

        self.transform = transforms.Identity(4)

    def ray_for_pixel(self, px: int, py: int) -> rays.Ray:
        """Given the x and y indices of a pixel, get the ray that is fired"""

        xoffset = (px + 0.5) * self.pixel_size
        yoffset = (py + 0.5) * self.pixel_size

        world_x = self.half_width - xoffset
        world_y = self.half_height - yoffset

        # Using the camera's transform, change the canvas point and origin.
        # remember the canvas is at z=-1
        pixel = self.transform.inverse() * points.Point(world_x, world_y, -1)
        origin = self.transform.inverse() * points.Point(0, 0, 0)
        direction = (pixel - origin).normalize()

        return rays.Ray(origin, direction)

    def render(self, scene: scenes.Scene):
        """Renders a scene and returns a filled in canvas"""

        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

        t0 = time.time()
        logging.info(f"Starting to render scene with size "
                     f"{self.hsize}, {self.vsize}")
        image = canvas.Canvas(self.hsize, self.vsize)

        for y in range(self.vsize):
            print(y)
            for x in range(self.hsize):
                ray = self.ray_for_pixel(x, y)
                color, _ = scene.color_at(ray)
                image.set(x, y, color)

        t1 = time.time()
        logging.info(f"Rendered scene in {round(t1-t0, 2)}s "
                     f"({round(self.hsize*self.vsize/(t1-t0), 2)} pps)")

        return image
