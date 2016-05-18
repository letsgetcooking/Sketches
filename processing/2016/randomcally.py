from geomerative import RPoint, RPath


W = H = 500
FPS = 20.0
DURATION = 4
N_FRAMES = DURATION * FPS
N_SAMPLES = 4
BG_COLOR = color(255)
MAIN_COLOR = color(0)
SHADOW_COLOR = color(130, 130, 170)
RECORD = False


DARK_BLUE = color(34,40,49)
BLUE = color(45,64,89)
ORANGE = color(255,87,34)
WHITE = color(238,238,238)


def make_path(x1, y1, x2, y2, n, jitter):
    vertices = []
    controls = []

    l = RPath(RPoint(x1, y1))
    l.addLineTo(RPoint(x2, y2))

    for i in range(n):
        v = l.getPoint(i / float(n))
        vertices.append(v)

    last = RPoint(-width / 2, 0)
    for i, v in enumerate(vertices):
        ctr1 = RPoint(v)
        j = RPoint(jitter, 0)
        j.rotate(random(TWO_PI))
        ctr1.add(j)
        ray = RPath(v)
        direction = RPoint(v)
        direction.sub(ctr1)
        direction.normalize()
        direction.scale(v.dist(ctr1) + 25)
        direction.add(v)
        ray.addLineTo(direction)
        ctr2 = ray.getPoint(random(0.75, 1))
        controls.extend([ctr1, ctr2] if ctr1.dist(last)
            < ctr2.dist(last) else [ctr2, ctr1])
        last = controls[-1]

    path = RPath(vertices[0])
    for i, v in enumerate(vertices[1:]):
        path.addBezierTo(controls[2 * i + 1], controls[2 * i + 2], v)

    return path

def draw_(t):
    background(WHITE)
    noStroke()

    t = min(t * 1.5, 1)
    n = 400.0

    for ip, path in enumerate(paths):
        tt = constrain(len(paths) * t - ip, 0, 1)
        fill(ORANGE)
        res = tt * n
        k1 = 120.0
        k2 = 120.0
        for i in range(int(res)):
            # th = 8 * (1 - i / res)
            th = 4 * ((1 - ((constrain(i / k1, 0, 1) - 1) ** 8)) * (1 - (constrain((i - res + k2) / k2, 0, 1) ** 8)))
            p = path.getPoint(i / n)
            ellipse(p.x, p.y, th, th)
    
        fill(BLUE)
        res = tt * n * (0.8 + 0.2 * tt)
        k1 = 120.0
        k2 = 120.0 + 80 * (1 - tt)
        for i in range(int(res)):
            # th = 8 * (1 - i / res)
            th = 6 * ((1 - ((constrain(i / k1, 0, 1) - 1) ** 8)) * (1 - (constrain((i - res + k2) / k2, 0, 1) ** 8)))
            p = path.getPoint(i / n)
            ellipse(p.x, p.y, th, th)

def setup():
    global paths

    size(W, H)
    frameRate(FPS)

    paths = []

    for i in range(4):
        w = (i + 1) * width / 5
        path = make_path(w, 220, w, 270, int(random(3, 7)), int(random(20, 50)))
        paths.append(path)


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
            saveFrame('gif/3###.gif')
        else:
            exit()
