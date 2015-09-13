from toxi.geom import Circle, Vec2D


W = H = 500
FPS = 20.0
DURATION = 2
N_FRAMES = DURATION * FPS
N_SAMPLES = 4
BG_COLOR = color(0)
FIRST_COLOR = color(90)
SECOND_COLOR = color(100)
THIRD_COLOR = color(105)
RECORD = False


def draw_(t):
    background(BG_COLOR)
    strokeWeight(4)
    strokeCap(SQUARE)
    noFill()

    stroke(FIRST_COLOR)
    for circ in icircles:
        ellipse(circ.x(), circ.y(), 2 * circ.getRadius(), 2 * circ.getRadius())

    colors = [SECOND_COLOR, THIRD_COLOR]
    cur_color = 0
    next_color = 1
    top = False

    for oi, ocircle in enumerate(ocircles):
        for layer in ocircle:
            center = Vec2D(layer.x(), layer.y())
            top = not top
            stroke(colors[cur_color])
            ellipse(layer.x(), layer.y(), 2 * layer.getRadius(), 2 * layer.getRadius())
            for icirc in icircles:
                intersection = layer.intersectsCircle(icirc)
                for p in intersection:
                    if top:
                        center = Vec2D(width / 2, height / 2)
                        rad = icirc.getRadius()
                        x, y = icirc.x(), icirc.y()
                        c = FIRST_COLOR
                    else:
                        center = Vec2D(layer.x(), layer.y())
                        rad = layer.getRadius()
                        x, y = layer.x(), layer.y()
                        c = colors[cur_color]

                    angle1 = 0.04
                    angle2 = 0.06

                    sub = p.sub(center)
                    sub.rotate(-angle1)
                    start = atan2(sub.y(), sub.x())
                    sub.rotate(2 * angle1)
                    end = atan2(sub.y(), sub.x())
                    stroke(BG_COLOR)
                    strokeWeight(7)
                    arc(x, y, 2 * rad, 2 * rad, start, end)

                    sub = p.sub(center)
                    sub.rotate(-angle2)
                    start = atan2(sub.y(), sub.x())
                    sub.rotate(2 * angle2)
                    end = atan2(sub.y(), sub.x())
                    stroke(c)
                    strokeWeight(4)
                    arc(x, y, 2 * rad, 2 * rad, start, end)
                top = not top
        cur_color = (cur_color + 1) % 2
        next_color = (cur_color + 1) % 2

    cur_color = 0
    next_color = 1
    top = False

    for oi, ocircle in enumerate(ocircles):
        ncircle = ocircles[(oi + 1) % len(ocircles)]
        top = not top
        for layer in ocircle:
            for nlayer in ncircle:
                intersection = layer.intersectsCircle(nlayer)
                for p in intersection:
                    if top:
                        stroke(colors[next_color])
                        center = Vec2D(layer.x(), layer.y())
                        x, y = layer.x(), layer.y()
                        rad = layer.getRadius()
                        c = colors[cur_color]
                    else:
                        stroke(colors[cur_color])
                        center = Vec2D(nlayer.x(), nlayer.y())
                        x, y = nlayer.x(), nlayer.y()
                        rad = nlayer.getRadius()
                        c = colors[next_color]

                    angle1 = 0.04
                    angle2 = 0.06

                    sub = p.sub(center)
                    sub.rotate(-angle1)
                    start = atan2(sub.y(), sub.x())
                    sub.rotate(2 * angle1)
                    end = atan2(sub.y(), sub.x())
                    stroke(BG_COLOR)
                    strokeWeight(7)
                    arc(x, y, 2 * rad, 2 * rad, start, end)

                    sub = p.sub(center)
                    sub.rotate(-angle2)
                    start = atan2(sub.y(), sub.x())
                    sub.rotate(2 * angle2)
                    end = atan2(sub.y(), sub.x())
                    stroke(c)
                    strokeWeight(4)
                    arc(x, y, 2 * rad, 2 * rad, start, end)
                top = not top
        cur_color = (cur_color + 1) % 2
        next_color = (cur_color + 1) % 2

def setup():
    global ocircles
    global icircles

    size(W, H)
    frameRate(FPS)

    resolution = 200.0
    ncircles = 6.0
    crad = 88.0
    cr = 108
    r = 120

    ocircles = []
    icircles = []

    for i in range(6):
        icircles.append(Circle(width / 2, height / 2, r - i * 11))

    for i in range(ncircles):
        ocircle = []
        x, y = (cr * cos(i / ncircles * TWO_PI + PI / 6 - 0.02) + width / 2,
            cr * sin(i / ncircles * TWO_PI + PI / 6 - 0.02) + height / 2)
        for j in range(3):
            ocircle.append(Circle(x, y, crad - j * 11))
        ocircles.append(ocircle)

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
            t = (frameCount + 0.5 * sample / float(N_SAMPLES)) / N_FRAMES
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

