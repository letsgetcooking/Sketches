W = H = 500
FPS = 20.0
DURATION = 4
N_FRAMES = DURATION * FPS
N_SAMPLES = 8
N_PARTICLES = 10000
RECORD = False


def draw_(t):
    global angle
    pushMatrix()
    background(54, 70, 93)
    noStroke()
    strokeWeight(15)
    translate(W / 2, H / 2)
    for i, particle in enumerate(particles):
        x, y, z = particle
        z -= t * 2500
        if -W / 6 < x < W / 6 and -H / 6 < y < H / 6:
            z = constrain(z, 100, 1000)
        if t < 0.5:
            stroke(lerpColor(color(54, 70, 93), color(255), constrain((100 + z) / 100.0, 0, 1)))
            pushMatrix()
            translate(x, y, z)
            point(0, 0, 0)
            popMatrix()
        elif t < 0.75:
            pushMatrix()
            if z == 100:
                rotateZ(-PI / 3 * ((t - 1.5) ** 3 + 1))
            stroke(lerpColor(color(54, 70, 93), color(255), constrain((100 + z) / 100.0, 0, 1)
                * (1 - constrain(8 * t - 7 + i / float(N_PARTICLES), 0, 1))))
            translate(x, y, z)
            point(0, 0, 0)
            popMatrix()
        else:
            pushMatrix()
            stroke(lerpColor(color(54, 70, 93), color(255), constrain((100 + z) / 100.0, 0, 1)
                * (1 - constrain(8 * t - 7 + i / float(N_PARTICLES), 0, 1))))
            if z == 100:
                if 7000 < i < 9000 and t > 0.77:
                    x *= 1 + sqrt(1 - (constrain(5 * (t - 0.77), 0, 1) - 1) ** 2) + i / float(N_PARTICLES)
                    y *= 1 + sqrt(1 - (constrain(5 * (t - 0.77), 0, 1) - 1) ** 2) + i / float(N_PARTICLES)
                else:
                    time = (t - 0.74) * 26
                    angle = -PI / 3 * (cos(2 * PI * (time ** 2.3)) / (time ** 5))
                    rotateZ(angle)
                translate(x, y, z)
                point(0, 0, 0)
            else:
                if z == 100:
                    rotateZ(-PI / 6 * 4 * (t - 0.5))
                translate(x, y, z)
                point(0, 0, 0)
            popMatrix()
    popMatrix()

def setup():
    global particles
    global angle
    size(W, H, P3D)
    frameRate(FPS)

    angle = PI / 3

    particles = []
    for i in range(N_PARTICLES):
        particles.append([randomGaussian() * W / 4,
            randomGaussian() * H / 4, (randomGaussian() + 1) * 200 + 800])

def draw():
    if not RECORD:
        t = (frameCount / float(N_FRAMES)) % 1.0
        draw_(t)
    else:
        result = [[0, 0, 0] for i in range(W * H)]
        for sample in range(N_SAMPLES):
            t = (frameCount + 0.1 * sample / float(N_SAMPLES)) / N_FRAMES
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
