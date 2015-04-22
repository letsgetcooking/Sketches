# Adds camera effect to arbitrary image set

W = H = 480
FPS = 20.0
WHITE = color(255)
RED = color(242, 100, 100)
CYAN = color(99, 255, 255)
RECORD = False
N_FRAMES = 60


def setup():
    global graphics
    global images
    size(W, H)
    frameRate(FPS)
    graphics = []
    for c in [RED, CYAN, WHITE]:
        pg = createGraphics(W, H)
        pg.beginDraw()
        pg.noFill()
        pg.stroke(c)
        pg.strokeWeight(2)
        for i in range(4):
            pg.line(40, 40, 80, 40)
            pg.line(40, 40, 40, 80)
            pg.translate(width, 0)
            pg.rotate(PI / 2.0)
        pg.strokeWeight(1)
        pg.line(pg.width / 2, pg.height / 2 - 20, pg.width / 2, pg.height / 2 + 20)
        pg.line(pg.width / 2 - 20, pg.height / 2, pg.width / 2 + 20, pg.height / 2)
        pg.text('REC', 380, 80)
        pg.noStroke()
        if c == WHITE:
            pg.fill(255, 0, 0)
        elif c == RED:
            pg.fill(c)
        else:
            pg.noFill()
        pg.ellipse(365, 75, 10, 10)
        pg.endDraw()
        pg.filter(BLUR, 1)
        graphics.append(pg)
    images = []
    for i in range(1, N_FRAMES+1):
        images.append(loadImage('images/%s.png' % nf(i, 4)))

def draw():
    index = (frameCount - 1) % N_FRAMES
    image(images[index], 0, 0)
    for pg in graphics:
        image(pg, random(-2, 2), 0)
    if RECORD:
        if frameCount <= N_FRAMES:
            saveFrame('png/####.png')
        else:
            exit()
