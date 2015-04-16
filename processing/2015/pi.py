N_WORMS = 8.0
FPS = 30.0
RECORD = False
PI_STR = ('3.14159265358979323846264338327950288419716939937510582097494'
'459230781640628620899862803482534211706798214808651328230664709384'
'460955058223172535940812848111745028410270193852110555964462294895'
'493038196442881097566593344612847564823378678316527120190914564856'
'692346034861045432664821339360726024914127372458700660631558817488'
'152092096282925409171536436789259036001133053054882046652138414695'
'1941511609')


class Segment(object):
    
    def __init__(self, head_size, n, worm_size=None):
        self.x = width / 2
        self.y = height / 2
        self.n = n
        self.head_size = head_size
        if worm_size:
            self.worm_size = worm_size
        else:
            self.worm_size = n
        if n > 1:
            self.next = Segment(head_size, n - 1,
                                worm_size=self.worm_size)
        else:
            self.next = None

    def move(self, x, y):
        easing = 1 - map(self.n, 1, self.worm_size, 0.1, 0.2)
        self.x = self.x + (x - self.x) * easing
        self.y = self.y + (y - self.y) * easing
        if self.next:
            self.next.move(self.x, self.y)

    def draw(self):
        fill(255)
        noStroke()
        seg_size = map(self.n, 1, self.worm_size, 1, self.head_size)
        ellipse(self.x, self.y, seg_size, seg_size)
        if self.next:
            self.next.draw()
            
            
def make_pi_frame():
    pushMatrix()
    n = int(width / 8)
    for i in range(4):
        pi_frag = PI_STR[i*n:(i+1)*n]
        text(pi_frag, 12, 10)
        translate(width, 0)
        rotate(PI / 2)
    popMatrix()
        
def setup():
    global worms
    global theta1
    global theta2
    size(500, 500)
    frameRate(FPS)
    theta1 = 0
    theta2 = 0
    worms = []
    for i in range(N_WORMS):
        worms.append(Segment(30, 50))
    
def draw():
    global theta1
    global theta2
    background(0)
    make_pi_frame()
    img = loadImage('pi.jpg')
    image(img, 120, 120, 260, 260)
    for i, worm in enumerate(worms):
        angle = 2 * PI * i / len(worms)
        x = (width - 100) / 2.0 * cos(theta1 + angle) + width / 2.0
        y = (height - 100) / 2.0 * sin(theta2 + angle) + height / 2.0
        worm.move(x, y)
        worm.draw()
    theta1 = theta1 + 2 * PI / FPS / N_WORMS * 2
    theta2 = theta2 + 2 * PI / FPS / N_WORMS * 2
    if RECORD:
        if frameCount > 2 * FPS: saveFrame('png/pi-####.png')
        if frameCount >= 2 * FPS + FPS / 2: exit()

