W = H = 500
FPS = 20.0
DURATION = 6
N_FRAMES = DURATION * FPS
N_SAMPLES = 1
BG_COLOR = color(46,148,185)
MAIN_COLOR = color(255)
LIVE_LEAF_COLOR = color(210,85,101)
DEAD_LEAF_COLOR = color(65, 175, 230)
RECORD = False


class Particle(object):
    def __init__(self, x, y, start):
        self.x, self.y = x, y
        self.start = start

    def display(self, t):
        tt = 1 - (max(0, t - self.start) - 1) ** 2

        center = PVector(-1.35 * width / 3, 90)
        center.sub(PVector(self.x, self.y))
        center.normalize()
        center.mult(-1.2 * width)
        pos = PVector(self.x, self.y)
        center.mult(tt)
        pos.add(center)

        fill(LIVE_LEAF_COLOR)
        ellipse(pos.x + noise(pos.x * 0.003 + self.x) * 200 * tt, \
            pos.y + noise(pos.y * 0.003 + self.y) * 200 * tt, 5, 5)


class Branch(object):
    def __init__(self, angle, length):
        self.angle = angle
        self.length = length
        self.left = None
        self.right = None
        self.middle = None

    def display(self):
        strokeWeight(self.length * 0.1)
        line(0, 0, 0, -self.length)

    def set_left(self, branch):
        self.left = branch

    def set_middle(self, branch):
        self.middle = branch

    def set_right(self, branch):
        self.right = branch


class Tree(object):
    def __init__(self, depth):
        self.root = Branch(0, 50)
        self.__make_tree(self.root, 8)

    def __display_branch(self, branch, windforce, bg=False):
        pushMatrix()
        rotate(branch.angle + windforce)
        branch.display()
        translate(0, -branch.length)
        if branch.left:
            self.__display_branch(branch.left, windforce * 1.3, bg=bg)
        if branch.right:
            self.__display_branch(branch.right, windforce * 1.3, bg=bg)
        if bg and branch.middle:
            self.__display_branch(branch.middle, windforce * 1.1, bg=bg)
        popMatrix()

    def __make_tree(self, branch, depth):
        if depth < 1:
            return
        branch.set_left(Branch(-random(PI / 18, PI / 6), branch.length * (0.6 + random(0.4))))
        branch.set_right(Branch(random(PI / 18, PI / 6), branch.length * (0.6 + random(0.4))))
        self.__make_tree(branch.left, depth - 1)
        self.__make_tree(branch.right, depth - 1)
        if random(1) > 0.6:
            branch.set_middle(Branch(random(-PI / 8, PI / 8), branch.length * (0.6 + random(0.4))))
            self.__make_tree(branch.middle, depth - 1)

    def __spray(self, branch, particles, coord, direction, t):
        d = direction.copy()
        d.normalize()
        d.rotate(branch.angle + t)
        d.mult(branch.length)

        c = coord.copy()
        c.add(d)

        if not branch.left and not branch.right:
            particles.append(c)
            return

        if branch.left:
            self.__spray(branch.left, particles, c, d, t * 1.3)
        if branch.right:
            self.__spray(branch.right, particles, c, d, t * 1.3)

    def display(self, t):
        tt = PI / 120.0 * (sin(t * TWO_PI) + 1) / 2.0

        pushMatrix()
        stroke(200)
        self.__display_branch(self.root, tt, bg=True)
        stroke(255)
        self.__display_branch(self.root, tt)
        popMatrix()

    def spray_particles(self, t):
        particles = []
        tt = PI / 120.0 * (sin(t * TWO_PI) + 1) / 2.0
        self.__spray(self.root, particles, PVector(0, 0), PVector(0, -1), tt)
        return particles


def keyPressed():
    global SEED
    if key == 'n':
        SEED = int(random(10000))

def draw_(t):
    background(BG_COLOR)
    stroke(255)
    strokeWeight(5)

    # noFill()
    # bezier(0, height - 20, 40, height - 20, width - 90, height - 20, width, height - 60);
    img = loadImage('gif_temp/' + nf(frameCount, 4) + '.gif')
    image(img, 0, 0)
    
    pushMatrix()
    translate(width / 3, height - 25)
    # tree.display(t)

    ps = tree.spray_particles(t)
    fill(LIVE_LEAF_COLOR)
    strokeWeight(1)

    if t < 0.5 and random(1) < 0.5 + t:
        dead = int(random(len(ps)))
        if not dead in deads:
            particles.append(Particle(ps[dead].x, ps[dead].y, t))
        deads.add(dead)

    if t > 0.8:
        for p in ps:
            ellipse(p.x, p.y, 25 * (t - 0.8), 25 * (t - 0.8))

    for dead in sorted(deads, reverse=True):
        del ps[dead]

    for p in ps:
        ellipse(p.x, p.y, 5, 5)

    for particle in particles:
        particle.display(t)
    popMatrix()

def setup():
    global tree
    global deads
    global particles
    global seed

    size(W, H)
    frameRate(FPS)

    seed = 2033093
    randomSeed(seed)

    tree = Tree(3)
    deads = set()
    particles = []

def draw():
    if not RECORD:
        t = (frameCount / float(N_FRAMES)) % 1.0
        draw_(t)

        # text(str(seed), 10, 20)
        # if frameCount == 1:
        #     save('test/' + str(seed) + '.png')
        # else:
        #     exit()
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
            
