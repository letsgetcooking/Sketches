from toxi.geom import Vec3D, Ray3D
from random import choice
from damkjer.ocd import Camera
from peasy import PeasyCam
from com.hamoid import VideoExport


W = H = 480
FPS = 20.0
DURATION = 18
N_FRAMES = DURATION * FPS
N_SAMPLES = 16
BG_COLOR = color(0, 72, 83)
TEXT_COLOR = color(153, 0, 36)
PALETTE = [color(0, 126, 128), color(0, 185, 189)]
RES = 5000.0
RAD = 200.0
N = 5
JITTER = 150
DISPLAY_MODE = 0
RECORD = False
VIDEO = False


class Path(object):
    def __init__(self, n, r, res):
        vertices = []
        controls = []

        for i in range(n):
            v = Vec3D(r * cos(i / float(n) * TWO_PI) + width / 2,
                r * sin(i / float(n) * TWO_PI) + height / 2, 0)
            vertices.append(v)

        last = Vec3D(width / 2, height / 2, 0)
        for v in vertices:
            ctr1 = v.copy()
            ctr1.jitter(JITTER)
            ray = Ray3D(v, v.sub(ctr1))
            ctr2 = ray.getPointAtDistance(v.distanceTo(ctr1) + random(50) - 25)
            controls.extend([ctr1, ctr2] if ctr1.distanceTo(last)
                < ctr2.distanceTo(last) else [ctr2, ctr1])
            last = controls[-1]

        lengths = []

        for i, v in enumerate(vertices):
            mcurve = []
            for j in range(res):
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

        for i, v in enumerate(vertices):
            cur_res = res * lengths[i] / max_length
            for j in range(1, cur_res):
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
        current_point = self.points[int(t * len(self.points))]
        next_point = self.points[(int(t * len(self.points)) + 1) % len(self.points)]
        return next_point.sub(current_point).getNormalized()

    def trace(self, t):
        return self.points[int(t * len(self.points))]


class Fragment(object):
    def __init__(self, x, y, z, ssize, ccolor):
        self.pos = Vec3D(x, y, z)
        self.size = ssize
        self.color = ccolor
        self.rotation = (random(TWO_PI), random(TWO_PI), random(TWO_PI))

    def display(self, t):
        fill(self.color)
        noStroke()
        pushMatrix()
        translate(self.pos.x(), self.pos.y(), self.pos.z())
        rotateX(self.rotation[0])
        rotateY(self.rotation[1])
        rotateZ(self.rotation[2])
        box(self.size)
        popMatrix()


def clear_frags():
    for i in range(0, len(path.points), 10):
        for j in range(len(frags) - 1, 0, -1):
            if path.points[i].distanceTo(frags[j].pos) < 40:
                del frags[j]

def draw_(t):
    background(BG_COLOR)
    strokeWeight(1)

    v1 = path.trace(t)
    d = path.get_direction(t)
    v2 = v1.add(d)

    cam.jump(v1.x(), v1.y(), v1.z())
    cam.aim(v2.x(), v2.y(), v2.z())
    cam.feed()

    for frag in frags:
        frag.display(t)

    # stroke(255, 0, 0)
    # path.display()
    # pushMatrix()
    # translate(v1.x(), v1.y(), v1.z())
    # sphere(5)
    # popMatrix()

    pscale = 1000
    n = 60.0
    this.flush()
    for i in range(n, 0, -1):
        scaled = d.scale(100 + (i + 1) * 5)
        vscaled = v1.add(scaled)
        d1 = Vec3D(d.y(), -d.x(), 0)
        d2 = d.cross(d1)
        pv1 = d1.scale(pscale).add(vscaled)
        pv2 = d2.scale(pscale).add(vscaled)
        pv3 = d1.scale(-pscale).add(vscaled)
        pv4 = d2.scale(-pscale).add(vscaled)
        fill(red(BG_COLOR), green(BG_COLOR), blue(BG_COLOR), 50 * (i / n) ** 8)
        noStroke()
        beginShape()
        vertex(pv1.x(), pv1.y(), pv1.z())
        vertex(pv2.x(), pv2.y(), pv2.z())
        vertex(pv3.x(), pv3.y(), pv3.z())
        vertex(pv4.x(), pv4.y(), pv4.z())
        endShape(CLOSE)
        this.flush()

def keyPressed():
    global path
    global DISPLAY_MODE

    if key == 'n':
        path = Path(N, RAD, RES)
    elif key == '1':
        DISPLAY_MODE = 0
    elif key == '2':
        DISPLAY_MODE = 1

def setup():
    global cam
    global path
    global frags
    global videoExport

    size(W, H, P3D)
    frameRate(FPS)
    videoExport = VideoExport(this, "iced.mp4")

    cam = Camera(this, width / 2, height / 2, 400)
    cam.aim(width / 2, height / 2, 0)
    cam.feed()

    # cam = PeasyCam(this, 500)
    # cam.pan(width / 2, height / 2)

    randomSeed(488378)
    path = Path(N, RAD, RES)

    randomSeed(31518)
    frags = []
    for i in range(5000):
        frags.append(Fragment(random(-width, 2 * width), random(-height, 2 * height),
            random(-1.5 * width, 1.5 * width), random(6, 18), choice(PALETTE)))
    clear_frags()

def draw():
    lights()
    if not RECORD:
        t = (frameCount / float(N_FRAMES)) % 1.0
        draw_(t)
    elif N_SAMPLES <= 1:
        t = (frameCount / float(N_FRAMES)) % 1.0
        draw_(t)
        if frameCount <= N_FRAMES:
            if VIDEO:
                videoExport.saveFrame()
            else:
                saveFrame('gif/####.gif')
        else:
            exit()
    else:
        result = [[0, 0, 0] for i in range(W * H)]
        for sample in range(N_SAMPLES):
            t = (frameCount + 0.15 * sample / float(N_SAMPLES)) / N_FRAMES
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
            if VIDEO:
                videoExport.saveFrame()
            else:
                saveFrame('gif/####.gif')
        else:
            exit()
