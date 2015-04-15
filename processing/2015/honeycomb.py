# For this sketch third-party library is required http://www.gicentre.net/handy/
from org.gicentre.handy import HandyRenderer


RECORD = False
FPS = 30.0
PERIOD = 2


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
    row_number, col_number = 6, 7
    center = (row_number - 1) // 2, (col_number - 1) // 2
    # h.setSeed(1234)
    background(0)
    offset = 80
    translate(offset, offset)
    hex_gen = HexagonGenerator(30, 3)
    colorMode(HSB, 100)
    for row in range(row_number):
        for col in range(col_number):
            if row == row_number - 1 and col % 2 == 1: continue
            rad = 1.5 * hex_gen.row_height * row_number * (frameCount % (FPS * PERIOD)) / (FPS * PERIOD) - 150
            hexagon = list(hex_gen(row, col))
            hexc = [0, 0]
            for x, y in hexagon:
                hexc = hexc[0] + x, hexc[1] + y
            hexc = hexc[0] / 6.0 - (width / 2 - offset), hexc[1] / 6.0 - (height / 2 - offset)
            hu = (row + col) * 10
            sat = 100
            br = 100 - constrain(abs(sqrt(hexc[0] ** 2 + hexc[1] ** 2) - rad), 0, 100)
            stroke(0, 0, br)
            fill(hu, sat, br)
            h.beginShape()
            for x, y in hexagon:
                h.vertex(x, y)
            h.endShape(CLOSE)
    if RECORD and frameCount <= PERIOD * FPS:
        saveFrame('png/####.png')
