W = H = 480
FPS = 20.0
D = 1.0
N_FRAMES = D * FPS
ROW_NUMBER, COL_NUMBER = 160, 16
HEX_SIZE = 5
SPEED = 200.0
N_SAMPLES = 8.0
RECORD = False


def draw_(t):
    background(0)

    pushMatrix()
    beginCamera()
    camera()
    translate(W / 2, -H / 4, 3 * H / 4)
    rotateX(t)
    scale(1.5)
    endCamera()

    for i in range(ROW_NUMBER):
        rotateX(2 * PI / ROW_NUMBER)
        pushMatrix()
        translate(0, H / 2, 0)
        rotateX(PI / 2)
        for j in range(COL_NUMBER):
            if i % 2 and j == 0:
                rotateY(PI / COL_NUMBER)
            rotateY(2 * PI / float(COL_NUMBER))
            stroke(255)
            strokeWeight(1)
            fill(15)
            translate(0, 0, COL_NUMBER * HEX_SIZE / PI)
            beginShape()
            x = y = -3
            for angle in range(0, 360, 60):
                x += cos(radians(angle)) * HEX_SIZE
                y += sin(radians(angle)) * HEX_SIZE
                vertex(x, y, 0)
            endShape(CLOSE)
            translate(0, 0, -COL_NUMBER * HEX_SIZE / PI)
        popMatrix()
    popMatrix()

def setup():
    global mshader
    global hex_gen
    global center
    size(W, H, P3D)
    frameRate(FPS)

def draw():
    if not RECORD:
        t = frameCount / SPEED
        draw_(t)
    else:
        result = [[0, 0, 0] for i in range(W * H)]
        for sample in range(N_SAMPLES):
            t = (frameCount + sample / N_SAMPLES) / SPEED
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
