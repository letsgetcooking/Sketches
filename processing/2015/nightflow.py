from toxi.geom import Vec3D, Ray3D
from damkjer.ocd import Camera

W = H = 500
FPS = 20.0
DURATION = 0.9
N_FRAMES = DURATION * FPS
N_SAMPLES = 1
BG_COLOR = color(28, 11, 43)
TEXT_COLOR = color(92, 101, 192)
RECORD = False


def draw_(t):
    background(BG_COLOR)

    fill(TEXT_COLOR)
    for p, ps, pl in zip(particles, psizes, plabels):
        textSize(ps)
        text(pl, p.x() + width * t, p.y(), p.z())

    if t < 0.5:
        tt = 2 * t
        cam.roll(-(cos(2 * PI * tt - PI) + 1) * (HALF_PI) / 10 / N_FRAMES)
    else:
        tt = 2 * (t - 0.5)
        cam.roll((cos(2 * PI * tt - PI) + 1) * (HALF_PI) / 10 / N_FRAMES)

    cam.feed()

def setup():
    global particles
    global cam
    global psizes
    global plabels

    size(W, H, P3D)
    frameRate(FPS)

    cam = Camera(this, width / 2, height / 2, 300)
    cam.jump(width / 2, height / 2, 0)
    cam.aim(width / 2 - 10, height / 2, 0)
    cam.roll(HALF_PI / 34)
    cam.feed()

    particles = []
    psizes = []
    plabels = []

    for i in range(2000):
        x1 = random(width)
        y1 = random(width)
        z1 = random(-350, -20)
        particles.append(Vec3D(x1, y1, z1))
        particles.append(Vec3D(x1 - width, y1, z1))
        particles.append(Vec3D(x1 - 2 * width, y1, z1))
        particles.append(Vec3D(x1 - 3 * width, y1, z1))
        particles.append(Vec3D(x1 - 4 * width, y1, z1))
        particles.append(Vec3D(x1 - 5 * width, y1, z1))
        s1 = int(random(10, 20))
        psizes.append(s1)
        psizes.append(s1)
        psizes.append(s1)
        psizes.append(s1)
        psizes.append(s1)
        psizes.append(s1)
        label1 = str(int(random(0, 7))) + ':' + nf(int(random(0, 60)), 2)
        plabels.append(label1)
        plabels.append(label1)
        plabels.append(label1)
        plabels.append(label1)
        plabels.append(label1)
        plabels.append(label1)

        x2 = random(width)
        y2 = random(width)
        z2 = random(20, 350)
        particles.append(Vec3D(x2, y2, z2))
        particles.append(Vec3D(x2 - width, y2, z2))
        particles.append(Vec3D(x2 - 2 * width, y2, z2))
        particles.append(Vec3D(x2 - 3 * width, y2, z2))
        particles.append(Vec3D(x2 - 4 * width, y2, z2))
        particles.append(Vec3D(x2 - 5 * width, y2, z2))
        s2 = int(random(10, 20))
        psizes.append(s2)
        psizes.append(s2)
        psizes.append(s2)
        psizes.append(s2)
        psizes.append(s2)
        psizes.append(s2)
        label2 = str(int(random(0, 7))) + ':' + nf(int(random(0, 60)), 2)
        plabels.append(label2)
        plabels.append(label2)
        plabels.append(label2)
        plabels.append(label2)
        plabels.append(label2)
        plabels.append(label2)

def draw():
    if not RECORD:
        t = (frameCount / float(N_FRAMES)) % 1.0
        draw_(t)
    elif N_SAMPLES <= 1:
        t = (frameCount / float(N_FRAMES)) % 1.0
        draw_(t)
        if frameCount <= N_FRAMES:
            saveFrame('gif/####.png')
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
