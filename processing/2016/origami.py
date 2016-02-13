from random import choice, shuffle
from toxi.geom import Vec3D
from Queue import Queue


W = H = 500
FPS = 30.0
DURATION = 8
N_FRAMES = DURATION * FPS
N_SAMPLES = 1
BG_COLOR = color(1, 155, 73)
MAIN_COLOR = color(245)
SURFW, SURFH = 300.0, 300.0
SURFX, SURFY = 9, 9
N_STATES = 15.0
STATES = 140.0
SELECTED = False
RECORD = False


CENTRAL, LEFTRIGHT, RIGHTLEFT, BOTTOMTOP, TOPBOTTOM, NONE = range(6)


class Tree(object):
    def __init__(self, val, kids=None, next=None):
        self.val = val
        self.kids = kids
        self.next = next
        Tree.fragments.add(val)

    def __iter__(self):
        return iter(Tree.fragments)

    def __len__(self):
        return len(Tree.fragments)

    def add_kid(self, val):
        if self.kids:
            self.kids.add_next(val)
        else:
            self.kids = Tree(val)
            Tree.fragments.add(val)

    def add_next(self, val):
        if not self.next:
            self.next = Tree(val)
            Tree.fragments.add(val)
        else:
            self.next.add_next(val)

    def random(self, branch=None):
        if not branch: branch = self
        r = random(1)
        if branch.next and r < 0.33:
            return self.random(branch.next)
        elif branch.kids and r < 0.66:
            return self.random(branch.kids)
        else:
            return branch

    @staticmethod
    def reset():
        Tree.fragments.clear()

    fragments = set()


class Fragment(object):
    def __init__(self, x, y, z, w, h):
        self.x = x
        self.y = y
        self.z = z
        self.width = w
        self.height = h
        self.enabled = False
        self.type = CENTRAL
        self.state = 0

    def display(self):
        fill(MAIN_COLOR)
        if self.enabled:
            t = self.state / N_STATES
            if self.type == CENTRAL:
                pos = Vec3D(self.x, self.y, self.z)
                a = Vec3D(0, 0, 0).add(pos)
                b = Vec3D(self.width, 0, 0).add(pos)
                c = Vec3D(self.width, self.height, 0).add(pos)
                d = Vec3D(0, self.height, 0).add(pos)
                beginShape()
                vertex(a.x(), a.y(), a.z())
                vertex(b.x(), b.y(), b.z())
                vertex(c.x(), c.y(), c.z())
                vertex(d.x(), d.y(), d.z())
                endShape(CLOSE)
            elif self.type == LEFTRIGHT:
                pos = Vec3D(self.x, self.y, self.z)
                a = Vec3D(0, 0, 0).add(pos)
                b = Vec3D(self.width, 0, 0).rotateY(PI * (1 - t)).add(pos)
                c = Vec3D(self.width, self.height, 0).rotateY(PI * (1 - t)).add(pos)
                d = Vec3D(0, self.height, 0).add(pos)
                beginShape()
                vertex(a.x(), a.y(), a.z())
                vertex(b.x(), b.y(), b.z())
                vertex(c.x(), c.y(), c.z())
                vertex(d.x(), d.y(), d.z())
                endShape(CLOSE)
            elif self.type == RIGHTLEFT:
                pos = Vec3D(self.x + self.width, self.y, self.z)
                a = Vec3D(0, 0, 0).add(pos)
                b = Vec3D(self.width, 0, 0).rotateY(PI * t).add(pos)
                c = Vec3D(self.width, self.height, 0).rotateY(PI * t).add(pos)
                d = Vec3D(0, self.height, 0).add(pos)
                beginShape()
                vertex(a.x(), a.y(), a.z())
                vertex(b.x(), b.y(), b.z())
                vertex(c.x(), c.y(), c.z())
                vertex(d.x(), d.y(), d.z())
                endShape(CLOSE)
            elif self.type == TOPBOTTOM:
                pos = Vec3D(self.x, self.y, self.z)
                a = Vec3D(0, 0, 0).add(pos)
                b = Vec3D(self.width, 0, 0).add(pos)
                c = Vec3D(self.width, self.height, 0).rotateX(-PI * (1 - t)).add(pos)
                d = Vec3D(0, self.height, 0).rotateX(-PI * (1 - t)).add(pos)
                beginShape()
                vertex(a.x(), a.y(), a.z())
                vertex(b.x(), b.y(), b.z())
                vertex(c.x(), c.y(), c.z())
                vertex(d.x(), d.y(), d.z())
                endShape(CLOSE)
            elif self.type == BOTTOMTOP:
                pos = Vec3D(self.x, self.y + self.height, self.z)
                a = Vec3D(0, 0, 0).add(pos)
                b = Vec3D(self.width, 0, 0).add(pos)
                c = Vec3D(self.width, self.height, 0).rotateX(-PI * t).add(pos)
                d = Vec3D(0, self.height, 0).rotateX(-PI * t).add(pos)
                beginShape()
                vertex(a.x(), a.y(), a.z())
                vertex(b.x(), b.y(), b.z())
                vertex(c.x(), c.y(), c.z())
                vertex(d.x(), d.y(), d.z())
                endShape(CLOSE)
        
    def disable(self):
        self.enabled = False
        self.state = 0

    def enable(self):
        if not self.enabled:
            self.enabled = True
            self.state = 0

    def set(self, tp):
        self.type = tp

    def update(self):
        if self.enabled and self.state < N_STATES:
            self.state += 1
        elif not self.enabled and self.state > 0:
            self.state -= 1


class Surface(object):
    def __init__(self, x, y, z, w, h, nrows, ncols):
        self.x = x
        self.y = y
        self.z = z
        self.width = w
        self.height = h
        self.nrows = nrows
        self.ncols = ncols
        self.cellw = self.width / self.ncols
        self.cellh = self.height / self.nrows
        self.fragments = []
        self.tree = None
        self.queue = []
        self.state = 0

        for j in range(self.ncols):
            self.fragments.append([])
            for i in range(self.nrows):
                x = self.x + i * self.cellw
                y = self.y + j * self.cellh
                f = Fragment(x, y, z, self.width / self.ncols, self.height / self.nrows)
                self.fragments[-1].append(f)

    def select(self, x, y):
        found = False
        for row in range(self.nrows):
            if self.fragments[row][0].y < y < self.fragments[row][0].y + self.fragments[row][0].width:
                for col in range(self.ncols):
                    if self.fragments[row][col].x < x < self.fragments[row][col].x + \
                        self.fragments[row][col].width:
                        self.trace(row, col)
                        found = True; break
            if found: break

    def trace(self, start_row, start_col):
        for row in self.fragments:
            for f in row:
                f.disable()

        self.state = 0
        Tree.reset()
        self.tree = Tree((start_row, start_col))
        self.fragments[start_row][start_col].set(CENTRAL)
        while len(self.tree) < self.nrows * self.ncols:
            branch = self.tree.random()
            row, col = branch.val
            neighbours = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
            shuffle(neighbours)
            for r, c in neighbours:
                if 0 <= r < self.nrows and 0 <= c < self.ncols and not (r, c) in self.tree:
                    if r < row: self.fragments[r][c].set(BOTTOMTOP)
                    elif r > row: self.fragments[r][c].set(TOPBOTTOM)
                    elif c < col: self.fragments[r][c].set(RIGHTLEFT)
                    elif c > col: self.fragments[r][c].set(LEFTRIGHT)
                    else: self.fragments[r][c].set(CENTRAL)
                    branch.add_kid((r, c))
                    break

        queue = Queue()
        queue.put(self.tree)
        self.queue = []
        while not queue.empty():
            branch = queue.get()
            self.queue.append(branch.val)
            kid = branch.kids
            while True:
                if not kid: break
                queue.put(kid)
                kid = kid.next

    def display(self):
        for row in self.fragments:
            for f in row:
                f.display()

    def update(self):
        if self.queue:
            t = self.state / STATES
            r, c = self.queue[int(t * (len(self.queue) - 1))]
            self.fragments[r][c].enable()
            if self.state < STATES: self.state += 1

        for row in self.fragments:
            for f in row:
                f.update()



def ease_in_out_cubic(t):
    t *= 2
    if t < 1:
        return 0.5 * t*t*t
    t -= 2
    return 0.5 * (t*t*t + 2)

def draw_(t):
    global SELECTED

    background(BG_COLOR)

    if t < 0.2:
        translate(-ease_in_out_cubic(1 - constrain(5 * t, 0, 1)) * 2 / 3.0 * width, 0, 0)
    elif not SELECTED:
        surf.select(width / 2, height / 2)
        SELECTED = True
    elif t > 0.8:
        translate(ease_in_out_cubic(constrain(5 * t - 4, 0, 1)) * 5 / 6.0 * width, 0, 0)

    surf.update()

    strokeWeight(4)
    center.display()
    surf.display()

    filter(BLUR, 3)

    strokeWeight(1.4)
    center.display()
    surf.display()

def mousePressed():
    surf.select(mouseX, mouseY)

def setup():
    global surf
    global center

    size(W, H, P3D)
    frameRate(FPS)
    stroke(0)

    surf = Surface(100, 100, 0, SURFW, SURFH, SURFX, SURFY)

    center = Fragment(width / 2 - SURFW / SURFX / 2, height / 2 - SURFH / SURFY / 2,
        0, SURFW / SURFX, SURFH / SURFY)
    center.set(CENTRAL)
    center.enable()

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
