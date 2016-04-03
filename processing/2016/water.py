from toxi.geom import Vec2D
from munkres import Munkres


W = H = 500
FPS = 20.0
DURATION = 3
N_FRAMES = DURATION * FPS
N_SAMPLES = 4
BG_COLOR = color(200, 220, 230)
MAIN_COLOR = color(37, 64, 72)
FRAME_COLOR = color(31, 38, 42)
SHADOW_COLOR = color(57, 95, 112)
RECORD = False


class Dot(object):
    def __init__(self, pos):
        self.pos = pos

    def display(self, t):
        pos = self.get_position(t)
        pushMatrix()
        translate(pos.x(), pos.y())
        ellipse(0, 0, 3, 3)

    def distance_to(self, other):
        return self.pos.distanceTo(other.pos)

    def get_position(self, state):
        return self.pos.add(Vec2D(50 * noise(5 * state + self.pos.x()),
            50 * noise(5 * state + 123 + self.pos.x())))

    def lerp_position(self, init_state, final_state, t):
        pos1 = self.get_position(init_state)
        pos2 = self.get_position(final_state)
        return pos2.sub(pos1).scale(t).add(pos1)


def draw_(t):
    background(BG_COLOR)

    pushMatrix()
    translate(-15, -20)

    fill(SHADOW_COLOR)
    stroke(SHADOW_COLOR)
    strokeWeight(30)
    rect(width / 4 + 20, height / 4 + 26, width / 2 - 10, height / 2 - 10)

    noStroke()
    fill(MAIN_COLOR)
    rect(width / 4 + 20, height / 4 + 30, width / 2 - 10, height / 2 - 10)

    noFill()

    strokeWeight(2)
    for d1 in circle:
        for d2 in circle:
            if d1 != d2 and d1.distance_to(d2) < 50:
                if t < 0.9:
                    pos1, pos2 = d1.get_position(t), d2.get_position(t)
                else:
                    t1, t2 = 0.9, 0.0
                    tt = constrain(10 * t - 9, 0, 1)
                    pos1, pos2 = d1.lerp_position(t1, t2, tt), d2.lerp_position(t1, t2, tt)
                mag = pos1.sub(pos2).magnitude()
                stroke(68, 189, 255, constrain(((1 - mag / 50.0) ** 2) * 1500, 0, 255))
                line(pos1.x(), pos1.y(), pos2.x(), pos2.y())

    filter(BLUR, 4)

    strokeWeight(1)
    for d1 in circle:
        for d2 in circle:
            if d1 != d2 and d1.distance_to(d2) < 50:
                if t < 0.9:
                    pos1, pos2 = d1.get_position(t), d2.get_position(t)
                else:
                    t1, t2 = 0.9, 0.0
                    tt = constrain(10 * t - 9, 0, 1)
                    pos1, pos2 = d1.lerp_position(t1, t2, tt), d2.lerp_position(t1, t2, tt)
                mag = pos1.sub(pos2).magnitude()
                stroke(144, 199, 226, constrain(((1 - mag / 50.0) ** 2) * 1500, 0, 255))
                line(pos1.x(), pos1.y(), pos2.x(), pos2.y())

    filter(BLUR, 5)

    for i in range(7):
        filter(ERODE)

    popMatrix()

def setup():
    global circle

    size(W, H)
    frameRate(FPS)

    R = 120
    dots = []

    for i in range(800):
        vec = Vec2D(random(width / 2) + width / 4, random(height / 2) + height / 4)
        for dot in dots:
            if vec.distanceTo(dot) < 20:
                break
        else:
            dots.append(vec)

    circle = [Dot(d) for d in dots]

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
