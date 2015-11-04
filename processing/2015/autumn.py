from controlP5 import ControlP5
from peasy import PeasyCam
from random import shuffle, sample, choice


W = H = 500
FPS = 30.0
DURATION = 4
N_FRAMES = DURATION * FPS
N_SAMPLES = 1
BG_COLOR = color(21, 35, 34)
MAIN_COLOR = color(35)
STROKE_COLOR = color(255)
PALETTE = [color(35, 21, 21), color(157, 71, 7), color(69, 27, 13),
            color(100, 73, 56), color(80, 24, 11)]
BOX_SIZE = 40.0
FIELD_W, FIELD_D = 1.5 * W, W
GRID_RES = 15
N_LIGHTS = 3
DISPLAY_MODE = 0
RECORD = False
RECORD_CNTR = 0


class Column(object):
    def __init__(self, x, y, z, top_radius, bottom_radius, tall, ccolor):
        self.pos = PVector(x, y, z)
        self.t_rad = top_radius
        self.b_rad = bottom_radius
        self.tall = tall
        self.color = ccolor
        self.brightness = 0

    def display(self):
        noStroke()
        h = hue(self.color)
        s = saturation(self.color)
        b = brightness(self.color)
        self.brightness += (b - self.brightness) * 0.1
        colorMode(HSB)
        fill(h, s, self.brightness)

        pushMatrix()
        translate(self.pos.x, self.pos.y, self.pos.z)

        box(BOX_SIZE, self.tall, BOX_SIZE)

        popMatrix()
        colorMode(RGB)

    def update(self):
        self.brightness = 255


class Particle(object):
    def __init__(self, x, y, z, ssize, radius):
        self.pos = PVector(x, y, z)
        self.size = ssize
        self.radius = radius


def init_lights():
    del lights[:]

    for i in range(N_LIGHTS):
        angle = random(TWO_PI)
        lights.append(PVector(cos(angle), 0.3, sin(angle)))
        brights = [150, 150, 150]
        if cp5:
            cp5.getController('light #' + str(int(i + 1))).setValue(angle)
            cp5.getController('bright #' + str(int(i + 1))).setValue(150)

def init_scene():
    del scene[:]

    n = FIELD_W / BOX_SIZE
    for i in range(-n / 2.0, n / 2.0):
        for j in range(FIELD_D / BOX_SIZE):
            if random(1) < 0.22:
                scene.append(Column(i * BOX_SIZE, -100, -j * BOX_SIZE, 20, 20,
                    random(550 - 300 * (i + n / 2.0) / n, 1500 - 700 * (i + n / 2.0) / n), choice(PALETTE)))

    del samples[:]
    samples.extend(sample(scene, min(len(scene) / 2, 50)))
    shuffle(samples)

    cp5.addMatrix('mymatrix').setGrid(GRID_RES, len(samples)).setPosition(10, 150) \
        .setSize(100, 100).setGap(1, 1).setInterval(int(1000 * DURATION / float(GRID_RES))) \
        .setMode(ControlP5.MULTIPLES).addListener(my_matrix_event)

def init_controls():
    global cp5

    cp5 = ControlP5(this)

    for i in range(N_LIGHTS):
        cp5.addSlider('light #' + str(int(i + 1))).setPosition(10, 20 + 20 * i).setSize(100, 10) \
            .setRange(0, TWO_PI).setValue(0).addListener(control_event)
        cp5.addSlider('bright #' + str(int(i + 1))).setPosition(10, 20 * (N_LIGHTS + 1) + 20 * i).setSize(100, 10) \
            .setRange(0, 255).setValue(0).addListener(control_event)

def control_event(ce):
    if ce.isFrom('light #1'):
        angle = (ce.getController().getValue())
        if lights:
            lights[0] = PVector(cos(angle), 0.3, sin(angle))
    elif ce.isFrom('light #2'):
        angle = (ce.getController().getValue())
        if lights:
            lights[1] = PVector(cos(angle), 0.3, sin(angle))
    elif ce.isFrom('light #3'):
        angle = (ce.getController().getValue())
        if lights:
            lights[2] = PVector(cos(angle), 0.3, sin(angle))
    elif ce.isFrom('bright #1'):
        br = (ce.getController().getValue())
        if brights:
            brights[0] = br
    elif ce.isFrom('bright #2'):
        br = (ce.getController().getValue())
        if brights:
            brights[1] = br
    elif ce.isFrom('bright #3'):
        br = (ce.getController().getValue())
        if brights:
            brights[2] = br

def my_matrix_event(ce):
    n_col = floor(GRID_RES * t) % GRID_RES
    cells = ce.getController().getCells()
    for i, cell in enumerate(cells[n_col]):
        if cell == 1:
            samples[i].update()

def draw_(t):
    background(BG_COLOR)

    lightFalloff(1.0, 0.001, 0.0)
    for _light, col in zip(lights, brights):
        directionalLight(col, col, col, _light.x, _light.y, _light.z)

    pushMatrix()
    rotateY(-PI / 6)
    translate(0, 0, -100)
    for obj in scene:
        obj.display()
    popMatrix()

    noLights()

def keyPressed():
    global DISPLAY_MODE
    global RECORD
    global RECORD_CNTR

    if key == '1':
        DISPLAY_MODE = 0
    elif key == '2':
        DISPLAY_MODE = 1
    elif key == ' ':
        init_lights()
    elif key == 'n':
        init_scene()
    elif key == 'a' and cp5:
        if cp5.isAutoDraw():
            cp5.setAutoDraw(False)
        else:
            cp5.setAutoDraw(True)
    elif key == 'r':
        RECORD_CNTR = 0
        RECORD = not RECORD

def setup():
    global scene
    global lights
    global brights
    global colors
    global samples
    global cp5

    size(W, H, P3D)
    frameRate(FPS)

    # cam = PeasyCam(this, 500)
    # cam.pan(width / 2, height / 2)

    brights = [0, 0, 0]
    colors = []

    cp5 = None
    init_controls()

    lights = []
    init_lights()

    samples = []
    scene = []
    init_scene()

def draw():
    global t
    global RECORD
    global RECORD_CNTR

    if not RECORD:
        t = (frameCount / float(N_FRAMES)) % 1.0
        draw_(t)
    elif N_SAMPLES <= 1:
        t = (frameCount / float(N_FRAMES)) % 1.0
        draw_(t)
        if RECORD_CNTR <= N_FRAMES:
            saveFrame('gif/####.gif')
            RECORD_CNTR += 1
        else:
            RECORD = False
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
        if RECORD_CNTR <= N_FRAMES:
            saveFrame('gif/####.gif')
            RECORD_CNTR += 1
        else:
            RECORD = False
