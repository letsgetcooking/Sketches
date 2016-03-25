from geomerative import RFont, RPoint, RG
from toxi.geom import Vec3D
from munkres import Munkres


W = H = 500
FPS = 20.0
DURATION = 2
N_FRAMES = DURATION * FPS
N_SAMPLES = 4
BG_COLOR = color(0)
MAIN_COLOR = color(0)
RECORD = False


class Dot(object):
    def __init__(self, *states):
        self.states = states
        self.state = 0

    def display(self):
        pos = self.get_position()
        pushMatrix()
        translate(pos.x(), pos.y(), pos.z())
        ellipse(0, 0, 3, 3)
        popMatrix()

    def distance_to(self, other):
        return self.get_position().distanceTo(other.get_position())

    def get_position(self):
        start_index = floor(self.state * (len(self.states))) % (len(self.states))
        finish_index = (floor(self.state * (len(self.states))) + 1) % (len(self.states))
        start = self.states[int(start_index)]
        finish = self.states[int(finish_index)]
        state = (self.state * (len(self.states)) - start_index) ** 9
        return finish.sub(start).scale(state).add(start).add(Vec3D(5 * noise(10 * self.state + start.x()),
            5 * noise(10 * self.state + 123 + start.x()), 0))

    def set_state(self, state):
        self.state = state


def draw_(t):
    background(BG_COLOR)

    strokeWeight(1)
    fill(22, 120, 225)

    a = 20 * (constrain(1 - (cos(t * TWO_PI) + 1) / 2, 0, 1) ** 3)

    for i, (dots, offset) in enumerate(zip([dots_zero, dots_zero, dots_colon, dots_zero, dots_onezero],
        [25, 125, 230, 285, 385 + a])):
        pushMatrix()
        translate(offset, 300 if offset != 230 else 280)

        for i, d in enumerate(dots):
            d.set_state(t)

        for d1 in dots:
            for d2 in dots:
                if d1 != d2 and d1.distance_to(d2) < 21:
                    pos1, pos2 = d1.get_position(), d2.get_position()
                    mag = pos1.sub(pos2).magnitude()
                    stroke(34, 79, 256, constrain(((1 - mag / 21.0) ** 2) * 1500, 0, 255))
                    line(pos1.x(), pos1.y(), pos1.z(), pos2.x(), pos2.y(), pos2.z())

        for i, d in enumerate(dots):
            d.display()
        popMatrix()

    filter(BLUR, 4)

    for i, (dots, offset) in enumerate(zip([dots_zero, dots_zero, dots_colon, dots_zero, dots_onezero],
        [25, 125, 230, 285, 385 + a])):
        pushMatrix()
        translate(offset, 300 if offset != 230 else 280)

        for i, d in enumerate(dots):
            d.set_state(t)

        for d1 in dots:
            for d2 in dots:
                if d1 != d2 and d1.distance_to(d2) < 21:
                    pos1, pos2 = d1.get_position(), d2.get_position()
                    mag = pos1.sub(pos2).magnitude()
                    stroke(14, 59, 236, constrain(((1 - mag / 21.0) ** 2) * 1500, 0, 255))
                    line(pos1.x(), pos1.y(), pos1.z(), pos2.x(), pos2.y(), pos2.z())

        for i, d in enumerate(dots):
            d.display()
        popMatrix()

def setup():
    global dots_one
    global dots_two
    global dots_colon
    global dots_zero
    global dots_onezero

    size(W, H, P3D)
    frameRate(FPS)
    RG.init(this)

    font = RFont('KOMIKA.ttf')
    font.setSize(140)
    k = 2
    m = 80.0
    n = 30.0

    one = []
    one_shape = font.toShape('1')
    while not len(one) == m:
        pnt = RPoint(random(width) / k, -random(height) / k)
        if one_shape.contains(pnt):
            one.append(Vec3D(pnt.x, pnt.y, random(15)))
    for i in range(int(n)):
        pnt = one_shape.getPoint(i / n)
        one.append(Vec3D(pnt.x, pnt.y, random(15)))

    two = []
    two_shape = font.toShape('2')
    while not len(two) == m:
        pnt = RPoint(random(width) / k, -random(height) / k)
        if two_shape.contains(pnt):
            two.append(Vec3D(pnt.x, pnt.y, random(15)))
    for i in range(int(n)):
        pnt = two_shape.getPoint(i / n)
        two.append(Vec3D(pnt.x, pnt.y, random(15)))

    colon = []
    colon_shape = font.toShape(':')
    while not len(colon) == 20.0:
        pnt = RPoint(random(width) / k, -random(height) / k)
        if colon_shape.contains(pnt):
            colon.append(Vec3D(pnt.x, pnt.y, random(15)))
    for i in range(12):
        pnt = colon_shape.getPoint(i / 12.0)
        colon.append(Vec3D(pnt.x, pnt.y, random(15)))

    zero = []
    zero_shape = font.toShape('0')
    while not len(zero) == m:
        pnt = RPoint(random(width) / k, -random(height) / k)
        if zero_shape.contains(pnt):
            zero.append(Vec3D(pnt.x, pnt.y, random(15)))
    for i in range(int(n)):
        pnt = zero_shape.getPoint(i / n)
        zero.append(Vec3D(pnt.x, pnt.y, random(15)))

    matrix = [[int(o_point.distanceTo(z_point)) for o_point in one] for z_point in zero]
    m = Munkres()
    indices_zeroone = m.compute(matrix)

    matrix = [[int(o_point.distanceTo(z_point)) for o_point in two] for z_point in one]
    m = Munkres()
    indices_onetwo = m.compute(matrix)

    indices = [[a, b, 0] for a, b in indices_zeroone]
    for index in indices:
        for onetwo in indices_onetwo:
            if index[1] == onetwo[0]:
                index[2] = onetwo[1]

    dots_one = [Dot(d, d) for d in one]
    dots_colon = [Dot(d, d) for d in colon]
    dots_zero = [Dot(d, d) for d in zero]

    dots_onezero = [Dot(zero[zi], one[oi], two[ti]) for zi, oi, ti in indices]

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
