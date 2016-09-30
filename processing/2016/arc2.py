from toxi.geom import Vec2D, Ray2D, Line2D


W = H = 500
FPS = 20.0
DURATION = 4
N_FRAMES = DURATION * FPS
N_SAMPLES = 8
BG_COLOR = color(255)
MAIN_COLOR = color(35)
SECOND_COLOR = color(210)
STROKE_COLOR = color(0)
RECORD = True


def draw_(t):
    background(BG_COLOR)

    offset = 100
    axis = Line2D(Vec2D(width, offset - 400 - height), Vec2D(width, height + offset))
    n = 200.0
    angle = PI / 4
    left_wave = []

    noFill()
    stroke(STROKE_COLOR)
    strokeWeight(4.9)

    for i in range(int(n)):
        tt = (2 * t) % 1
        dist_left = (n - i - 1) * 20 * (abs(tt - 0.5) * 2 + 1.2) + (1 - i / n) * 58 * (sin(t * TWO_PI + i / 4.0) + 1) / 2

        start = axis.toRay2D().getPointAtDistance(i / n * axis.getLength())
        direction_left = Vec2D(0, 1).rotate(angle)
        left = Ray2D(start, direction_left)
        v1 = left.getPointAtDistance(dist_left)
        v2 = start

        beginShape()
        vertex(v1.x(), v1.y())
        vertex(v2.x(), v2.y())
        endShape()

        left_wave.append(v1)

    fill(MAIN_COLOR)
    strokeWeight(3)
    stroke(MAIN_COLOR)

    beginShape()
    for v in left_wave:
        vertex(v.x(), v.y())
    vertex(width, height)
    vertex(0, height)
    endShape(CLOSE)

    noFill()
    strokeWeight(8)
    stroke(STROKE_COLOR)

    beginShape()
    for v in left_wave:
        vertex(v.x(), v.y())
    endShape()

    pushMatrix()
    translate(random(1), random(1))

    fill(15)
    noStroke()
    n = 10.0
    ellipse(width / 2, height / 2, 320, 320)
    for i in range(1, int(n)):
        r = 160 * i / n
        noFill()
        stroke(35)
        strokeWeight(1)
        ellipse(width / 2, height / 2, 2 * r, 2 * r)

    strokeWeight(8)
    stroke(SECOND_COLOR)
    fill(SECOND_COLOR)
    rectMode(CENTER)
    for i in range(1, int(n)):
        r = 160 * i / n
        # strokeWeight(1 + 9 * (sin((1 - t) * TWO_PI + i / 2.0) + 1) / 2 * (sin((1 - t) * 2 * TWO_PI + i / 2.0) + 1))
        arc_length = PI / 4.0 + i * PI / 52.0
        m = 120.0 + 480 * i / n
        for j in range(3):
            a = j * TWO_PI / 3.0 + TWO_PI * t * ((n - i) + 1) / 3.0
            for j in range(int(m)):
                angle = arc_length * j / m + a
                x, y = r * cos(angle) + width / 2, r * sin(angle) + height / 2
                ellipse(x, y, 3, 3)
                if j == 0 or j == m - 1:
                    pushMatrix()
                    translate(x, y)
                    rotate(angle)
                    rect(0, 0, 3, 3)
                    popMatrix()

    noFill()
    stroke(SECOND_COLOR)
    strokeWeight(10)
    ellipse(width / 2, height / 2, 318, 318)

    popMatrix()

def setup():
    size(W, H)
    frameRate(FPS)

    strokeJoin(MITER)
    strokeCap(PROJECT)

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
            t = (frameCount + 0.25 * sample / float(N_SAMPLES)) / N_FRAMES
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
