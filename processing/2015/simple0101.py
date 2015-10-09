from toxi.geom import Line2D, Ray2D, Vec2D


W = H = 500
FPS = 30.0
DURATION = 8
N_FRAMES = DURATION * FPS
N_SAMPLES = 8
K = 0.2
BG_COLOR = color(230)
MAIN_COLOR = color(25)
BG_FRAME_COLOR = color(0)
FRAME_COLOR = color(255)
RECORD = False


def draw_triangle(length, start, pg):
    pg.noFill()
    pg.stroke(MAIN_COLOR)
    pg.strokeWeight(8)
    pg.strokeCap(PROJECT)
    pg.pushMatrix()
    pg.translate(0, 40)

    t = 0.5
    r = 200
    n = 3.0
    dist = 18
    len_sum = 0

    rays = []
    for i in range(n):
        x, y = r * cos(TWO_PI * i / n - HALF_PI) + width / 2, r * sin(TWO_PI * i / n - HALF_PI) + height / 2
        direction = Vec2D(1, 0)
        direction.rotate(PI / 3 + i * TWO_PI / n)
        ray = Ray2D(x, y, direction)
        rays.append(ray)

    points = [None for _ in range(n)]

    lines = [[], [], []]

    first = 500
    for i, ray in enumerate(rays):
        dist1 = max(dist, first - start)
        dist2 = dist + first - min(length, first)
        p1 = ray.getPointAtDistance(dist1)
        p2 = ray.getPointAtDistance(dist2)
        if abs(dist1 - dist2) > 1:
            lines[i].append((p1.x(), p1.y(), p2.x(), p2.y()))
        points[i] = ray.getPointAtDistance(dist)

    len_sum += min(length, first)

    k = 6
    for i in range(k):
        tmp_points = [None for _ in range(n)]
        for j in range(n):
            p1 = points[j]
            d1 = Vec2D(1, 0)
            d1.rotate(TWO_PI / 3.0 + j * TWO_PI / 3.0 - i * TWO_PI / 3.0)
            ray1 = Ray2D(p1.x(), p1.y(), d1)

            p2 = points[(j + 1) % len(points)]
            d2 = Vec2D(1, 0)
            d2.rotate(TWO_PI / 3.0 + (j + 1) * TWO_PI / 3.0 - i * TWO_PI / 3.0)
            ray2 = Ray2D(p2.x(), p2.y(), d2)

            p_at_dist = ray2.getPointAtDistance(dist)
            dtp = ray1.getDistanceToPoint(p_at_dist)
            dist1 = max(min(start - len_sum, dtp * 1.165), 0)
            dist2 = min(length - len_sum, dtp * 1.165)
            p1 = ray1.getPointAtDistance(dist1)
            p2 = ray1.getPointAtDistance(dist2)
            if p1.distanceToSquared(p2) > 1:
                lines[j].append((p1.x(), p1.y(), p2.x(), p2.y()))
            tmp_points[j] = ray1.getPointAtDistance(dtp * 1.165)
        len_sum += dist2
        points = tmp_points

    end_lines = [[], [], []]
    _length = 0
    for i in range(n):
        p1 = points[i]
        d1 = Vec2D(1, 0)
        d1.rotate(TWO_PI / 3.0 + i * TWO_PI / 3.0 - (k - 1) * TWO_PI / 3.0)
        ray1 = Ray2D(p1.x(), p1.y(), d1)
        p2 = ray1.getPointAtDistance(length - len_sum)
        if ray1.distanceToSquared(p2) > 1:
            _line = Line2D(ray1.x(), ray1.y(), p2.x(), p2.y())
            _length = _line.getLength()
            if _length > 10:
                ray = _line.toRay2D()
                p1 = ray.getPointAtDistance(15 + max(start - len_sum, 0))
                p2 = ray.getPointAtDistance(_length)
                end_lines[i].append((p1.x(), p1.y(), p2.x(), p2.y()))

                p1 = ray.getPointAtDistance(0 + max(start - len_sum, 0))
                p2 = ray.getPointAtDistance(_length)
                end_lines[i].append((p1.x(), p1.y(), p2.x(), p2.y()))
    len_sum += _length

    for i in range(n):
        pg.beginShape()
        for j, _line in enumerate(lines[i]):
            if j == 0:
                pg.vertex(_line[0], _line[1])
                pg.vertex(_line[2], _line[3])
            else:
                pg.vertex(_line[2], _line[3])
        pg.endShape()

    for i in range(n):
        pg.stroke(BG_COLOR)
        pg.strokeWeight(12)
        for end_line in end_lines[i]:
            pg.line(end_line[0], end_line[1], end_line[2], end_line[3])
            pg.stroke(MAIN_COLOR)
            pg.strokeWeight(8)

    pg.popMatrix()

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
    background(BG_COLOR)
    tt = t * 3000
    draw_triangle(tt, constrain(tt - 1000, 0, 10000), this)
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
            t = (frameCount + K * sample / float(N_SAMPLES)) / N_FRAMES
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
