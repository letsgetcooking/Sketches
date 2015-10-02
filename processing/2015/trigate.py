W = H = 500
FPS = 20.0
DURATION = 1
N_FRAMES = DURATION * FPS
N_SAMPLES = 8
BG_COLOR = color(0)
MAIN_COLOR = color(255)
RECORD = False


def draw_(t):
    background(BG_COLOR)
    stroke(67, 191, 212)
    strokeWeight(3)
    rectMode(CENTER)
    n = 10.0
    for i in range(n):
        fill(55, 93, 102)
        for j in range(3):
            pushMatrix()
            translate(width / 2, height / 2 + height / 5, (i - n + 1) * height + height * t)
            rotateZ(j / 3.0 * TWO_PI - PI / 6)
            rotateX(-0.005)
            translate(height - (((i - n + 1) * height + height * t) / 500.0) ** 2, 0, 0)
            rect(0, 0, height, 4 * height)
            popMatrix()
        this.flush()
        if i < n - 2:
            fill(0, 90)
        elif i < n - 1:
            fill(0, 90 * (1 - t))
        else:
            fill(0, 0)
        pushMatrix()
        translate(width / 2, height / 2 + 50, (i - n + 1.5) * height + height * t)
        rect(0, 0, 6 * width, 6 * height)
        popMatrix()
        this.flush()

def setup():
    size(W, H, P3D)
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

