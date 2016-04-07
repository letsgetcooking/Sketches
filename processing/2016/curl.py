from random import choice, shuffle
from collections import deque
from toxi.geom import Vec2D, Ray2D, Line2D
from toxi.color import ColorGradient, TColor
from geomerative import RG, RPath, RShape


W = H = 500
FPS = 30.0
DURATION = 8
N_FRAMES = DURATION * FPS
N_SAMPLES = 1
BG_COLOR = color(25)
SHADOW_COLOR = color(61, 50, 54)
MAIN_COLOR = color(215, 133, 86)
STROKE_COLOR = color(14, 18, 21)
SURFW, SURFH = 400.0, 436.0
N_STATES = 15.0
GAP = 2
STATES = 170.0
SELECTED = False
RECORD = False


CENTRAL, LEFTRIGHT, RIGHTLEFT, BOTTOMTOP, TOPBOTTOM, NONE = range(6)
COLORS = [(249, 237, 105), (240, 138, 93), (184, 59, 94), (106, 44, 112), (249, 237, 105)]
PALETTE1 = [(r / 255.0, g / 255.0, b / 255.0) for r, g, b in COLORS]
PALETTE2 = [(0, 0, 0), (0, 0, 0)]
DRAW_PIPELINE = []


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

    def find(self, val):
        if self.val == val:
            return self
        elif self.kids:
            kids = []
            kid = self.kids
            while True:
                if not kid: break
                kids.append(kid)
                kid = kid.next
            for kid in kids:
                res = kid.find(val)
                if res:
                    return res
        return None

    def get_path_to(self, val, track, branch=None):
        if not branch: branch = self

        if branch.val == val:
            track.append(branch.val)
            return True

        kids = []
        kid = branch.kids
        while True:
            if not kid: break
            kids.append(kid)
            kid = kid.next

        for kid in kids:
            if self.get_path_to(val, track, kid):
                track.insert(0, kid.val)
                return True

        return False

    def random(self, branch=None):
        if not branch: branch = self
        r = random(1)
        if branch.next and r < 0.5:
            return self.random(branch.next)
        elif branch.kids and r < 0.75:
            return self.random(branch.kids)
        else:
            return branch

    @staticmethod
    def reset():
        Tree.fragments.clear()

    fragments = set()


class Fragment(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.enabled = False
        self.type = CENTRAL
        self.state = 0

    def display(self, t):
        if self.enabled:
            if self.type == CENTRAL:
                angle = 0
            elif self.type == LEFTRIGHT:
                angle = HALF_PI
            elif self.type == RIGHTLEFT:
                angle = PI + HALF_PI
            elif self.type == TOPBOTTOM:
                angle = PI
            elif self.type == BOTTOMTOP:
                angle = 0
            else:
                angle = 0

            pos = Vec2D(self.x + self.width / 2, self.y + self.height / 2)
            t1, t2 = constrain(4 * self.state / N_STATES, 0, 1), \
                    constrain(4 * self.state / N_STATES - 1, 0, 3) / 3.0

            rpath = None

            if not self.type == CENTRAL:
                a = Vec2D((self.width / 2.7) * cos(PI + PI / 2.3), (self.width / 2.7) * sin(PI + PI / 2.3))
                b = Vec2D((self.width / 2.5) * cos(PI / 3.5), (self.width / 2.5) * sin(PI / 3.5))
                a.addSelf(Vec2D(0, self.width)).rotate(angle).addSelf(pos)
                b.rotate(angle).addSelf(pos)
                ab = Line2D(a, b)
                p = ab.toRay2D().getPointAtDistance(t1 * ab.getLength())
                rpath = RPath(a.x(), a.y())
                rpath.addLineTo(p.x(), p.y())


            coils = 3.0
            radius = self.width / 2.5
            rotation = PI / 3.5
            theta_max = coils * TWO_PI
            if self.type == CENTRAL:
                theta_max += PI / 7.0
            away_step = radius / theta_max
            chord = 1.0
            theta = theta_max

            while theta > theta_max * (1 - t2):
                away = away_step * theta
                around = theta + rotation
                x = cos(around) * away
                y = sin(around) * away
                v = Vec2D(x, y)
                v.rotate(angle)
                v.addSelf(pos)
                if rpath:
                    rpath.addLineTo(v.x(), v.y())
                else:
                    rpath = RPath(v.x(), v.y())
                theta -= chord / away

            if rpath:
                rshape = RShape(rpath)
                draw_shape(rshape, 150, 3, t)


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
            self.state += 2
        elif not self.enabled and self.state > 0:
            self.state -= 2


class Surface(object):
    def __init__(self, x, y, w, h, nrows, ncols, hmap):
        self.x = x
        self.y = y
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
                    f = Fragment(x, y, self.cellw, self.cellh)
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
        candidates = [start_pos,]
        while candidates:
            row, col = choice(candidates)
            neighbours = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
            shuffle(neighbours)
            for r, c in neighbours:
                if (r, c) in self.fragments and not (r, c) in self.tree:
                    if r < row: self.fragments[(r, c)].set(BOTTOMTOP)
                    elif r > row: self.fragments[(r, c)].set(TOPBOTTOM)
                    elif c < col: self.fragments[(r, c)].set(RIGHTLEFT)
                    elif c > col: self.fragments[(r, c)].set(LEFTRIGHT)
                    else: self.fragments[r][c].set(CENTRAL)
                    branch = self.tree.find((row, col))
                    branch.add_kid((r, c))
                    candidates.append((r, c))
                    break
            deads = []
            for row, col in candidates:
                neighbours = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
                for neighbour in neighbours:
                    if neighbour in self.fragments and not neighbour in self.tree:
                        break
                else:
                    deads.append((row, col))
            for dead in deads:
                candidates.remove(dead)

        queue = deque()
        queue.append(self.tree)
        self.queue = []
        while queue:
            branch = queue.popleft()
            self.queue.append(branch.val)
            kid = branch.kids
            while True:
                if not kid: break
                queue.append(kid)
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

    def display(self, t):
        for pos in self.fragments:
            self.fragments[pos].display(t)

    def reset(self):
        for pos in self.fragments:
            self.state = 0
            self.fragments[pos].disable()

    def update(self):
        if self.queue:
            t = self.state / STATES
            r, c = self.queue[int(t * (len(self.queue) - 1))]
            self.fragments[(r, c)].enable()
            if self.state < STATES: self.state += 1

        for pos in self.fragments:
            self.fragments[pos].update()


def draw_shape(shape, res, w, t, scolor=None):
    noStroke()

    res = int(res)
    grad = ColorGradient()
    for i, col in enumerate(PALETTE):
        grad.addColorAt(i / float(len(PALETTE)) * res, TColor.newRGB(*col))
    colors = grad.calcGradient(0, res)

    if scolor:
        fill(scolor)
        beginShape()
        for p in shape.getPoints():
            vertex(p.x, p.y)
        endShape(CLOSE)

    for i in range(res):
        p = shape.getPoint(i / float(res))
        col = colors.get(int((i + t * res) % res)).toARGB()
        fill(col)
        DRAW_PIPELINE.append((0 if i < 10 else 1, (p.x, p.y, w), col))
        
def ease_in_out_cubic(t):
    t *= 2
    if t < 1:
        return 0.5 * t*t*t
    t -= 2
    return 0.5 * (t*t*t + 2)

def draw_(t):
    global SELECTED
    global PALETTE
    del DRAW_PIPELINE[:]

    background(BG_COLOR)
    if not SELECTED:
        closest = surf.select(width / 2, height)
        SELECTED = True
    surf.update()

    tt = max(0, 6 * t - 5)
    tt2 = max(0, 9 * t - 8)

    PALETTE = PALETTE2
    surf.display(t)
    DRAW_PIPELINE.sort(key=lambda x: x[0])
    for layer, (x, y, w), col in DRAW_PIPELINE:
        fill(col)
        ellipse(x, y, w, w)

    filter(BLUR, 4)

    PALETTE = PALETTE1
    surf.display(t)
    DRAW_PIPELINE.sort(key=lambda x: x[0])
    for layer, (x, y, w), col in DRAW_PIPELINE:
        fill(col)
        ellipse(x, y, w, w)

    noStroke()
    fill(0, 255 * tt2)
    rect(0, 0, width, height)

def mousePressed():
    surf.select(mouseX, mouseY)

def setup():
    global surf
    global hmap
    global particles
    global frag

    size(W, H)
    frameRate(FPS)
    RG.init(this)

    hmap = loadImage('map.png')
    surf = Surface((width - SURFW) / 2, (height - SURFH) / 2 + SURFH - SURFW, SURFW,
        SURFH, hmap.height, hmap.width, hmap)

def draw():
    if not RECORD:
        prev = ((frameCount - 1) / float(N_FRAMES)) % 1.0
        t = (frameCount / float(N_FRAMES)) % 1.0
        if prev > t: surf.reset()
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
            
