import math

import colors
import lights
import points
import vectors

BLACK = colors.Color(0, 0, 0)

class Material:

    def __init__(self, ambient=0.1, diffuse=0.9, specular=0.9, shininess=200.0,
                 color=colors.Color(1, 1, 1)):

        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        self.color = color

    def __eq__(self, other) :
        """Equality check returns true if all attributes match"""
        return self.__dict__ == other.__dict__


    def lighting(self,
                 light: lights.Light,
                 point: points.Point,
                 eyev: vectors.Vector,
                 normalv: vectors.Vector,
                 in_shadow: bool=False) -> colors.Color:
        """Calculate Phong lighting model for a material"""

        if in_shadow is True:
            return self.color * self.ambient

        # combine the surface color with the light's color/intensity
        effective_color = self.color * light.intensity

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
