W = H = 480
SIZE = 180.0
IN_SIZE = 60.0
FPS = 20.0
D = 2.0
N_FRAMES = D * FPS
N_SAMPLES = 4.0
WEIGHT = 3
MINE_COLOR = color(73, 38, 36)
BLUR_COLOR = color(255, 215, 0)
BG_COLOR = color(32, 27, 27)
RECORD = False


def polar2cart(r,theta):
    return r * cos(theta), r * sin(theta)

def make_triangle(radius):
    return [polar2cart(radius, i * 2*PI/3 + PI/6) for i in range(3)]

def easing(x):
    return x ** 3

def draw_(t):
    background(BG_COLOR)
    for i in range(2):
        pushMatrix()
        noStroke()
        fill([BLUR_COLOR, MINE_COLOR][i])
        translate(width / 2, height / 2)
        rotate(PI/3 * t)
        triangle = make_triangle(SIZE / 2 + SIZE / 2 * easing(t))
        beginShape()
        for x, y in triangle:
            vertex(x, y)
        for j in range(3):
            beginContour()
            triangle = make_triangle(IN_SIZE / 2)
            xc, yc = polar2cart(SIZE / 2 * easing(t), j * 2*PI/3 + PI/6)
            triangle.reverse()
            for x, y in triangle:
                vertex(xc + x, yc + y)
            endContour()
        endShape(CLOSE)
        rotate(PI/3)
        for j in range(3):
            fill([BLUR_COLOR, MINE_COLOR][i])
            triangle = make_triangle(SIZE / 2 + SIZE / 2 * easing(t))
            xc, yc = polar2cart(SIZE / 2 + 2 * SIZE * easing(t), j * 2*PI/3 + PI/6)
            beginShape()
            for x, y in triangle:
                vertex(xc + x, yc + y)
            triangle = make_triangle(IN_SIZE / 2 + IN_SIZE / 2 * easing(t))
            triangle.reverse()
            beginContour()
            for x, y in triangle:
                vertex(xc + x, yc + y)
            endContour()
            endShape(CLOSE)
        popMatrix()
        if i == 0: filter(BLUR, 4)

def setup():
    size(W, H)
    frameRate(FPS)

def draw():
    if not RECORD:
        t = (frameCount % N_FRAMES) / N_FRAMES
        draw_(t)
    else:
        result = [[0, 0, 0] for i in range(W * H)]
        for sample in range(N_SAMPLES):
            t = ((frameCount - 1 + sample / N_SAMPLES) % N_FRAMES) / N_FRAMES
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
            
