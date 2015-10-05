W = H = 500
FPS = 20.0
DURATION = 6
N_FRAMES = DURATION * FPS
N_SAMPLES = 4
N_SCALE = 0.2
BG_COLOR = color(20, 18, 21)
CORE_COLOR = color(100, 36, 21)
CORE_COLOR1 = color(86, 26, 26)
CORE_COLOR2 = color(185, 105, 60)
PALETTE = [color(69, 76, 82), color(114, 129, 122), color(50, 58, 61), color(122, 173, 184)]
RECORD = False


class Planet:
    def __init__(self, x, y, r, size, angle, speed, color):
        self.x = x
        self.y = y
        self.radius = r
        self.size = size
        self.angle = angle
        self.speed = speed
        self.color = color

    def display(self, t):
        stroke(100)
        strokeWeight(1.4)
        noFill()
        ellipse(self.x, self.y, 2 * self.radius, 2 * self.radius)

        stroke(0)
        fill(self.color)
        x = self.radius * cos(self.angle + t * self.speed * TWO_PI) + self.x
        y = self.radius * sin(self.angle + t * self.speed * TWO_PI) + self.y
        ellipse(x, y, 2 * self.size, 2 * self.size)

        for i in range(max(1, int(self.size / 10.0))):
            r = self.size + 0.2 * self.size * (i + 1)

            stroke(100)
            strokeWeight(0.7)
            noFill()
            ellipse(x, y, 2 * r, 2 * r)

            noStroke()
            fill(180)
            sp_angle = -self.speed * t * TWO_PI * (2 * (i % 2) - 1) * (i + 1)
            sp_rad = self.size / 8.0
            ellipse(x + r * sin(sp_angle), y + r * cos(sp_angle), sp_rad, sp_rad)


def polar2cart(r, theta):
    """ polar coordinates to cartesian """
    return r * cos(theta), r * sin(theta)

def make_rads(radius):
    rads = []
    rads.append(radius)

    if radius > 40:
        radius *= 0.75
        inner_rads = make_rads(radius)
        rads.extend(inner_rads)
    return rads

def draw_stars(t):
    randomSeed(1234)
    strokeWeight(1.5)
    noStroke()
    fill(120)
    for i in range(5000):
        if random(1) < 0.05:
            rad = 3 * noise(2 * cos(t * TWO_PI) + i, 2 * sin(t * TWO_PI) + i) + 1
        else:
            rad = 2 * noise(2 * cos(t * TWO_PI) + i, 2 * sin(t * TWO_PI) + i)
        ellipse(width / 2 * randomGaussian() + width / 2,
            height / 2 * randomGaussian() + height / 2, rad, rad)

def draw_sun(t):
    r = 20
    n = 180.0
    for i in range(n):
        a = i / n * TWO_PI
        fill(lerpColor(CORE_COLOR1, CORE_COLOR2, noise(cos(a) + 123,
            sin(a) + 576, 10 * abs(t - 0.5))))
        x, y = r * cos(a) + width / 2, r * sin(a) + height / 2
        ellipse(x, y, 3, 3)

    fill(CORE_COLOR)
    ellipse(width / 2, height / 2, 34, 34)

def draw_(t):
    background(BG_COLOR)
    draw_stars(t)

    for planet in planets:
        planet.display(t)

    draw_sun(t)

def setup():
    global planets

    size(W, H)
    frameRate(FPS)

    planets = []
    rads = make_rads(200)
    for i, rad in enumerate(rads):
        planets.append(Planet(width / 2, height / 2, rad, rad / 10,
            random(TWO_PI), 2 * (i % 2) - 1, PALETTE[i % len(PALETTE)]))


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
            t = (frameCount + 0.25 * sample / float(N_SAMPLES)) / N_FRAMES
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
