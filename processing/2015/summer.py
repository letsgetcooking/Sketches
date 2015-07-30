W = H = 500
FPS = 20.0
DURATION = 4
N_FRAMES = DURATION * FPS
N_SAMPLES = 4
TREE_COLOR = color(23, 135, 19)
BG_COLOR = color(23, 174, 255)
MAIN_COLOR = color(255, 251, 0)
STROKE_COLOR = color(255, 234, 173)
SECOND_COLOR = color(255, 164, 0)
FRAME_COLOR = color(50, 50, 30)
LIGHT_GREEN = color(200, 255, 50)
WHITE = color(255)
BLACK = color(0)
GREEN = color(3, 70, 50)
MASK_COLOR = color(255)
N_BEAMS = 60.0
NOISE_SCALE = 1
RAD = 50
DIST = 50
RECORD = False


class Leaf:

    def __init__(self, x, y, size, col, dynamic):
        self.pos = PVector(x, y)
        self.size = size
        self.dynamic = dynamic
        self.color = col
        self.light = 0

    def apply_light(self, power):
        self.light += power

    def display(self):
        rectMode(CENTER)
        noStroke()
        fill(lerpColor(self.color, LIGHT_GREEN, self.light))
        pushMatrix()
        translate(self.pos.x, self.pos.y)
        if self.dynamic:
            self.size += 0.5 * sin(frameCount / 10.0)
        rect(0, 0, self.size, self.size)
        popMatrix()
        self.light = 0

class Forest:

    def __init__(self, n_leaves):
        self.leaves = []
        count = 0
        center = PVector(width / 2, height / 2)
        while count < n_leaves:
            angle = random(TWO_PI)
            x_noise, y_noise = polar2cart(10, angle)
            noise_v = noise(x_noise + 100, y_noise + 200)
            leaf_x, leaf_y = polar2cart(random(180 + 80 * noise_v, 400), angle)
            leaf_x += width / 2
            leaf_y += height / 2
            if 0 < leaf_x < width and 0 < leaf_y < height:
                tone = width / 2 - center.dist(PVector(leaf_x, leaf_y))
                colorMode(HSB)
                col = color(62, 180, random(tone + 50, tone + 100))
                self.leaves.append(Leaf(leaf_x, leaf_y, random(10, 20),
                    col, False))
                count += 1

    def apply_light(self, light_pos):
        for leaf in self.leaves:
            dist = leaf.pos.dist(light_pos)
            if dist < 100:
                leaf.apply_light(0.4 * (1 - dist / 100.0) ** 2)

    def display(self):
        for leaf in self.leaves:
            leaf.display()


def draw_frame(rad):
    fill(FRAME_COLOR)
    noStroke()
    beginShape()
    vertex(0, 0)
    vertex(0, height)
    vertex(width, height)
    vertex(width, 0)
    beginContour()
    for i in range(12):
        x, y = polar2cart(rad, i * TWO_PI / 12.0)
        vertex(x + width / 2, y + height / 2)
    endContour()
    endShape(CLOSE)

def polar2cart(r, theta):
    """ polar coordinates to cartesian """
    return r * cos(theta), r * sin(theta)

def cart2polar(x, y):
    """ cartesian coordinates to polar """
    return sqrt(x ** 2 + y ** 2), atan2(y, float(x))

def lsf(x):
    """
    Big-lambda shape function
    """
    if x < 0.5:
        return 2 * x
    else:
        return 2 * (1 - x)

def draw_(t):
    background(BG_COLOR)

    pushMatrix()
    translate(W / 2, H / 2)

    # drawing sun beams
    stroke(STROKE_COLOR)
    strokeWeight(3)
    fill(lerpColor(MAIN_COLOR, WHITE, 0.2))
    for i in range(0, N_BEAMS, 2):

        beginShape()

        angle = i * TWO_PI / N_BEAMS
        a = sin(angle)
        b = cos(angle)
        noise_v = noise(a * NOISE_SCALE + 100, b * NOISE_SCALE + 200,
            4 * lsf(t) * NOISE_SCALE + 300)
        x1, y1 = polar2cart(RAD + 10, i / N_BEAMS * 2 * PI)
        x2, y2 = polar2cart(RAD + noise_v * 150, i / N_BEAMS * 2 * PI)
        vertex(x1, y1)
        vertex(x2, y2)

        forest.apply_light(PVector(x2 + width / 2, y2 + height / 2))

        angle = (i + 1) * TWO_PI / N_BEAMS
        a = sin(angle)
        b = cos(angle)
        noise_v = noise(a * NOISE_SCALE + 100, b * NOISE_SCALE + 200,
            4 * lsf(t) * NOISE_SCALE + 300)
        x1, y1 = polar2cart(RAD + 10, (i + 1) / N_BEAMS * 2 * PI)
        x2, y2 = polar2cart(RAD + noise_v * 150, (i + 1) / N_BEAMS * 2 * PI)
        vertex(x2, y2)
        vertex(x1, y1)

        forest.apply_light(PVector(x2 + width / 2, y2 + height / 2))

        endShape(CLOSE)

    # drawing mask and filling it with noise
    noStroke()
    fill(MASK_COLOR)
    ellipse(0, 0, 2 * RAD, 2 * RAD)
    loadPixels()
    for i in range(W / 2 - RAD, W / 2 + RAD):
        for j in range(H / 2 - RAD, H / 2 + RAD):
            if pixels[i * W + j] == color(255):
                r, theta = cart2polar(i - W / 2, j - H / 2)
                phi = t * 2 * PI
                x_noise = (DIST + r * cos(theta)) * cos(phi)
                y_noise = (DIST + r * cos(theta)) * sin(phi)
                z_noise = r * sin(theta)
                noise_v = noise(x_noise * NOISE_SCALE / 30.0 + 100, y_noise *
                    NOISE_SCALE / 30.0 + 200, z_noise * NOISE_SCALE / 30.0 + 300)
                pixels[i * W + j] = lerpColor(SECOND_COLOR, MAIN_COLOR, noise_v)
    updatePixels()

    # drawing sun contour
    stroke(STROKE_COLOR)
    strokeWeight(3)
    noFill()
    ellipse(0, 0, 2 * RAD, 2 * RAD)

    popMatrix()

    # drawing trees
    draw_frame(240)
    # forest.display()


def setup():
    global forest
    size(W, H)
    frameRate(FPS)
    forest = Forest(2000)

def draw():
    # drawing with SSAA when recording
    colorMode(RGB)
    if not RECORD:
        t = (frameCount / float(N_FRAMES)) % 1.0
        draw_(t)
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
