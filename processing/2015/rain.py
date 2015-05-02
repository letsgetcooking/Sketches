import random


W = H = 480
FPS = 20.0
D = 4.0
N_FRAMES = D * FPS
N_SAMPLES = 8.0
DROPS_N = 40
BLUR_COLOR = color(133, 236, 92)
BG_COLOR = color(15, 22, 14)
MAIN_COLOR = color(41, 31, 25)
SQUARE_X, SQUARE_Y = 120, 120
SQUARE_SIZE = 240
BORDER_X, BORDER_Y = SQUARE_X + 40, SQUARE_X + SQUARE_SIZE - 40
GAP, X, Y, LENGTH = 0, 1, 2, 3
RECORD = False


def draw_(step):
    background(BG_COLOR)
    for i in range(2):
        noStroke()
        fill([BLUR_COLOR, MAIN_COLOR][i])
        beginShape()
        vertex(SQUARE_X, SQUARE_Y)
        vertex(SQUARE_X + SQUARE_SIZE, SQUARE_Y)
        vertex(SQUARE_X + SQUARE_SIZE, SQUARE_Y + SQUARE_SIZE)
        vertex(SQUARE_X, SQUARE_Y + SQUARE_SIZE)
        for di, drop in enumerate(drops):
            drop_y = (drop[Y] + step * H / N_FRAMES) % H
            beginContour()
            vertex(drop[X] - drop[GAP], drop_y)
            vertex(drop[X] - drop[GAP], drop_y + drop[LENGTH])
            vertex(drop[X] + drop[GAP], drop_y + drop[LENGTH])
            vertex(drop[X] + drop[GAP], drop_y)
            endContour()
            if drop_y + drop[LENGTH] > H:
                beginContour()
                vertex(drop[X] - drop[GAP], 0)
                vertex(drop[X] - drop[GAP], drop_y + drop[LENGTH] - H)
                vertex(drop[X] + drop[GAP], drop_y + drop[LENGTH] - H)
                vertex(drop[X] + drop[GAP], 0)
                endContour()
            drops[di][Y] = drop_y
        endShape(CLOSE)
        if i == 0: filter(BLUR, 6)

def setup():
    global drops
    size(W, H)
    frameRate(FPS)
    drops = []
    for i in range(DROPS_N):
        gap = 1
        length = random.randint(20, 200)
        x = random.randint(i * W / DROPS_N, (i + 1) * W / DROPS_N)
        y = random.randint(0, H)
        drops.append([gap, x, y, length])

def draw():
    if not RECORD:
        step = 1
        draw_(step)
    else:
        result = [[0, 0, 0] for i in range(W * H)]
        for sample in range(N_SAMPLES):
            step = 1 / N_SAMPLES
            draw_(step)
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
            saveFrame('png/####.png')
        else:
            exit()
