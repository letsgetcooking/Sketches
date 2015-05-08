W = H = 480
FPS = 20.0
D = 0.8
N_FRAMES = D * FPS
HEX_SIZE = 1
SPACING = 2
ROW_NUMBER, COL_NUMBER = 140, 140
SCREEN_COLOR = color(65)
RECORD = False


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
    global mshader
    size(W, H, P2D)
    frameRate(FPS)
    mshader = loadShader('colorfrag.glsl')
    mshader.set('resolution', float(W), float(H))
    mshader.set('size', float(W / 3), float(H / 3))
    mshader.set('position1', float(W / 4), float(H / 4))
    mshader.set('position2', float(5 * W / 6), float(H / 4))
    mshader.set('position3', float(-W / 6), float(H / 7))
    mshader.set('position4', float(4 * W / 3), float(H / 7))
    mshader.set('position5', float(W / 2), float(6 * H / 5))
    mshader.set('position6', float(-W / 9), float(H / 2))
    mshader.set('position7', float(10 * W / 9), float(H / 2))
    shader(mshader)


def draw():
    background(SCREEN_COLOR)
    translate(0, -5)
    mshader.set('time', 2 * PI * frameCount / N_FRAMES)
    hex_gen = HexagonGenerator(HEX_SIZE, SPACING)
    for row in range(ROW_NUMBER):
        for col in range(COL_NUMBER):
            hexagon = list(hex_gen(row, col))
            stroke(255)
            strokeWeight(1)
            fill(255)
            beginShape()
            for x, y in hexagon:
                vertex(x, y)
            endShape(CLOSE)
    if RECORD:
        if frameCount <= N_FRAMES:
            saveFrame('gif/####.gif')
        else:
            exit()
