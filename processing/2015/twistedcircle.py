W = H = 480
FPS = 20.0
SPEED = 6.0
BG_COLOR = color(47, 60, 47)
RECORD = False
TWIST = 8.0
TWIST_SPEED = 10.0
R = 150


def setup():
    size(W, H, P3D)
    frameRate(FPS)
    ortho()
    noFill()
    strokeWeight(7)
    colorMode(HSB, 100)

def draw():
    theta = TWIST * constrain(sin(2 * PI * (((frameCount % (SPEED * FPS)) /
        TWIST_SPEED) % FPS) / FPS + 5 * PI / 6), -1, 0)
    background(BG_COLOR)
    beginShape()
    translate(width / 2, height / 2, 0)
    for i in range(360):
        stroke(i/360.0 * 100, 100, 100)
        x = R * cos(radians(i))
        y = R * sin(radians(i))
        z = 0
        if i < 180:
            j = theta * (180 - i - 90)
        else:
            j = theta * (i - 180 - 90)
        xr = x
        yr = y * cos(radians(j)) - z * sin(radians(j))
        zr = y * sin(radians(j)) + z * cos(radians(j))
        vertex(xr, yr, zr)
    rotateY(-frameCount / FPS / SPEED * PI)
    endShape(CLOSE)
    if RECORD:
        if frameCount > 2 * SPEED * FPS:
            exit()
        else:
            saveFrame('png/####.png')
