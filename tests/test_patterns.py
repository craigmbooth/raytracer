import unittest

import colors
import patterns
import points

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
