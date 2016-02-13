from toxi.geom import Polygon2D, PolygonClipper2D, Vec2D
from toxi.processing import ToxiclibsSupport


W = H = 500
FPS = 20.0
DURATION = 4
N_FRAMES = DURATION * FPS
N_SAMPLES = 4
BG_COLOR = color(255)
MAIN_COLOR = color(255)
SURFW, SURFH = 300.0, 300.0
SURFX, SURFY = 9, 9
N_STATES = 15.0
STATES = 140.0
RECORD = False


def draw_(t):
    background(BG_COLOR)
    tsup.polygon2D(heart)

def setup():
    global heart
    global tsup

    size(W, H)
    frameRate(FPS)
    tsup = ToxiclibsSupport(this)

    heart = Polygon2D()

    n = 60
    r = 10
    for i in range(n):
        angle = i / float(n) * TWO_PI
        x = 16 * sin(angle) ** 3
        y = 13 * cos(angle) - 5 * cos(2 * angle) - 2 * cos(3 * angle) - cos(4 * angle)
        heart.add(Vec2D(r * x + width / 2, -r * y + height / 2 - height / 20))

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
