# toxiclibs requiered
from toxi.geom import Vec2D
from toxi.geom import Line2D

W = H = 500
FPS = 20.0
DURATION = 4
N_FRAMES = DURATION * FPS
N_SAMPLES = 2
SIZE = 200
DOT_DIST = 1
STEP = 5
LINES_N = 60
RECORD = False


def polar2cart(r, theta):
    return r * cos(theta), r * sin(theta)

def draw_(t):
    colorMode(HSB, 100)
    pushMatrix()
    background(100, 0, 15)
    translate(width / 2, height / 2 + 35)

    # lines
    for c in range(3):
        for i in range(LINES_N):
            stroke(10 * i / float(LINES_N), 100, 100, 30)
            cur_a = (i * STEP / 3 - int(t / 3.0 * len(points)) + c * len(points) / 3) % len(points)
            cur_b = (i * STEP - int(t / 3.0 * len(points)) + LINES_N + c * len(points) / 3) % len(points)
            point_a = points[cur_a]
            point_b = points[cur_b]
            line(point_a.x(), point_a.y(), point_b.x(), point_b.y())

    stroke(0, 0, 80)

    # big triangle
    for edge in big_triangle:
        line(edge.a.x(), edge.a.y(), edge.b.x(), edge.b.y())

    # little triangle
    for edge in little_triangle:
        line(edge.a.x(), edge.a.y(), edge.b.x(), edge.b.y())

    popMatrix()
    colorMode(RGB)

def setup():
    global little_triangle
    global big_triangle
    global points
    size(W, H)
    frameRate(FPS)
    noFill()
    strokeWeight(1)

    # edges

    big_triangle = []
    for i in range(3):
        x1, y1 = polar2cart(SIZE / 2, i / 3.0 * 2 * PI - PI / 6)
        xm, ym = polar2cart(SIZE, (i + 0.5) / 3.0 * 2 * PI - PI / 6)
        x2, y2 = polar2cart(SIZE / 2, (i + 1) / 3.0 * 2 * PI - PI / 6)
        big_triangle.append(Line2D(Vec2D(x1, y1), Vec2D(xm, ym)))
        big_triangle.append(Line2D(Vec2D(xm, ym), Vec2D(x2, y2)))

    little_triangle = []
    for i in range(3):
        x1, y1 = polar2cart(SIZE / 2, i / 3.0 * 2 * PI - 5 * PI / 6)
        x2, y2 = polar2cart(SIZE / 2, (i + 1) / 3.0 * 2 * PI - 5 * PI / 6)
        little_triangle.append(Line2D(Vec2D(x1, y1), Vec2D(x2, y2)))

    # points

    points = []
    for i, edge in enumerate(big_triangle):
        _points = edge.splitIntoSegments(None, DOT_DIST, False)
        for p in _points:
            points.append(p)
        if i % 2 == 1:
            for j, e in enumerate(little_triangle):
                edge = little_triangle[(j + i / 2 + 2) % len(little_triangle)]
                _points = edge.splitIntoSegments(None, DOT_DIST, False)
                for p in _points:
                    points.append(p)

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
