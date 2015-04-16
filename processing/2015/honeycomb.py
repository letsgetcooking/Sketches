# For this sketch third-party library is required http://www.gicentre.net/handy/
from org.gicentre.handy import HandyRenderer


RECORD = False
FPS = 30.0
PERIOD = 2
ROW_NUMBER, COL_NUMBER = 6, 7
HEX_SIZE = 30


class HexagonGenerator(object):
    """Returns a hexagon generator for hexagons of the specified size."""
    def __init__(self, edge_length, spacing):
        self.edge_length = edge_length
        self.spacing = spacing

    @property
    def col_width(self):
        return self.edge_length * 1.5 + self.spacing

    @property
    def row_height(self):
        return 2 * sin(PI / 3) * self.edge_length + self.spacing

    def __call__(self, row, col):
        x = col * self.col_width
        y = (row + 0.5 * (col % 2)) * self.row_height
        for angle in range(0, 360, 60):
          x += cos(radians(angle)) * self.edge_length
          y += sin(radians(angle)) * self.edge_length
          yield x, y


def setup():
    global h
    global img
    size(480, 480)
    frameRate(FPS)
    h = HandyRenderer(this)
    background(0)
    h.setBackgroundColour(0)

def draw():
    center = (ROW_NUMBER - 1) // 2, (COL_NUMBER - 1) // 2
    background(0)
    hex_gen = HexagonGenerator(HEX_SIZE, 3)
    offset_x = (width - COL_NUMBER * hex_gen.col_width + hex_gen.col_width /
        2.0) / 2
    offset_y = (height - ROW_NUMBER * hex_gen.row_height) / 2
    translate(offset_x, offset_y)
    colorMode(HSB, 100)
    for row in range(ROW_NUMBER):
        for col in range(COL_NUMBER):
            if row == ROW_NUMBER - 1 and col % 2 == 1: continue
            rad = (1.5 * hex_gen.row_height * ROW_NUMBER * (frameCount % (FPS *
                PERIOD)) / (FPS * PERIOD) - 4 * hex_gen.row_height)
            hexagon = list(hex_gen(row, col))
            hexc = [0, 0]
            for x, y in hexagon:
                hexc = hexc[0] + x, hexc[1] + y
            hexc = (hexc[0] / 6.0 - (width / 2 - offset_x), hexc[1] / 6.0 -
                (height / 2 - offset_y))
            hu = 100 * (row + col) / (ROW_NUMBER + COL_NUMBER)
            sat = 100
            br = (100 - constrain(abs(sqrt(hexc[0] ** 2 + hexc[1] ** 2) - rad),
                0, 100))
            stroke(0, 0, br)
            fill(hu, sat, br)
            h.beginShape()
            for x, y in hexagon:
                h.vertex(x, y)
            h.endShape(CLOSE)
    if RECORD and frameCount <= PERIOD * FPS:
        saveFrame('png/####.png')
