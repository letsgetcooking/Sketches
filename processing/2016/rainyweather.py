from toxi.geom import Vec2D, Ray2D, Line2D


W = H = 500
FPS = 20.0
DURATION = 3
N_FRAMES = DURATION * FPS
N_SAMPLES = 1
BG_COLOR = color(255)
DEEP_COLOR = color(10)
MAIN_COLOR = color(85)
FIGURE_COLOR = color(120)
STROKE_COLOR = color(0)
WATER_COLOR = color(12, 19, 25)
RECORD = False


class Segment(object):
    def __init__(self, dx, dy, size):
        self.dx, self.dy = dx, dy
        self.size = size

    def display(self):
        ellipse(0, 0, 2 * self.size, 2 * self.size)


class Sprout(object):
    def __init__(self, x, y, fatness, size):
        self.x = x
        self.y = y
        self.fatness = fatness
        self.size = size
        self.seed = int(random(1000))
        self.speed = 1
        self.segments = []
        for i in range(int(self.size)):
            seg = Segment((len(self.segments) - i) * (2 * noise(0.05 * i) - 1),
                -2 * ((1.2 * self.size - i) / (float(self.size) / 2)), (1 - i / float(self.size)) * self.fatness)
            self.segments.append(seg)

    def display(self, t):
        randomSeed(self.seed)
        pushMatrix()
        translate(self.x, self.y)

        strokeWeight(self.size / 20.0)

        noFill()
        stroke(5)
        for i in range(self.size / 2):
            arc(0, i - 10, 3 * self.fatness, 1.2 * self.fatness, -PI, 0);
        stroke(MAIN_COLOR)
        arc(0, 0 - 10, 3 * self.fatness, 1.2 * self.fatness, -PI, 0);

        noStroke()
        fill(FIGURE_COLOR)

        pushMatrix()
        ellipse(0, 0, 2 * self.fatness, 2 * self.fatness)
        for i, seg in enumerate(self.segments):
            translate(seg.dx + 2 * ((len(self.segments) - i) / (len(self.segments) / 3.0)) *
                (i / (self.size / 2.0)) * sin(self.speed * TWO_PI * (i / float(len(self.segments)) + t) + self.seed), seg.dy)
            fill(floor(random(2)) * 120 + 20)
            seg.display()
        popMatrix()

        stroke(DEEP_COLOR)
        noFill()
        for i in range(self.size / 2):
            arc(0, i - 10, 3 * self.fatness, 1.2 * self.fatness, 0, PI);
        stroke(MAIN_COLOR)
        arc(0, 0 - 10, 3 * self.fatness, 1.2 * self.fatness, 0, PI);

        popMatrix()


def draw_(t):
    background(BG_COLOR)

    offset = -300
    axis = Line2D(Vec2D(width, offset - 200), Vec2D(width, 1.2 * height + offset))
    n = 130.0
    angle = PI / 4
    left_wave = []

    noFill()
    stroke(STROKE_COLOR)

    for i in range(int(n)):
        dist_left = (n - i - 1) * 8.5 + (1 - i / n) * 58 * (sin(t * TWO_PI + i / 4.0) + 1) / 2

        start = axis.toRay2D().getPointAtDistance(i / n * axis.getLength())
        direction_left = Vec2D(0, 1).rotate(angle)
        left = Ray2D(start, direction_left)
        v1 = left.getPointAtDistance(dist_left)
        v2 = start

        if random(1) < 0.04:
            strokeWeight(4.6)
        else:
            strokeWeight(5)

        beginShape()
        vertex(v1.x(), v1.y())
        vertex(v2.x(), v2.y())
        endShape()

        left_wave.append(v1)

    noStroke()
    fill(DEEP_COLOR)
    rectMode(CORNER)
    rect(0, height / 2, width, height / 2)

    stroke(MAIN_COLOR)
    strokeWeight(3)
    bezier(0, height / 2, 150, height / 2 - 10, width - 150, height / 2 - 10, width, height / 2)

    for sprout in sprouts:
        sprout.display(t)

    if 0.74 < t < 0.77 or 0.8 < t < 0.92:
        filter(INVERT)

def setup():
    global sprouts

    size(W, H)
    frameRate(FPS)

    strokeJoin(MITER)
    strokeCap(PROJECT)

    sprouts = []
    sprouts.append(Sprout(width / 2, height / 2 + 120, 50, 80))

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
