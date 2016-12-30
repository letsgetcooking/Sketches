from toxi.geom import Vec2D


W = H = 500
FPS = 20.0
DURATION = 3
N_FRAMES = DURATION * FPS
N_SAMPLES = 4
RECORD = False

BG_COLOR = color(25)
MAIN_COLOR = color(0)
LEAF1_COLOR, LEAF2_COLOR = color(158, 215, 99), color(44, 158, 75)
TREE_COLOR = color(20, 140, 80)


def draw_branch(x1, y1, x2, y2, w, shadow=False):
    p1 = PVector(x1, y1)
    p2 = PVector(x2, y2)
    length = int(p1.dist(p2))
    n_leafs = int(2.5 * length)

    randomSeed(1234)

    for i in range(n_leafs):
        x = random(1) ** 2

        if not shadow:
            r = random(1)
            if r < .33:
                col = LEAF1_COLOR
            elif .33 < r < .66:
                col = LEAF2_COLOR
            else:
                col = TREE_COLOR
        else:
            col = color(10)
        
        pos1 = p2.copy()
        pos1.sub(p1)
        direction = pos1.copy()
        pos1.mult(x)
        pos1.add(p1)

        pos2 = PVector((w + random(w / 2) - (w - 1) * i / 600.0)
            * i / float(n_leafs), 0)
        pos2.rotate(PI / 3 + random(-1, 1) * PI / 8 +
            PVector.angleBetween(direction, PVector(1, 0)))
        pos2.add(pos1)

        stroke(col)
        line(pos1.x, pos1.y, pos2.x, pos2.y)
        
        pos1 = p2.copy()
        pos1.sub(p1)
        pos1.mult(x)
        pos1.add(p1)

        pos2 = PVector((w + random(w / 2) - (w - 1) * i / 600.0)
            * i / float(n_leafs), 0)
        pos2.rotate(-PI / 3 + random(-1, 1) * PI / 8 +
            PVector.angleBetween(direction, PVector(1, 0)))
        pos2.add(pos1)

        stroke(col)
        line(pos1.x, pos1.y, pos2.x, pos2.y)


def draw_star(x, y, r, verticies=[0,1,2,3,4,5,6,7,8,9], col=color(255, 225, 0)):
    noStroke()
    fill(col)
    v = Vec2D(0, -0.5 * r)
    vm = Vec2D(0, -0.2 * r)
    beginShape()
    for vert in verticies:
        if vert % 2 == 1:
            vr = v.getRotated((vert - 1) / 10.0 * TWO_PI).add(Vec2D(x, y))
        else:
            vr = vm.getRotated((vert - 1) / 10.0 * TWO_PI).add(Vec2D(x, y))
        vertex(vr.x(), vr.y())
    endShape(CLOSE)


def draw_stars(t):
    randomSeed(1234)
    strokeWeight(1.5)
    noStroke()
    fill(120)
    for i in range(5000):
        if random(1) < 0.05:
            rad = 3 * noise(2 * cos(t * TWO_PI) + i, 2 * sin(t * TWO_PI) + i) + 1
        else:
            rad = 2 * noise(2 * cos(t * TWO_PI) + i, 2 * sin(t * TWO_PI) + i)
        ellipse(width / 2 * randomGaussian() + width / 2,
            height / 2 * randomGaussian() + height / 2, rad, rad)


def draw_(t):
    background(BG_COLOR)

    pushMatrix()

    translate(width / 2 - 100, 500)
    scale(0.5, 0.4)
    shearX(-PI / 4.0)

    pushMatrix()
    translate(0, -100)

    for i in range(10):
        rotate(PI / 180.0 * sin(t * TWO_PI))
        draw_branch(0, 0, (10 - i) * 10 + 10, (10 - i) * 2, 8, shadow=True)
        draw_branch(0, 0, -(10 - i) * 10 - 10, (10 - i) * 2, 8, shadow=True)
        draw_branch(0, 0, 0, -30, 8, shadow=True)
        translate(0, -30)

    popMatrix()

    draw_branch(0, 0, 0, -100, 10, shadow=True)
    popMatrix()

    pushMatrix()
    translate(width / 2 - 100, 400)

    for i in range(10):
        rotate(PI / 180.0 * sin(t * TWO_PI))
        draw_branch(0, 0, (10 - i) * 10 + 10, (10 - i) * 2, 8, shadow=True)
        draw_branch(0, 0, -(10 - i) * 10 - 10, (10 - i) * 2, 8, shadow=True)
        draw_branch(0, 0, 0, -30, 8, shadow=True)
        translate(0, -30)

    translate(0, -15)
    draw_star(0, 0, 25)

    popMatrix()

    pushMatrix()
    translate(width / 2 - 100, 500)
    draw_branch(0, 0, 0, -100, 10, shadow=True)
    popMatrix()

    filter(BLUR, 2)

    draw_stars(t)

    pushMatrix()
    translate(width / 2 - 100, 400)

    for i in range(10):
        rotate(PI / 180.0 * sin(t * TWO_PI))
        draw_branch(0, 0, (10 - i) * 10 + 10, (10 - i) * 2, 6)
        draw_branch(0, 0, -(10 - i) * 10 - 10, (10 - i) * 2, 6)
        draw_branch(0, 0, 0, -30, 6)
        translate(0, -30)

    translate(0, -15)
    draw_star(0, 0, 25)

    popMatrix()

    pushMatrix()
    translate(width / 2 - 100, 500)
    draw_branch(0, 0, 0, -100, 8)
    popMatrix()


def setup():
    global c_x_last

    size(W, H)
    frameRate(FPS)

    c_x_last = 0

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
            saveFrame('png/####.png')
        else:
            exit()
