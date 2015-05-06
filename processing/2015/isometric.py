W = H = 480
FPS = 20.0
D = 3.0
N_FRAMES = D * FPS
N_SAMPLES = 4.0
TILE_W, TILE_H = 40, 20
RECORD = False


def draw_block(x, y, z, c):
    top = c
    left = color(hue(c), saturation(c), max(0, brightness(c) - 40))
    right = color(hue(c), saturation(c), max(0, brightness(c) - 20))

    # draw top
    pushMatrix()
    translate((y - x) * TILE_W / 2, (x + y) * TILE_H / 2)

    beginShape()
    fill(top)
    vertex(0, - z * TILE_H)
    vertex(TILE_W / 2, TILE_H / 2 - z * TILE_H)
    vertex(0, TILE_H - z * TILE_H)
    vertex(- TILE_W / 2, TILE_H / 2 - z * TILE_H)
    endShape(CLOSE)

    # draw left
    beginShape()
    fill(left)
    vertex(- TILE_W / 2, TILE_H / 2 - z * TILE_H)
    vertex(0, TILE_H - z * TILE_H)
    vertex(0, TILE_H)
    vertex(- TILE_W / 2, TILE_H / 2)
    endShape(CLOSE)

    # draw right
    beginShape()
    fill(right)
    vertex(TILE_W / 2, TILE_H / 2 - z * TILE_H)
    vertex(0, TILE_H - z * TILE_H)
    vertex(0, TILE_H)
    vertex(TILE_W / 2, TILE_H / 2)
    endShape(CLOSE)
    popMatrix()

def draw_(t):
    pushMatrix()
    colorMode(HSB, 100)
    background(0)
    translate(width / 2, 240)
    for k in range(2):
        for i in range(10):
            for j in range(10):
                r_color = color(56 + 4 * (sin(i / 20.0 * 2*PI + t * 2*PI)
                    + cos(j / 20.0 * 2*PI + t * 2*PI)), 100, 100)
                draw_block(i, j, 4.5 + 2 * (sin(i / 20.0 * 2*PI + t * 2*PI)
                    + cos(j / 20.0 * 2*PI + t * 2*PI)), r_color)
        if k == 0:
            filter(BLUR, 4)
    popMatrix()
    colorMode(RGB)

def setup():
    size(W, H, P2D)
    frameRate(FPS)

def draw():
    if not RECORD:
        t = frameCount / N_FRAMES
        draw_(t)
    else:
        result = [[0, 0, 0] for i in range(W * H)]
        for sample in range(N_SAMPLES):
            t = (frameCount + 0.25 * sample / N_SAMPLES) / N_FRAMES
            draw_(t)
            this.flush()
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
