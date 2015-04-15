N_FRAMES = 40.0
FPS = 20.0


def setup():
    size(256, 256)
    background(255)
    fill(0)
    frameRate(FPS)
    
def draw():
    background(255)
    for i in range(4):
        with pushMatrix():
            translate(width/2, height/2)
            rotate(i/2.0*PI)
            line(0, -height/4-25, 0, -height/4)
    for i in range(4):
        with pushMatrix():
            w_d, h_d = ((0, 0), (1, 0), (1, 1), (0, 1))[i]
            translate(width/4+w_d*width/2, height/4+h_d*height/2)
            rotate(i/2.0*PI+(-1 if i%2 else 1)*2*PI*(1-cos(PI*(frameCount/N_FRAMES)))/2)
            arc(0, 0, 50, 50, HALF_PI, 2*PI, PIE)
    saveFrame("png/illusion-1###.png")
    if frameCount >= N_FRAMES:
        exit()

