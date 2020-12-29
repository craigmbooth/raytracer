import unittest

import colors
import patterns
import points
import shapes
import transforms

# Couple of utility colors to make tests more readable
BLACK = colors.Color(0, 0, 0)
WHITE = colors.Color(1, 1, 1)

class TestPatterns(unittest.TestCase):
    """Tests on the patterns module"""

    def test_initialize_stripe(self):
        """Test that we can initialize a stripe pattern"""

        stripes = patterns.StripePattern(WHITE, BLACK)
        self.assertEqual(stripes.color_a, WHITE)
        self.assertEqual(stripes.color_b, BLACK)
        self.assertEqual(stripes.transform, transforms.Identity(4))

    def test_stripes_in_y(self):
        """Test that the default pattern is constant in y"""

        stripes = patterns.StripePattern(WHITE, BLACK)

        self.assertEqual(stripes.pattern_at(points.Point(0, 0, 0,)), WHITE)
        self.assertEqual(stripes.pattern_at(points.Point(0, 1, 0,)), WHITE)
        self.assertEqual(stripes.pattern_at(points.Point(0, 2, 0,)), WHITE)

    def test_stripes_in_z(self):
        """Test that the default pattern is constant in z"""

        stripes = patterns.StripePattern(WHITE, BLACK)

        self.assertEqual(stripes.pattern_at(points.Point(0, 0, 0)), WHITE)
        self.assertEqual(stripes.pattern_at(points.Point(0, 0, 1)), WHITE)
        self.assertEqual(stripes.pattern_at(points.Point(0, 0, 2)), WHITE)

    def test_stripes_in_x(self):
        """Test that the default pattern alternates in x"""

        stripes = patterns.StripePattern(WHITE, BLACK)

        self.assertEqual(stripes.pattern_at(points.Point(0, 0, 0)), WHITE)
        self.assertEqual(stripes.pattern_at(points.Point(0.9, 0, 0)), WHITE)
        self.assertEqual(stripes.pattern_at(points.Point(1, 0, 0)), BLACK)
        self.assertEqual(stripes.pattern_at(points.Point(-0.1, 0, 0)), BLACK)
        self.assertEqual(stripes.pattern_at(points.Point(-1, 0, 0)), BLACK)
        self.assertEqual(stripes.pattern_at(points.Point(-1.1, 0, 0)), WHITE)


    def test_object_transformation(self):
        """Test that pattern is affected by an object transform"""

        shape = shapes.Sphere()
        shape.set_transform(transforms.Scale(2, 2, 2))

        p = patterns.StripePattern(WHITE, BLACK)

        self.assertEqual(p.pattern_at_shape(shape, points.Point(1.5, 0, 0)),
                         WHITE)


    def test_pattern_transformation(self):
        """Test that pattern is affected by a pattern transform"""

        shape = shapes.Sphere()

        p = patterns.StripePattern(WHITE, BLACK)
        p.set_transform(transforms.Scale(2, 2, 2))

        self.assertEqual(p.pattern_at_shape(shape, points.Point(1.5, 0, 0)),
                         WHITE)

    def test_pattern_object_transformation(self):
        """Test that pattern is affected by pattern and object transforms"""

        shape = shapes.Sphere()
        shape.set_transform(transforms.Scale(2, 2, 2))

        p = patterns.StripePattern(WHITE, BLACK)
        p.set_transform(transforms.Translate(0.5, 0, 0))

        self.assertEqual(p.pattern_at_shape(shape, points.Point(2.5, 0, 0)),
                         WHITE)

    def test_gradient(self):
        """Test that the gradient pattern works"""

        p = patterns.GradientPattern(WHITE, BLACK)

        self.assertEqual(p.pattern_at(points.Point(0, 0, 0,)), WHITE)
        self.assertEqual(p.pattern_at(points.Point(0.25, 0, 0,)),
                         colors.Color(0.75, 0.75, 0.75))
        self.assertEqual(p.pattern_at(points.Point(0.5, 0, 0,)),
                         colors.Color(0.5, 0.5, 0.5))
        self.assertEqual(p.pattern_at(points.Point(0.75, 0, 0,)),
                         colors.Color(0.25, 0.25, 0.25))


    def test_rings(self):
        """Test the ring pattern works"""

        p = patterns.RingPattern(WHITE, BLACK)

        self.assertEqual(p.pattern_at(points.Point(0, 0, 0,)), WHITE)
        self.assertEqual(p.pattern_at(points.Point(1, 0, 0,)), BLACK)
        self.assertEqual(p.pattern_at(points.Point(0, 0, 1,)), BLACK)
        self.assertEqual(p.pattern_at(points.Point(0.708, 0, 0.708,)), BLACK)


    def test_checkers(self):
        """Test the checkerboard pattern works"""

        p = patterns.CheckerPattern(WHITE, BLACK)

        self.assertEqual(p.pattern_at(points.Point(0, 0, 0,)), WHITE)
        self.assertEqual(p.pattern_at(points.Point(0.99, 0, 0,)), WHITE)
        self.assertEqual(p.pattern_at(points.Point(1.01, 0, 0,)), BLACK)

        self.assertEqual(p.pattern_at(points.Point(0, 0.99, 0,)), WHITE)
        self.assertEqual(p.pattern_at(points.Point(0, 1.01, 0,)), BLACK)

        self.assertEqual(p.pattern_at(points.Point(0, 0, 0.99)), WHITE)
        self.assertEqual(p.pattern_at(points.Point(0, 0, 1.01)), BLACK)
