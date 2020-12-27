import math

import raytracer.cameras as cameras
import raytracer.canvas as canvas
import raytracer.colors as colors
import raytracer.lights as lights
import raytracer.materials as materials
import raytracer.scenes as scenes
import raytracer.shapes as shapes
import raytracer.points as points
import raytracer.transforms as transforms
import raytracer.rays as rays
import raytracer.vectors as vectors
if __name__ == "__main__":


    floor = shapes.Plane(
        material=materials.Material(
            color=colors.Color(154/255, 184/255, 252/255),
            specular=0.0,
            reflective=0.3
        )
    )
    floor.set_transform(
        transforms.Translate(0, -0.5, 0)
    )

    middle = shapes.Sphere(
        material=materials.Material(
            color=colors.Color(0.1, 1.0, 0.5),
            specular=0.3,
            diffuse=0.7,
            reflective=0.5
            )
        )

    middle.set_transform(
        transforms.Translate(-0.5, 1, 0.5)
    )

    right = shapes.Sphere(
        material=materials.Material(
            color=colors.Color(0.5, 1, 0.1),
            specular=0.3,
            diffuse=0.7
            )
        )

    right.set_transform(
        transforms.Translate(1.5, 0.5, -0.5) *
        transforms.Scale(0.5, 0.5, 0.5)
    )

    left = shapes.Sphere(
        material=materials.Material(
            color=colors.Color(1, 0.8, 1),
            specular=0.3,
            diffuse=0.7
            )
        )

    left.set_transform(
        transforms.Translate(-1.5, 1, -0.75) *
        transforms.Scale(0.33, 0.33, 0.33)
    )

    light = lights.PointLight(
        points.Point(-10, 10, -10),
        colors.Color(1, 1, 1)
    )

    scene = scenes.Scene(
        [floor, middle, right, left],
        [light],
    )

    camera = cameras.Camera(120, 60, math.pi/3)
    camera.transform = transforms.ViewTransform(
        points.Point(0, 1.5, -5),
        points.Point(0, 1, 0),
        vectors.Vector(0, 1, 0)
        )

    canvas = camera.render(scene)
    canvas.to_ppm(f"scene1.ppm")
