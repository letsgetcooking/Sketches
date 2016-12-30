W = H = 500
FPS = 20.0
DURATION = 3
N_FRAMES = DURATION * FPS
N_SAMPLES = 1
RECORD = False

TEXT_COLOR = color(148, 129, 56)
CURSOR_COLOR = color(200)

FONT_NAME = 'whitrabt.ttf'

STRINGS = [
            'MERRY CHRISTMAS!',
            ' HAPPY NEW YEAR!',
            '',
            'MERRY CHRISTMAS!',
            ' HAPPY NEW YEAR!',
            '',
            '',
            '',
        ]

SSUM = sum([len(s) for s in STRINGS])
LIGHTS = []


def draw_(t):
    global LIGHTS
    global c_x_last

    img = loadImage('images/' + nf(max(frameCount % 61, 1), 4) + '.png')
    image(img, 0, 0)

    pg = createGraphics(250, 200)
    pg.beginDraw()
    pg.fill(TEXT_COLOR)
    pg.stroke(CURSOR_COLOR)
    pg.strokeWeight(4)
    pg.strokeCap(SQUARE)
    my_font = createFont(FONT_NAME, 22)
    pg.textFont(my_font)

    str_num, sym_ctr = 0, 0
    for string in STRINGS:
        sym_ctr += len(string)
        if SSUM * t < sym_ctr:
            break
        str_num += 1
    str_pos, sym_ctr = 0, 0
    for string in STRINGS:
        sym_ctr += len(string)
        if SSUM * t < sym_ctr:
            str_pos = int(len(string) - (sym_ctr - SSUM * t))
            break

    t_offset = 20
    t_gap = 27
    c_len = 20

    for i, string in enumerate(STRINGS[:str_num]):
        pg.text(string, t_offset, (i + 1) * t_gap)

    cur_text = STRINGS[str_num][:str_pos]
    tw = pg.textWidth(cur_text)
    pg.text(cur_text, t_offset, (str_num + 1) * t_gap)

    c_x, c_y = tw + t_offset + 6, (str_num + 1) * t_gap - 18
    pg.line(c_x, c_y, c_x, c_y + c_len)
    for i in range(int(c_len)):
        for j in range(int(constrain(c_x + 24 - c_x_last, 0, 1000))):
            LIGHTS.append([c_x + 6 - j, c_y + i, 1.0])
    c_x_last = c_x

    for light in LIGHTS:
        light[2] -= 0.08

    tmp_lights = []
    for light in LIGHTS:
        if light[2] > 0:
            tmp_lights.append(light)
    LIGHTS = tmp_lights

    pg.loadPixels()
    for light in LIGHTS:
        cur_color = pg.pixels[int(light[1] * pg.width + light[0])]
        hu = hue(cur_color)
        sa = saturation(cur_color)
        br = brightness(cur_color)
        al = alpha(cur_color)
        colorMode(HSB)
        pg.pixels[int(light[1] * pg.width + light[0])] = color(hu, sa, br + 80 * light[2] ** 2, al)
        colorMode(RGB)
    pg.updatePixels()

    pg.endDraw()

    tt = constrain(t - 0.8, 0, 1) * 5

    pushMatrix()
    translate(245, 80)
    image(pg, 0, -(1 / (1 + exp(-map(tt, 0, 1, -6, 6)))) * (len(STRINGS) * t_gap + 10))
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
