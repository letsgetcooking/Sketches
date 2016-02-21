W = H = 500
FPS = 30.0
DURATION = 4
N_FRAMES = DURATION * FPS
N_SAMPLES = 4
BG_COLOR = color(180)
MAIN_COLOR = color(0)
RECORD = False


def ease_in_out_cubic(t):
    t *= 2
    if t < 1:
        return 0.5 * t*t*t
    t -= 2
    return 0.5 * (t*t*t + 2)

def draw_triangle(x, y, r, a):
    beginShape()
    for i in range(3):
        angle = i / 3.0 * TWO_PI + TWO_PI / 6.0 + a
        tx, ty = r * sin(angle) + x, r * cos(angle) + y
        vertex(tx, ty)
    endShape(CLOSE)

def draw_(t):
    background(BG_COLOR)

    fill(35, 150)
    noStroke()
    for i in range(5):
        draw_triangle(width / 2 + (i - 2) * 43 * ease_in_out_cubic(constrain(4 * t, 0, 1))
            - (i - 2) * 43 * ease_in_out_cubic(constrain(4 * t - 3, 0, 1)),
            height / 2, 100, 0)

    noFill()
    stroke(65)
    strokeWeight(5)
    for i in range(10):
        arc(i * 30 + 115, 320, 30, 30,
            PI * (1 - constrain(10 * ease_in_out_cubic(constrain(4 * t - 1, 0, 1)) - i, 0, 1)),
            PI * (1 - constrain(10 * ease_in_out_cubic(constrain(4 * t - 2, 0, 1)) - i, 0, 1)))

def setup():
    global drops

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
