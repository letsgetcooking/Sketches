W = H = 500
FPS = 20.0
DURATION = 4
N_FRAMES = DURATION * FPS
N_SAMPLES = 32
BG_COLOR = color(255)
MAIN_COLOR = color(155, 0, 0)
RECORD = False


def ease_in_circ(t):
    return 1 - sqrt(1 - t ** 2)

def ease_in_cubic(t):
    return t ** 3

def ease_out_circ(t):
    return sqrt(1 - (t - 1) ** 2)

def ease_out_expo(t):
    return 1 if t == 1 else -2 ** (-10 * t) + 1

def ease_in_out_cubic(t):
    t *= 2
    if t < 1:
        return 0.5 * t*t*t
    t -= 2
    return 0.5 * (t*t*t + 2)

def draw_(t):
    background(BG_COLOR)

    tt1 = ease_in_cubic(constrain(2 * t, 0, 1))
    tt2 = ease_out_circ(constrain(2 * t, 0, 1))
    tt3 = constrain(2 * t - 1, 0, 1)
    tt4 = ease_in_cubic(constrain(2 * t - 1, 0, 1))
    tt5 = ease_out_expo(constrain(2 * t, 0, 1))
    tt6 = ease_in_cubic(constrain(2 * t - 1, 0, 1))

    noFill() if t < 0.3 else fill(MAIN_COLOR)
    stroke(MAIN_COLOR)
    ellipseMode(CENTER)

    n = 15.0
    rad = 150
    erad = rad / (1 + 21 * tt1)
    r = rad * (1 + 3 * (1 - tt2))
    strokeWeight(12 + 11 * (1 - tt1))

    circles_num = max(1, int(tt6 * 10))
    for k in range(circles_num):
        offset = (k - int(circles_num / 2)) * PI / 100.0
        a = 4 * TWO_PI + offset
        x, y = r * cos(tt3 * a) + width / 2, r * sin(tt3 * a) - r * (1 - tt1) + height / 2
        ellipse(x, y, 2 * erad, 2 * erad)
        for i in range(1, int(n)):
            angle = i / n * TWO_PI * tt1 + tt3 * a
            if angle < PI / 200.0: continue
            x, y = r * cos(angle) + width / 2, r * sin(angle) - r * (1 - tt1) + height / 2
            ellipse(x, y, 2 * erad, 2 * erad)

def setup():
    size(W, H)
    frameRate(FPS)

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
