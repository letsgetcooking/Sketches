W = H = 480
FPS = 20.0
DURATION = 5
N_FRAMES = DURATION * FPS
N_SAMPLES = 8
WD = HD = 5
DD = 5
SIZE = 50
SPEED = 5
BG_COLOR = color(35)
RECORD = False


def draw_(t):
    background(BG_COLOR)
    fill(0)
    stroke(160)

    # camera
    beginCamera()
    camera()
    translate(0, -constrain(2 * (t - 0.5), 0, 1) * (H - H / (DD + 1)), (height / 2.0) / tan(PI*30.0 / 180.0) +
        constrain(2 * t, 0, 1) * (H - H / (DD + 1)) - 2 * H / (DD + 1))
    endCamera()

    # main environment
    pushMatrix()
    translate(0, 0, H)

    for m in range(2):
        for n in range(3):
            for i in range(1, (WD + 1)):
                for j in range(1, (HD + 1)):
                    for k in range(1, (DD + 1)):
                        if (i != WD / 2 + 1) or (j != HD / 2 + 1):
                            pushMatrix()
                            translate(i * W / (WD + 1), j * H / (HD + 1), -k * H / (DD + 1))
                            box(SIZE)
                            popMatrix()
            if n == 0:
                translate(0, 0, -H + H / (DD + 1))
            elif n == 1:
                translate(0, 0, -H)
        translate(0, H - H / (DD + 1), H)
    popMatrix()

    # cube ahead

    pushMatrix()
    translate(W / 2, H / 2 + constrain(2 * (t - 0.5), 0, 0.2) * (H - H / (DD + 1)),
        constrain(2 * t, 0, 1) * (H - H / (DD + 1)) - H - 0.5 * H / (DD + 1) - (H - H / (DD + 1)))
    box(SIZE)
    popMatrix()

    if t > 0.5:
        for (tlim, dlim) in [(0.3, 0.4), (0.5, 0.8), (0.8, 1.3), (1.0, 2.0)]:
            pushMatrix()
            translate(W / 2, H / 2 + constrain(2 * (t - 0.5), 0, tlim) * (H - H / (DD + 1)),
                - H - 0.5 * H / (DD + 1) - dlim * (H - H / (DD + 1)))
            box(SIZE)
            popMatrix()

    this.flush()

    # fading screens
    translate(0, H - H / (DD + 1), -2 * H + 1.5 * H / (DD + 1))

    for i in range(2):
        alpha = 150
        c = color(35)
        fill(c, alpha)
        beginShape()
        vertex(-(1-i)*W, 0, 0)
        vertex(2*(1-i)*W + W, 0, 0)
        vertex(2*(1-i)*W + W, 2*(1-i)*H + H, 0)
        vertex(-(1-i)*W, 2*(1-i)*H + H, 0)
        endShape(CLOSE)
        translate(0, -(H - H / (DD + 1)), H - H / (DD + 1))

def setup():
    size(W, H, P3D)
    frameRate(FPS)
    strokeWeight(1)

def draw():
    this.flush()
    if not RECORD:
        t = (frameCount / float(N_FRAMES)) % 1.0
        draw_(t)
    else:
        result = [[0, 0, 0] for i in range(W * H)]
        for sample in range(N_SAMPLES):
            t = (frameCount + 0.25 * sample / float(N_SAMPLES)) / N_FRAMES
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
