from toxi.color import ColorGradient, TColor, ToneMap


W = H = 500
FPS = 30.0
DURATION = 1
N_FRAMES = DURATION * FPS
N_SAMPLES = 4
BG_COLOR = color(17, 14, 15)
PALETTE = [TColor.newHex('EFAC41'), TColor.newHex('DE8531'), TColor.newHex('B32900'),
            TColor.newHex('6C1305'), TColor.newHex('330A04'), TColor.newHex('EFAC41')]
BG_FRAME_COLOR = color(5, 1, 2)
FRAME_COLOR = color(35, 29, 30)
RECORD = False


def draw_frame():
    a = 50
    w = 5

    fill(BG_FRAME_COLOR)
    noStroke()
    beginShape()
    vertex(0, 0)
    vertex(width, 0)
    vertex(width, height)
    vertex(0, height)
    beginContour()
    vertex(a, a)
    vertex(a, height - a)
    vertex(width - a, height - a)
    vertex(width - a, a)
    endContour()
    endShape(CLOSE)

    fill(FRAME_COLOR)
    stroke(0)
    strokeWeight(2)
    beginShape()
    vertex(a - w, a - w)
    vertex(width - a + w, a - w)
    vertex(width - a + w, height - a + w)
    vertex(a - w, height - a + w)
    beginContour()
    vertex(a, a)
    vertex(a, height - a)
    vertex(width - a, height - a)
    vertex(width - a, a)
    endContour()
    endShape(CLOSE)

def draw_(t):
    background(BG_COLOR)
    noStroke()

    n = 32.0
    m = 12.0
    k = 10.0
    for i in range(n):
        for j in range(k):
            a = sqrt(i / n)
            c = tmap.getToneFor((j / k - t + a) % 1)
            fill(255 * c.red(), 255 * c.green(), 255 * c.blue())
            r = 60 + j * m
            x, y = r * cos(i / n * TWO_PI) + width / 2, r * sin(i / n * TWO_PI) + height / 2
            ellipse(x, y, 8, 8)
    draw_frame()

def setup():
    global tmap

    size(W, H)
    frameRate(FPS)

    gradient = ColorGradient()
    for i, tcolor in enumerate(PALETTE):
        gradient.addColorAt(255 * i / float(len(PALETTE)), tcolor)

    tmap = ToneMap(0, 1, gradient)

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
