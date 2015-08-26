from toxi.geom import Vec2D, Ray2D


W = H = 500
FPS = 20.0
DURATION = 2
N_FRAMES = DURATION * FPS
N_SAMPLES = 4
BG_COLOR = color(201, 184, 73)
COLOR1 = color(111, 11, 0)
COLOR2 = color(201, 104, 35)
RECORD = False


def polar2cart(r, theta):
    """ polar coordinates to cartesian """
    return r * cos(theta), r * sin(theta)

def cart2polar(x, y):
    """ cartesian coordinates to polar """
    return sqrt(x ** 2 + y ** 2), atan2(y, float(x))

def draw_(t):
    background(BG_COLOR)

    m = 64.0
    pushMatrix()
    translate(W / 2, H / 2)
    rotate(TWO_PI / (m / 2.0) * t)
    translate(-W / 2, -H / 2)

    center = Vec2D(W / 2, H / 2)

    for j in range(m):
        for k in range(4):
            tt = (t + 0.125 * (j % 2) + 0.25 * k) % 1
            n = 60.0
            w = 120.0
            l = 340 - w
            a = Vec2D(W / 2 - 40 * cos(TWO_PI * j / m) , H / 2 - 40 * sin(TWO_PI * j / m))
            r = Ray2D(a, Vec2D(cos(TWO_PI * j / m), sin(TWO_PI * j / m)))
            b = r.getPointAtDistance(l)
            noStroke()

            for i in range(n):
                p = r.getPointAtDistance(tt * l + i / n * w)
                rad_k = 8
                rad = int(constrain(tt * l, 0, w / 2) * constrain(l - tt * l, 0, w / 2)
                    / ((w / 2) ** 2) * rad_k * exp(-((i / n * 16 - 8) ** 2) / 10.0))
                fill(lerpColor(COLOR1, COLOR2, (p.distanceTo(center) + 100 * (m % 2)) / 250.0))
                ellipse(p.x(), p.y(), rad, rad)
    popMatrix()

def setup():
    size(W, H, P3D)
    frameRate(FPS)

def draw():
    if not RECORD:
        t = (frameCount / float(N_FRAMES)) % 1.0
        draw_(t)
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
