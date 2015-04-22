W, H = 480, 480
FPS = 20.0
RECORD = False
N_SAMPLES = 4
CW = 100
PERIOD = 3.0
N_FRAMES = FPS * PERIOD
COLOR = color(110, 255, 148)
BG_COLOR = color(35)


def draw_(t):
    background(BG_COLOR)
    pushMatrix()
    translate(width / 2, height / 2, 0)
    rotateX(-PI / 6)
    rotateY(t / 4)
    translate(-CW / 2, CW / 2, CW / 2)
    for k in range(1, 4):
        for i in range(4):
            beginShape()
            vertex(0, 0, 60 * k * constrain(sin(t), 0, 1))
            vertex(CW, 0, 60 * k * constrain(sin(t), 0, 1))
            vertex(CW, -CW, 60 * k * constrain(sin(t), 0, 1))
            vertex(0, -CW, 60 * k * constrain(sin(t), 0, 1))
            endShape(CLOSE)
            translate(CW, 0, 0)
            rotateY(PI / 2)
    popMatrix()
    filter(BLUR, 1)

def setup():
    size(W, H, P3D)
    frameRate(FPS)
    noFill()
    stroke(COLOR)
    strokeWeight(3)
    ortho()

def draw():
    if not RECORD:
        t = 2 * PI * frameCount / N_FRAMES
        draw_(t)
    else:
        result = [[0, 0, 0] for i in range(W * H)]
        for sample in range(N_SAMPLES):
            t = 2 * PI * (frameCount - 1 + sample / N_SAMPLES) / N_FRAMES
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
        if frameCount >= N_FRAMES:
            exit()
        saveFrame('png/####.png')
