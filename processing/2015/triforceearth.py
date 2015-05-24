# toxiclibs requiered
from toxi.geom import Vec2D
from toxi.geom import Line2D

W = H = 500
FPS = 20.0
DURATION = 4
N_FRAMES = DURATION * FPS
N_SAMPLES = 4
SIZE = 200
DOT_DIST = 1
SEEDS = [random(10000) for i in range(20)]
RECORD = False


def draw_branch(depth, windforce):
    if depth < 10:
        randomSeed(SEEDS[2 * depth])
        line(0, 0, 0, -height / 20.0)
        pushMatrix()
        translate(0, -height / 23.0)
        rotate(random(-PI / 4, PI / 4) + windforce)
        scale(0.8)
        draw_branch(depth + 1, windforce * 1.1)
        popMatrix()

        randomSeed(SEEDS[2 * depth+1])
        pushMatrix()
        translate(0, -height / 20.0)
        rotate(random(-PI / 4, PI / 4) + windforce)
        scale(0.8)
        draw_branch(depth + 1, windforce * 1.1)
        popMatrix()

def polar2cart(r, theta):
    return r * cos(theta), r * sin(theta)

def draw_(t):
    pushMatrix()
    randomSeed(t * 12345)
    colorMode(HSB, 100)
    background(100, 0, 15)

    pushMatrix()
    translate(width / 2, height / 2 - 35)

    strokeWeight(4)
    stroke(8, 46, 30, 50)
    fill(0, 0, 15)
    rect_w = 550
    rect_h = 10
    rect_y = width / 5
    rectMode(CENTER)
    rect(0, rect_y, rect_w, rect_h)

    # lines

    stroke(40, 80, 37, 50)
    noFill()
    for i in range(20):
        strokeWeight(0.7)
        for p1, p2 in zip(points[0], points[1]):
            x1 = min(p1.x()+random(500), p2.x())
            x2 = max(x1, p2.x()-random(500))
            line(x1, p1.y(), x2, p2.y())
        strokeWeight(1)

    popMatrix()

    pg = createGraphics(W, H)
    pg.beginDraw()
    pg.colorMode(HSB, 100)
    pg.translate(width / 2, height / 2 - 35)
    pg.noFill<kt()
    pg.stroke(0, 0, 80)

    pg.stroke(8, 46, 30, 100)

    # big triangle
    pg.strokeWeight(9)
    pg.beginShape()
    for i in range(3):
        x, y = polar2cart(SIZE, i / 3.0 * 2 * PI + PI / 2)
        pg.vertex(x, y)
    pg.endShape(CLOSE)

    # little triangle
    pg.strokeWeight(7)
    pg.fill(0, 0, 15, 80)
    pg.beginShape()
    for i in range(3):
        x, y = polar2cart(SIZE / 2 + 25, i / 3.0 * 2 * PI - PI / 2)
        pg.vertex(x, y)
    pg.endShape(CLOSE)
    pg.endDraw()

    image(pg, 0, 0)

    # tree
    translate(W / 2, H / 2 + 22)
    stroke(8, 71, 69)
    strokeWeight(2)
    draw_branch(0, sin(t * 2 * PI) * PI / 200)

    colorMode(RGB)
    popMatrix()

def setup():
    global points
    size(W, H)
    frameRate(FPS)

    # edges

    big_triangle = []
    for i in range(3):
        x1, y1 = polar2cart(SIZE, i / 3.0 * 2 * PI + PI / 2)
        x2, y2 = polar2cart(SIZE, (i + 1) / 3.0 * 2 * PI + PI / 2)
        big_triangle.append(Line2D(Vec2D(x1, y1), Vec2D(x2, y2)))

    little_triangle = []
    for i in range(3):
        x1, y1 = polar2cart(SIZE / 2, i / 3.0 * 2 * PI + PI / 6)
        x2, y2 = polar2cart(SIZE / 2, (i + 1) / 3.0 * 2 * PI + PI / 6)
        little_triangle.append(Line2D(Vec2D(x1, y1), Vec2D(x2, y2)))

    # points

    points = [[], []]
    for i in range(2):
        _points = big_triangle[2 * i].splitIntoSegments(None, DOT_DIST, False)
        for _point in _points:
            points[i].append(_point)
    points[1].reverse()

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
