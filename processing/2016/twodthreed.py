from toxi.geom import Vec2D, Ray2D, Line2D


W = H = 500
FPS = 20.0
DURATION = 6
N_FRAMES = DURATION * FPS
N_SAMPLES = 8
SHAPE_SIZE = 800.0
SHADOW_COLOR = color(15)
BG_COLOR = color(35)
RECORD = False


PALETTE = [color(17,100,77), color(160,176,70), color(242,201,78),
    color(247,129,69), color(242,78,78), color(242,78,138)]
PALETTE = PALETTE[::-1]


class Cube(object):
    def __init__(self, size):
        d = 10
        self.px = [-d,  d,  d, -d, -d,  d,  d, -d]
        self.py = [-d, -d,  d,  d, -d, -d,  d,  d]
        self.pz = [-d, -d, -d, -d,  d,  d,  d,  d]
         
        self.p2x = [0, 0, 0, 0, 0, 0, 0, 0]
        self.p2y = [0, 0, 0, 0, 0, 0, 0, 0]
        self.distances = [0, 0, 0, 0, 0, 0, 0, 0]

        self.size = size

    def display(self, bg=False):
        faces = self.get_faces()
        for face in sorted(faces, key=lambda f: min([self.distances[i] for i in f])):
            if not bg:
                fill(PALETTE[faces.index(face)])
            else:
                fill(SHADOW_COLOR)
            beginShape()
            for i in face:
                vertex(self.p2x[i], self.p2y[i])
            endShape(CLOSE)

    def display_face(self, index, bg=False):
        faces = self.get_faces()
        face = sorted(faces, key=lambda f: max([self.distances[i] for i in f]),
            reverse=True)[index]
        if not bg:
            fill(PALETTE[faces.index(face)])
        else:
            fill(SHADOW_COLOR)
        beginShape()
        for i in face:
            vertex(self.p2x[i], self.p2y[i])
        endShape(CLOSE)

    def get_faces(self):
        return [(0, 1, 2, 3), (1, 5, 6, 2), (5, 4, 7, 6), (4, 0, 3, 7), (2, 6, 7, 3), (1, 5, 4, 0)]

    def update(self, t):
        r = [0, 0, 0]
        r[0] = r[0] + TWO_PI * t
        r[1] = r[1] + TWO_PI * t
        r[2] = r[2] + TWO_PI * t

        if r[0] >= 360.0 * PI / 180.0: r[0] = 0
        if r[1] >= 360.0 * PI / 180.0: r[1] = 0
        if r[2] >= 360.0 * PI / 180.0: r[2] = 0

        for i in range(8):
            px2 = self.px[i]
            py2 = cos(r[0]) * self.py[i] - sin(r[0]) * self.pz[i]
            pz2 = sin(r[0]) * self.py[i] + cos(r[0]) * self.pz[i]

            px3 = cos(r[1]) * px2 + sin(r[1]) * pz2
            py3 = py2
            pz3 = -sin(r[1]) * px2 + cos(r[1]) * pz2

            ax = cos(r[2]) * px3 - sin(r[2]) * py3
            ay = sin(r[2]) * px3 + cos(r[2]) * py3
            az = pz3 - 150

            self.p2x[i] = width / 2 + ax * self.size / az
            self.p2y[i] = height / 2 + ay * self.size / az
            self.distances[i] = pz3


def ease_in_out_cubic(t):
    t *= 2
    if t < 1:
        return 0.5 * t * t * t
    t -= 2
    return 0.5 * (t * t * t + 2)


def draw_(t):
    background(BG_COLOR)

    ttttt = (constrain(8 * t / 2.0, 0, 1) - 1) ** 2
    tt = 1 - constrain(8 * t - 2, 0, 1) ** 2
    ttt = constrain(8 * t - 3, 0, 4) / 4.0
    tttt = constrain((8 * t - 6.5) / 1.5, 0, 1) ** 2

    cube.update((ttt + 0.42) % 1)

    pushMatrix()
    translate(5 + 340 * tttt - 400 * ttttt, 0)
    if 0 < ttt < 1:
        cube.display(bg=True)
    else:
        pushMatrix()
        translate(-55 * tt, 0)
        cube.display_face(0, bg=True)
        popMatrix()

        pushMatrix()
        translate(0, -50 * tt)
        cube.display_face(1, bg=True)
        popMatrix()
        
        pushMatrix()
        translate(50 * tt, 15 * tt)
        cube.display_face(2, bg=True)
        popMatrix()
    popMatrix()

    filter(BLUR, 4)

    pushMatrix()
    translate(5 + 340 * tttt - 400 * ttttt, 0)
    if 0 < ttt < 1:
        cube.display()
    else:
        pushMatrix()
        translate(-55 * tt, 0)
        cube.display_face(0)
        popMatrix()

        pushMatrix()
        translate(0, -50 * tt)
        cube.display_face(1)
        popMatrix()
        
        pushMatrix()
        translate(50 * tt, 15 * tt)
        cube.display_face(2)
        popMatrix()
    popMatrix()

    # stroke(255)
    # fill(255)
    # for i in range(8):
    #     ellipse(cube.p2x[i], cube.p2y[i], 3, 3)
    #     text(str(i), cube.p2x[i], cube.p2y[i])

def setup():
    global cube

    size(W, H)
    frameRate(FPS)

    cube = Cube(SHAPE_SIZE)
    cube.update(0.42)

def draw():
    if not RECORD:
        t = (frameCount / float(N_FRAMES)) % 1.0
        draw_(t)
    elif N_SAMPLES <= 1:
        t = (frameCount / float(N_FRAMES)) % 1.0
        draw_(t)
        if frameCount <= N_FRAMES:
            saveFrame('png/####.png')
        else:
            exit()
    else:
        result = [[0, 0, 0] for i in range(W * H)]
        for sample in range(N_SAMPLES):
            t = (frameCount + 0.25 * sample / float(N_SAMPLES)) / N_FRAMES
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
