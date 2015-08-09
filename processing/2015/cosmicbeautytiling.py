from toxi.geom import Triangle2D, Line2D, Vec2D
from random import choice


W = H = 500
FPS = 20.0
DURATION = 4
N_FRAMES = DURATION * FPS
N_SAMPLES = 1
BG_COLOR = color(15)
MAIN_COLOR = color(109, 238, 220)
SECOND_COLOR = color(40, 30, 28)
THIRD_COLOR = color(208, 217, 102)
RECORD = False


class Figure:

    def __init__(self, x, y, area, angle):
        a = sqrt(2.31 * area)
        R = 0.577 * a
        A = Vec2D(R * cos(-HALF_PI + angle), R * sin(-HALF_PI + angle)).add(Vec2D(x, y))
        B = Vec2D(R * cos(-HALF_PI + TWO_PI / 3.0 + angle), R * sin(-HALF_PI + TWO_PI / 3.0 + angle)).add(Vec2D(x, y))
        C = Vec2D(R * cos(-HALF_PI + 2 * TWO_PI / 3.0 + angle), R * sin(-HALF_PI + 2 * TWO_PI / 3.0 + angle)).add(Vec2D(x, y))
        self.shape = Triangle2D(A, B, C)
        self.x = x
        self.y = y

    def display(self):
        beginShape()
        vertex(self.shape.a.x(), self.shape.a.y())
        vertex(self.shape.b.x(), self.shape.b.y())
        vertex(self.shape.c.x(), self.shape.c.y())
        endShape(CLOSE)

    def drawon(self, pg):
        pg.beginShape()
        pg.vertex(self.shape.a.x(), self.shape.a.y())
        pg.vertex(self.shape.b.x(), self.shape.b.y())
        pg.vertex(self.shape.c.x(), self.shape.c.y())
        pg.endShape(CLOSE)

    def intersect(self, figure):
        return self.shape.intersectsTriangle(figure.shape)

    def intersectLine(self, line):
        if (Line2D(self.shape.a, self.shape.b).intersectLine(line) or
            Line2D(self.shape.b, self.shape.c).intersectLine(line) or
            Line2D(self.shape.a, self.shape.c).intersectLine(line)):
            return True
        return False


class TiledRect:

    def __init__(self, x, y, w, h):
        self.x = int(x)
        self.y = int(y)
        self.width = int(w)
        self.height = int(h)

        self.direction = 'UP'
        self.filling = self.make_tiling(self.width, self.height, 500 + 2500 * w * h / 90000.0)
        self.shift_value = 0

    def display(self):
        copy(self.filling, 0, self.height - self.shift_value, self.width, self.shift_value,
                self.x, self.y, self.width, self.shift_value)
        copy(self.filling, 0, 0, self.width, self.height - self.shift_value,
                self.x, self.y + self.shift_value, self.width, self.height - self.shift_value)

    def drawon(self, pg):
        pg.copy(self.filling, 0, self.height - self.shift_value, self.width, self.shift_value,
                self.x, self.y, self.width, self.shift_value)
        pg.copy(self.filling, 0, 0, self.width, self.height - self.shift_value,
                self.x, self.y + self.shift_value, self.width, self.height - self.shift_value)

    def make_tiling(self, w, h, max_area):
        figures = []
        angle = 0 if self.direction == 'UP' else PI
        for i in range(1, 2000):
            area = max_area * (i ** (-1.0 - 0.2 * (1 - w * h / 90000.0)))
            for j in range(200):
                candidates = []
                f = Figure(random(w), random(h), area, angle)
                candidates.append(f)

                if f.intersectLine(Line2D(Vec2D(self.x, self.y), Vec2D(self.x + self.width, self.y))):
                    candidates.append(Figure(f.x, f.y + h, area, angle))
                if f.intersectLine(Line2D(Vec2D(self.x, self.y + self.height), Vec2D(self.x + width, self.y + self.height))):
                    candidates.append(Figure(f.x, f.y - h, area, angle))

                for fig in figures:
                    for cand in candidates:
                        if fig.intersect(cand):
                            break
                    else:
                        continue
                    break
                else:
                    for cand in candidates:
                        figures.append(cand)
                    break

        pg = createGraphics(w, h)
        pg.beginDraw()
        pg.background(SECOND_COLOR)
        pg.noStroke()
        pg.fill(MAIN_COLOR)
        for figure in figures:
            figure.drawon(pg)
        pg.endDraw()
        return pg

    def shift(self, amt):
        if self.direction == 'DOWN':
            self.shift_value = int(self.height * amt)
        elif self.direction == 'UP':
            self.shift_value = int(self.height * (1 - amt))


def draw_(t):
    background(BG_COLOR)

    tile.shift(t)
    tile.display()

    fill(BG_COLOR)
    stroke(0)
    strokeWeight(6)
    R = 0.577 * 300
    beginShape()
    vertex(-10, -10)
    vertex(width + 10, -10)
    vertex(width + 10, height + 10)
    vertex(-10, height + 10)
    beginContour()
    for i in range(3):
        vertex(R * cos(-HALF_PI - i * TWO_PI / 3.0) + width / 2, R * sin(-HALF_PI - i * TWO_PI / 3.0) + height / 2 + 40)
    endContour()
    endShape(CLOSE)

    noFill()
    stroke(THIRD_COLOR)
    strokeWeight(4)
    R = 0.577 * 300
    beginShape()
    for i in range(3):
        vertex(R * cos(-HALF_PI + i * TWO_PI / 3.0) + width / 2, R * sin(-HALF_PI + i * TWO_PI / 3.0) + height / 2 + 40)
    endShape(CLOSE)

    noFill()
    stroke(THIRD_COLOR)
    strokeWeight(2)
    R = 0.577 * 330
    A = Vec2D(R * cos(-HALF_PI + 0 * TWO_PI / 3.0) + width / 2, R * sin(-HALF_PI + 0 * TWO_PI / 3.0) + height / 2 + 40)
    B = Vec2D(R * cos(-HALF_PI + 1 * TWO_PI / 3.0) + width / 2, R * sin(-HALF_PI + 1 * TWO_PI / 3.0) + height / 2 + 40)
    C = Vec2D(R * cos(-HALF_PI + 2 * TWO_PI / 3.0) + width / 2, R * sin(-HALF_PI + 2 * TWO_PI / 3.0) + height / 2 + 40)
    AB = Line2D(A, B).toRay2D()
    BC = Line2D(B, C).toRay2D()
    CA = Line2D(C, A).toRay2D()

    dist1 = constrain(330 * t - 50, 0, 330)
    dist2 = constrain(330 * t + 100, 0, 330)
    if dist2 - dist1 > 0:
        AB1, AB2 = AB.getPointAtDistance(dist1), AB.getPointAtDistance(dist2)
        line(AB1.x(), AB1.y(), AB2.x(), AB2.y())
        BC1, BC2 = BC.getPointAtDistance(dist1), BC.getPointAtDistance(dist2)
        line(BC1.x(), BC1.y(), BC2.x(), BC2.y())
        CA1, CA2 = CA.getPointAtDistance(dist1), CA.getPointAtDistance(dist2)
        line(CA1.x(), CA1.y(), CA2.x(), CA2.y())

    dist1 = constrain(330 * t + 280, 0, 330)
    dist2 = constrain(330 * t + 330, 0, 330)
    if dist2 - dist1 > 0:
        AB1, AB2 = AB.getPointAtDistance(dist1), AB.getPointAtDistance(dist2)
        line(AB1.x(), AB1.y(), AB2.x(), AB2.y())
        BC1, BC2 = BC.getPointAtDistance(dist1), BC.getPointAtDistance(dist2)
        line(BC1.x(), BC1.y(), BC2.x(), BC2.y())
        CA1, CA2 = CA.getPointAtDistance(dist1), CA.getPointAtDistance(dist2)
        line(CA1.x(), CA1.y(), CA2.x(), CA2.y())

    dist1 = constrain(330 * t - 380, 0, 330)
    dist2 = constrain(330 * t - 230, 0, 330)
    if dist2 - dist1 > 0:
        AB1, AB2 = AB.getPointAtDistance(dist1), AB.getPointAtDistance(dist2)
        line(AB1.x(), AB1.y(), AB2.x(), AB2.y())
        BC1, BC2 = BC.getPointAtDistance(dist1), BC.getPointAtDistance(dist2)
        line(BC1.x(), BC1.y(), BC2.x(), BC2.y())
        CA1, CA2 = CA.getPointAtDistance(dist1), CA.getPointAtDistance(dist2)
        line(CA1.x(), CA1.y(), CA2.x(), CA2.y())

def setup():
    global tile
    size(W, H)
    frameRate(FPS)
    tile = []

    tile = TiledRect(100, 100, 300, 300)

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
