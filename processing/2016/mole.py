from toxi.geom import Vec3D, Ray3D
from random import choice
from damkjer.ocd import Camera
from peasy import PeasyCam


W = H = 500
FPS = 20.0
DURATION = 7
N_FRAMES = DURATION * FPS
N_SAMPLES = 4
MAIN_COLOR = color(0)
PALETTE = [color(35), color(230)]
BG_COLOR = PALETTE[0]
RES = 5000.0
LENGTH = 3000.0
N = 4
JITTER = 400
RECORD = False


class Path(object):
    def __init__(self, n, length, res):
        vertices = []
        controls = []
        self.length = length

        for i in range(n):
            v = Vec3D(i / float(n) * length, 0, 0)
            vertices.append(v)

        last = Vec3D(-width / 2, 0, 0)
        for i, v in enumerate(vertices):
            if v is vertices[0] or v is vertices[-1]:
                ctr1 = v.add(Vec3D(120, 0, 0))
            else:
                ctr1 = v.copy()
                ctr1.jitter(JITTER)
            ray = Ray3D(v, v.sub(ctr1))
            ctr2 = ray.getPointAtDistance(v.distanceTo(ctr1) + random(50) - 25)
            controls.extend([ctr1, ctr2] if ctr1.distanceTo(last)
                < ctr2.distanceTo(last) else [ctr2, ctr1])
            last = controls[-1]

        lengths = []

        for i, v in enumerate(vertices[:-1]):
            mcurve = []
            for j in range(int(res)):
                a = v
                b = controls[(2 * i + 1) % len(controls)]
                c = controls[(2 * i + 2) % len(controls)]
                d = vertices[(i + 1) % len(vertices)]
                x = bezierPoint(a.x(), b.x(), c.x(), d.x(), j / float(res))
                y = bezierPoint(a.y(), b.y(), c.y(), d.y(), j / float(res))
                z = bezierPoint(a.z(), b.z(), c.z(), d.z(), j / float(res))
                mcurve.append(Vec3D(x, y, z))
            curve_len = 0.0
            for j, v in enumerate(mcurve[:-1]):
                curve_len += v.distanceTo(mcurve[j + 1])
            lengths.append(curve_len)

        max_length = max(lengths)

        self.points = []

        for i, v in enumerate(vertices[:-1]):
            cur_res = res * lengths[i] / max_length
            for j in range(1, int(cur_res)):
                a = v
                b = controls[(2 * i + 1) % len(controls)]
                c = controls[(2 * i + 2) % len(controls)]
                d = vertices[(i + 1) % len(vertices)]
                x = bezierPoint(a.x(), b.x(), c.x(), d.x(), j / float(cur_res))
                y = bezierPoint(a.y(), b.y(), c.y(), d.y(), j / float(cur_res))
                z = bezierPoint(a.z(), b.z(), c.z(), d.z(), j / float(cur_res))
                self.points.append(Vec3D(x, y, z))

    def display(self):
        if DISPLAY_MODE == 0:
            stroke(255, 0, 0)
            noFill()
            beginShape()
            for v in self.points:
                vertex(v.x(), v.y(), v.z())
            endShape(CLOSE)
        else:
            noStroke()
            fill(255, 0, 0, 10)
            for v in self.points:
                pushMatrix()
                translate(v.x(), v.y(), v.z())
                sphere(20)
                popMatrix()

    def get_direction(self, t):
        cur_index = int(t * (len(self.points)))
        current_point = self.points[cur_index % len(self.points)].copy()
        next_index = int(t * len(self.points)) + 1
        next_point = self.points[next_index % len(self.points)].copy()
        if cur_index >= len(self.points):
            current_point.addSelf(Vec3D(self.length, 0, 0))
        if next_index >= len(self.points):
            next_point.addSelf(Vec3D(self.length, 0, 0))
        return next_point.sub(current_point).getNormalized()

    def trace(self, t):
        return self.points[int(t * (len(self.points) - 1))]


def draw_(t):
    background(BG_COLOR)
    strokeWeight(1)

    v1 = path.trace(t % 1)
    direction = Vec3D(0, 0, 0)
    for i in range(6):
        dt = path.get_direction(t + i * 0.01)
        direction.addSelf(dt)
    direction.scale(1 / 6.0)
    v2 = v1.add(direction)

    cam.jump(v1.x(), v1.y(), v1.z())
    cam.aim(v2.x(), v2.y(), v2.z())
    cam.feed()

    r = 100
    noStroke()
    for i in range(40):
        fill(PALETTE[i % len(PALETTE)])
        pos1 = path.trace(i / 41.0)
        d1 = path.get_direction(i / 41.0)
        v1 = d1.cross(d1.getRotatedX(HALF_PI))
        v1.normalizeTo(r)

        pos2 = path.trace((i + 1) / 41.0)
        d2 = path.get_direction((i + 1) / 41.0)
        v2 = d2.cross(d2.getRotatedX(HALF_PI))
        v2.normalizeTo(r)
        if v2.angleBetween(v1, True) > HALF_PI:
            v2.rotateX(PI)

        beginShape(QUAD_STRIP)
        for j in range(101):
            p1 = v1.getRotatedAroundAxis(d1, j * TWO_PI / 100.0)
            vert1 = p1.add(pos1)
            vertex(vert1.x(), vert1.y(), vert1.z())
            p2 = v2.getRotatedAroundAxis(d2, j * TWO_PI / 100.0)
            vert2 = p2.add(pos2)
            vertex(vert2.x(), vert2.y(), vert2.z())
        endShape(CLOSE)

    pos = path.trace(1)
    translate(pos.x(), pos.y(), pos.z())

    for i in range(40):
        fill(PALETTE[i % len(PALETTE)])
        pos1 = path.trace(i / 41.0)
        d1 = path.get_direction(i / 41.0)
        v1 = d1.cross(d1.getRotatedX(HALF_PI))
        v1.normalizeTo(r)

        pos2 = path.trace((i + 1) / 41.0)
        d2 = path.get_direction((i + 1) / 41.0)
        v2 = d2.cross(d2.getRotatedX(HALF_PI))
        v2.normalizeTo(r)
        if v2.angleBetween(v1, True) > HALF_PI:
            v2.rotateX(PI)

        beginShape(QUAD_STRIP)
        for j in range(101):
            p1 = v1.getRotatedAroundAxis(d1, j * TWO_PI / 100.0)
            vert1 = p1.add(pos1)
            vertex(vert1.x(), vert1.y(), vert1.z())
            p2 = v2.getRotatedAroundAxis(d2, j * TWO_PI / 100.0)
            vert2 = p2.add(pos2)
            vertex(vert2.x(), vert2.y(), vert2.z())
        endShape(CLOSE)

def setup():
    global cam
    global frags
    global circles
    global path

    size(W, H, P3D)
    frameRate(FPS)

    cam = Camera(this, width / 2, height / 2, 400)
    cam.aim(width / 2, height / 2, 0)
    cam.feed()

    # cam = PeasyCam(this, 1000)
    # cam.pan(width / 2 + 2700, height / 2)

    randomSeed(488378)
    path = Path(N, LENGTH, RES)

def draw():
    if not RECORD:
        t = (frameCount / float(N_FRAMES)) % 1.0
        draw_(t)
    elif N_SAMPLES <= 1:
        t = (frameCount / float(N_FRAMES)) % 1.0
        draw_(t)
        if frameCount <= N_FRAMES:
            saveFrame('imgs/####.gif')
        else:
            exit()
    else:
        result = [[0, 0, 0] for i in range(W * H)]
        for sample in range(N_SAMPLES):
            t = (frameCount + 0.25 * sample / float(N_SAMPLES)) / N_FRAMES
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
            saveFrame('imgs/####.gif')
        else:
            exit()
