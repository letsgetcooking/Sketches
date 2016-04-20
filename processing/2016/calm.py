from toxi.geom import Vec3D


W = H = 500
FPS = 30.0
DURATION = 2
N_FRAMES = DURATION * FPS
N_SAMPLES = 4
BG_COLOR = color(72,45,87)
MAIN_COLOR = color(0)
RECORD = True


COLOR1 = color(234,236,198)
COLOR2 = color(53,31,57)
COLOR3 = color(199,211,182)
COLOR4 = color(165,187,163)
PALETTE = [COLOR1, COLOR2, COLOR3, COLOR4]


CENTRAL, BOTTOM_OPEN, TOP_OPEN, BOTTOM_CLOSE, TOP_CLOSE, NONE = range(6)


class Particle(object):
    def __init__(self, x, y, w, h, col, ptype, direction):
        self.x = x
        self.y = y
        self.z = 0
        self.width, self.height = w, h
        self.color = col
        self.type = ptype
        self.direction = direction

    def display(self, t, is_shadow=False):
        inverse = False

        if self.type == CENTRAL:
            pos = Vec3D(self.x, self.y, self.z)
            a = Vec3D(0, 0, 0).add(pos)
            b = Vec3D(self.width - 5, 0, 0).add(pos)
            c = Vec3D(self.width - 5, (self.height - 5), 0).add(pos)
            d = Vec3D(0, (self.height - 5), 0).add(pos)
            for v in [a, b, c, d]:
                v.addSelf(Vec3D(0, self.direction * self.height * t, 0))
        elif self.type == TOP_OPEN:
            pos = Vec3D(self.x, self.y, self.z)
            a = Vec3D(0, 0, 0).add(pos)
            b = Vec3D(self.width - 5, 0, 0).add(pos)
            c = Vec3D(self.width - 5, self.height - 5, 0).rotateX(-PI * (1 - t)).add(pos)
            d = Vec3D(0, self.height - 5, 0).rotateX(-PI * (1 - t)).add(pos)
            for v in [a, b, c, d]:
                v.addSelf(Vec3D(0, self.direction * self.height * t - 5 * (1 - t), 0))
            if t < 0.46: inverse = True
        elif self.type == BOTTOM_OPEN:
            pos = Vec3D(self.x, self.y + self.height, self.z)
            a = Vec3D(0, 0, 0).add(pos)
            b = Vec3D(self.width - 5, 0, 0).add(pos)
            c = Vec3D(self.width - 5, self.height - 5, 0).rotateX(-PI * t).add(pos)
            d = Vec3D(0, self.height - 5, 0).rotateX(-PI * t).add(pos)
            for v in [a, b, c, d]:
                v.addSelf(Vec3D(0, self.direction * (self.height - 5) * t, 0))
            if t > 0.46: inverse = True
        elif self.type == BOTTOM_CLOSE:
            pos = Vec3D(self.x, self.y + self.height, self.z)
            a = Vec3D(0, 0, 0).add(pos)
            b = Vec3D(self.width - 5, 0, 0).add(pos)
            c = Vec3D(self.width - 5, self.height - 5, 0).rotateX(-PI * (1 - t)).add(pos)
            d = Vec3D(0, self.height - 5, 0).rotateX(-PI * (1 - t)).add(pos)
            for v in [a, b, c, d]:
                v.addSelf(Vec3D(0, self.direction * self.height * t - 5 * (1 - t), 0))
            if t < 0.53: inverse = True
        elif self.type == TOP_CLOSE:
            pos = Vec3D(self.x, self.y, self.z)
            a = Vec3D(0, -self.height + 5, 0).rotateX(PI * (1 - t)).add(pos)
            b = Vec3D(self.width - 5, -self.height + 5, 0).rotateX(PI * (1 - t)).add(pos)
            c = Vec3D(self.width - 5, 0, 0).add(pos)
            d = Vec3D(0, 0, 0).add(pos)
            for v in [a, b, c, d]:
                v.addSelf(Vec3D(0, self.direction * self.height * t - 5 * t, 0))
            if t < 0.54: inverse = True

        if is_shadow:
            color2 = color(25)
            color3 = color(25)
            color4 = color(25)
        else:
            color2 = COLOR2
            color3 = COLOR3
            color4 = COLOR4

        noStroke()
        if not inverse:
            fill(color3)
            beginShape()
            vertex(a.x(), a.y(), a.z())
            vertex(b.x(), b.y(), b.z())
            vertex(c.x(), c.y(), c.z())
            endShape(CLOSE)

            fill(color4)
            beginShape()
            vertex(a.x(), a.y(), a.z())
            vertex(d.x(), d.y(), d.z())
            vertex(c.x(), c.y(), c.z())
            endShape(CLOSE)
        else:
            fill(color3)
            beginShape()
            vertex(b.x(), b.y(), b.z())
            vertex(c.x(), c.y(), c.z())
            vertex(d.x(), d.y(), d.z())
            endShape(CLOSE)

            fill(color4)
            beginShape()
            vertex(a.x(), a.y(), a.z())
            vertex(b.x(), b.y(), b.z())
            vertex(d.x(), d.y(), d.z())
            endShape(CLOSE)

        noFill()
        stroke(color2)
        beginShape()
        vertex(a.x(), a.y(), a.z())
        vertex(b.x(), b.y(), b.z())
        vertex(c.x(), c.y(), c.z())
        vertex(d.x(), d.y(), d.z())
        endShape(CLOSE)


def draw_(t):
    background(COLOR1)

    strokeWeight(2)
    for particle in particles:
        particle.display(t, is_shadow=True)

    filter(BLUR, 4)

    for particle in particles:
        particle.display(t)


def setup():
    global particles

    size(W, H, P3D)
    frameRate(FPS)

    particles = []
    r = 150
    w = h = 10
    gap = 2 * r / float(w)
    for i in range(w):
        for j in range(h):
            x = (i - w / 2 + 0.15) * gap + width / 2
            y = (j - h / 2 + 0.5 * (i % 2) - 0.25) * gap + height / 2
            if j == 0 and i % 2:
                ptype = BOTTOM_CLOSE
            elif j == h-1 and i % 2:
                ptype = TOP_OPEN
            elif j == 0 and not i % 2:
                ptype = BOTTOM_OPEN
            elif j == h-1 and not i % 2:
                ptype = TOP_CLOSE
            else:
                ptype = CENTRAL
            p1 = Particle(x, y, gap, gap, COLOR3, ptype, -(2 * (i % 2) - 1))
            p2 = Particle(x, y, gap, gap, COLOR3, ptype, -(2 * (i % 2) - 1))
            particles.append(p2)

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
