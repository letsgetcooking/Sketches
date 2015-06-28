from toxi.geom import Vec3D
from random import choice


W = H = 500
FPS = 20.0
DURATION = 3
N_FRAMES = DURATION * FPS
N_SAMPLES = 1
DIM = 150
NS = 0.01
RECORD = False


class Particle:
    """
    Particle(rad) - random particle with distance from (0, 0) equal rad
    Particle(x, y, z) - particle in (x, y, z)
    """
    def __init__(self, *args):
        if len(args) == 1:
            self.pos = Vec3D.randomVector().scaleSelf(args[0])
        elif len(args) == 3:
            self.pos = Vec3D(args[0], args[1], args[2])

    @property
    def x(self):
        return self.pos.x()

    @property
    def y(self):
        return self.pos.y()

    @property
    def z(self):
        return self.pos.z()

def draw_(t):
    background(0)
    for i, center in enumerate([(W / 3 - 10, H / 3, 395), (2 * W / 3 + 10, 2 * H / 3, 395)]):
        pushMatrix()
        translate(center[0], center[1], center[2])
        rotateY((-1 + 2 * (1 - i)) * (sin(2 * PI * t - PI / 2) + 1) * 0.5 * PI / 2 + PI / 2 * i)
        strokeWeight(2)
        for particle in particles:
            stroke(particle.color)
            point(particle.x, particle.y, particle.z)
        popMatrix()

def setup():
    global particles
    size(W, H, OPENGL)
    frameRate(FPS)
    ortho()

    sad_img = loadImage('sadc.png')
    happy_img = loadImage('happyc.png')
    sad_img.loadPixels()
    happy_img.loadPixels()

    particles = []
    for i in range(1000000):
        x, y, z = int(random(sad_img.width)), int(random(sad_img.height)), int(random(happy_img.width))
        if (random(0, 255) < brightness(sad_img.pixels[y * sad_img.width + x]) and
            random(0, 255) < brightness(happy_img.pixels[y * happy_img.width + z])):
            particle = Particle(x - sad_img.width / 2, y - sad_img.height / 2, z - sad_img.width / 2)
            particle.color = color(255, (brightness(sad_img.pixels[y * sad_img.width + x]) +
                brightness(happy_img.pixels[y * happy_img.width + z])) / 3.0)
            particles.append(particle)

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
