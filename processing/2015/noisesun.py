# http://letsgetprocessing.tumblr.com/

W = H = 500
FPS = 20.0
DURATION = 8
N_FRAMES = DURATION * FPS
N_SAMPLES = 4
MAIN_COLOR = color(201, 104, 35)
DARK_COLOR = color(111, 11, 0)
BG_COLOR = color(26, 13, 10)
MASK_COLOR = color(255)
RAD = 140
RECORD = False


def polar2cart(r,theta):
    """ polar coordinates to cartesian """
    return r * cos(theta), r * sin(theta)

def draw_(t):
    pushMatrix()
    translate(W / 2, H / 2)
    background(BG_COLOR)

    # drawing mask and filling it with noise
    stroke(MASK_COLOR)
    fill(MASK_COLOR)
    ellipse(0, 0, 2 * RAD, 2 * RAD)
    loadPixels()
    for i in range(W / 2 - RAD, W / 2 + RAD):
        for j in range(H / 2 - RAD, H / 2 + RAD):
            if pixels[i * W + j] == color(255):
                noise_v = noise((j - H / 2) * 0.02 + 100, (i - W / 2) * 0.02 + 200)
                pixels[i * W + j] = lerpColor(DARK_COLOR, MAIN_COLOR, noise_v)
    updatePixels()

    # drawing sun contour
    stroke(MAIN_COLOR)
    strokeWeight(5)
    noFill()
    ellipse(0, 0, 2 * RAD, 2 * RAD)

    # drawing sun beams
    n = 160.0
    for i in range(n):
        stroke(MAIN_COLOR)
        strokeWeight(2)
        x_noise, y_noise = polar2cart(RAD, i / n * 2 * PI)
        x1, y1 = polar2cart(RAD + 10, i / n * 2 * PI)
        noise_v = noise(x_noise * 0.02 + 100, y_noise * 0.02 + 200)
        x2, y2 = polar2cart(RAD + 10 + noise_v * 100, i / n * 2 * PI)
        line(x1, y1, x2, y2)

    # drawing noise value inside circle
    x_noise, y_noise = polar2cart(RAD, (t * n) / n * 2 * PI)
    noise_v = noise(x_noise * 0.02 + 100, y_noise * 0.02 + 200)
    fill(lerpColor(DARK_COLOR, MAIN_COLOR, noise_v))
    ellipse(x_noise, y_noise, 20, 20)

    popMatrix()

def setup():
    size(W, H)
    frameRate(FPS)

def draw():
    # drawing with SSAA when recording
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
