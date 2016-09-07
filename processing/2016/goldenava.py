W = 400
FPS = 20.0
DURATION = 4
N_FRAMES = DURATION * FPS
N_SAMPLES = 4
RECORD = False


BGCOLOR = color(237, 238, 240)
MAINCOLOR = color(35)
WRES = 5
HRES = 8
F = 1.618


def draw_(t):
    pass

def setup():
    size(W, int(W * (HRES / float(WRES))))
    frameRate(FPS)

    background(BGCOLOR)

    noStroke()
    fill(MAINCOLOR)
    rectMode(CENTER)

    s = width * height * (1 - 1 / F)
    cube_w = sqrt(s / float(WRES * HRES))
    gap = (width - cube_w * WRES) / float(WRES + 1)
    offset = (height - ((cube_w + gap) * HRES + gap)) / 2.0
    for i in range(WRES):
        for j in range(HRES):
            rect((cube_w / 2 + gap) * (i + 1) + cube_w / 2 * i, \
                (cube_w / 2 + gap) * (j + 1) + cube_w / 2 * j + offset, cube_w, cube_w)

    save("ava.png")

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
