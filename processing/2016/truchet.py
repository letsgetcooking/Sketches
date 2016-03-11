from toxi.geom import Polygon2D, Vec2D
from toxi.processing import ToxiclibsSupport
from random import choice


W = H = 500
FPS = 20.0
DURATION = 6
N_FRAMES = DURATION * FPS
N_SAMPLES = 1
BG_COLOR = color(255)
MAIN_COLOR = color(0)
GRID_W, GRID_H = 10, 10
RECORD = False


class Diamond(object):
    def __init__(self, x, y, angle):
        self.pos = Vec2D(x, y)
        self.angle = angle
        self.cur_angle = angle
        self.size = 46
        self.target = Vec2D(x, y)
        self.rotation = False

    def display(self, shadow=False):
        rectMode(CENTER)

        pushMatrix()
        translate(self.pos.x(), self.pos.y())
        rotate(self.cur_angle)
        if shadow:
            fill(0)
            rect(0, 0, self.size, self.size, 8)
        else:
            fill(255)
            rect(0, 0, self.size, self.size, 8)
            strokeWeight(5)
            stroke(0)
            noFill()
            arc(-self.size / 2, -self.size / 2, self.size, self.size, 0, HALF_PI)
            arc(self.size / 2, self.size / 2, self.size, self.size, PI, PI + HALF_PI)
            strokeWeight(1)
            stroke(50)
            rect(0, 0, self.size, self.size, 8)
        popMatrix()

    def move_to(self, x, y):
        self.target = Vec2D(x, y)

    def rotate(self):
        self.rotation = True

    def update(self, t):
        path = self.target.sub(self.pos).scale(t)
        self.pos.addSelf(path)

        if self.rotation:
            self.cur_angle = self.angle + t * HALF_PI
            if t > 0.99:
                self.rotation = False
                self.cur_angle = self.angle = self.angle + HALF_PI

def ease_in_out_cubic(t):
    t *= 2
    if t < 1:
        return 0.5 * t*t*t
    t -= 2
    return 0.5 * (t*t*t + 2)

def draw_(t):
    global time

    background(BG_COLOR)
    strokeCap(SQUARE)
    noFill()

    for diamond in diamonds:
        diamond.update(ease_in_out_cubic((t * GRID_H) % 1))

    for diamond in diamonds: diamond.display(shadow=True)
    filter(BLUR, 2)
    for diamond in diamonds: diamond.display()

    if t > time:
        time = (time + 1.0 / GRID_H) % 1.0
        if t < 0.9:
            for _ in range(20): choice(diamonds).rotate()
        else:
            for diamond in diamonds:
                if diamond.angle % PI:
                    diamond.rotate()

def setup():
    global diamonds
    global time
    global tsup

    size(W, H)
    frameRate(FPS)
    tsup = ToxiclibsSupport(this)

    diamonds = []
    for i in range(GRID_W):
        for j in range(GRID_H):
            x = (i + 0.5) * width / GRID_W
            y = (j + 0.5) * height / GRID_H
            diamonds.append(Diamond(x, y, 0))

    time = 0.0

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
