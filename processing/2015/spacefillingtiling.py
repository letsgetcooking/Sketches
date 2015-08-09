from toxi.geom import Circle, Vec2D
from random import choice


W = H = 500
FPS = 20.0
DURATION = 4
N_FRAMES = DURATION * FPS
N_SAMPLES = 1
BG_COLOR = color(213, 80, 56)
MAIN_COLOR = color(166, 209, 202)
SECOND_COLOR = color(8, 4, 25)
THIRD_COLOR = color(139, 173, 142)
RECORD = False


class TiledRect:

    def __init__(self, x, y, w, h):
        self.x = int(x)
        self.y = int(y)
        self.width = int(w)
        self.height = int(h)

        if self.width >= self.height:
            self.direction = choice(('LEFT', 'RIGHT'))
        else:
            self.direction = choice(('UP', 'DOWN'))
        self.filling = self.make_tiling(self.width, self.height, 500 + 2500 * w * h / 40000.0)
        self.shift_value = 0

    def display(self):
        if self.direction in ('LEFT', 'RIGHT'):
            copy(self.filling, self.width - self.shift_value, 0, self.shift_value, self.height,
                    self.x, self.y, self.shift_value, self.height)
            copy(self.filling, 0, 0, self.width - self.shift_value, self.height,
                    self.x + self.shift_value, self.y, self.width - self.shift_value, self.height)
        else:
            copy(self.filling, 0, self.height - self.shift_value, self.width, self.shift_value,
                    self.x, self.y, self.width, self.shift_value)
            copy(self.filling, 0, 0, self.width, self.height - self.shift_value,
                    self.x, self.y + self.shift_value, self.width, self.height - self.shift_value)
        noFill()
        stroke(0)
        strokeWeight(2)
        rect(self.x, self.y, self.width, self.height)

    def make_tiling(self, w, h, max_area):
        circles = []
        for i in range(1, 500):
            rad = sqrt(max_area * (i ** (-0.75 - 0.2 * (1 - w * h / 40000.0))) / PI)
            for j in range(400):
                candidates = []
                c = Circle(random(w), random(h), rad)
                candidates.append(c)
                if self.direction in ('LEFT', 'RIGHT'):
                    if c.x() - rad < 0:
                        candidates.append(Circle(c.x() + w, c.y(), rad))
                    if c.x() + rad > w:
                        candidates.append(Circle(c.x() - w, c.y(), rad))
                else:
                    if c.y() - rad < 0:
                        candidates.append(Circle(c.x(), c.y() + h, rad))
                    if c.y() + rad > h:
                        candidates.append(Circle(c.x(), c.y() - h, rad))
                for circle in circles:
                    for cand in candidates:
                        if circle.containsPoint(Vec2D(cand.x(), cand.y())) or cand.intersectsCircle(circle):
                            break
                    else:
                        continue
                    break
                else:
                    for cand in candidates:
                        circles.append(cand)
                    break

        pg = createGraphics(w, h)
        pg.beginDraw()
        pg.background(SECOND_COLOR)
        pg.noStroke()
        pg.fill(MAIN_COLOR)
        for circle in circles:
            pg.ellipse(circle.x(), circle.y(), 2 * circle.getRadius(), 2 * circle.getRadius())
        pg.endDraw()
        return pg

    def shift(self, amt):
        if self.direction == 'RIGHT':
            self.shift_value = int(self.width * amt)
        elif self.direction == 'DOWN':
            self.shift_value = int(self.height * amt)
        elif self.direction == 'LEFT':
            self.shift_value = int(self.width * (1 - amt))
        elif self.direction == 'UP':
            self.shift_value = int(self.height * (1 - amt))

def make_rectangle(x, y, w, h, min_side, rectangles):
    random_value = random(1)
    if w >= h and w > 2 * min_side and random_value > 0.2 + 0.2 * min_side / float(w):
        left_w = min_side + random(w - 2 * min_side)
        right_w = w - left_w
        make_rectangle(x, y, left_w, h, min_side, rectangles)
        make_rectangle(x + left_w, y, right_w, h, min_side, rectangles)
    elif w < h and h > 2 * min_side and random_value > 0.2 + 0.2 * min_side / float(h):
        left_h = min_side + random(h - 2 * min_side)
        right_h = h - left_h
        make_rectangle(x, y, w, left_h, min_side, rectangles)
        make_rectangle(x, y + left_h, w, right_h, min_side, rectangles)
    else:
        rectangles.append(TiledRect(x, y, w, h))


def draw_(t):
    background(BG_COLOR)
    strokeWeight(2)
    fill(THIRD_COLOR)
    rect(105, 105, 290, 290)
    for rectangle in rectangles:
        rectangle.shift(t)
        rectangle.display()

def setup():
    global rectangles
    size(W, H)
    frameRate(FPS)
    rectangles = []
    make_rectangle(110, 110, 280, 280, 30, rectangles)

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

