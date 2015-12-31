from toxi.geom import Sphere, Vec3D
from peasy import PeasyCam
from damkjer.ocd import Camera
from random import choice


W = H = 500
FPS = 20.0
DURATION = 4
N_FRAMES = DURATION * FPS
N_SAMPLES = 4
BG_COLOR = color(10)
MAIN_COLOR = color(30)
PALETTE = [color(229, 202, 85), color(61, 89, 38), color(30, 46, 17), color(207, 22, 20), color(163, 18, 13)]
RECORD = False

MIN_DIST, MAX_DIST = 80, 120
MIN_DEV, MAX_DEV = 50, 100
MIN_ANGLE, MAX_ANGLE = -9, 9
MIN_OBST, MAX_OBST = 10, 30
NSEG = 3
DEBUG = False


class Path(object):
    def __init__(self, p1, p2):
        self.points = [p1, ]
        self.lengths = []
        self.n_seg = NSEG
        self.res = 100

        control1 = p2.sub(p1).getNormalized().rotateX(random(
            PI / float(MIN_ANGLE), PI / float(MAX_ANGLE)))
        control2 = control1.copy()
        control2.invert()
        control1.scaleSelf(random(MIN_DIST, MAX_DIST))
        control2.scaleSelf(random(MIN_DIST, MAX_DIST))
        self.points.append(control1.add(p1))
        for i in range(self.n_seg - 1):
            rvec = p2.sub(p1).scale((i + 1) / float(self.n_seg))
            perp = rvec.cross(Vec3D(0, 1, 0)).getRotatedAroundAxis(p2.sub(p1).getNormalized(), random(TWO_PI)). \
                getNormalized().scale(random(MIN_DEV, MAX_DEV))

            paral1 = rvec.getNormalized().rotateX(random(
                PI / float(MIN_ANGLE), PI / float(MAX_ANGLE)))
            paral2 = paral1.copy().invert().scale(random(MIN_DIST, MAX_DIST))
            paral1.scaleSelf(random(MIN_DIST, MAX_DIST))

            rvec.addSelf(p1.add(perp))
            paral1.addSelf(rvec)
            paral2.addSelf(rvec)
            self.points.append(paral2)
            self.points.append(rvec)
            self.points.append(paral1)
        self.points.append(control2.add(p2))
        self.points.append(p2)

        self.compute_lengths()

    def compute_lengths(self):
        del self.lengths[:]
        a1 = self.points[0]
        prev_point = a1
        for i in range(1, len(self.points) - 2, 3):
            c1, c2, a2 = self.points[i], self.points[i+1], self.points[i+2]
            curve_len = 0.0
            for j in range(self.res):
                t = (j + 1) / float(self.res)
                x = bezierPoint(a1.x(), c1.x(), c2.x(), a2.x(), t)
                y = bezierPoint(a1.y(), c1.y(), c2.y(), a2.y(), t)
                z = bezierPoint(a1.z(), c1.z(), c2.z(), a2.z(), t)
                next_point = Vec3D(x, y, z)
                curve_len += prev_point.distanceTo(next_point)
                prev_point = next_point
            self.lengths.append(curve_len)
            a1 = a2

    def display(self):
        beginShape()
        a1 = self.points[0]
        vertex(a1.x(), a1.y(), a1.z())
        for i in range(1, len(self.points) - 2, 3):
            c1, c2, a2 = self.points[i], self.points[i+1], self.points[i+2]
            bezierVertex(c1.x(), c1.y(), c1.z(), c2.x(), c2.y(), c2.z(), a2.x(), a2.y(), a2.z())
        endShape()
        for i in range(1, len(self.points) - 2, 3):
            a2 = self.points[i+2]
            pushMatrix()
            translate(a2.x(), a2.y(), a2.z())
            box(4)
            popMatrix()

    def trace(self, t):
        length = t * sum(self.lengths)
        current_len = 0
        current_seg = 0
        current_t = 0
        for i, l in enumerate(self.lengths):
            if current_len + l > length:
                current_seg = i
                current_t = (length - current_len) / float(self.lengths[i])
                break   
            current_len += l
        a1 = self.points[3 * current_seg]
        c1 = self.points[3 * current_seg + 1]
        c2 = self.points[3 * current_seg + 2]
        a2 = self.points[3 * current_seg + 3]
        x = bezierPoint(a1.x(), c1.x(), c2.x(), a2.x(), current_t)
        y = bezierPoint(a1.y(), c1.y(), c2.y(), a2.y(), current_t)
        z = bezierPoint(a1.z(), c1.z(), c2.z(), a2.z(), current_t)
        return Vec3D(x, y, z)


class Obstacle(Sphere):
    def __init__(self, pos, r, col, angle):
        super(Obstacle, self).__init__(pos, r)
        self.color = col
        self.angle = angle

    def display(self, t):
        stroke(self.color)
        strokeWeight(3)
        fill(167, 197, 189)
        v = Vec3D(0, 0.5 * self.radius, 0)
        vm = Vec3D(0, 0.25 * self.radius, 0)
        for i in range(6):
            vr = v.getRotatedZ(i / 6.0 * TWO_PI).getRotatedY(self.angle + t * TWO_PI).add(Vec3D(self.x(), self.y(), self.z()))
            vc1 = Vec3D(0, 0, 0.15 * self.radius).getRotatedY(self.angle + t * TWO_PI).add(Vec3D(self.x(), self.y(), self.z()))
            vc2 = Vec3D(0, 0, -0.15 * self.radius).getRotatedY(self.angle + t * TWO_PI).add(Vec3D(self.x(), self.y(), self.z()))

            vrm = vm.getRotatedZ((i + 0.5) / 6.0 * TWO_PI).getRotatedY(self.angle + t * TWO_PI).add(Vec3D(self.x(), self.y(), self.z()))
            vrn = v.getRotatedZ((i + 1) / 6.0 * TWO_PI).getRotatedY(self.angle + t * TWO_PI).add(Vec3D(self.x(), self.y(), self.z()))

            beginShape()
            vertex(vr.x(), vr.y(), vr.z())
            vertex(vrm.x(), vrm.y(), vrm.z())
            vertex(vc1.x(), vc1.y(), vc1.z())
            endShape(CLOSE)
            beginShape()
            vertex(vr.x(), vr.y(), vr.z())
            vertex(vrm.x(), vrm.y(), vrm.z())
            vertex(vc2.x(), vc2.y(), vc2.z())
            endShape(CLOSE)

            beginShape()
            vertex(vrn.x(), vrn.y(), vrn.z())
            vertex(vrm.x(), vrm.y(), vrm.z())
            vertex(vc1.x(), vc1.y(), vc1.z())
            endShape(CLOSE)
            beginShape()
            vertex(vrn.x(), vrn.y(), vrn.z())
            vertex(vrm.x(), vrm.y(), vrm.z())
            vertex(vc2.x(), vc2.y(), vc2.z())
            endShape(CLOSE)

    def is_intersects_path(self, path):
        intersects = False
        for i in range(path.n_seg):
            a = path.points[3*i]
            b = path.points[3*i+1]
            c = path.points[3*i+2]
            d = path.points[3*i+3]
            res = 50
            for j in range(res):
                bpx = bezierPoint(a.x(), b.x(), c.x(), d.x(), j / float(res))
                bpy = bezierPoint(a.y(), b.y(), c.y(), d.y(), j / float(res))
                bpz = bezierPoint(a.z(), b.z(), c.z(), d.z(), j / float(res))
                if self.containsPoint(Vec3D(bpx, bpy, bpz)):
                    intersects = True
                    break
            if intersects: break
        return intersects


def make_new_path(p1, p2):
    global path

    for _ in range(500):
        path = Path(p1, p2)
        for obstacle in obstacles:
            if obstacle.is_intersects_path(path):
                break
        else:
            break

def display_fog(t):
    d = 10
    n = 50
    s = 500
    for i in range(n, 0, -1):
        noStroke()
        fill(200, 220, 220, 60 * (i / float(n)) ** 3)
        p = path.trace(t)
        beginShape()
        vertex(p.x() - s, p.y() - s, p.z() - i * d)
        vertex(p.x() + s, p.y() - s, p.z() - i * d)
        vertex(p.x() + s, p.y() + s, p.z() - i * d)
        vertex(p.x() - s, p.y() + s, p.z() - i * d)
        endShape(CLOSE)
        this.flush()

def draw_(t):
    background(BG_COLOR)
    noStroke()
    fill(MAIN_COLOR)
    lights()

    if not DEBUG:
        p_view = path.trace(t)
        cam.jump(p_view.x(), p_view.y(), p_view.z())
        cam.aim(p_view.x(), p_view.y(), p_view.z() - 100)
        cam.feed()

    for obstacle in outer_obstacles:
        obstacle.display(t)
        this.flush()

    for obstacle in obstacles:
        obstacle.display(t)
        this.flush()

    display_fog(t)

    if DEBUG:
        noFill()
        stroke(255)
        path.display()

        stroke(255, 0, 0)
        p = path.trace(t)
        pushMatrix()
        translate(p.x(), p.y(), p.z())
        box(8)
        popMatrix()

def setup():
    global obstacles
    global outer_obstacles
    global cam
    global tree_img

    size(W, H, P3D)
    frameRate(FPS)

    if not DEBUG:
        cam = Camera(this, width / 2, height / 2, 400)
    else:
        cam = PeasyCam(this, 500)
        cam.pan(width / 2, height / 2)

    obstacles1 = []
    obstacles2 = []
    obstacles3 = []
    for i in range(50):
        for j in range(4):
            rw = random(-width + j * width, j * width)
            rh = random(20)
            h = random(0, height)
            col = choice(PALETTE)
            rangle = random(TWO_PI)
            obstacles1.append(Obstacle(Vec3D(rw, h, -height + i * 10 + rh), 40, col, rangle))
            obstacles2.append(Obstacle(Vec3D(rw, h, -height + i * 10 + rh - height), 40, col, rangle))
            obstacles3.append(Obstacle(Vec3D(rw, h, -height + i * 10 + rh - 2 * height), 40, col, rangle))
    obstacles = obstacles1
    outer_obstacles = obstacles2 + obstacles3

    make_new_path(Vec3D(width / 2, height / 2, 0), Vec3D(width / 2, height / 2, -height))

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
