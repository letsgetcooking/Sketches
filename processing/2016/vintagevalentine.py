from random import choice, shuffle
from toxi.geom import Vec3D
from Queue import Queue


W = H = 500
FPS = 30.0
DURATION = 8
N_FRAMES = DURATION * FPS
N_SAMPLES = 1
BG_COLOR = color(237, 213, 153)
SHADOW_COLOR = color(121, 86, 64)
MAIN_COLOR = color(206, 93, 79)
STROKE_COLOR = color(73, 40, 51)
FRAME_COLOR1 = color(188, 184, 137)
FRAME_COLOR2 = color(161, 136, 114)
SURFW, SURFH = 360.0, 300.0
N_STATES = 15.0
STATES = 140.0
SELECTED = False
RECORD = False


CENTRAL, LEFTRIGHT, RIGHTLEFT, BOTTOMTOP, TOPBOTTOM, NONE = range(6)


class Tree(object):
    """
    Must be a singleton-class
    """
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

    def get_path_to(self, pos, track, branch=None):
        if not branch: branch = self

        if branch.val == pos:
            track.append(branch.val)
            return True

        kids = []
        kid = branch.kids
        while True:
            if not kid: break
            kids.append(kid)
            kid = kid.next

        for kid in kids:
            if self.get_path_to(pos, track, kid):
                track.insert(0, kid.val)
                return True

        return False

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
    def __init__(self, x, y, z, w, h, nrows, ncols, hmap):
        self.x = x
        self.y = y
        self.z = z
        self.width = w
        self.height = h
        self.nrows = nrows
        self.ncols = ncols
        self.cellw = self.width / self.ncols
        self.cellh = self.height / self.nrows
        self.fragments = dict()
        self.tree = None
        self.queue = []
        self.state = 0

        hmap.loadPixels()
        for j in range(self.ncols):
            for i in range(self.nrows):
                if brightness(hmap.pixels[i * hmap.width + j]) < 200:
                    x = self.x + j * self.cellw
                    y = self.y + i * self.cellh
                    f = Fragment(x, y, z, self.cellw, self.cellh)
                    self.fragments[(i, j)] = f

    def select(self, x, y):
        closest = None
        min_dist = 9999999
        for pos in self.fragments:
            f = self.fragments[pos]
            dist = ((f.x + f.width / 2) - x) ** 2 + ((f.y + f.height / 2) - y) ** 2
            if dist < min_dist:
                closest = pos
                min_dist = dist

        self.trace(closest)

    def trace(self, start_pos):
        for pos in self.fragments:
            self.fragments[pos].disable()

        self.state = 0
        Tree.reset()
        self.tree = Tree(start_pos)
        self.fragments[start_pos].set(CENTRAL)
        while len(self.tree) < len(self.fragments):
            branch = self.tree.random()
            row, col = branch.val
            neighbours = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
            shuffle(neighbours)
            for r, c in neighbours:
                if (r, c) in self.fragments and not (r, c) in self.tree:
                    if r < row: self.fragments[(r, c)].set(BOTTOMTOP)
                    elif r > row: self.fragments[(r, c)].set(TOPBOTTOM)
                    elif c < col: self.fragments[(r, c)].set(RIGHTLEFT)
                    elif c > col: self.fragments[(r, c)].set(LEFTRIGHT)
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

        temp = self.queue[:]
        self.queue = [temp.pop(0)]
        index = 0
        while temp:
            if index > len(temp) - 1:
                index = 0
                self.queue.append(temp.pop(index))
                continue
            r1, c1 = self.queue[-1]
            r2, c2 = temp[index]
            dist = (r1 - r2) ** 2 + (c1 - c2) ** 2
            path = []
            self.tree.get_path_to((r2, c2), path)
            if dist > 4 and all(pos in self.queue for pos in path):
                self.queue.append(temp.pop(index))            
                index = 0
            else:
                index += 1

    def display(self):
        for pos in self.fragments:
            self.fragments[pos].display()

    def update(self):
        if self.queue:
            t = self.state / STATES
            r, c = self.queue[int(t * (len(self.queue) - 1))]
            self.fragments[(r, c)].enable()
            if self.state < STATES: self.state += 1

        for pos in self.fragments:
            self.fragments[pos].update()


def draw_frame():
    r = 420
    offset = 80
    ellipse(-offset, -offset, r, r)
    ellipse(-offset, height + offset, r, r)
    ellipse(width + offset, height + offset, r, r)
    ellipse(width + offset, -offset, r, r)

def draw_(t):
    global SELECTED

    background(BG_COLOR)
    if not SELECTED:
        heart.select(220, 250)
        SELECTED = True
    heart.update()

    strokeWeight(4)
    stroke(SHADOW_COLOR)
    fill(SHADOW_COLOR)
    heart.display()

    strokeWeight(10)
    draw_frame()

    filter(BLUR, 4)

    strokeWeight(2)
    stroke(STROKE_COLOR)
    fill(MAIN_COLOR)
    heart.display()

    strokeWeight(10)
    stroke(FRAME_COLOR2)
    fill(FRAME_COLOR1)
    draw_frame()

def mousePressed():
    heart.select(mouseX, mouseY)

def setup():
    global heart
    global hmap
    global particles

    size(W, H, P3D)
    frameRate(FPS)

    hmap = loadImage('heartmap1.png')
    heart = Surface((width - SURFW) / 2, (height - SURFH) / 2 + 10, 0, SURFW,
        SURFH, hmap.height, hmap.width, hmap)

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
