from random import choice

W = H = 500
FPS = 20.0
DURATION = 4
N_FRAMES = DURATION * FPS
N_SAMPLES = 4
BG_COLOR = color(23, 174, 255)
MAIN_COLOR = color(255, 251, 0)
STROKE_COLOR = color(255, 234, 173)
SECOND_COLOR = color(255, 164, 0)
WHITE = color(255)
BLACK = color(0)
GREEN = color(3, 70, 50)
MASK_COLOR = color(255)
N_BEAMS = 160.0
NOISE_SCALE = 1
RAD = 50
RECORD = False


class Path:

    def __init__(self, radius, color):
        self.radius = radius
        self.color = color
        self.points = []

    def add_point(self, x, y):
        new_point = PVector(x, y)
        self.points.append(new_point)

    def display(self):
        fill(self.color)
        stroke(self.color)
        strokeWeight(self.radius)
        beginShape()
        for _point in self.points:
            vertex(_point.x, _point.y)
        endShape()

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
    background(10)

    pushMatrix()
    translate(W / 2, H / 2)

    flame.display()
    filter(BLUR, 4)

    noStroke()
    fill(25)
    pushMatrix()
    rotate(PI / 12.0)
    rect(0, -30, 400, 60)
    popMatrix()

    strokeWeight(20)
    stroke(35)
    fill(0)
    ellipse(0, 0, 400, 400)

    noStroke()
    fill(lerpColor(MAIN_COLOR, WHITE, 0.8))
    beginShape()
    for i in range(0, N_BEAMS):


        angle = i * TWO_PI / N_BEAMS
        a = sin(angle)
        b = cos(angle)
        noise_v = noise(a * NOISE_SCALE + 100, b * NOISE_SCALE + 200,
            4 * lsf(t) * NOISE_SCALE + 300)
        x, y = polar2cart(80 + noise_v * 60, i / N_BEAMS * 2 * PI)
        vertex(x, y)

    endShape(CLOSE)

    pos_x, pos_y = 0, 0
    stroke(STROKE_COLOR)
    strokeWeight(5)
    noFill()
    ellipse(pos_x, pos_y, 2 * RAD + 5, 2 * RAD + 5)
    
    noStroke()
    fill(SECOND_COLOR)
    ellipse(pos_x, pos_y, 2 * RAD, 2 * RAD)

    popMatrix()


def setup():
    global flame
    size(W, H)
    frameRate(FPS)
    flame = Path(20, color(67, 207, 250, 80))
    n = 180.0
    coords = []
    for i in range(n + 1):
        x, y = polar2cart(220 + 20 * sin(int(random(1, 30)) * TWO_PI * i / n + 2)
            * cos(5 * TWO_PI * i / n + 6)
            * cos(2 * TWO_PI * i / n + 13), TWO_PI * i / n)
        coords.append((x, y))
    for x, y in coords:
        flame.add_point(x, y)

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
