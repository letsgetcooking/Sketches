from toxi.geom import Line2D, Vec2D
from toxi.color import ColorGradient, TColor
from toxi.math import CosineInterpolation


W = H = 500
FPS = 30.0
DURATION = 1
N_FRAMES = DURATION * FPS
N_SAMPLES = 4
BG_COLOR = color(42, 46, 46)
MAIN_COLOR = color(62, 66, 66)
STROKE_COLOR = color(25)
RES = 200
R_MAIN = 60
R_HEX = 120
RECORD = False
PALETTE = [color(0, 95, 107), color(0, 140, 158), color(0, 180, 204),
        color(0, 223, 252), color(0, 95, 107)]


class Poly(dict):
    def __init__(self,*arg,**kw):
        super(Poly, self).__init__(*arg, **kw)

    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]


def draw_contour():
    strokeWeight(4)
    stroke(STROKE_COLOR)
    noFill()
    for ribbon in ribbons:
        beginShape()
        vertex(ribbon[0].a.x(), ribbon[0].a.y())
        vertex(ribbon[0].b.x(), ribbon[0].b.y())
        vertex(ribbon[1].b.x(), ribbon[1].b.y())
        vertex(ribbon[1].a.x(), ribbon[1].a.y())
        endShape(CLOSE)

def draw_gradient(t):
    noStroke()
    for i in range(6):
        ribbon = ribbons[i]
        a = ribbon[0]
        b = ribbon[1]
        for j in range(100):
            c = Line2D(a.toRay2D().getPointAtDistance(a.getLength() * j / 100.0),
                b.toRay2D().getPointAtDistance(b.getLength() * j / 100.0))
            for k in range(RES):
                v = c.toRay2D().getPointAtDistance(c.getLength() * k / float(RES))
                fill(colors.get(int((k + t * RES) % RES)).toARGB())
                ellipse(v.x(), v.y(), 2, 2)

def draw_(t):
    background(BG_COLOR)

    r = R_MAIN + R_HEX
    if t < 0.5:
        tt = (2 * t) ** 2
    else:
        tt = (2 * t - 2) ** 2

    pushMatrix()
    translate(width / 2, height / 2 - 15 + tt * (r - r * cos(PI / 6)))
    rotate(t * TWO_PI / 6)
    draw_contour()
    filter(BLUR, 4)
    draw_gradient(0)
    popMatrix()

    pushMatrix()
    translate(width / 2, height / 2 - 10)
    stroke(MAIN_COLOR)
    fill(MAIN_COLOR)
    strokeWeight(5)
    h = r
    line(-150, h, 150, h)

    l = Line2D(Vec2D(-150, h + 1), Vec2D(150, h + 1))
    strokeWeight(3)
    for i in range(21):
        p = l.toRay2D().getPointAtDistance(constrain(l.getLength()
            * i / 10.0 - 2 * t * r * sin(PI / 6), 0, l.getLength()))
        if p.x() != l.a.x() and p.x() != l.b.x():
            line(p.x(), p.y(), p.x() - 5, p.y() + 5)
    popMatrix()

def setup():
    global colors
    global shadow
    global ribbons
    global hexs

    size(W, H)
    frameRate(FPS)
    strokeJoin(BEVEL)
    noFill()

    hexs = []
    for i in range(6):
        hx = Poly()
        angle = TWO_PI * i / 6.0 - PI / 6.0
        centerx, centery = R_MAIN * cos(angle), R_MAIN * sin(angle)
        for j, letter in enumerate(['a', 'b', 'c', 'd', 'e', 'f']):
            a = TWO_PI * j / 6.0 - PI / 6.0
            x, y = R_HEX * cos(a) + centerx, R_HEX * sin(a) + centery
            hx[letter] = Vec2D(x, y)
        hexs.append(hx)

    # translate(width / 2, height / 2)
    # for i, hx in enumerate(hexs):
    #     for l in ['a', 'b', 'c', 'd', 'e', 'f']:
    #         v = hx[l]
    #         ellipse(v.x(), v.y(), 3, 3)
    #         text(l + str(i), v.x(), v.y())


    ribbons = []
    ribbons.append((Line2D(hexs[5].f, hexs[5].e),
        Line2D(hexs[0].f, hexs[3].a)))
    ribbons.append((Line2D(hexs[0].a, hexs[0].f),
        Line2D(hexs[1].a, hexs[4].b)))
    ribbons.append((Line2D(hexs[1].b, hexs[1].a),
        Line2D(hexs[2].b, hexs[5].c)))
    ribbons.append((Line2D(hexs[2].c, hexs[2].b),
        Line2D(hexs[3].c, hexs[0].d)))
    ribbons.append((Line2D(hexs[3].d, hexs[3].c),
        Line2D(hexs[4].d, hexs[1].e)))
    ribbons.append((Line2D(hexs[4].e, hexs[4].d),
        Line2D(hexs[5].e, hexs[2].f)))

    grad = ColorGradient()
    grad.setInterpolator(CosineInterpolation())
    for i, col in enumerate(PALETTE):
        grad.addColorAt(i / float(len(PALETTE)) * RES, TColor.newRGB(
            red(col) / 255.0, green(col) / 255.0, blue(col) / 255.0))
    colors = grad.calcGradient(0, RES)

def draw():
    if not RECORD:
        t = (frameCount / float(N_FRAMES)) % 1.0
        draw_(t)
    elif N_SAMPLES <= 1:
        t = (frameCount / float(N_FRAMES)) % 1.0
        draw_(t)
        if frameCount <= N_FRAMES:
            saveFrame('gif/####.png')
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
            saveFrame('gif/####.png')
        else:
            exit()
