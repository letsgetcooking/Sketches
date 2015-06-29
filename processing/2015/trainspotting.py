W = H = 500
FPS = 20.0
DURATION = 10
N_FRAMES = DURATION * FPS
N_SAMPLES = 1
N_GRAINS = 10
RECORD = False

FUNCTIONS = [
    lambda t: cos(t * PI) * sin(0.5 * t * PI) * cos(10 * t * PI),
    lambda t: cos(2 * t * PI) * sin(5 * t * PI) * cos(7 * t * PI),
    lambda t: cos(5 * t * PI) * sin(8 * t * PI) * cos(0.2 * t * PI),
    lambda t: cos(2 * t * PI) * sin(6 * t * PI) * cos(3 * t * PI),
    lambda t: cos(t * PI) * sin(5 * t * PI) * cos(5 * t * PI)
]
WEIGHTS = [25, 4, 6, 2, 10]
LIGHT = [(0.15, 0.16), (0.17, 0.2), (0.355, 0.36), (0.365, 0.37), (0.375, 0.38),
    (0.4, 0.405), (0.415, 0.42), (0.45, 0.48), (0.53, 0.54), (0.55, 0.56), (0.57, 0.58), (0.6, 1.25)]

def draw_(t):
    global FUNCTIONS_TMP, WEIGHTS_TMP
    global grain_ctr
    if t < 0.01:
        FUNCTIONS_TMP, WEIGHTS_TMP = FUNCTIONS[:], WEIGHTS[:]

    lines_black = createGraphics(W, H)
    lines_black.beginDraw()
    lines_black.background(0)
    lines_black.stroke(255)

    lines_grey = createGraphics(W, H)
    lines_grey.beginDraw()
    lines_grey.background(15)
    lines_grey.stroke(0)

    for w, f in zip(WEIGHTS_TMP, FUNCTIONS_TMP):
        lines_black.strokeWeight(w)
        lines_grey.strokeWeight(w)
        x = 1.2 * W * f(1.25 * t) * (1.25 * t + 0.8) / 2 + 2 * W / 3 * constrain(10 * 1.25 * t, 0, 1) - W / 10
        lines_black.line(x, 0, x, H)
        lines_grey.line(x, 0, x, H)
        if -W / 10 > x or x > W + 30:
            WEIGHTS_TMP.remove(w)
            FUNCTIONS_TMP.remove(f)

    lines_black.endDraw()
    lines_grey.endDraw()

    image(text_bg, 0, 0)

    blend(lines_black, 0, 0, W, H, 0, 0, W, H, MULTIPLY)
    blend(lines_grey, 0, 0, W, H, 0, 0, W, H, LIGHTEST)

    for low, high in LIGHT:
        if low < 1.25 * t < high:
            blend(text_fg, 0, 0, W, H, 0, 0, W, H, ADD)

    loadPixels()
    if len(FUNCTIONS_TMP) <= 1:
        fill(0)
        if len(FUNCTIONS_TMP) == 1:
            w = 1.2 * W * FUNCTIONS_TMP[0](1.25 * t) * (1.25 * t + 0.8) / 2 + 2 * W / 3 * constrain(10 * 1.25 * t, 0, 1) - W / 10
        else:
            w = W
        w = constrain(w, 0, W)
        for i in range(H):
            for j in range(w):
                c = pixels[i * W + j]
                if brightness(c) > 100:
                    stroke(255)
                    line(j, i, constrain(j + 20 * (1 - constrain(8 * (1.25 * t - 0.9), 0, 1)), 0, w), i)
    filter(BLUR, 2)

    for low, high in LIGHT:
        if low < 1.25 * t < high:
            blend(text_fg, 0, 0, W, H, 0, 0, W, H, ADD)

    tint(255, 40)
    if not frameCount % 3:
        image(grain[grain_ctr], 0, 0)
        grain_ctr = (grain_ctr + 1) % len(grain)
    tint(255, 255)

def setup():
    global text_bg
    global text_fg
    global grain
    global grain_ctr
    size(W, H)
    frameRate(FPS)

    text_bg = createGraphics(W, H)
    text_bg.beginDraw()
    text_bg.background(255)
    text_bg.fill(0)
    font = createFont('Franklin Gothic', 48)
    text_bg.textFont(font)
    text_bg.text('TRAINSPOTTING', W / 3, 7 * H / 12)
    text_bg.filter(BLUR, 1)
    text_bg.endDraw()

    text_fg = createGraphics(W, H)
    text_fg.beginDraw()
    font = createFont('Franklin Gothic', 48)
    text_fg.textFont(font)
    text_fg.text('TRAINSPOTTING', W / 3, 7 * H / 12)
    text_fg.filter(BLUR, 1)
    text_fg.endDraw()

    grain_ctr = 0
    grain = []
    for i in range(N_GRAINS):
        grain.append(loadImage('grain/grain%i.png' % (i + 1)))

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
