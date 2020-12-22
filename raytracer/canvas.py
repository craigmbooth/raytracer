import raytracer.colors

MAX_LINE_LEN = 70

class Canvas:

    def __init__(self, width: int, height: int):

        self.width = width
        self.height = height

        self.canvas = [[raytracer.colors.Color(0, 0, 0)] * height for
                           _ in range(width)]

    def __repr__(self):
        return f"Canvas [w={self.width}, h={self.height}]"

    def set(self, x, y, color: raytracer.colors.Color):
        self.canvas[x][y] = color

    def get(self, x, y) -> raytracer.colors.Color:
        return self.canvas[x][y]

    @staticmethod
    def clamp(minval, x, maxval):
        return min(max(minval, x), maxval)

    def _get_ppm_file_content(self):
        """Convert the canvas into a string containing the PPM file content"""
        header = f"P3\n{self.width} {self.height}\n255\n"


        content_string = ""
        for i in range(self.height):
            row_string = ""
            for j in range(self.width):
                r = round(self.clamp(0, self.canvas[j][i].red*255, 255))
                g = round(self.clamp(0, self.canvas[j][i].green*255, 255))
                b = round(self.clamp(0, self.canvas[j][i].blue*255, 255))

                row_string += f"{r} {g} {b} "

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
        with open(filename, "w") as f:
            f.write(content)
