from toxi.geom import Line3D, Vec3D, Ray3D
import pickle


W = H = 500
FPS = 20.0
DURATION = 4
N_FRAMES = DURATION * FPS
N_SAMPLES = 4
BG_COLOR = color(220)
MAIN_COLOR = color(255)
COLOR1 = color(65)
COLOR2 = color(65)
STROKE_COLOR = color(0)
SEEDS = [int(random(10000)) for i in range(20)]
RECORD = False


class Comet:
    def __init__(self, x, y, d, w, thickness, path_length, offset):
        self.width = w
        self.res = w / 2
        self.path_length = path_length
        a = Vec3D(x, y, 0)
        self.start = Ray3D(a, d)
        self.thickness = thickness
        self.offset = offset

    def display(self, t):
        pushMatrix()
        stroke(STROKE_COLOR)

        center = Vec3D(W / 2, H / 2, 0)
        t = (t + self.offset) % 1
        w = self.width * t + 5
        th = self.thickness * (1 - (2 * t - 1) ** 2)
        strokeWeight(th)

        p1 = self.start.getPointAtDistance(t * self.path_length)
        p2 = self.start.getPointAtDistance(t * self.path_length + 50)
        line(p1.x(), p1.y(), p2.x(), p2.y())

        popMatrix()


def draw_branch(depth, windforce):
    if depth < 10:
        randomSeed(SEEDS[2 * depth])
        line(0, 0, 0, -height / 10.0)
        pushMatrix()
        translate(0, -height / 13.0)
        rotate(random(-PI / 4, PI / 4) + windforce)
        scale(0.8)
        draw_branch(depth + 1, windforce * 1.1)
        popMatrix()

        randomSeed(SEEDS[2 * depth + 1])
        pushMatrix()
        translate(0, -height / 10.0)
        rotate(random(-PI / 4, PI / 4) + windforce)
        scale(0.8)
        draw_branch(depth + 1, windforce * 1.1)
        popMatrix()

def draw_(t):
    background(BG_COLOR)

    for comet in comets:
        comet.display(3 * t)

    strokeWeight(4)
    stroke(STROKE_COLOR)
    pushMatrix()
    translate(W / 2, H / 2 + 120)
    draw_branch(0, sin(t * 2 * PI) * PI / 200)
    popMatrix()

    bc, fb = lines[0], lines[1]
    b = fb.b

    strokeWeight(1)

    pushMatrix()
    translate(width / 2, -200)
    rotate(-1.5 * HALF_PI)

    stroke(STROKE_COLOR)
    line(bc.a.x(), bc.a.y(), bc.b.x(), bc.b.y())
    line(fb.a.x(), fb.a.y(), fb.b.x(), fb.b.y())

    noStroke()
    fill(MAIN_COLOR)
    for p1, p2 in zip(bc.splitIntoSegments(None, 20, False), fb.splitIntoSegments(None, 20, False)):
        triangle(p1.x(), p1.y(), p2.x(), p2.y(), b.x(), b.y())

    stroke(STROKE_COLOR)
    noFill()
    for p1, p2 in zip(bc.splitIntoSegments(None, 20, False), fb.splitIntoSegments(None, 20, False)):
        line(p1.x(), p1.y(), p2.x(), p2.y())
    popMatrix()

def mousePressed():
    global SEEDS
    SEEDS = [int(random(10000)) for i in range(20)]

def keyPressed():
    global SEEDS

    if key == 's':
        pickle.dump(SEEDS, open('seeds.pkl', 'wb'))
    elif key == 'l':
        SEEDS = pickle.load(open('seeds.pkl', 'rb'))

def setup():
    global lines
    global comets

    size(W, H)
    frameRate(FPS)

    r = 800

    b = Vec3D(-r, -r, r)
    c = Vec3D(r, -r, r)
    f = Vec3D(-r, r, r)

    bc = Line3D(b, c)
    fb = Line3D(f, b)

    lines = [bc, fb]

    comets = []
    for _ in range(100):
        comets.append(Comet(random(-100, width), 0, Vec3D(0.3, 1, 0), 350.0, 1.0, 320.0, random(1)))

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
