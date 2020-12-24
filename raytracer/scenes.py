"""The scene is the collection of objects, camera and lights to be rendered"""

from typing import List

import colors
import intersections
import lights
import rays
import shapes

class Scene:
    """The scene is the collection of objects, light and camera that constitutes
    an image
    """

    def __init__(self, objects: List[shapes.Shape]=None,
                 lights: List[lights.Light]=None) -> None:

        if objects is None:
            self.objects = []
        else:
            self.objects = objects

        if lights is None:
            self.lights = []
        else:
            self.lights = lights


    def intersect(self, r: rays.Ray) -> intersections.Intersections:
        """Intersect the ray r with all the objects in the scene and return
        intersections sotred by t value
        """

        for i, shape in enumerate(self.objects):
            if i == 0:
                all_intersections = shape.intersect(r)
            else:
                all_intersections += shape.intersect(r)

        return all_intersections


    def shade_hit(self,
                  computations: intersections.Computations) -> colors.Color:
        """Given some pre-calculated values about a hit, calculate its color"""

        color = colors.Color(0, 0, 0)
        for light in self.lights:
            color += computations.object.material.lighting(light,
                    computations.point, computations.eyev, computations.normalv)
        return color
