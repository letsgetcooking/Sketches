from toxi.geom import Vec2D
from random import choice


W, H = 1000, 500
FPS = 20.0
DURATION = 4
N_FRAMES = DURATION * FPS
N_SAMPLES = 1
PPI = 91
E = round(2.5 * PPI)
MU = 1 / 3.0
SEPARATION = lambda z: round((1 - MU * z) * E / (2 - MU * z))
FAR = SEPARATION(0)
COLORS = (color(149, 31, 43), color(224, 223, 177), color(165, 163, 108),
    color(245, 244, 215), color(83, 82, 51))
RECORD = False


def make_depthmap():
    dm = createGraphics(W, H)
    dm.beginDraw()
    dm.background(0)
    dm.noStroke()
    dm.fill(120)
    dm.textFont(createFont('Impact', 324))
    dm.text('ART',250, 370)
    dm.endDraw()
    return dm

def make_background():
    grid = createGraphics(E / 2, H)
    grid.beginDraw()
    grid.background(0)
    grid.stroke(0)
    grid.strokeWeight(1.3)
    for i in range(40):
        for j in range(8):
            grid.fill(choice(COLORS))
            grid.rect(j * E / 16, i * E / 16, E / 16, E / 16)
    grid.endDraw()

    bg_strip = createGraphics(E / 2, H)
    bg_strip.loadPixels()
    grid.loadPixels()
    for i in range(H):
        for j in range(E / 2):
            index = int(i * (E / 2) +
                (j + 100 * noise(i * 0.01, j * 0.01)) % (E / 2))
            bg_strip.pixels[int(i * (E / 2) + j)] = grid.pixels[index]
    bg_strip.updatePixels()

    bg = createGraphics(W, H)
    bg.beginDraw()
    bg.background(0)
    for i in range(ceil(W / (E / 2))):
        bg.image(bg_strip, W - (i + 1) * E / 2, 0)
    bg.endDraw()
    return bg

def make_stereogram(dm, bg):
    st = createImage(W, H, RGB)
    st.loadPixels()
    dm.loadPixels()
    for i in range(H):
        same = [x for x in range(W)]
        for j in range(W):
            z_value = red(dm.pixels[i * W + j]) / 255.0
            s = SEPARATION(z_value)
            left = int(j - s / 2)
            right = int(left + s)
            if 0 <= left and right < W:
                dj = 1
                visible = True
                while True:
                    zt = z_value + 2 * (2 - MU * z_value) * dj / (MU * E)
                    visible = (dm.pixels[i * W + j - dj] / 255.0 < zt and
                        dm.pixels[i * W + j + dj] / 255.0 < zt)
                    if not visible or zt >=1: break
                    dj += 1
                if visible:
                    l = same[left]
                    while l != left and l != right:
                        if l < right:
                            left = l
                            l = same[left]
                        else:
                            same[left] = right
                            left = right
                            l = same[left]
                            right = l
                    same[left] = right
        for j in range(W - 1, -1, -1):
            if same[j] == j:
                st.pixels[i * W + j] = bg.pixels[i * W + j]
            else:
                st.pixels[i * W + j] = st.pixels[i * W + same[j]]
    st.updatePixels()
    return st

def draw_(t):
    if show_original:
        image(bg, 0, 0)
    else:
        image(pg, 0, 0)

def setup():
    global bg, pg, show_original
    size(W, H)
    frameRate(FPS)

    dm = make_depthmap()
    bg = make_background()
    pg = make_stereogram(dm, bg)

    show_original = False

def mouseClicked():
    global show_original
    show_original = not show_original

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
            pixels[i] = color(rgb[0] / N_SAMPLES, rgb[1] / N_SAMPLES, rgb[2] /
                N_SAMPLES)
        updatePixels()
        if frameCount <= N_FRAMES:
            saveFrame('gif/####.gif')
        else:
            exit()
