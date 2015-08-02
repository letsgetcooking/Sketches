from toxi.sim.automata import CAMatrix, CARule2D
from toxi.color import ToneMap, ColorGradient, NamedColor
from com.hamoid import VideoExport


W, H = 500, 500
FPS = 30.0
DURATION = 6
N_FRAMES = DURATION * FPS
RESOLUTION = 50
FADING = False
RECORD = False
RECORD_VIDEO = False


def setup():
    global ca
    global tone_map
    global vi_exp

    size(W, H)
    frameRate(FPS)

    ca = CAMatrix(width, height)
    birth_rules = (1, 5, 6, 7, 8)
    survival_rules = (0, 3, 5, 6, 7, 8)
    rule = CARule2D(birth_rules, survival_rules, 256, False)
    rule.setAutoExpire(True)
    ca.setRule(rule)

    img = loadImage('deer.png')
    ca.drawBoxAt(width / 2, height / 2, width, 1)
    ca.drawBoxAt(width / 2, height / 2, img.width, 0)
    img.loadPixels()
    for i in range(img.width):
        for j in range(img.height):
            if img.pixels[j * img.width + i] == color(0, 0, 0):
                ca.drawBoxAt(i + (width - img.width) // 2, j + (height - img.height) // 2, 2, 1)

    grad = ColorGradient()
    grad.addColorAt(0, NamedColor.BLACK)
    grad.addColorAt(120, NamedColor.KHAKI)
    grad.addColorAt(150, NamedColor.SIENNA)
    grad.addColorAt(255, NamedColor.BLACK)
    tone_map = ToneMap(0, rule.getStateCount() - 1, grad)

    vi_exp = VideoExport(this, 'video.mp4')
    vi_exp.setFrameRate(FPS)

def draw():
    global FADING
    loadPixels()
    if frameCount > 130 and not FADING:
        birth_rules = (5, 7)
        survival_rules = (4, 5, 7, 8)
        rule = CARule2D(birth_rules, survival_rules, 256, False)
        rule.setAutoExpire(True)
        ca.setRule(rule)
        FADING = True
    ca.update()
    ca.update()
    tone_map.getToneMappedArray(ca.getMatrix(), pixels)
    updatePixels()
    if frameCount > 130:
        stroke(0)
        strokeWeight(100)
        noFill()
        rect(0, 0, width, height)

    if RECORD:
        if frameCount < N_FRAMES:
            saveFrame('gif/####.gif')
        else:
            exit()
    if RECORD_VIDEO:
        if frameCount < N_FRAMES:
            vi_exp.saveFrame()
        else:
            exit()
