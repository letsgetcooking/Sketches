from toxi.geom import Line2D, Vec2D
import random


W = H = 500
FPS = 20.0
DURATION = 8.0
N_FRAMES = DURATION * FPS
N_SAMPLES = 4.0
BACK_COLOR = color(2, 100, 117)
BG_COLOR = color(254, 251, 175)
GEM_COLOR = color(255, 209, 59)
FLOW_COLOR = color(251, 184, 41)
RECORD = False


class Rule(object):
    def __init__(self, predecessor, successor):
        self.predecessor = predecessor
        self.successor = successor

class LSystem(object):
    def __init__(self, axiom, angle):
        self.axiom = axiom
        self.angle = angle
        self.sentence = axiom
        self.generation = 0
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def generate(self):
        next = ''
        for c in self.sentence:
            next += self.interpret(c)
        self.sentence = next

    def get_sentence(self):
        return self.sentence

    def interpret(self, c):
        for rule in self.rules:
            if c == rule.predecessor:
                return rule.successor
        return c

    def render(self):
        pass

class TestLSystem(LSystem):
    def __init__(self, axiom, angle, s_scale):
        super(TestLSystem, self).__init__(axiom, angle)
        self.scale = s_scale

    def render(self, pg):
        pg.pushMatrix()
        for c in self.sentence:
            if c == 'F':
                pg.line(0, 0, self.scale, 0)
                pg.translate(self.scale, 0)
            elif c == 'f':
                pg.translate(self.scale, 0)
            elif c == 'r':
                pg.ellipse(0, 0, self.scale, self.scale)
            elif c == '+':
                pg.rotate(-self.angle)
            elif c == '-':
                pg.rotate(self.angle)
            elif c == '[':
                pg.pushMatrix()
            elif c == ']':
                pg.popMatrix()
        pg.popMatrix()

    def save(self, lines, circles):
        pos = Vec2D(0, 0)
        d = Vec2D(self.scale, 0)
        pos_stack = []
        d_stack = []
        for c in self.sentence:
            if c == 'F':
                p1 = pos.copy()
                p2 = pos.add(d)
                for _line in lines:
                    if (_line.a.isInCircle(p1, 2) and _line.b.isInCircle(p2, 2) or
                        _line.a.isInCircle(p2, 2) and _line.b.isInCircle(p1, 2)):
                        break
                else:
                    lines.append(Line2D(p1, p2))
                pos = pos.add(d)
            elif c == 'f':
                pos = pos.add(d)
            elif c == 'r':
                for circle in circles:
                    if pos.isInCircle(circle, 5):
                        break
                else:
                    circles.append(pos)
            elif c == '+':
                d.rotate(-self.angle)
            elif c == '-':
                d.rotate(self.angle)
            elif c == '[':
                pos_stack.append(pos.copy())
                d_stack.append(d.copy())
            elif c == ']':
                pos = pos_stack.pop()
                d = d_stack.pop()

class Node(object):
    def __init__(self):
        self.lines = []
        self.next = []
        self.has_circle = False

    def add_data(self, data):
        self.data.append(data)

    def add_node(self, node):
        self.next.append(node)

def make_l_system(axiom, rules, angle, s_scale, n_gens):
    ls = TestLSystem(axiom, angle, s_scale)
    for rule in rules:
        ls.add_rule(rule)

    for i in range(n_gens):
        ls.generate()

    return ls

def make_image(x, y, w, h, ls, col, vertices=None, graph=False):

    pg = createGraphics(w, h)

    pg.beginDraw()
    pg.translate(x, y)

    if vertices:
        pg.fill(FLOW_COLOR)
        pg.noStroke()

        pg.beginShape()
        for v in vertices:
            pg.vertex(v.x(), v.y())
        pg.endShape()

    pg.fill(GEM_COLOR)
    pg.stroke(col)

    if not graph:
        ls.render(pg)
    else:
        lines = []
        circles = []
        ls.save(lines, circles)

        for _line in lines:
            pg.line(_line.a.x(), _line.a.y(), _line.b.x(), _line.b.y())
        for circle in circles:
            pg.ellipse(circle.x(), circle.y(), 16, 16)

    pg.endDraw()

    return pg

def make_shape(lines):
    points = []
    edges = [[None, None] for _ in range(len(lines))]
    for i, _line in enumerate(lines):
        a_exist, b_exist = False, False
        for p in points:
            if _line.a.isInCircle(p, 2):
                a_exist = True
                edges[i][0] = p
            if _line.b.isInCircle(p, 2):
                b_exist = True
                edges[i][1] = p

        if not a_exist:
            points.append(_line.a)
            edges[i][0] = points[-1]
        if not b_exist:
            points.append(_line.b)
            edges[i][1] = points[-1]

    neighbors = {}
    for edge in edges:
        if neighbors.get(edge[0]) == None:
            neighbors[edge[0]] = set()
        neighbors[edge[0]].add(edge[1])
        if neighbors.get(edge[1]) == None:
            neighbors[edge[1]] = set()
        neighbors[edge[1]].add(edge[0])

    center = Vec2D(0, 0)
    poly = []
    for p in points:
        if p.distanceToSquared(center) > 3800:
            poly.append(p)

    first = poly[0]

    cur_point = first
    vertices = []
    vertices.append(cur_point)

    while True:
        cands = []

        for neig in neighbors[cur_point]:
            if neig in poly and not neig in vertices:
                cands.append(neig)

        if len(cands) > 1:
            cur_point = max(cands, key=center.distanceToSquared)
            vertices.append(cur_point)
        elif len(cands) == 1:
            cur_point = cands[0]
            vertices.append(cur_point)
        else:
            break

    return vertices

def draw_(t):
    background(BACK_COLOR)
    image(bg_pg, 0, 0)

    pushMatrix()
    translate(width / 2 + 5, height / 2 - 60)
    rotate(t * TWO_PI / 6)
    image(sun_pg, -width / 2, -height / 2)
    popMatrix()

    pushStyle()
    noStroke()
    fill(BG_COLOR)

    beginShape()
    for i in range(9):
        vertex(160 * cos(i / 8.0 * PI) + width / 2, 160 * sin(i / 8.0 * PI) + height / 2 + 26)
    endShape()

    popStyle()

    image(ground_pg, 0, 0)

def setup():
    global bg_pg
    global ground_pg
    global sun_pg
    size(W, H)
    frameRate(FPS)

    bg_ls = make_l_system('F', [Rule('F', '+FffFf[FF]+FF'),], PI / 6, 10, 7)
    bg_pg = make_image(W / 2, H / 4 + 145, W, H, bg_ls, color(BG_COLOR), graph=False)

    ground_ls = make_l_system('F', [Rule('F', 'F[f--f+F]F'),], PI / 3, 9, 5)
    ground_pg = make_image(W / 2 - 145, H / 4 + 150, W, H, ground_ls, color(35), graph=True)

    sun_ls = make_l_system('F', [Rule('F', 'F+F+r-F-F--F+F+r-F-F-'),], -PI / 3, 18, 3)

    lines = []
    circles = []
    sun_ls.save(lines, circles)
    vertices = make_shape(lines)
    sun_pg = make_image(W / 2, H / 2, W, H, sun_ls, color(35), vertices=vertices, graph=True)

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
