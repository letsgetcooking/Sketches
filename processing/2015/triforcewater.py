# toxiclibs requiered
from toxi.geom import Vec2D
from toxi.geom import Line2D

W = H = 500
FPS = 20.0
DURATION = 3
N_FRAMES = DURATION * FPS
N_SAMPLES = 4
SIZE = 200
DOT_DIST = 1
STEP = 4
LINES_N = 70
RECORD = False


def polar2cart(r, theta):
    return r * cos(theta), r * sin(theta)

def draw_(t):
    colorMode(HSB, 100)
    background(100, 0, 15)

    pushMatrix()
    translate(width / 2, height / 2 - 35)

    # lines
    strokeWeight(5)
    for c in range(3):
        for i in range(LINES_N, 0, -1):
            stroke(50 + 10 * i / float(LINES_N), 100, 100, 100)
            strokeCap(SQUARE)
            cur_a = (i * STEP / 2 - int(t / 3.0 * len(points)) + c * len(points) / 3) % len(points)
            cur_b = (i * STEP - int(t / 3.0 * len(points)) + LINES_N + c * len(points) / 3) % len(points)
            point_a = points[cur_a]
            point_b = points[cur_b]
            line(point_a.x(), point_a.y(), point_b.x(), point_b.y())

    popMatrix()

    colorMode(RGB)

    pg = createGraphics(W, H)
    pg.beginDraw()
    pg.colorMode(HSB, 100)
    pg.translate(width / 2, height / 2 - 35)
    pg.noFill()
    pg.stroke(0, 0, 80)

    # big triangle
    pg.stroke(57, 100, 100, 100)
    pg.strokeWeight(12)
    pg.beginShape()
    for i in range(3):
        x, y = polar2cart(SIZE, i / 3.0 * 2 * PI + PI / 2)
        pg.vertex(x, y)
    pg.endShape(CLOSE)

    # little triangle
    pg.strokeWeight(9)
    pg.strokeJoin(BEVEL)
    pg.beginShape()
    for i in range(3):
        x, y = polar2cart(SIZE / 2, i / 3.0 * 2 * PI - PI / 2)
        pg.vertex(x, y)
    pg.endShape(CLOSE)
    pg.endDraw()

    tint(255, 255, 255, 70)
    image(pg, 0, 0)

def setup():
    global points
    size(W, H)
    frameRate(FPS)

    # edges

    big_triangle = []
    for i in range(3):
        x1, y1 = polar2cart(SIZE / 2, i / 3.0 * 2 * PI - PI / 2)
        xm, ym = polar2cart(SIZE, (i + 0.5) / 3.0 * 2 * PI - PI / 2)
        x2, y2 = polar2cart(SIZE / 2, (i + 1) / 3.0 * 2 * PI - PI / 2)
        big_triangle.append(Line2D(Vec2D(x1, y1), Vec2D(xm, ym)))
        big_triangle.append(Line2D(Vec2D(xm, ym), Vec2D(x2, y2)))

    little_triangle = []
    for i in range(3):
        x1, y1 = polar2cart(SIZE / 2, i / 3.0 * 2 * PI + PI / 6)
        x2, y2 = polar2cart(SIZE / 2, (i + 1) / 3.0 * 2 * PI + PI / 6)
        little_triangle.append(Line2D(Vec2D(x1, y1), Vec2D(x2, y2)))

    # points

    points = []
    for i, edge in enumerate(big_triangle):
        _points = edge.splitIntoSegments(None, DOT_DIST, False)
        for p in _points:
            points.append(p)
        if i % 2 == 1:
            for j, e in enumerate(little_triangle):
                edge = little_triangle[(j + i / 2) % len(little_triangle)]
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
