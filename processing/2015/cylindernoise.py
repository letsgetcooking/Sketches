from random import choice


W = H = 500
FPS = 20.0
DURATION = 4
N_FRAMES = DURATION * FPS
MAIN_COLOR = color(50, 41, 54)
SECOND_COLOR = color(147, 198, 181)
BG_COLOR = color(12, 10, 20)
NOISE_SCALE = 0.05
N_SAMPLES = 4
RECORD = False


class NoisedRect:

    def __init__(self, x, y, w, h, noise_scale):
        self.x = int(x)
        self.y = int(y)
        self.width = int(w)
        self.height = int(h)

        if self.width >= self.height:
            self.direction = choice(('LEFT', 'RIGHT'))
        else:
            self.direction = choice(('UP', 'DOWN'))
        self.filling = self.make_noise(noise_scale, self.width, self.height)
        self.shift_value = 0

    def display(self):
        if self.direction in ('LEFT', 'RIGHT'):
            copy(self.filling, self.width - self.shift_value, 0, self.shift_value, self.height,
                    self.x, self.y, self.shift_value, self.height)
            copy(self.filling, 0, 0, self.width - self.shift_value, self.height,
                    self.x + self.shift_value, self.y, self.width - self.shift_value, self.height)
        else:
            copy(self.filling, 0, self.height - self.shift_value, self.width, self.shift_value,
                    self.x, self.y, self.width, self.shift_value)
            copy(self.filling, 0, 0, self.width, self.height - self.shift_value,
                    self.x, self.y + self.shift_value, self.width, self.height - self.shift_value)
        noFill()
        stroke(0)
        strokeWeight(2)
        rect(self.x, self.y, self.width, self.height)

    def make_noise(self, noise_scale, w, h):
        noiseDetail(8, 0.6)
        noise_img = createImage(w, h, RGB)
        noise_img.loadPixels()
        offset_x, offset_y, offset_z = 10 * random(10), 10 * random(10) + 100, 10 * random(10) + 200
        is_noise_vertical = True if h > w else False
        for x in range(w):
            for y in range(h):
                if is_noise_vertical:
                    x, y = y, x
                    w, h = h, w
                angle = TWO_PI * x / float(w)
                a = w / TWO_PI * sin(angle)
                b = w / TWO_PI * cos(angle)
                noize_v = noise(a * noise_scale + offset_x, b * noise_scale + offset_y,
                    y * noise_scale + offset_z)
                if is_noise_vertical:
                    x, y = y, x
                    w, h = h, w
                noise_img.pixels[y * w + x] = lerpColor(MAIN_COLOR, SECOND_COLOR, noize_v)
        noise_img.updatePixels()
        return noise_img

    def shift(self, amt):
        if self.direction == 'RIGHT':
            self.shift_value = int(self.width * amt)
        elif self.direction == 'DOWN':
            self.shift_value = int(self.height * amt)
        elif self.direction == 'LEFT':
            self.shift_value = int(self.width * (1 - amt))
        elif self.direction == 'UP':
            self.shift_value = int(self.height * (1 - amt))

def make_rectangle(x, y, w, h, min_side, rectangles):
    random_value = random(1)
    if w >= h and w > 2 * min_side and random_value > 0.2 + 0.2 * min_side / float(w):
        left_w = min_side + random(w - 2 * min_side)
        right_w = w - left_w
        make_rectangle(x, y, left_w, h, min_side, rectangles)
        make_rectangle(x + left_w, y, right_w, h, min_side, rectangles)
    elif w < h and h > 2 * min_side and random_value > 0.2 + 0.2 * min_side / float(h):
        left_h = min_side + random(h - 2 * min_side)
        right_h = h - left_h
        make_rectangle(x, y, w, left_h, min_side, rectangles)
        make_rectangle(x, y + left_h, w, right_h, min_side, rectangles)
    else:
        rectangles.append(NoisedRect(x, y, w, h, NOISE_SCALE))

def draw_(t):
    background(BG_COLOR)
    noStroke()
    fill(SECOND_COLOR)
    rect(110 - 4, 110 - 4, 280 + 8, 280 + 8)
    for rectangle in rectangles:
        rectangle.shift(t)
        rectangle.display()

def setup():
    global rectangles
    size(W, H)
    frameRate(FPS)
    rectangles = []
    make_rectangle(110, 110, 280, 280, 30, rectangles)

def draw():
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
