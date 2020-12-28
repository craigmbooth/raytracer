"""The scene is the collection of objects, camera and lights to be rendered"""
import math
from typing import List, Tuple

import colors
import intersections
import lights
import points
import rays
import shapes

class Scene:
    """The scene is the collection of objects, light and camera that constitutes
    an image
    """

    def __init__(self, objects: List[shapes.Shape]=None,
                 lights: List[lights.Light]=None,
                 recursion_limit: int=5) -> None:

        if objects is None:
            self.objects = []
        else:
            self.objects = objects

        if lights is None:
            self.lights = []
        else:
            self.lights = lights

        self.recursion_limit = recursion_limit

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
                  computations: intersections.Computations,
                  remaining=5) -> Tuple[colors.Color, int]:
        """Given some pre-calculated values about a hit, calculate its color"""

        surface = colors.Color(0, 0, 0)

        for light in self.lights:

            in_shadow = self.is_shadowed(computations.over_point, light)

            surface += computations.object.material.lighting(light,
                    computations.over_point, computations.eyev,
                    computations.normalv, in_shadow = in_shadow)

            reflected, remaining = self.reflected_color(computations,
                                                        remaining=remaining)
            refracted, remaining = self.refracted_color(computations,
                                                        remaining=remaining)

        return surface + reflected + refracted, remaining

    def color_at(self, ray: rays.Ray, remaining=5) -> Tuple[colors.Color, int]:
        """Calculates the color of a ray in the scene"""

        # List out all the surfaces the ray intersects
        ray_intersections = self.intersect(ray)

        # Find the closest one, in front of the camera (the "hit"):
        hit = ray_intersections.hit()

        # If there were no hits, return the background color
        if hit is None:
            return colors.Color(0, 0, 0), remaining

        # Else, calculate the color of the pixel
        precomputes = hit.precompute(ray, all_intersections=ray_intersections)
        return self.shade_hit(precomputes, remaining)

    def is_shadowed(self, point: points.Point, light: lights.Light) -> bool:
        """Returns True if the point is shadowed from the light"""

        v = light.position - point
        distance = v.magnitude()
        direction = v.normalize()

        ray = rays.Ray(point, direction)
        intersections = self.intersect(ray)

        hit = intersections.hit()
        if hit is not None and hit.t < distance:
            return True

        return False

    def reflected_color(self,
                        precomputes: intersections.Computations,
                        remaining: int=5) -> Tuple[colors.Color, int]:
        """Calculate the reflected color of a hit on a surface.

        remaining tracks how many levels of recursion we have done, and when
        it is zero, simply returns black
        """

        if remaining == 0:
            # If we have gone too far down the recursion stack, just return
            # black
            return colors.Color(0, 0, 0), 0

        if precomputes.object.material.reflective == 0:
            # If the material is not reflective, return black
            return colors.Color(0, 0, 0), 0

        # Fire a new ray from the intersection point at the reflection angle
        reflect_ray = rays.Ray(precomputes.over_point, precomputes.reflectv)

        remaining -= 1

        color, remaining = self.color_at(reflect_ray, remaining=remaining)

        return color * precomputes.object.material.reflective, remaining


    def refracted_color(self,
                        precomputes: intersections.Computations,
                        remaining: int=5) -> Tuple[colors.Color, int]:
        """Calculate the refracted color of a hit on a surface.

        remaining tracks how many levels of recursion we have done, and when
        it is zero, simply returns black
        """

        #if remaining == 0:
        #    # If we have gone too far down the recursion stack, just return
        #    # black
        #    return colors.Color(0, 0, 0), remaining

        if precomputes.object.material.transparency == 0:
            # If the material is not transparent, return black
            return colors.Color(0, 0, 0), remaining

        # Check for total internal refraction
        n_ratio = precomputes.n1 / precomputes.n2
        cos_i = precomputes.eyev.dot(precomputes.normalv)
        sin2_t = n_ratio ** 2 * (1 - cos_i ** 2)
        if sin2_t > 1:
            return colors.Color(0, 0, 0), remaining

        cos_t = math.sqrt(1.0 - sin2_t)

        direction = precomputes.normalv * (n_ratio * cos_i - cos_t) - precomputes.eyev * n_ratio

        refract_ray = rays.Ray(precomputes.under_point, direction)

        color = self.color_at(refract_ray, remaining-1)[0] * precomputes.object.material.transparency

        return color, remaining
