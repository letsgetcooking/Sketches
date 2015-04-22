W = H = 480
WHITE = color(255)
RED = color(242, 100, 100)
CYAN = color(99, 255, 255)


def setup():
    global graphics
    size(W, H)
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
        graphics.append(pg)

def draw():
    background(35)
    for pg in graphics:
        image(pg, random(-2, 2), 0)
    filter(BLUR, 1)
