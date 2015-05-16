from ddf.minim import Minim
from ddf.minim.analysis import FFT
from java.awt.event import KeyEvent


W = 854
H = 480
FPS = 24.0
FILENAME = 'song.mp3'
SCALE = 4
RECORDING = False


def setup():
    global fft_lin
    global song
    global mshader
    global pg
    size(W, H, P2D)
    frameRate(FPS)

    pg = createGraphics(W, H)
    pg.noStroke()
    pg.fill(255)

    mshader = loadShader('sound.glsl')
    mshader.set('resolution', float(W), float(H))

    minim = Minim(this)
    song = minim.loadFile('trentemoller.mp3', 1024)

    fft_lin = FFT(song.bufferSize(), song.sampleRate())
    fft_lin.linAverages(120)

def draw():
    fft_lin.forward(song.mix)
    w = 2 * width / fft_lin.avgSize()
    pg.beginDraw()
    pg.rectMode(CENTER)
    pg.background(0)
    for i in range(fft_lin.avgSize() / 4.0):
        pg.rect(width / 2 + i * w, height / 2, w, fft_lin.getAvg(i) * SCALE)
        pg.rect(width / 2 - i * w, height / 2, w, fft_lin.getAvg(i) * SCALE)
    pg.endDraw()

    shader(mshader)

    beginShape()
    textureMode(NORMAL)
    texture(pg)
    vertex(0, 0, 0, 0)
    vertex(W, 0, 1, 0)
    vertex(W, H, 1, 1)
    vertex(0, H, 0, 1)
    endShape()

    if RECORDING and not song.isPlaying():
        exit()

def keyPressed():
    global RECORDING
    if key == CODED:
        if keyCode == KeyEvent.VK_F9:
            song.play()
            RECORDING = True
