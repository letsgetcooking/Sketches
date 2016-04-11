from toxi.color import ColorGradient, TColor
from toxi.geom import Vec2D
from geomerative import RG, RPath, RPoint, RShape
import pickle


W = H = 500
FPS = 20.0
DURATION = 3
N_FRAMES = DURATION * FPS
N_SAMPLES = 1
BG_COLOR = color(35, 30, 30)
MAIN_COLOR = color(0)
RECORD = False


COLORS = [(171,0,11), (255,247,0), (255,136,0), (222,74,0), (171,0,11)]
PALETTE1 = [(r / 255.0, g / 255.0, b / 255.0) for r, g, b in COLORS]
PALETTE2 = [(0, 0, 0),]
PALETTE = PALETTE1


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
        p = shape.getPoint(i / float(res))
        pg.fill(colors.get(int((i + t * res) % res)).toARGB())
        pg.ellipse(p.x, p.y, w * fat_k, w * fat_k)

def draw_(t):
    global PALETTE

    background(BG_COLOR)
    noFill()

    make_curls((sin(t * TWO_PI) + 1) / 2)
            
    offset = (float(len(main_shape.getPoints())) - 620.0) / float(len(main_shape.getPoints()))

    PALETTE = PALETTE2
    draw_shape(main_shape, 2000, 4, t)

    minlen, maxlen = 0, 0
    for mshape in mshapes:
        length = len(mshape.getPoints())
        if length > maxlen:
            maxlen = length
        if length < minlen:
            minlen = length

    for i, mshape in enumerate(mshapes):
        k = (len(mshape.getPoints()) - float(minlen)) / (float(maxlen) - float(minlen))
        draw_shape(mshape, 350 * k, 4, (t - (1 - i / float(len(mshapes))) * offset) % 1)

    filter(BLUR, 4)

    PALETTE = PALETTE1
    draw_shape(main_shape, 2000, 4, t)
    minlen, maxlen = 0, 0
    for mshape in mshapes:
        length = len(mshape.getPoints())
        if length > maxlen:
            maxlen = length
        if length < minlen:
            minlen = length

    for i, mshape in enumerate(mshapes):
        k = (len(mshape.getPoints()) - float(minlen)) / (float(maxlen) - float(minlen))
        draw_shape(mshape, 350 * k, 3, (t - (1 - i / float(len(mshapes))) * offset) % 1)

    filter(ERODE)

def make_curls(t):
    global main_shape
    global mshapes

    points = []
    mshapes = []

    coils = 8
    radius = 100
    rotation = PI / 8.0
    theta_max = coils * TWO_PI
    away_step = radius / theta_max
    chord = 2
    theta = chord / away_step
    path = None
    cntr = 0
    while theta < theta_max:
        away = away_step * theta
        around = theta + rotation
        p = RPoint(width / 2 + cos(around) * away, height / 2 + sin(around) * away)
        dist = sqrt((p.x - width / 2) ** 2 + (p.y - height) ** 2) / height
        offset = RPoint(0, -20)
        offset.rotate(PI / 3.0 * dist * (t - 0.5))
        p.add(offset)
        if not path:
            path = RPath(p)
        else:
            path.addLineTo(p)
        theta += chord / away
        cntr += 1
    path.addBezierTo(width / 2 + 2 * radius / 3, height / 2 + 100, width / 2, height - 100, width / 2, height)
    main_shape = RShape(path)

    for i, p in enumerate(main_shape.getPoints()):
        if i > 620 and not i % 15:
            prev = main_shape.getPoints()[i - 2]
            prev.sub(p)
            angle = atan2(prev.x, prev.y)

            tt = (i- 620.0) / (len(main_shape.getPoints()) - 620.0)
            k = 2 * (1 - (2 * tt - 1) ** 2) / 3.0 + 0.33

            mcoils = int(5 * k)
            mradius = 24 * k
            mrotation = PI / 6.0 * dist * constrain(t - 0.5, -1, 0)
            mtheta_max = mcoils * TWO_PI
            maway_step = mradius / mtheta_max
            mchord = 2 * k
            mtheta = mchord / maway_step
            mpath = None
            while mtheta < mtheta_max:
                away = maway_step * mtheta
                around = mtheta + mrotation
                next_point = RPoint(cos(around) * away, sin(around) * away)
                new_point = RPoint(next_point)
                new_point.rotate(-angle - HALF_PI)
                offset = RPoint(0, -2 * mradius * k - 5)
                offset.rotate(-angle - HALF_PI)
                dist = sqrt((new_point.x - width / 2) ** 2 + (new_point.y - height) ** 2) / height
                offset.rotate(PI / 6.0 * dist * constrain(t - 0.5, -1, 0))
                new_point.add(offset)
                new_point.add(p)
                if not mpath:
                    mpath = RPath(new_point)
                else:
                    mpath.addLineTo(new_point)
                mtheta += mchord / away

            new_point = RPoint(next_point)
            new_point.rotate(-angle - HALF_PI)
            offset = RPoint(0, -mradius * k - 2.5)
            offset.rotate(-angle - HALF_PI)
            dist = sqrt((new_point.x - width / 2) ** 2 + (new_point.y - height) ** 2) / height
            offset.rotate(PI / 6.0 * dist * constrain(t - 0.5, -1, 0))
            new_point.add(offset)
            new_point.add(p)
            mpath.addBezierTo(new_point, p, p)
            mshape = RShape(mpath)
            mshapes.append(mshape)

def setup():
    size(W, H)
    frameRate(FPS)
    RG.init(this)

    make_curls(0)

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
