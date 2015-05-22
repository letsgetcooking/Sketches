# toxiclibs requiered
from toxi.geom import Vec2D
from toxi.geom import Line2D

W = H = 500
FPS = 20.0
DURATION = 5
N_FRAMES = DURATION * FPS
N_SAMPLES = 2
SIZE = 200
DOT_DIST = 1
STEP = 20
LINES_N = 24
RECORD = False


def polar2cart(r, theta):
    return r * cos(theta), r * sin(theta)

def draw_(t):
    colorMode(HSB, 100)
    pushMatrix()
    background(0, 0, 15)
    translate(width / 2, height / 2 + 35)

    stroke(0, 0, 70)
    fill(0, 0, 15)
    rect_w = 550
    rect_h = 3
    rect_y = -width / 6
    rectMode(CENTER)
    rect(0, rect_y, rect_w, rect_h)

    fill(0, 0, 15, 70)
    noStroke()
    beginShape()
    for edge in big_triangle:
        vertex(edge.a.x(), edge.a.y())
        vertex(edge.b.x(), edge.b.y())
    endShape(CLOSE)
    noFill()

    # lines
    particles = [[], [], []]
    for c in range(3):
        for i in range(LINES_N):
            cur_a = (i * STEP / 2 - int(t / 3.0 * len(points)) + c * len(points) / 3) % len(points)
            cur_b = (i * STEP - int(t / 3.0 * len(points)) + LINES_N / 2 + c * len(points) / 3) % len(points)
            point_a = points[cur_a]
            point_b = points[cur_b]
            cur_line = Line2D(point_a, point_b)
            linepoins = cur_line.splitIntoSegments(None, STEP, False)
            for _point in linepoins:
                particles[c].append(_point)

    dist_min = 6
    dist_max = 20

    for _points in particles:
        for i1, _point1 in enumerate(_points):
            for i2, _point2 in enumerate(_points):
                if dist_min < _point1.distanceTo(_point2) < dist_max:
                    stroke(0, 0, 40, 40)
                    prev_point = _points[constrain(i1 - 40, 0, len(_points) - 1)]
                    next_point = _points[constrain(i2 + 40, 0, len(_points) - 1)]
                    curve(prev_point.x(), prev_point.y(), _point1.x(), _point1.y(),
                        _point2.x(), _point2.y(), next_point.x(), next_point.y())

    dist_min = 1
    dist_max = 20

    for pi, particle1 in enumerate(particles[0]):
        stroke(50 + 8 * pi / float(len(particles[0])), 40, 100, 50)
        for particle2 in particles[1]:
            if dist_min < particle1.distanceTo(particle2) < dist_max:
                line(particle1.x(), particle1.y(), particle2.x(), particle2.y())

    for pi, particle1 in enumerate(particles[1]):
        stroke(50 + 8 * pi / float(len(particles[0])), 40, 100, 50)
        for particle2 in particles[2]:
            if dist_min < particle1.distanceTo(particle2) < dist_max:
                line(particle1.x(), particle1.y(), particle2.x(), particle2.y())

    for pi, particle1 in enumerate(particles[2]):
        stroke(50 + 8 * pi / float(len(particles[0])), 40, 100, 50)
        for particle2 in particles[0]:
            if dist_min < particle1.distanceTo(particle2) < dist_max:
                line(particle1.x(), particle1.y(), particle2.x(), particle2.y())

    stroke(0, 0, 80)

    # big triangle
    for edge in big_triangle:
        line(edge.a.x(), edge.a.y(), edge.b.x(), edge.b.y())

    # little triangle
    for ei, edge in enumerate(little_triangle):
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
