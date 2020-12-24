"""File describes the "canvas" object, which is a 2d canvas of pixels, which.
Also contains utility  functions to write the canvas to disk
"""

from typing import Union

import colors

# The maximum number of characters in a line of a ppm file
MAX_LINE_LEN = 70

class Canvas:
    """At its heart, the canvas is a 2d array where you can write a color to
    each pixel.  The canvas also handles dumping this structure to an image.
    """
    def __init__(self, width: int, height: int) -> None:

        self.width = width
        self.height = height

        self.canvas = [[colors.Color(0, 0, 0)] * height for
                           _ in range(width)]

    def __repr__(self) -> str:
        return f"Canvas [w={self.width}, h={self.height}]"

    def set(self, x_coord: int, y_coord: int, color: colors.Color) -> None:
        """Set the pixel at (x_coord, ycoord) to the color in `color`"""
        self.canvas[x_coord][y_coord] = color

    def get(self, x_coord: int, y_coord: int) -> colors.Color:
        """Retrieve the value of the pixel at `x_coord`, `y_coord`"""
        return self.canvas[x_coord][y_coord]

    @staticmethod
    def clamp(minval: Union[int, float], val: Union[int, float],
              maxval: Union[int, float]) -> float:
        """Return a value clamped between `minval` and `maxval`"""
        return min(max(minval, val), maxval)

    def _get_ppm_file_content(self) -> str:
        """Convert the canvas into a string containing the PPM file content"""
        header = f"P3\n{self.width} {self.height}\n255\n"


        content_string = ""
        for i in range(self.height):
            row_string = ""
            for j in range(self.width):
                red = round(self.clamp(0, self.canvas[j][i].red*255, 255))
                green = round(self.clamp(0, self.canvas[j][i].green*255, 255))
                blue = round(self.clamp(0, self.canvas[j][i].blue*255, 255))

                row_string += f"{red} {green} {blue} "

            split_row_string = ""
            len_current_row = 0
            for val in row_string.split():

                if len_current_row + len(str(val)) + 2 < MAX_LINE_LEN:
                    split_row_string += str(val) + " "
                    len_current_row += len(str(val)) + 1
                else:
                    split_row_string = split_row_string.strip()
                    split_row_string += "\n" + str(val) + " "
                    len_current_row = len("\n") + len(str(val)) + len(" ")

            content_string += split_row_string.strip()
            content_string += "\n"

        return header+content_string

    def to_ppm(self, filename: str) -> None:
        """Write the canvas out to a file with the given filename"""

        content = self._get_ppm_file_content()
        with open(filename, "w") as file_handle:
            file_handle.write(content)
