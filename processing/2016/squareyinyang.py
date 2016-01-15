W = H = 500
FPS = 30.0
DURATION = 4
N_FRAMES = DURATION * FPS
N_SAMPLES = 1
BG_COLOR = (0, 0, 20)
LEAF_COLOR = (0, 0, 20)
RECORD = False


class Leaf(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 30
        self.current_color = LEAF_COLOR[:2] + (LEAF_COLOR[2] + random(-5, 5),)
        self.current_color = color(*self.current_color)
        self.color = self.current_color

    def display(self):
        rectMode(CENTER)
        fill(self.current_color)
        noStroke()
        rect(self.x, self.y, self.w, self.w)

    def display_on_pg(self, pg):
        pg.rectMode(CENTER)
        pg.fill(0, 0, 10)
        pg.noStroke()
        pg.rect(self.x, self.y, self.w, self.w)

    def illuminate(self, col, lvl):
        self.current_color = lerpColor(self.current_color, col, lvl)

    def update(self):
        self.current_color = lerpColor(self.current_color, self.color, 0.025)


class Leaves(object):
    def __init__(self, x, y, r):
        self.leaves = []
        for _ in range(2000):
            lx, ly = x + random(-150, 150), y + random(-150, 150)
            self.leaves.append(Leaf(lx, ly))

    def apply_light(self, x, y, col):
        for leaf in self.leaves:
            in_square = abs(leaf.x - x) < 100 and abs(leaf.y - y) < 100
            dist = (leaf.x - x) ** 2 + (leaf.y - y) ** 2
            if in_square:
                leaf.illuminate(col, 1 - dist / 20000.0)

    def display(self):
        for leaf in self.leaves:
            leaf.display()

    def display_shadow(self, pg):
        pg.beginDraw()
        for leaf in self.leaves:
            leaf.display_on_pg(pg)
        pg.filter(BLUR, 8)
        pg.endDraw()

    def update(self):
        for leaf in self.leaves:
            leaf.update()


def draw_(t):
    background(*BG_COLOR)
    image(bg_image, 0, 0)
    image(shadow, 0, 0)

    tt = (4 * t) % 1.0
    if 0 <= t < 0.25:
        x1, y1 = width / 2 - 90, height / 2 - 90 + 180 * tt
        x2, y2 = width / 2 + 90, height / 2 + 90 - 180 * tt
    elif 0.25 <= t < 0.5:
        x1, y1 = width / 2 - 90 + 180 * tt, height / 2 + 90
        x2, y2 = width / 2 + 90 - 180 * tt, height / 2 - 90
    elif 0.5 <= t < 0.75:
        x1, y1 = width / 2 + 90, height / 2 + 90 - 180 * tt
        x2, y2 = width / 2 - 90, height / 2 - 90 + 180 * tt
    else:
        x1, y1 = width / 2 + 90 - 180 * tt, height / 2 - 90
        x2, y2 = width / 2 - 90 + 180 * tt, height / 2 + 90
    leaves.apply_light(x1, y1, color(0, 0, 0))
    leaves.apply_light(x2, y2, color(0, 0, 100))
    leaves.update()
    leaves.display()

    pushMatrix()
    fill(0, 0, 95)
    translate(x1, y1)
    rotate(-t * TWO_PI)
    rect(0, 0, 20, 20)
    popMatrix()
    pushMatrix()
    fill(0, 0, 5)
    translate(x2, y2)
    rotate(-t * TWO_PI)
    rect(0, 0, 20, 20)
    popMatrix()

def setup():
    global leaves
    global bg_image
    global shadow

    size(W, H)
    frameRate(FPS)

    colorMode(HSB, 360, 100, 100)
    leaves = Leaves(width / 2, height / 2, 130)

    bg_image = createGraphics(width, height)
    bg_image.beginDraw()
    bg_image.colorMode(HSB, 360, 100, 100)
    bg_image.noStroke()
    for _ in range(1000):
        bg_image.pushMatrix()
        bg_image.fill(0, 0, random(20, 30))
        bg_image.translate(random(width), random(height))
        bg_image.rotate(random(TWO_PI))
        bg_image.rect(0, 0, 50, 50)
        bg_image.popMatrix()
    bg_image.endDraw()

    shadow = createGraphics(width, height)
    leaves.display_shadow(shadow)

def draw():
    if not RECORD:
        t = (frameCount / float(N_FRAMES)) % 1.0
        draw_(t)
    elif N_SAMPLES <= 1:
        t = (frameCount / float(N_FRAMES)) % 1.0
        draw_(t)
        if frameCount <= 2 * N_FRAMES:
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
        if frameCount <= 2 * N_FRAMES:
            saveFrame('gif/####.gif')
        else:
            exit()
