from toxi.color import ColorGradient, TColor


W = H = 500
FPS = 20.0
DURATION = 5
N_FRAMES = DURATION * FPS
N_SAMPLES = 4
BG_COLOR = color(255)
MAIN_COLOR = color(100, 200, 200)
RECORD = False


COLORS = [(210, 210, 210), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255)]
PALETTE = [(r / 255.0, g / 255.0, b / 255.0) for r, g, b in COLORS]


def draw_line(x1, y1, x2, y2, w, t):
    noStroke()
    length = int(sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2))
    k = 30.0
    grad = ColorGradient()
    for i, col in enumerate(PALETTE):
        grad.addColorAt(i / float(len(PALETTE)) * length, TColor.newRGB(*col))
    colors = grad.calcGradient(0, length)
    for i in range(length):
        fill(colors.get(int((i + t * length) % length)).toARGB())
        ft = (1 - ((constrain(i / k, 0, 1) - 1) ** 8)) * \
            (1 - (constrain((i - length + k) / k, 0, 1) ** 8))
        x = x1 + (x2 - x1) * i / float(length)
        y = y1 + (y2 - y1) * i / float(length)
        ft = 1
        ellipse(x, y, w * ft, w * ft)

def ease_in_out_cubic(t):
    t *= 2
    if t < 1:
        return 0.5 * t ** 3
    t -= 2
    return 0.5 * (t ** 3 + 2)

def draw_(t):
    background(BG_COLOR)
    strokeCap(SQUARE)

    m = 32
    n = 1800.0
    rads = [180 * ease_in_out_cubic(i / 15.0) for i in range(15)]

    fill(50)
    stroke(50)
    ellipse(width / 2, height / 2, 360, 360)
    filter(BLUR, 4)
    fill(BG_COLOR)
    stroke(BG_COLOR)
    ellipse(width / 2, height / 2, 360, 360)

    for i in range(len(rads) - 1):
        w = 0.2 + i / float(len(rads)) * 1.8
        r1, r2 = rads[i], rads[i+1]
        for j in range(int(n)):
            angle = j / n * TWO_PI
            x1, y1 = r1 * sin(angle) + width / 2, r1 * cos(angle) + height / 2
            x2, y2 = r2 * sin(angle) + width / 2, r2 * cos(angle) + height / 2
            if ceil(((j / n + 8 * (len(rads) - i) / float(len(rads)) * (1 - cos(t * PI) ** 8) / float(m)) % 1) * m) % 2:
                draw_line(x1, y1, x2, y2, w, 0)
            else:
                stroke(0)
                strokeWeight(w)
                line(x1, y1, x2, y2)

    stroke(180)
    noFill()
    for i, r in enumerate(rads):
        strokeWeight(0.5 + 1.5 * (1 - (2 * i / float(len(rads)) - 1) ** 2))
        ellipse(width / 2, height / 2, 2 * r, 2 * r)

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
            t = (frameCount + 0.5 * sample / float(N_SAMPLES)) / N_FRAMES
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
