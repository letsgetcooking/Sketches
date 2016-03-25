from toxi.geom import Polygon2D, Vec2D, Line2D
from toxi.processing import ToxiclibsSupport


W = H = 500
FPS = 20.0
DURATION = 4
N_FRAMES = DURATION * FPS
N_SAMPLES = 4
BG_COLOR = color(55)
HEAT_COLOR = color(89, 2, 2)
MAIN_COLOR = color(35)
SHADOW_COLOR = color(0)
RECORD = False


def ease_out_cubic(t):
    return (t - 1) ** 3 + 1

def draw_(t):
    background(lerpColor(BG_COLOR, HEAT_COLOR, 1 - (2 * max(0, t - 0.2) * 1.25 - 1) ** 2))

    tt = ((t - 0.2) * 1.25) ** 2

    if t > 0.2:
        npoly = Polygon2D()
        ns = 0.02

        for v in square.vertices:
            nv = v.copy()
            nv.addSelf(Vec2D(0, 2000 * noise(ns * v.x() + 1234) * tt + v.x() * tt / 10.0))
            npoly.add(nv)
        fill(SHADOW_COLOR)
        tsup.polygon2D(npoly)
        filter(BLUR, 4)
        fill(MAIN_COLOR)
        tsup.polygon2D(npoly)
    else:
        a = 300
        rectMode(CENTER)
        fill(SHADOW_COLOR)
        rect(width / 2 - 500 * (1 - ease_out_cubic((5 * t) ** 2)), height / 2, a, a)
        filter(BLUR, 4)
        fill(MAIN_COLOR)
        rect(width / 2 - 500 * (1 - ease_out_cubic((5 * t) ** 2)), height / 2, a, a)

def setup():
    global square
    global tsup

    size(W, H)
    frameRate(FPS)

    tsup = ToxiclibsSupport(this)

    a = Vec2D(100, 100)
    b = Vec2D(400, 100)
    c = Vec2D(400, 400)
    d = Vec2D(100, 400)
    ab = Line2D(a, b)
    bc = Line2D(b, c)
    cd = Line2D(c, d)
    da = Line2D(d, a)

    n = 100
    square = Polygon2D()
    for l in [ab, bc, cd, da]:
        for i in range(n):
            p = l.toRay2D().getPointAtDistance(i / float(n) * l.getLength())
            square.add(p)

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
            t = (frameCount + 0.25 * sample / float(N_SAMPLES)) / N_FRAMES
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
