from toxi.geom import Vec2D, Ray2D, Line2D


W = H = 500
FPS = 20.0
DURATION = 3
N_FRAMES = DURATION * FPS
N_SAMPLES = 1
BG_COLOR = color(255)
DEEP_COLOR = color(0)
MAIN_COLOR = color(65)
FIGURE_COLOR = color(220)
FIGURE_COLOR2 = color(130)
STROKE_COLOR = color(0)
WATER_COLOR = color(12, 19, 25)
RECORD = False


LOW, MIDDLE, HIGH = range(3)


class Bubble(object):
    def __init__(self, x, y, size, angle, type):
        self.x, self.y = x, y
        self.size = size
        self.angle = angle
        self.type = type

    def display(self, t):
        strokeWeight(1)
        noFill()

        if self.type == LOW:
            x = self.x - t * width
        elif self.type == MIDDLE:
            x = self.x - t * width / 2
        else:
            x = self.x - t * width / 3
        y = self.y + 100 * noise(0.003 * x + self.y)
        a = PI / 24 * sin(t * TWO_PI)

        pushMatrix()
        translate(x, y)
        rotate(self.angle + a)
        rectMode(CENTER)
        stroke(FIGURE_COLOR2)
        strokeWeight(1.5)
        fill(DEEP_COLOR)
        rect(0, 0, self.size, self.size)
        rotate(-self.angle - a)
        fill(DEEP_COLOR)
        noStroke()
        rect(0, self.size / 2, 2 * self.size, self.size)
        stroke(MAIN_COLOR)
        strokeWeight(1)
        line(-self.size, 0, self.size, 0)
        popMatrix()

    def distance_to(self, other):
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


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
            strokeWeight(4.8)
        else:
            strokeWeight(5)

        beginShape()
        vertex(v1.x(), v1.y())
        vertex(v2.x(), v2.y())
        endShape()

        left_wave.append(v1)

    fill(0)
    strokeWeight(3)
    stroke(MAIN_COLOR)

    beginShape()
    for v in left_wave:
        vertex(v.x(), v.y())
    vertex(width + 20, height / 2)
    vertex(width + 20, height + 20)
    vertex(-20, height + 20)
    endShape(CLOSE)

    for bubble in bubbles:
        bubble.display(t)

    if 0.76 < t < 0.78 or 0.8 < t < 0.87:
        filter(INVERT)

def setup():
    global bubbles

    size(W, H)
    frameRate(FPS)

    strokeJoin(MITER)
    strokeCap(PROJECT)

    bubbles_low = []
    bubbles_middle = []
    bubbles_high = []
    bubbles = []

    while len(bubbles) < 25:
        x, y, s = random(width / 2), random(height / 2 + height / 25, height), random(15, 50)
        a = random(PI / 6) - PI / 12
        bubble = Bubble(x, y, s, a, HIGH)
        for b in bubbles:
            if bubble.distance_to(b) < bubble.size + b.size:
                break
        else:
            if y < height / 2 + height / 25 + (height - (height / 2 + height / 25)) / 3:
                t = HIGH
                bubbles_high.append(Bubble(x - 2 * width / 3, y, s, a, t))
                bubbles_high.append(Bubble(x - width / 3, y, s, a, t))
                bubbles_high.append(Bubble(x, y, s, a, t))
                bubbles_high.append(Bubble(x + width / 3, y, s, a, t))
                bubbles_high.append(Bubble(x + 2 * width / 3, y, s, a, t))
                bubbles_high.append(Bubble(x + width, y, s, a, t))
                bubbles_high.append(Bubble(x + width + width / 3, y, s, a, t))
            elif y < height / 2 + height / 25 + 2 * (height - (height / 2 + height / 25)) / 3.0:
                t = MIDDLE
                bubbles_middle.append(Bubble(x, y, s + 10, a, t))
                bubbles_middle.append(Bubble(x + width / 2, y, s + 10, a, t))
                bubbles_middle.append(Bubble(x + width, y, s + 10, a, t))
                bubbles_middle.append(Bubble(x + width + width / 2, y, s + 10, a, t))
            else:
                t = LOW
                bubbles_low.append(Bubble(x, y, s + 20, a, t))
                bubbles_low.append(Bubble(x + width, y, s + 20, a, t))

            bubbles = bubbles_high + bubbles_middle + bubbles_low

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
