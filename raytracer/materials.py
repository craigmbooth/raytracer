"""Module contains a class that represents the material a shape is made of"""
from typing import Union
import math

import colors
import lights
import patterns
import points
import vectors

BLACK = colors.Color(0, 0, 0)

class Material:

    def __init__(self, shape=None,
                 ambient: float=0.1, diffuse: float=0.9,
                 specular: float=0.9, shininess: float=200.0,
                 reflective: float=0.0, transparency: float=0.0,
                 refractive_index: float=1.0,
                 pattern: Union[patterns.Pattern, None]=None,
                 color: colors.Color=colors.Color(1, 1, 1)) -> None:

        self.shape = shape
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        self.reflective = reflective
        self.color = color
        self.pattern = pattern
        self.transparency = transparency
        self.refractive_index = refractive_index

    def __eq__(self, other) :
        """Equality check returns true if all attributes match"""

        dct_1 = {k: v for k, v in self.__dict__.items() if k != "shape"}
        dct_2 = {k: v for k, v in other.__dict__.items() if k != "shape"}
        return dct_1 == dct_2


    def lighting(self,
                 light: lights.Light,
                 point: points.Point,
                 eyev: vectors.Vector,
                 normalv: vectors.Vector,
                 in_shadow: bool=False) -> colors.Color:
        """Calculate Phong lighting model for a material"""

        if self.pattern is not None:
            color = self.pattern.pattern_at_shape(self.shape, point)
        else:
            color = self.color

        if in_shadow is True:
            return color * self.ambient

        # combine the surface color with the light's color/intensity
        effective_color = color * light.intensity

        # find the direction to the light source
        light_to_point = light.position - point
        lightv = light_to_point.normalize()

        # compute the ambient contribution
        ambient = effective_color * self.ambient

        # light_dot_normal represents the cosine of the angle between the
        # light vector and the normal vector. A negative number means the
        # light is on the other side of the surface.
        light_dot_normal = lightv.dot(normalv)
        if light_dot_normal < 0:
            diffuse = BLACK
            specular = BLACK
        else:
            # compute the diffuse contribution
            diffuse = effective_color * self.diffuse * light_dot_normal

        # reflect_dot_eye represents the cosine of the angle between the
        # reflection vector and the eye vector. A negative number means the
        # light reflects away from the eye.
        reflectv = -lightv.reflect(normalv)
        reflect_dot_eye = reflectv.dot(eyev)

        if reflect_dot_eye <= 0:
            specular = BLACK
        else:
            # compute the specular contribution
            factor = math.pow(reflect_dot_eye, self.shininess)
            specular = light.intensity * self.specular * factor

        return colors.Color(
            red=ambient.red + diffuse.red + specular.red,
            green=ambient.green + diffuse.green + specular.green,
            blue=ambient.blue + diffuse.blue + specular.blue)
