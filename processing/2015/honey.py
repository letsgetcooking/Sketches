RECORD = False
FPS = 20.0
PERIOD = 2
ROW_NUMBER, COL_NUMBER = 14, 15
HEX_SIZE = 20


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
    size(480, 480)
    frameRate(FPS)
    strokeWeight(3)

def draw():
    background(0)
    hex_gen = HexagonGenerator(HEX_SIZE, 5)
    center = (ROW_NUMBER // 2 * hex_gen.col_width + hex_gen.col_width / 3,
        (COL_NUMBER - 1) // 2 * hex_gen.row_height)
    offset_x = (width - COL_NUMBER * hex_gen.col_width + hex_gen.col_width /
        2.0) / 2
    offset_y = (height - ROW_NUMBER * hex_gen.row_height) / 2
    translate(offset_x, offset_y)
    for row in range(ROW_NUMBER):
        for col in range(COL_NUMBER):
            if row == ROW_NUMBER - 1 and col % 2 == 1: continue
            rad = (1.5 * hex_gen.row_height * ROW_NUMBER * (frameCount % (FPS *
                PERIOD)) / (FPS * PERIOD) - 8 * hex_gen.row_height)
            hexagon = list(hex_gen(row, col))
            hexc = (hexagon[0][0] - hex_gen.col_width / 3 - center[0],
                hexagon[0][1] + hex_gen.row_height / 2 - center[1])
            alpha = 255 * int(map(constrain(abs(sqrt(hexc[0] ** 2 + hexc[1] ** 2) - rad),
                0, 100), 0, 100, 0, 1))
            stroke(255, 191, 0, alpha)
            fill(255, 252, 77, alpha)
            beginShape()
            for x, y in hexagon:
                vertex(x, y)
            endShape(CLOSE)
    if RECORD and frameCount <= PERIOD * FPS:
        saveFrame('png/####.png')
