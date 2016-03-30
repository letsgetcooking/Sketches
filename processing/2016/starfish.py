from toxi.geom import Vec2D, Ray2D, Line2D


W = H = 500
FPS = 20.0
DURATION = 3
N_FRAMES = DURATION * FPS
N_SAMPLES = 4
BG_COLOR = color(18, 114, 123)
DEEP_COLOR = color(10)
MAIN_COLOR = color(70)
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
        for i in range(self.size):
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
            r = random(2)
            fill(floor(r) * 246 + 20, floor(r) * 105 + 20, floor(r) * 80 + 20)
            seg.display()
        popMatrix()

        stroke(DEEP_COLOR)
        noFill()
        for i in range(self.size):
            arc(0, i - 10, 3 * self.fatness, 1.2 * self.fatness, 0, PI);
        stroke(MAIN_COLOR)
        arc(0, 0 - 10, 3 * self.fatness, 1.2 * self.fatness, 0, PI);

        popMatrix()


def draw_(t):
    background(BG_COLOR)

    pushMatrix()
    translate(width / 2, height / 2)
    rotate(TWO_PI / 5.0 * t)
    for i in range(5):
        rotate(TWO_PI / 5.0)
        for sprout in sprouts:
            sprout.display(t)
    popMatrix()

    noStroke()
    fill(DEEP_COLOR)
    ellipse(width / 2, height / 2, 100, 100)

def setup():
    global sprouts

    size(W, H)
    frameRate(FPS)

    strokeJoin(MITER)
    strokeCap(PROJECT)

    sprouts = []
    sprouts.append(Sprout(0, -90, 40, 40))

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
            t = (frameCount + 0.5 * sample / float(N_SAMPLES)) / N_FRAMES
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
