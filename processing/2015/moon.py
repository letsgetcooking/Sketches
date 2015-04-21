SPEED = 8.0
FPS = 12.0
MOD = 2.0
RECORD = False
MOON_COLOR = color(100, 199, 255)
MOON_COLOR = color(255, 0, 0)
INTERLACING = False
FRAME = True
W = H = 480
MOON_W = MOON_H = 320
FRAME_W = 40


def make_noise(noise_scale, w, h):
    noiseDetail(8, 0.6)
    noise_img = createImage(w, h, RGB)
    noise_img.loadPixels()
    for x in range(w):
        for y in range(h):
            angle = 2 * MOD * PI * x / w
            a = w + w / (2 * PI) * sin(angle)
            b = 488 + w / (2 * PI) * cos(angle)
            c = 255 * noise(a * noise_scale, b * noise_scale,
                2 * y * noise_scale)
            noise_img.pixels[y * h + x] = color(c)
    noise_img.updatePixels()
    return noise_img

def make_interlace(interlace):
    interlace_img = createImage(width, height, RGB)
    interlace_img.loadPixels()
    for i in range(width):
        for j in range(height):
            interlace_img.pixels[j * width + i] = color(255 *
                (1 - constrain(sin(j / 1.5), interlace, 1) + interlace))
    interlace_img.updatePixels()
    return interlace_img

def make_frame(w):
    interlace_img = createGraphics(width, height)
    interlace_img.beginDraw()
    interlace_img.background(255)
    interlace_img.fill(0)
    interlace_img.noStroke()
    interlace_img.rect(0, 0, width, w)
    interlace_img.rect(width - w, 0, w, height)
    interlace_img.rect(0, height - w, width, w)
    interlace_img.rect(0, 0, w, height)
    interlace_img.endDraw()
    return interlace_img

def setup():
    global noise_image
    frameRate(FPS)
    size(W, H)
    if INTERLACING:
        global interlace_image
        global interlace_image_t
        interlace_image = make_interlace(-1.0)
        interlace_image_t = make_interlace(0.9)
    if FRAME:
        global frame_image
        frame_image = make_frame(FRAME_W)
    noise_image = make_noise(0.008, W, H)

def draw():
    background(35)
    noStroke()
    fill(MOON_COLOR)
    ellipse(width / 2, height / 2, MOON_W, MOON_H)
    if INTERLACING:
        blend(interlace_image, 0, 0, width, height, 0, 0, width, height, MULTIPLY)
    x_offset = int(frameCount % (SPEED * FPS / MOD) * width / FPS / SPEED)
    blend(noise_image, 0, 0, width, height, x_offset - width, 0, width, height, MULTIPLY)
    blend(noise_image, 0, 0, width, height, x_offset, 0, width, height, MULTIPLY)
    if FRAME:
        blend(frame_image, 0, 0, width, height, 0, 0, width, height, DARKEST)
    filter(BLUR, 3)
    if INTERLACING:
        blend(interlace_image_t, 0, 0, width, height, 0, 0, width, height, MULTIPLY)
    if RECORD and frameCount <= SPEED * FPS / MOD:
        saveFrame('png/####.png')
