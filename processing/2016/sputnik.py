W = H = 500
FPS = 30.0
DURATION = 4
N_FRAMES = DURATION * FPS
N_SAMPLES = 1
BG_COLOR = color(35)
PSTROKE_COLOR = color(0, 95, 107)
PLANET_COLOR = color(0, 140, 158)
SSTROKE_COLOR = color(0, 110, 124)
SPUTNIK_COLOR = color(0, 140, 158)
BIG_R = 140.0
LITTLE_R = 26.0
RECORD = False


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

def draw_planet(t):
    r = 2 * BIG_R

    imageMode(CENTER)
    image(img, width / 2, height / 2)

    noFill()
    stroke(PSTROKE_COLOR)
    strokeWeight(10)
    ellipse(width / 2, height / 2, r, r)

def draw_sputnik(t):
    x, y = (width / 2 + (BIG_R + 2 * LITTLE_R) * sin(2 * PI * t - PI / 2),
            height / 2 + 15 * sin(2 * PI * t - PI / 2) + 15 * sin(2 * PI * t))
    r = LITTLE_R + LITTLE_R / 5 * sin(2 * PI * t)

    fill(SPUTNIK_COLOR)
    noStroke()
    ellipse(x, y, 2 * r, 2 * r)

    noFill()
    stroke(SSTROKE_COLOR)
    strokeWeight(6)
    ellipse(x, y, 2 * r, 2 * r)

def draw_(t):
    background(BG_COLOR)
    noStroke()
    # draw_stars(t)

    if t < 0.5:
        draw_planet(t)
        draw_sputnik(t)
        
    else:
        draw_sputnik(t)
        draw_planet(t)

def setup():
    global img

    size(W, H)
    frameRate(FPS)

    mp = loadImage('map.png')
    mp.loadPixels()

    img = createImage(300, 300, ARGB)
    img.loadPixels()
    noiseDetail(3, 0.5)
    noise_scale = 0.02
    for i in range(img.width):
        for j in range(img.height):
            n = noise(noise_scale * i + 123, noise_scale * j + 456)
            col = mp.pixels[min(int(n * mp.width), 39)]
            img.pixels[j * img.width + i] = col
    img.updatePixels()

    mask = createGraphics(img.width, img.height)
    mask.beginDraw()
    mask.background(0)
    mask.noStroke()
    mask.fill(255)
    mask.ellipseMode(CENTER)
    mask.ellipse(mask.width / 2, mask.height / 2, 2 * BIG_R, 2 * BIG_R)
    mask.endDraw()

    img.loadPixels()
    mask.loadPixels()
    for i, pix in enumerate(mask.pixels):
        if pix == color(0):
            img.pixels[i] = color(0, 0)
    img.updatePixels()

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
