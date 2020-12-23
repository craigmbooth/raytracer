import unittest

import canvas
import colors

class TestCanvas(unittest.TestCase):

    def test_empty_canvas(self):
        """Test that an empty canvas is filled with black pixels"""

        c = canvas.Canvas(10, 20)

        self.assertEqual(len(c.canvas), 10)
        self.assertEqual(len(c.canvas[0]), 20)

        for i in range(10):
            for j in range(20):
                self.assertEqual(c.canvas[i][j],
                                 colors.Color(0, 0, 0))


    def test_write_to_canvas(self):
        """Test we can write to and read from a canvas"""

        c = canvas.Canvas(10, 20)
        red = colors.Color(1, 0, 0)

        c.set(2, 3, red)

        self.assertEqual(c.canvas[2][3], red)


    def test_ppm_file_content(self):
        """Test the content of the PPM header is correct"""

        c = canvas.Canvas(5, 3)
        c1 = colors.Color(1.5, 0, 0)
        c2 = colors.Color(0, 0.5, 0)
        c3 = colors.Color(-0.5, 0, 1)

        c.set(0, 0, c1)
        c.set(2, 1, c2)
        c.set(4, 2, c3)

        ppm_content = c._get_ppm_file_content()

        ppm_lines = ppm_content.split("\n")

        self.assertEqual(ppm_lines[0], "P3")
        self.assertEqual(ppm_lines[1], "5 3")
        self.assertEqual(ppm_lines[2], "255")
        self.assertEqual(ppm_lines[3], "255 0 0 0 0 0 0 0 0 0 0 0 0 0 0")
        self.assertEqual(ppm_lines[4], "0 0 0 0 0 0 0 128 0 0 0 0 0 0 0")
        self.assertEqual(ppm_lines[5], "0 0 0 0 0 0 0 0 0 0 0 0 0 0 255")


    def test_ppm_long_line_splitting(self):
        """Test that we split longer lines at or before 70 characters"""

        c = canvas.Canvas(10, 2)
        for i in range(c.width):
            for j in range(c.height):
                c.set(i, j, colors.Color(1, 0.8, 0.6))

        ppm_content = c._get_ppm_file_content()
        ppm_lines = ppm_content.split("\n")

        self.assertEqual(ppm_lines[3],
            "255 204 153 255 204 153 255 204 153 255 204 153 255 204 153 255 204")
        self.assertEqual(ppm_lines[4],
            "153 255 204 153 255 204 153 255 204 153 255 204 153")
        self.assertEqual(ppm_lines[5],
            "255 204 153 255 204 153 255 204 153 255 204 153 255 204 153 255 204")
        self.assertEqual(ppm_lines[6],
            "153 255 204 153 255 204 153 255 204 153 255 204 153")


    def test_ppm_ends_with_newline(self):
        """Satisfy picky image viewers by ensuring the ppm file ends in a
        newline
        """

        c = canvas.Canvas(5, 3)
        ppm_content = c._get_ppm_file_content()
        self.assertEqual(ppm_content[-1:], "\n")



if __name__ == "__main__":
    unittest.main()
