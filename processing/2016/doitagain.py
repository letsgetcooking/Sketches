# doitagain.glsl required

W = H = 500
FPS = 30.0
DURATION = 2
N_FRAMES = DURATION * FPS
N_SAMPLES = 1
BG_COLOR = color(255)
MAIN_COLOR = color(0)
FONTNAME = 'MontereyFLF-Bold.ttf'
RECORD = False


def draw_(t):
    background(BG_COLOR)
    shader(mshader)
    mshader.set('time', t)
    rect(0, 0, width, height)

    resetShader()
    if t < 0.1:
        myFont = createFont(FONTNAME, 190)
        textFont(myFont)
        fill(255 * (1 - t * 10))
        text('IT', width / 2, height / 2)
    else:
        myFont = createFont(FONTNAME, 120)
        textFont(myFont)
        fill(0)
        text('AGAIN', width / 2, height / 2)

def setup():
    global mshader

    size(W, H, P2D)
    frameRate(FPS)

    mshader = loadShader('doitagain.glsl')
    mshader.set('resolution', float(W), float(H))
    textAlign(CENTER, CENTER)

def draw():
    if not RECORD:
        t = (frameCount / float(N_FRAMES)) % 1.0
        draw_(t)
    elif N_SAMPLES <= 1:
        t = (frameCount / float(N_FRAMES)) % 1.0
        draw_(t)
        if frameCount <= N_FRAMES:
            saveFrame('gif/2###.gif')
        else:
            exit()
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
        if frameCount < N_FRAMES:
            saveFrame('gif/####.gif')
        else:
            exit()
