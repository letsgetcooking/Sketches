from geomerative import RPath, RPoint


W = H = 500
FPS = 20.0
DURATION = 4
N_FRAMES = DURATION * FPS
N_SAMPLES = 4
BG_COLOR = color(153, 50, 32)
MAIN_COLOR = color(62, 146, 163)
FIRST_COLOR = color(21, 23, 26)
SECOND_COLOR = color(62, 146, 163)
RECORD = False


ANCHOR, CONTROL = range(2)


class Point(object):
    def __init__(self, x, y, tp):
        self.x = x
        self.y = y
        self.type = tp
        self.radius = 13 if self.type == ANCHOR else 10
        self.is_active = False
        self.is_visible = False

    def display(self):
        if not self.is_visible:
            return

        stroke(255)

        if self.is_active:
            br = 100
        else:
            br = 50
        if self.type == ANCHOR:
            fill(200, br)
        else:
            fill(200, 0, 0, br)
        ellipse(self.x, self.y, 2 * self.radius, 2 * self.radius)

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    def set(self, x, y):
        self.x, self.y = x, y

    def toggle(self):
        self.is_visible = not self.is_visible


class Tube(object):
    def __init__(self, x, y, size, path):
        self.x, self.y = x, y
        self.size = size
        self.fatness = 1.0
        self.path = path
        self.seed = int(random(1000))

    def display(self, t):
        randomSeed(self.seed)
        noStroke()
        res = 350.0
        tt = res * t
        fill(FIRST_COLOR)
        for i in range(int(tt)):
            if i == 0 or i > res - 1:
                continue
            if not i % 4:
                fill(lerpColor(FIRST_COLOR, SECOND_COLOR, floor(random(2))))
            p = self.path.getPoint(constrain(i / res, 0, 1))
            x, y = p.x, p.y
            prev = self.path.getPoint(constrain((i - 1) / res, 0, 1))
            prev.sub(p)
            angle = atan2(prev.x, prev.y)
            pushMatrix()
            translate(x, y)
            rotate(-angle + HALF_PI)
            k = 70.0
            s = self.fatness * self.size * ((1 - ((constrain(i / k, 0, 1) - 1) ** 8)) * (1 - (constrain((i - tt + k) / k, 0, 1) ** 8)))
            ellipse(0, 0, 0.5 * s, 2 * s)
            popMatrix()

    def set_fatness(self, f):
        self.fatness = f


def create_p(points):
    path = RPath(points[0].x, points[0].y)
    path.addLineTo(points[1].x, points[1].y)
    path.addBezierTo(points[2].x, points[2].y, points[3].x, points[3].y, points[4].x, points[4].y)
    path.addBezierTo(points[5].x, points[5].y, points[6].x, points[6].y, points[7].x, points[7].y)

    return Tube(points[0].x, points[0].y, 30, path)

def create_five(points):
    path = RPath(points[0].x, points[0].y)
    path.addBezierTo(points[1].x, points[1].y, points[2].x, points[2].y, points[3].x, points[3].y)
    path.addBezierTo(points[4].x, points[4].y, points[5].x, points[5].y, points[6].x, points[6].y)
    path.addBezierTo(points[7].x, points[7].y, points[8].x, points[8].y, points[9].x, points[9].y)
    path.addLineTo(points[10].x, points[10].y)

    return Tube(points[0].x, points[0].y, 30, path)

def keyPressed():
    global tubes
    
    if key == 'u' or key == 'U':
        tubes = []
        tubes.append(create_p(points_p))
        tubes.append(create_five(points_five))
    elif key == 't' or key == 'T':
        for p in points_p:
            p.toggle()
        for p in points_five:
            p.toggle()

def mouseDragged():
    global state

    if mouseButton == RIGHT:
        state = mouseX / float(width)
    elif mouseButton == LEFT:
        for p in points_p:
            if p.is_active:
                p.set(mouseX, mouseY)
        for p in points_five:
            if p.is_active:
                p.set(mouseX, mouseY)

def mousePressed():
    closest = None
    min_dist = 999999999
    for p in points_p:
        dist = (p.x - mouseX) ** 2 + (p.y - mouseY) ** 2
        if dist < p.radius ** 2 and dist < min_dist:
            min_dist = dist
            closest = p
    if closest:
        closest.activate()

    closest = None
    min_dist = 999999999
    for p in points_five:
        dist = (p.x - mouseX) ** 2 + (p.y - mouseY) ** 2
        if dist < p.radius ** 2 and dist < min_dist:
            min_dist = dist
            closest = p
    if closest:
        closest.activate()

def mouseReleased():
    for p in points_p:
        p.deactivate()

    for p in points_five:
        p.deactivate()

def draw_(t):
    global SECOND_COLOR
    background(BG_COLOR)

    SECOND_COLOR = FIRST_COLOR
    for tube in tubes:
        tt = 1 / (1 + exp(-map(min(1, 2 * t), 0, 1, -6, 6)))
        ft = constrain(1 - max(0, 8 * t - 7) ** 2, 0, 1)
        tube.set_fatness(min(1, 10 * t) * ft)
        tube.display(tt)

    filter(BLUR, 4)

    SECOND_COLOR = MAIN_COLOR
    for tube in tubes:
        tt = 1 / (1 + exp(-map(min(1, 2 * t), 0, 1, -6, 6)))
        ft = constrain(1 - max(0, 8 * t - 7) ** 2, 0, 1)
        tube.set_fatness(min(1, 10 * t) * ft)
        tube.display(tt)

    for p in points_p:
        p.display()

    for p in points_five:
        p.display()

def setup():
    global state
    global points_p
    global points_five
    global tubes

    size(W, H)
    frameRate(FPS)

    state = 0.1
    length = 150

    x, y = 100, height / 2 + 140

    x1, y1 = x - length / 20, y - length
    cx1, cy1 = x - length / 15, y - length * 1.5
    cx2, cy2 = x - length / 15, y - length * 1.7
    x2, y2 = x + length / 3, y - length * 1.7

    cx3, cy3 = x + length / 4 + 0.75 * length, y - length * 1.7
    cx4, cy4 = x + length / 4 + 0.75 * length, y + length - length * 1.7
    x3, y3 = x + length / 4, y + length - length * 1.7

    points_p = [Point(x, y, ANCHOR), Point(x1, y1, ANCHOR), Point(cx1, cy1, CONTROL), Point(cx2, cy2, CONTROL),
            Point(x2, y2, ANCHOR), Point(cx3, cy3, CONTROL), Point(cx4, cy4, CONTROL), Point(x3, y3, ANCHOR)]

    x, y =  310, height / 2 + 115
    x1, y1 =  x - 20, y
    cx1, cy1 = x + length * 0.9, y + length / 4
    cx2, cy2 = x + length, y - length * 0.8 - length / 8
    x2, y2 = x + length / 4, y - length * 0.8

    cx3, cy3 = x, y + length / 20 - length * 0.8
    cx4, cy4 = x, y + length / 6 - length * 1.2
    x4, y4 = x, y - length * 1.2

    cx5, cy5 = x, y - length / 6 - length * 1.2
    cx6, cy6 = x + length / 15, y - length * 1.5
    x6, y6 = x + length / 4, y - length * 1.5

    x7, y7 = x + length * 0.9, y - length * 1.5

    points_five = [Point(x1, y1, ANCHOR), Point(cx1, cy1, CONTROL), Point(cx2, cy2, CONTROL), Point(x2, y2, ANCHOR),
                    Point(cx3, cy3, CONTROL), Point(cx4, cy4, CONTROL), Point(x4, y4, ANCHOR),
                    Point(cx5, cy5, CONTROL), Point(cx6, cy6, CONTROL), Point(x6, y6, ANCHOR),
                    Point(x7, y7, ANCHOR)]

    tubes = []
    tubes.append(create_p(points_p))
    tubes.append(create_five(points_five))

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
