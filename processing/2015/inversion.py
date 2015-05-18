# toxiclibs requiered
from toxi.geom import Vec2D
from toxi.geom import Circle


W = H = 480
FPS = 20.0
DURATION = 4
N_FRAMES = DURATION * FPS
HEX_SIZE = 10
SPACING = 5
ROW_NUMBER = 23
COL_NUMBER = 26
TRANSCOLOR = color(0, 0, 0, 255)
N_SAMPLES = 4
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


def draw_(t):
    p1 = Vec2D(width / 2, height / 4 + height * t / 2 - (5 * ((2 * t + 1) % 2.0 - 1))**7)
    p2 = Vec2D(width / 2, 3 * height / 4 - height * t / 2)
    circle = Circle.from2Points(p1, p2)

    pg = createGraphics(W, H)
    pg.beginDraw()
    pg.stroke(200)
    pg.strokeWeight(4)
    pg.background(35 - 35 * round(t))
    pg.fill(35 * round(t))
    pg.ellipse(circle.x(), circle.y(), 2 * circle.radius, 2 * circle.radius)
    pg.endDraw()

    pg.loadPixels()
    for i, pix in enumerate(pg.pixels):
        if pix == TRANSCOLOR:
            pg.pixels[i] = color(0, 0)
    pg.updatePixels()

    background(0)
    pushMatrix()
    translate(-20, -20)
    for row in range(ROW_NUMBER):
        for col in range(COL_NUMBER):
            beginShape()
            for x, y in hex_gen(row, col):
                vertex(x, y)
            endShape(CLOSE)
    popMatrix()
    image(pg, 0, 0)
        
def setup():
    global hex_gen
    size(W, H)
    frameRate(FPS)
    noFill()
    stroke(200)
    strokeWeight(0.7)
    hex_gen = HexagonGenerator(HEX_SIZE, SPACING)

def draw():
    if not RECORD:
        t = (frameCount / float(N_FRAMES)) % 1.0
        draw_(t)
    else:
        result = [[0, 0, 0] for i in range(W * H)]
        for sample in range(N_SAMPLES):
            t = (frameCount + 0.1 * sample / float(N_SAMPLES)) / N_FRAMES
            draw_(t)
            loadPixels()
            for i, pix in enumerate(pixels):
                result[i][0] += red(pix)
                result[i][1] += green(pix)
                result[i][2] += blue(pix)
        loadPixels()
        for i, rgb in enumerate(result):
            pixels[i] = color(rgb[0] / N_SAMPLES, rgb[1] / N_SAMPLES, rgb[2] / N_SAMPLES)
        updatePixels()
        if frameCount <= N_FRAMES:
            saveFrame('gif/####.gif')
        else:
            exit()
