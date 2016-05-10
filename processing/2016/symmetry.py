from toxi.geom import Vec2D, Line2D, Rect
from toxi.processing import ToxiclibsSupport


W = H = 500
FPS = 20.0
DURATION = 1
N_FRAMES = DURATION * FPS
N_SAMPLES = 4
BG_COLOR = color(255)
MAIN_COLOR = color(0)
SHAPE_COLOR = color(35)
STROKE_COLOR = color(80)
RECORD = False


def draw_(t):
    background(BG_COLOR)
    noFill()

    strokeWeight(0.6)
    for i in range(1000):
        x, y = random(width), random(height)
        l = random(10)
        line(x, y, x + l, y)

    pushMatrix()
    translate(width / 2, height / 2)
    rotate(PI / 10)

    v1 = Vec2D(0, -230) 
    v1.rotate(-PI / 10)
    v2 = Vec2D(0, 230)
    v2.rotate(-PI / 10)
    l = Line2D(v1, v2)

    vs1 = []
    vs2 = []

    for i in range(40):
        r = abcd.copy()
        r.scale(((i + t) / 36.0) ** 12)

        v1 = r.getTopLeft().add(Vec2D(2 * r.getRight(), 0))
        v2 = l.closestPointTo(v1)
        if abcd.containsPoint(v1):
            vs1.append((v2.x(), v2.y() + 1))
            vs1.append((v1.x(), v1.y() + 1))
        elif abcd.containsPoint(v2):
            p = abcd.intersectsRay(Line2D(v1, v2).toRay2D(), 0, width)
            if p:
                vs1.append((v2.x(), v2.y() + 1))
                vs1.append((p.x(), p.y()))

        v1 = r.getBottomRight().add(Vec2D(2 * r.getLeft(), 0))
        v2 = l.closestPointTo(v1)
        if abcd.containsPoint(v1):
            vs2.append((v2.x() - 1, v2.y() - 0.06 * i))
            vs2.append((v1.x() - 1, v1.y()))
        elif abcd.containsPoint(v2):
            p = abcd.intersectsRay(Line2D(v1, v2).toRay2D(), 0, width)
            if p:
                vs2.append((v2.x() - 1, v2.y()))
                vs2.append((p.x() - 1, p.y()))

    noStroke()
    fill(BG_COLOR)
    tls.rect(abcd)

    v = abcd.intersectsRay(l.toRay2D(), 0, 200)
    vs1.append((v.x(), v.y()))

    v = abcd.getBottomRight().add(Vec2D(2 * abcd.getLeft(), 0))
    vs2.append((v.x() - 1, v.y()))

    fill(SHAPE_COLOR)
    noStroke()

    beginShape()
    vertex(abcd.getTopLeft().x(), abcd.getTopLeft().y())
    vertex(vs1[-1][0], vs1[-1][1])
    vertex(0, 0)
    vertex(v.x(), v.y())
    endShape(CLOSE)

    beginShape()
    for v in vs1:
        vertex(*v)
    endShape(CLOSE)

    beginShape()
    for v in vs2:
        vertex(*v)
    endShape(CLOSE)

    stroke(STROKE_COLOR)
    strokeWeight(1.5)
    noFill()
    for i in range(40):
        r = abcd.copy()
        r.scale(((i + t) / 36.0) ** 12)
        if i < 36:
            tls.rect(r)

    strokeWeight(5)
    stroke(MAIN_COLOR)
    tls.rect(abcd)

    popMatrix()

def setup():
    global abcd
    global tls

    size(W, H)
    frameRate(FPS)
    tls = ToxiclibsSupport(this)

    abcd = Rect(-105, -170, 210, 340)

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
