from toxi.geom import Line2D, Ray2D, Vec2D


W = H = 500
FPS = 20.0
DURATION = 4
N_FRAMES = DURATION * FPS
N_SAMPLES = 4
RECORD = False


def draw_(t):
    background(0)

    stroke(255)
    strokeWeight(2)
    r = 150
    n = 3.0
    rays = []
    for i in range(n):
        x, y = r * cos(TWO_PI * i / n - HALF_PI) + width / 2, r * sin(TWO_PI * i / n - HALF_PI) + height / 2 + 30
        direction = Vec2D(1, 0)
        direction.rotate(PI / 3 + i * TWO_PI / n)
        ray = Ray2D(x, y, direction)
        rays.append(ray)
    for i, ray in enumerate(rays):
        p1 = ray.getPointAtDistance(constrain(600 / 0.577 * (0.5 - t), 0, 1000))
        p2 = ray.getPointAtDistance(constrain(600 / 0.577 * (0.5 - t) + 300 / 0.577, 150 / 0.577, 1000))
        line(p1.x(), p1.y(), p2.x(), p2.y())

def setup():
    size(W, H)
    frameRate(FPS)

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
