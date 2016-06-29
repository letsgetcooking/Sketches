from geomerative import RPath, RPoint
from toxi.color import ColorGradient, TColor


W = H = 500
FPS = 20.0
DURATION = 2
N_FRAMES = DURATION * FPS
N_SAMPLES = 4
BG_COLOR = color(35)
MAIN_COLOR = color(0)
RECORD = False

PALETTE = ((0, 0, 0),)


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

def draw_shape(shape, res, w, t, scolor=None, pg=None):
    if not pg:
        pg = this

    pg.pushStyle()
    pg.noStroke()

    res = int(res)
    grad = ColorGradient()
    for i, col in enumerate(PALETTE):
        grad.addColorAt(i / float(len(PALETTE)) * res, TColor.newRGB(*col))
    colors = grad.calcGradient(0, res)

    if scolor:
        pg.fill(scolor)
        pg.beginShape()
        for p in shape.getPoints():
            pg.vertex(p.x, p.y)
        pg.endShape(CLOSE)

    for i in range(res):
        k = 20.0
        fat_k = (1 - ((constrain(i / k, 0, 1) - 1) ** 8)) \
                * (1 - (constrain((i - res + k) / k, 0, 1) ** 8))
        fat_k = fat_k * (i / float(res) * 0.85 + 0.15)
        p = shape.getPoint(i / float(res))
        pg.fill(colors.get(int((i + t * res) % res)).toARGB())
        pg.ellipse(p.x, p.y, w * fat_k, w * fat_k)

    pg.popStyle()

def make_spiral():
    path = None
    prev = None
    for i in range(900):
        theta = i / 900.0 * 5.25 * TWO_PI
        r = 10 * exp(0.1 * theta)
        x, y = r * cos(theta) + width / 2, r * sin(theta) + height / 2
        p = RPoint(x, y)
        if not prev or p.dist(prev) > 3:
            if not path:
                path = RPath(p)
            else:
                path.addLineTo(p)
            prev = p
    return path


def draw_(t):
    global PALETTE
    background(BG_COLOR)

    PALETTE = ((0.05,0.05,0.05), )

    draw_shape(path, 3000, 10, 0)
    filter(BLUR, 2)

    PALETTE = ((247,182,121), (231,124,124), (181,92,108),
        (97,48,93), (181,92,108), (247,182,121))
    PALETTE = [[comp / 255.0 for comp in col] for col in PALETTE]

    n = 200.0
    for i in range(1, int(n)):
        center = RPoint(width / 2, height / 2)
        p1 = RPoint(center)
        p2 = path.getPoint(max(1 / n, i / n - 1 / n * t))
        p1.sub(p2)
        p1.scale(-20)
        p1.add(p2)
        other = RPath(p2)
        other.addLineTo(p1)

        points = path.intersectionPoints(other)
        if points:
            if len(points) > 1:
                if points[0].dist(p2) > 5:
                    p1 = p2
                    p2 = points[0]
                else:
                    p1 = points[0]
                    p2 = points[1]
            elif len(points) > 0:
                if points[0].dist(p2) > 5:
                    p1 = p2
                    p2 = points[0]
                else:
                    p2 = p1
                    p1 = points[0]
        if i < n * 0.3:
            fatness = 1.8 * (i / float(n) * 0.25 + 0.75)
        else:
            fatness = 1.8 * ((((i - 0.3 * n) / (0.7 * n) - 1) ** 2) * 0.75 + 0.25)
        draw_line(p1.x, p1.y, p2.x, p2.y, fatness, t)

    PALETTE = ((247,182,121), (231,124,124), (181,92,108),
        (97,48,93), (247,182,121))
    PALETTE = [[comp / 255.0 for comp in col] for col in PALETTE]

    draw_shape(path, 3000, 8, 0)

def setup():
    global path

    size(W, H)
    frameRate(FPS)

    path = make_spiral()

def draw():
    if not RECORD:
        t = (frameCount / float(N_FRAMES)) % 1.0
        draw_(t)
    elif N_SAMPLES <= 1:
        t = (frameCount / float(N_FRAMES)) % 1.0
        draw_(t)
        if frameCount <= N_FRAMES:
            saveFrame('png/####.png')
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
            saveFrame('png/####.png')
        else:
            exit()
