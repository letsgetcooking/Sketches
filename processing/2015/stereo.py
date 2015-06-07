from toxi.geom import Vec2D


W, H = 1000, 500
FPS = 20.0
DURATION = 1
N_FRAMES = DURATION * FPS
N_SAMPLES = 1
N_STRIPS = 8

BANDW = W / (N_STRIPS + 1)
DEPTH_FACTOR = 20
COLORS = [color(106, 74, 60), color(204, 51, 63),
            color(235, 104, 65), color(237, 201, 81)]
RECORD = False


def draw_(t):
    pass

def setup():
    size(W, H)
    frameRate(FPS)

    pg = createGraphics(BANDW, H)
    pg.beginDraw()
    pg.noFill()
    pg.background(0)
    pg.stroke(255, 251, 0)
    pg.ellipseMode(CENTER)
    ellipses = []
    ellipse_rad = 16
    for i in range(2000):
        new_ellipse = Vec2D(random(BANDW), random(H))
        for _ellipse, _left, _right in ellipses:
            if (new_ellipse.distanceTo(_ellipse) < ellipse_rad or
                new_ellipse.distanceTo(_left) < ellipse_rad or
                new_ellipse.distanceTo(_right) < ellipse_rad): break
        else:
            new_left = Vec2D(new_ellipse.x() - BANDW, new_ellipse.y())
            new_right = Vec2D(new_ellipse.x() + BANDW, new_ellipse.y())
            ellipses.append((new_ellipse, new_left, new_right))
    for triple in ellipses:
        angle = random(2 * PI)
        for _ellipse in triple:
            pg.pushMatrix()
            pg.translate(_ellipse.x(), _ellipse.y())
            pg.rotate(angle)
            pg.ellipse(0, 0, ellipse_rad, ellipse_rad)
            pg.line(0, -ellipse_rad / 2, 0, ellipse_rad / 2)
            pg.line(0, 0, -ellipse_rad / 3, ellipse_rad / 3)
            pg.line(0, 0, ellipse_rad / 3, ellipse_rad / 3)
            pg.popMatrix()
    pg.endDraw()

    depth_mask = createGraphics(N_STRIPS * BANDW, H)
    depth_mask.beginDraw()
    depth_mask.background(0)
    depth_mask.stroke(200)
    depth_mask.strokeWeight(35)
    depth_mask.noFill()
    depth_mask.ellipseMode(CENTER)
    depth_mask.ellipse(W / 2, H / 2, 300, 300)
    depth_mask.translate(W / 2, H / 2)
    depth_mask.line(0, -150, 0, 150)
    depth_mask.line(0, 0, -100, 100)
    depth_mask.line(0, 0, 100, 100)
    depth_mask.endDraw()

    background(0)
    # image(depth_mask, 0, 0)
    image(pg, 0, 0)

    max_a = 0
    loadPixels()
    depth_mask.loadPixels()
    for i in range(H):
        for j in range(N_STRIPS * BANDW):
            displace = red(depth_mask.pixels[i * N_STRIPS * BANDW + j]) / 255.0 * DEPTH_FACTOR
            index = int(j + displace)
            pixels[i * W + j + BANDW] = pixels[i * W + index]
    updatePixels()

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
            saveFrame('gif/####.png')
        else:
            exit()
