from collections import deque
from toxi.geom import Vec3D


W = H = 500
FPS = 30.0
DURATION = 8
N_FRAMES = DURATION * FPS
N_SAMPLES = 1
BG_COLOR = color(61, 49, 64)
MAIN_COLOR = color(252, 208, 54)
STROKE_COLOR = color(250, 178, 44)
SHADOW_COLOR = color(93, 90, 94)
INTER_COLOR = lerpColor(SHADOW_COLOR, BG_COLOR, 0.6)
RAD, GAP = 16, 6
N_LAYERS = 6
N_STATES = 60
RECORD = False


CENTRAL, T0, T60, T120, T180, T240, T300 = range(7)

def angle_to_type(angle):
    angle = (angle + TWO_PI / 12.0) % TWO_PI
    if 0 <= angle < TWO_PI / 6:
        return T0
    elif TWO_PI / 6 <= angle < 2 * TWO_PI / 6:
        return T60
    elif 2 * TWO_PI / 6 <= angle < 3 * TWO_PI / 6:
        return T120
    elif 3 * TWO_PI / 6 <= angle < 4 * TWO_PI / 6:
        return T180
    elif 4 * TWO_PI / 6 <= angle < 5 * TWO_PI / 6:
        return T240
    else:
        return T300


class Tree(object):
    def __init__(self, val, kids=None, next=None):
        self.val = val
        self.kids = kids
        self.next = next

    def add_kid(self, val):
        if self.kids:
            self.kids.add_next(val)
        else:
            self.kids = Tree(val)

    def add_next(self, val):
        if not self.next:
            self.next = Tree(val)
        else:
            self.next.add_next(val)

    def layer(self, n):
        if n < 0: return []
        nodes = []
        if n == 0:
            nodes.append(self.val)
        else:
            kids = []
            kid = self.kids
            while True:
                if not kid: break
                kids.append(kid)
                kid = kid.next
            for kid in kids:
                nodes.extend(kid.layer(n - 1))
        return nodes

    def nodes(self):
        stack = deque()
        stack.append(self)
        while stack:
            branch = stack.pop()
            yield branch.val
            kid = branch.kids
            while True:
                if not kid: break
                stack.append(kid)
                kid = kid.next


class Cell(object):
    def __init__(self, x, y, z, r, cell_type):
        self.x, self.y, self.z = x, y, z
        self.radius = r
        self.type = cell_type
        self.state = 0
        self.enabled = False

    def __eq__(self, other):
        if (self.x - other.x) ** 2 + (self.y - other.y) ** 2 < 16:
            return True
        else:
            return False 

    def display(self):
        if not self.enabled: return
        vertices = []
        for i in range(6):
            x, y = self.radius * cos(i / 6.0 * TWO_PI), self.radius * sin(i / 6.0 * TWO_PI)
            v = Vec3D(x, y, self.z)
            vertices.append(v)
        r = self.radius + GAP / 2
        if self.type == T0:
            axis = vertices[2].sub(vertices[3]).getNormalized()
            bias = Vec3D(r * cos(0), r * sin(0), 0)
        elif self.type == T60:
            axis = vertices[3].sub(vertices[4]).getNormalized()
            bias = Vec3D(r * cos(TWO_PI / 6), r * sin(TWO_PI / 6), 0)
        elif self.type == T120:
            axis = vertices[4].sub(vertices[5]).getNormalized()
            bias = Vec3D(r * cos(2 * TWO_PI / 6), r * sin(2 * TWO_PI / 6), 0)
        elif self.type == T180:
            axis = vertices[5].sub(vertices[0]).getNormalized()
            bias = Vec3D(r * cos(3 * TWO_PI / 6), r * sin(3 * TWO_PI / 6), 0)
        elif self.type == T240:
            axis = vertices[0].sub(vertices[1]).getNormalized()
            bias = Vec3D(r * cos(4 * TWO_PI / 6), r * sin(4 * TWO_PI / 6), 0)
        elif self.type == T300:
            axis = vertices[1].sub(vertices[2]).getNormalized()
            bias = Vec3D(r * cos(5 * TWO_PI / 6), r * sin(5 * TWO_PI / 6), 0)
        else:
            axis = None
            bias = None

        beginShape()
        for v in vertices:
            if axis and bias:
                v.addSelf(bias)
                v.rotateAroundAxis(axis,
                    -(1 - min(1, 2 * self.state / float(N_STATES))) * PI)
                v.subSelf(bias)
            vertex(v.x() + self.x, v.y() + self.y, v.z())
        endShape(CLOSE)

    def enable(self):
        self.enabled = True

    def reset(self):
        self.state = 0
        self.enabled = False

    def update(self):
        if self.enabled:
            self.state = min(self.state + 1, N_STATES)


class Honeycomb(object):
    def __init__(self, x, y, z, nlayers, rad, gap):
        self.x, self.y, self.z = x, y, z
        self.cells = Tree(Cell(x, y, z, rad, CENTRAL))

        queue = deque()
        queue.append(self.cells)
        r = 2 * 0.87 * rad + gap
        for layer in range(nlayers):
            for i in range(6):
                angle = (i + 0.5) / 6.0 * TWO_PI
                for branch in queue:
                    x, y = r * cos(angle) + branch.val.x, r * sin(angle) + branch.val.y
                    new_cell = Cell(x, y, z, rad, angle_to_type(angle))
                    if not new_cell in self.cells.nodes():
                        branch.add_kid(new_cell)

            for i in range(len(queue)):
                branch = queue.popleft()
                kids = []
                kid = branch.kids
                while True:
                    if not kid: break
                    kids.append(kid)
                    kid = kid.next
                for kid in kids:
                    queue.append(kid)

    def display(self):
        for cell in self.cells.nodes():
            cell.display()

    def display_layer(self, n):
        for cell in self.cells.layer(n):
            cell.display()

    def enable(self):
        for cell in self.cells.nodes():
            cell.state = N_STATES
            cell.enable()

    def reset(self):
        for cell in self.cells.nodes():
            cell.reset()

    def update(self, t):
        n = int(ceil(t * N_LAYERS))
        for cell in self.cells.layer(n):
            cell.enable()
        for cell in self.cells.nodes():
            cell.update()


def ease_in_out_cubic(t):
    t *= 2
    if t < 1:
        return 0.5 * t*t*t
    t -= 2
    return 0.5 * (t*t*t + 2)

def mousePressed():
    c = Cell(mouseX, mouseY, 0, RAD, CENTRAL)
    print c in hcomb.cells.nodes()

def draw_(t):
    background(BG_COLOR)

    hcomb.update(min(1.5 * t, 1))

    tt1 = max(0, 7 * t - 6)

    strokeWeight(4)
    stroke(SHADOW_COLOR)
    fill(SHADOW_COLOR)
    hcomb_bg.display()

    pos = ease_in_out_cubic(tt1) * 25

    filter(BLUR, 2)

    strokeWeight(3)

    pushMatrix()
    translate(0, 0, -pos)
    stroke(lerpColor(STROKE_COLOR, INTER_COLOR, ease_in_out_cubic(tt1)))
    fill(lerpColor(MAIN_COLOR, INTER_COLOR, ease_in_out_cubic(tt1)))
    hcomb.display()
    popMatrix()

    stroke(STROKE_COLOR)
    fill(MAIN_COLOR)
    center.display()

def setup():
    global hcomb, hcomb_bg
    global center

    size(W, H, P3D)
    frameRate(FPS)

    hcomb = Honeycomb(width / 2, height / 2, 0, N_LAYERS, RAD, GAP)
    hcomb_bg = Honeycomb(width / 2, height / 2, -10, N_LAYERS, RAD, GAP)
    hcomb_bg.enable()

    center = Cell(width / 2, height / 2, 0, RAD, CENTRAL)
    center.state = N_STATES
    center.enable()

def draw():
    if not RECORD:
        tprev = ((frameCount - 1) / float(N_FRAMES)) % 1.0
        tcurr = (frameCount / float(N_FRAMES)) % 1.0
        if tcurr < tprev:
            hcomb.reset()
        draw_(tcurr)
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
