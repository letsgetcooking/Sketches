from toxi.geom import Vec2D


W = H = 500
FPS = 20.0
DURATION = 12
N_FRAMES = DURATION * FPS
N_SAMPLES = 1
BG_COLOR = color(255)
MAIN_COLOR = color(0)
GAP = 6
MAX_HELPLESSNESS = 8
MAX_SPEED = 5
UNIT_SIZE = 20
RECORD = False


DARK_RED = color(83, 12, 12)
RED = color(143, 14, 14)
ORANGE = color(250, 126, 10)
WHITE = color(247, 246, 222)


class Goal(object):
    def __init__(self, x, y):
        self.pos = Vec2D(x, y)
        self.size = 30

    def display(self):
        stroke(RED)
        strokeWeight(3)
        fill(DARK_RED)
        ellipse(self.pos.x(), self.pos.y(), self.size - 6, self.size - 6)


class Unit(object):
    def __init__(self, x, y):
        self.pos = Vec2D(x, y)
        self.size = UNIT_SIZE
        self.speed = 1
        self.helplessness = 0

    def display(self):
        stroke(RED)
        strokeWeight(3)
        fill(ORANGE)
        ellipse(self.pos.x(), self.pos.y(), self.size, self.size)

    def update(self):
        if self.helplessness < MAX_HELPLESSNESS and self.pos.distanceTo(goal.pos) > self.size / 2 + goal.size / 2 + GAP:
            d = goal.pos.sub(self.pos).getNormalizedTo(self.speed)
            score = -999999999
            next_pos = None
            min_dist = 0
            for th in range(360):
                theta = radians(th)
                new_pos = self.pos.add(d.getRotated(theta))
                new_dist_to_goal = new_pos.distanceTo(goal.pos)
                min_dist_to_other = min(new_pos.distanceTo(unit.pos) for unit in units if not unit is self)
                new_score = min_dist_to_other - new_dist_to_goal
                if new_score > score and not min_dist_to_other < GAP + self.size:
                    score = new_score
                    next_pos = new_pos
                    min_dist = min_dist_to_other
            if next_pos:
                if self.pos.distanceTo(goal.pos) <= next_pos.distanceTo(goal.pos):
                    next_pos = self.pos.add(next_pos.sub(self.pos).getNormalized())
                    self.helplessness += 1
                    self.speed = 1
                else:
                    self.speed = min(self.speed + 1, MAX_SPEED)
                self.pos = next_pos
        if N_FRAMES - frameCount < UNIT_SIZE / 2:
            self.size = max(0, self.size - 2)


def draw_(t):
    background(WHITE)
    noStroke()

    goal.display()
    for unit in units:
        unit.update()
        unit.display()

def setup():
    global units
    global goal

    size(W, H)
    frameRate(FPS)

    goal = Goal(width / 2, height / 2)
    units = []
    for i in range(300):
        r = random(350, 800)
        angle = random(TWO_PI)
        x, y = r * cos(angle) + width / 2, r * sin(angle) + height / 2
        for unit in units:
            if Vec2D(x, y).distanceTo(unit.pos) < GAP + UNIT_SIZE:
                break
        else:
            units.append(Unit(x, y))

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
