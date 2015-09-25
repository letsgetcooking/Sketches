from toxi.geom import Vec3D, Ray3D


W = H = 500
FPS = 20.0
DURATION = 2
N_FRAMES = DURATION * FPS
N_SAMPLES = 1
BG_COLOR = color(0, 25, 42)
COLOR1 = color(150, 207, 234)
COLOR2 = color(150, 207, 234)
DEPTH = -100
RECORD = False


class Star:
    def __init__(self, x, y, w, thickness, path_length, offset):
        self.width = w
        self.res = w / 2
        self.path_length = path_length
        a = Vec3D(x, y, 0)
        self.start = Ray3D(a, Vec3D(0, 0, -1))
        self.thickness = thickness
        self.offset = offset

    def display(self, t):
        pushMatrix()
        noStroke()

        center = Vec3D(W / 2, H / 2, 0)
        t = (t + self.offset) % 1
        th = self.thickness * (1 - (2 * t - 1) ** 2)

        for i in range(self.res):
            p = self.start.getPointAtDistance(t * self.path_length +
                i / self.res * self.width)
            rad = (constrain(t * self.path_length, 0, self.width / 2) *
                constrain(self.path_length - t * self.path_length, 0,
                self.width / 2) / ((self.width / 2) ** 2) * th *
                exp(-((i / self.res * 16 - 8) ** 2) / 10.0))
            rad = constrain(rad, 0.4, 10000)
            fill(lerpColor(COLOR1, COLOR2, (p.distanceTo(center))))
            ellipse(p.x(), p.y(), rad, rad)

        popMatrix()


class Comet:
    def __init__(self, x, y, d, w, thickness, path_length, offset):
        self.width = w
        self.res = w / 2
        self.path_length = path_length
        a = Vec3D(x, y, 0)
        self.start = Ray3D(a, d)
        self.thickness = thickness
        self.offset = offset

    def display(self, t):
        pushMatrix()
        noStroke()

        center = Vec3D(W / 2, H / 2, 0)
        t = (t + self.offset) % 1
        w = self.width * t + 5
        th = self.thickness * (1 - (2 * t - 1) ** 2)

        for i in range(self.res):
            p = self.start.getPointAtDistance(t * self.path_length +
                i / self.res * w)
            rad = (constrain(t * self.path_length, 0, w / 2) *
                constrain(self.path_length - t * self.path_length, 0,
                w / 2) / ((w / 2) ** 2) * th *
                i / self.res)
            rad = constrain(rad, 0.4, 10000)
            fill(lerpColor(COLOR1, COLOR2, (p.distanceTo(center))))
            ellipse(p.x(), p.y(), rad, rad)

        popMatrix()


def draw_(t):
    background(BG_COLOR)

    for star in stars:
        star.display(t)

    for comet in comets:
        comet.display(t)
    
def setup():
    global stars
    global comets

    size(W, H, P3D)
    frameRate(FPS)

    stars = []
    comets = []

    for _ in range(800):
        stars.append(Star(random(10, width - 10), random(10, height - 10),
            random(100, 300), random(1, 3), random(300, 600), random(0, 1)))
    for _ in range(25):
        stars.append(Star(random(10, width - 10), random(10, height - 10),
            random(100, 300), random(4, 5), random(300, 600), random(0, 1)))

    comets.append(Comet(0, 130, Vec3D(1, 0.30, 0), 350.0, 4.0, 400.0, 0.2))

def draw():
    if not RECORD:
        t = (frameCount / float(N_FRAMES)) % 1.0
        draw_(t)
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
