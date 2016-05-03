from toxi.geom import Vec3D, Ray3D
from random import choice
from damkjer.ocd import Camera
from peasy import PeasyCam


W = H = 500
FPS = 20.0
DURATION = 8
N_FRAMES = DURATION * FPS
N_SAMPLES = 1
BG_COLOR = color(255)
MAIN_COLOR = color(0)
N_IMAGES = 160
RECORD = False


def draw_(t):
    background(BG_COLOR)
    strokeWeight(1)
    image(imgs[frameCount % len(imgs)], 100, 100)

    stroke(MAIN_COLOR)
    noFill()
    rect(100, 100, 300, 300)

def setup():
    global imgs

    size(W, H, P3D)
    frameRate(FPS)

    imgs = []
    for i in range(N_IMAGES):
        imgs.append(loadImage('imgs/' + nf(i + 1, 4) + '.gif'))

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
