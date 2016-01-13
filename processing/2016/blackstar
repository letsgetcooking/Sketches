from toxi.geom import Vec2D, Vec3D


W = H = 500
FPS = 20.0
DURATION = 5
N_FRAMES = DURATION * FPS
N_SAMPLES = 1
BG_COLOR = color(23, 24, 25)
STAR_COLOR = color(180, 178, 160)
OUTER_COLOR = color(16, 18, 19)
MAIN_COLOR = color(0)
BOARDW, BOARDH = 24, 24
PATH_LENGTH = 120.0
RECORD = False


class Board(object):
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.state = [[0 for _ in range(h)] for _ in range(w)]

    def update(self, particles):
        for particle in particles:
            column_width = width / (self.w + 1)
            column_height = height / (self.h + 1)
            column = int(floor((particle.x - column_width / 2) // column_width))
            if column >= self.h: return
            for i in range(self.h):
                celly = i * column_height
                if celly > particle.y or celly < 0:
                    self.state[column][i] = 0
                else:
                    self.state[column][i] = 1 - min(PATH_LENGTH, particle.y - celly) / PATH_LENGTH


class Particle(object):
    def __init__(self, x, y):
        self.s = y
        self.x = x
        self.y = y

    def display(self):
        fill(0)
        ellipseMode(CENTER)
        ellipse(self.x, self.y, 5, 5)

    def update(self, t):
        h = height + PATH_LENGTH
        self.y = (self.s + t * h) % h


def make_big_star(t):
    star = createGraphics(width, height, P3D)
    star.beginDraw()
    star.background(0, 0)

    lx, ly, lz = 200 * cos(t * TWO_PI) + width / 2, 200 * sin(t * TWO_PI) + height / 2, 36
    star.lights()
    star.pointLight(255, 255, 255, lx, ly, lz)

    star.stroke(14)
    star.strokeWeight(1)
    star.fill(15)
    t = 0
    r = 250
    angle = 0
    x, y, z = width / 2, height / 2, 0
    v = Vec3D(0, 0.5 * r, 0)
    vm = Vec3D(0, 0.20 * r, 0)
    v.rotateZ(TWO_PI / 10)
    vm.rotateZ(TWO_PI / 10)
    n = 5.0

    for i in range(n):
        vr = v.getRotatedZ(i / n * TWO_PI).getRotatedY(angle + t * TWO_PI).add(Vec3D(x, y, z))
        vc1 = Vec3D(0, 0, 0.10 * r).getRotatedY(angle + t * TWO_PI).add(Vec3D(x, y, z))
        vc2 = Vec3D(0, 0, -0.10 * r).getRotatedY(angle + t * TWO_PI).add(Vec3D(x, y, z))

        vrm = vm.getRotatedZ((i + 0.5) / n * TWO_PI).getRotatedY(angle + t * TWO_PI).add(Vec3D(x, y, z))
        vrn = v.getRotatedZ((i + 1) / n * TWO_PI).getRotatedY(angle + t * TWO_PI).add(Vec3D(x, y, z))

        star.beginShape()
        star.vertex(vr.x(), vr.y(), vr.z())
        star.vertex(vrm.x(), vrm.y(), vrm.z())
        star.vertex(vc1.x(), vc1.y(), vc1.z())
        star.endShape(CLOSE)
        star.beginShape()
        star.vertex(vr.x(), vr.y(), vr.z())
        star.vertex(vrm.x(), vrm.y(), vrm.z())
        star.vertex(vc2.x(), vc2.y(), vc2.z())
        star.endShape(CLOSE)

        star.beginShape()
        star.vertex(vrn.x(), vrn.y(), vrn.z())
        star.vertex(vrm.x(), vrm.y(), vrm.z())
        star.vertex(vc1.x(), vc1.y(), vc1.z())
        star.endShape(CLOSE)
        star.beginShape()
        star.vertex(vrn.x(), vrn.y(), vrn.z())
        star.vertex(vrm.x(), vrm.y(), vrm.z())
        star.vertex(vc2.x(), vc2.y(), vc2.z())
        star.endShape(CLOSE)

    star.endDraw()
    return star

def draw_star(x, y, r, verticies, col):
    noStroke()
    fill(col)
    v = Vec2D(0, -0.5 * r)
    vm = Vec2D(0, -0.2 * r)
    beginShape()
    for vert in verticies:
        if vert % 2 == 1:
            vr = v.getRotated((vert - 1) / 10.0 * TWO_PI).add(Vec2D(x, y))
        else:
            vr = vm.getRotated((vert - 1) / 10.0 * TWO_PI).add(Vec2D(x, y))
        vertex(vr.x(), vr.y())
    endShape(CLOSE)

def draw_(t):
    background(BG_COLOR)

    for particle in particles:
        particle.update(t)

    board.update(particles)

    for i in range(BOARDW):
        for j in range(BOARDH):
            col = lerpColor(BG_COLOR, STAR_COLOR, board.state[i][j])
            draw_star(20 + i * 20, 20 + j * 20, 15, stars[int(j + len(stars) * noise(i)) % len(stars)], col)

    draw_star(width / 2, height / 2, 276, (1,2,3,4,5,6,7,8,9,10), OUTER_COLOR)
    frame = big_star[int(frameCount % N_FRAMES)]
    image(frame, 0, 0)

    # #make a star
    # star = make_big_star(t)
    # star.save('star/%s.png' % (nf(frameCount, 4),))

def setup():
    global big_star
    global stars
    global board
    global particles
    global hits

    size(W, H)
    frameRate(FPS)

    big_star = []
    for i in range(N_FRAMES):
        big_star.append(loadImage('star/%s.png' % (nf(i + 1, 4),)))

    stars = [(1,5,8), (1,2,3,4,5,6,7,8,9,10), (3,7,8,9), (3,4,5,9), (1,5,6,7), (1,2,3,4,5,8)]
    board = Board(BOARDW, BOARDH)

    particles = []
    for i in range(40):
        particles.append(Particle(random(width), random(height + PATH_LENGTH)))

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
