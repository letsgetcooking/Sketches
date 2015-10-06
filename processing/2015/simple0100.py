W = H = 500
FPS = 20.0
DURATION = 3
N_FRAMES = DURATION * FPS
N_SAMPLES = 4
BG_COLOR = color(50, 47, 56)
MAIN_COLOR = color(0, 180, 255)
BG_FRAME_COLOR = color(5, 5, 15)
FRAME_COLOR = color(55, 55, 80)
RECORD = False


def draw_cube(x, y, a, r, t):
    if 0 <= t < 0.5:
        tt = 2 * t
    else:
        tt = 1.0

    beginShape()
    for i in range(4):
        p1 = PVector(-a / 2, a / 2)
        p2 = PVector(-a / 2 + r, a / 2 + r - r * (cos(tt * PI) + 1))
        p3 = PVector(a / 2 - r, a / 2 + r - r * (cos(tt * PI) + 1))
        p4 = PVector(a / 2, a / 2)

        p1.rotate(-i * HALF_PI)
        p2.rotate(-i * HALF_PI)
        p3.rotate(-i * HALF_PI)
        p4.rotate(-i * HALF_PI)

        pos = PVector(x, y)
        center = PVector(width / 2, height / 2)
        if 0.5 <= t < 1.0:
            ttt = 1 - (cos(2 * (t - 0.5) * PI) + 1) / 2.0
            p1.rotate(ttt * HALF_PI)
            p2.rotate(ttt * HALF_PI)
            p3.rotate(ttt * HALF_PI)
            p4.rotate(ttt * HALF_PI)

        p1.add(pos)
        p2.add(pos)
        p3.add(pos)
        p4.add(pos)

        if i == 0:
            vertex(p1.x, p1.y)
            bezierVertex(p2.x, p2.y, p3.x, p3.y, p4.x, p4.y)
        else:
            bezierVertex(p2.x, p2.y, p3.x, p3.y, p4.x, p4.y)
    endShape()

def draw_frame():
    a = 50
    w = 5

    fill(BG_FRAME_COLOR)
    noStroke()
    beginShape()
    vertex(0, 0)
    vertex(width, 0)
    vertex(width, height)
    vertex(0, height)
    beginContour()
    vertex(a, a)
    vertex(a, height - a)
    vertex(width - a, height - a)
    vertex(width - a, a)
    endContour()
    endShape(CLOSE)

    fill(FRAME_COLOR)
    stroke(0)
    strokeWeight(2)
    beginShape()
    vertex(a - w, a - w)
    vertex(width - a + w, a - w)
    vertex(width - a + w, height - a + w)
    vertex(a - w, height - a + w)
    beginContour()
    vertex(a, a)
    vertex(a, height - a)
    vertex(width - a, height - a)
    vertex(width - a, a)
    endContour()
    endShape(CLOSE)

def draw_(t):
    a = 40
    r = 4

    if 0.0 <= t < 0.5:
        background(BG_COLOR)
        fill(MAIN_COLOR)
        offset = 0
    else:
        background(MAIN_COLOR)
        fill(BG_COLOR)
        offset = a
    noStroke()

    tt = (2 * t) % 1

    for i in range(10):
        for j in range(18):
            x, y = 2 * i * a + (j % 2) * a - a / 2 - offset + 10, j * a - a / 2 + 10
            draw_cube(x, y, a, r, tt)

    draw_frame()

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
