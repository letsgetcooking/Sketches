from toxi.geom import Circle, Vec2D


W = H = 500
FPS = 20.0
DURATION = 3
N_FRAMES = DURATION * FPS
N_SAMPLES = 4
BG_COLOR = color(29, 30, 33)
FIRST_COLOR = color(122, 118, 69)
SECOND_COLOR = color(128, 124, 69)
THIRD_COLOR = color(130, 124, 62)
RECORD = True


def draw_(t):
    background(BG_COLOR)
    strokeWeight(4)
    noFill()

    tf = constrain(t * 2.5, 0, 1)
    ts = constrain((t - 0.6) * 2.5, 0, 1)

    stroke(FIRST_COLOR)
    for ii, circ in enumerate(icircles):
        at = TWO_PI * tf + PI / 12 * ii - TWO_PI * ts
        of = TWO_PI * ts + PI / 12 * ii
        n = 1000.0
        for i in range(n):
            x, y = circ.getRadius() * cos(at * i / n + of) + width / 2, circ.getRadius() * sin(at * i / n + of) + height / 2
            point(x, y)

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
            for ii, icirc in enumerate(icircles):
                intersection = layer.intersectsCircle(icirc)
                at = TWO_PI * tf + PI / 12 * ii - TWO_PI * ts
                of = TWO_PI * ts + PI / 12 * ii
                for p in intersection:
                    c = Vec2D(width / 2, height / 2)
                    s = p.sub(c)
                    pangle = atan2(s.y(), s.x())
                    if pangle < 0:
                        pangle += TWO_PI
                    if (of < pangle < at + of) or ((at + of) > TWO_PI and
                        constrain(of - TWO_PI, 0, TWO_PI) < pangle < (at + of) % TWO_PI):
                        if top:
                            center = Vec2D(width / 2, height / 2)
                            rad = icirc.getRadius()
                            x, y = icirc.x(), icirc.y()
                            col = FIRST_COLOR
                        else:
                            center = Vec2D(layer.x(), layer.y())
                            rad = layer.getRadius()
                            x, y = layer.x(), layer.y()
                            col = colors[cur_color]

                        l1 = 2
                        l2 = 6

                        angle1 = l1 / rad
                        angle2 = l2 / rad

                        for c, w, a in [(BG_COLOR, 8, angle1), (col, 4, angle2)]:
                            sub = p.sub(center)
                            sub.rotate(-a)
                            start = atan2(sub.y(), sub.x())
                            if start < 0:
                                start += TWO_PI
                            sub.rotate(2 * a)
                            end = atan2(sub.y(), sub.x())
                            if end < 0:
                                end += TWO_PI
                            stroke(c)
                            strokeWeight(w)
                            if abs(end - start) > PI:
                                start -= TWO_PI
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
                        col = colors[cur_color]
                    else:
                        stroke(colors[cur_color])
                        center = Vec2D(nlayer.x(), nlayer.y())
                        x, y = nlayer.x(), nlayer.y()
                        rad = nlayer.getRadius()
                        col = colors[next_color]

                    l1 = 2
                    l2 = 6

                    angle1 = l1 / rad
                    angle2 = l2 / rad

                    for c, w, a in [(BG_COLOR, 8, angle1), (col, 4, angle2)]:
                        sub = p.sub(center)
                        sub.rotate(-a)
                        start = atan2(sub.y(), sub.x())
                        if start < 0:
                            start += TWO_PI
                        sub.rotate(2 * a)
                        end = atan2(sub.y(), sub.x())
                        if end < 0:
                            end += TWO_PI
                        stroke(c)
                        strokeWeight(w)
                        if abs(end - start) > PI:
                            start -= TWO_PI
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
        x, y = (cr * cos(i / ncircles * TWO_PI + PI / 6) + width / 2,
            cr * sin(i / ncircles * TWO_PI + PI / 6) + height / 2)
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

