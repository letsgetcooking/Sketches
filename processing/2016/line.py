from toxi.color import ColorGradient, TColor
from toxi.geom import Vec2D
from geomerative import RG, RShape
import pickle


W = H = 500
FPS = 20.0
DURATION = 3
N_FRAMES = DURATION * FPS
N_SAMPLES = 4
BG_COLOR = color(0)
MAIN_COLOR = color(0)
RECORD = False


COLORS = [(249, 237, 105), (240, 138, 93), (184, 59, 94), (106, 44, 112), (249, 237, 105)]
PALETTE = [(r / 255.0, g / 255.0, b / 255.0) for r, g, b in COLORS]


def draw_line(x1, y1, x2, y2, w, t):
    noStroke()
    length = int(sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2))
    k = 30.0
    grad = ColorGradient()
    for i, col in enumerate(PALETTE):
        grad.addColorAt(i / float(len(PALETTE)) * length, TColor.newRGB(*col))
    colors = grad.calcGradient(0, length)
    for i in range(length):
        fill(colors.get(int((i + t * length) % length)).toARGB())
        ft = (1 - ((constrain(i / k, 0, 1) - 1) ** 8)) * \
            (1 - (constrain((i - length + k) / k, 0, 1) ** 8))
        x = x1 + (x2 - x1) * i / float(length)
        y = y1 + (y2 - y1) * i / float(length)
        ft = 1
        ellipse(x, y, w * ft, w * ft)

def draw_shape(shape, res, w, t, scolor=None):
    noStroke()

    res = int(res)
    grad = ColorGradient()
    for i, col in enumerate(PALETTE):
        grad.addColorAt(i / float(len(PALETTE)) * res, TColor.newRGB(*col))
    colors = grad.calcGradient(0, res)

    if scolor:
        fill(scolor)
        beginShape()
        for p in shape.getPoints():
            vertex(p.x, p.y)
        endShape(CLOSE)

    for i in range(res):
        p = shape.getPoint(i / float(res))
        fill(colors.get(int((i + t * res) % res)).toARGB())
        ellipse(p.x, p.y, w, w)

def draw_(t):
    background(BG_COLOR)

    pushMatrix()
    translate(width / 2, height / 2)

    for i in range(9):
        filter(BLUR, 1)
        rotate(-PI / 36.0 * sin(((t + i / 16.0) % 1) * TWO_PI))
        sc = 1 + 1.8 * (9 - i) / 9.0
        newshape = RShape(mshape)
        newshape.scale(sc)
        draw_shape(newshape, 200 * sc, 5, t, color(0))

    filter(ERODE)
    popMatrix()

def setup():
    global circle
    global mshape

    size(W, H)
    frameRate(FPS)
    RG.init(this)

    mshape = RShape.createRectangle(-50, -50, 100, 100)

def draw():
    if not RECORD:
        t = (frameCount / float(N_FRAMES)) % 1.0
        draw_(t)
    elif N_SAMPLES <= 1:
        t = (frameCount / float(N_FRAMES)) % 1.0
        draw_(t)
        if frameCount <= N_FRAMES:
            saveFrame('gif/####.gif')
        else:
            exit()
    else:
        result = [[0, 0, 0] for i in range(W * H)]
        for sample in range(N_SAMPLES):
            t = (frameCount + sample / float(N_SAMPLES)) / N_FRAMES
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
