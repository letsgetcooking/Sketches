W = H = 500
FPS = 20.0
DURATION = 1
N_FRAMES = DURATION * FPS
N_SAMPLES = 8
RECORD = False

BG_COLOR = color(53,44,73)
MAIN_COLOR = color(94,145,161)
PALETTE = [color(165,32,95), color(33,146,145), color(249,160,75), color(251,212,130)]

WIDTH = 200
HEIGHT = 50


def draw_(t):
    background(BG_COLOR)

    noStroke()
    for i, p in enumerate(points):
        fill(PALETTE[i % len(PALETTE)])
        r = 150
        a = p.x / float(WIDTH) * TWO_PI
        x, y = r * cos(a) + width / 2, r * sin(a) + height / 2

        for j in range(18):
            pushMatrix()
            translate(x, y, -p.y * 5 + (HEIGHT * 5) * (t - j) + 220)
            rotateY(HALF_PI)
            rotateX(-atan2(y - height / 2, x - width / 2) + PI)
            ellipse(0, 0, 22, 22)
            popMatrix()

def setup():
    global points

    size(W, H, P3D)
    frameRate(FPS)

    r = 6
    k = 30
    w = r / sqrt(2)
    grid = []
    active = []

    # STEP 0
    cols = floor(WIDTH / w)
    rows = floor(HEIGHT / w)
    for i in range(cols * rows):
        grid.append(())

    # STEP 1
    x = random(WIDTH)    
    y = random(HEIGHT)
    i = floor(x / w)
    j = floor(y / w)
    pos = PVector(x, y)
    grid[int(i + j * cols)] = pos
    active.append(pos)

    # STEP 2
    while active:
        randi = floor(random(len(active)))
        pos = active[randi]
        found = False

        for n in range(k):
            sample = PVector.random2D()
            m = random(r, 2 * r)
            sample.setMag(m)
            sample.add(pos)

            if 0 <= sample.x < WIDTH - 1 and 0 <= sample.y < HEIGHT - 1:
                col = floor(sample.x / w)
                row = floor(sample.y / w)
                ok = True
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        di = col + i
                        dj = row + j
                        index = int(di + dj * cols)
                        if index >= len(grid):
                            continue
                        neighbor = grid[index]
                        if neighbor:
                            d = PVector.dist(sample, neighbor)
                            if d < r:
                                ok = False
                index = int(col + row * cols)
                if ok and index < len(grid):
                    found = True
                    grid[index] = sample
                    active.append(sample)
            
        if not found:
            active.pop(randi)

    points = []
    for cell in grid:
        if cell:
            points.append(cell)

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
