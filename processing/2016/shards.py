from toxi.geom.mesh2d import Voronoi
from toxi.geom import SutherlandHodgemanClipper
from toxi.geom import Vec2D
from toxi.geom import Line2D
from toxi.geom import Polygon2D
from toxi.geom import Rect
from toxi.util.datatypes import BiasedFloatRange


W = H = 500
FPS = 20.0
BG_COLOR = color(53,44,73)
MAIN_COLOR = color(28, 33, 48)
RECORD = False

IMPACT = Vec2D(250, 250)
N_FRAMES = 20


class LineResolver(object):
    def __init__(self, n_buckets=10):
        self.buckets = {i: [] for i in range(n_buckets)}
        self.n_buckets = n_buckets
        self.norm = 4

    def __iter__(self):
        self.n = 0
        self.i = 0
        return self

    def __get_bucket(self, line2d):
        return int(constrain(line2d.a.x() // (W / self.n_buckets), 0, self.n_buckets - 1))

    def __normalize(self, line2d):
        if line2d.a.x() < line2d.b.x():
            return line2d.copy()
        else:
            return Line2D(line2d.b, line2d.a)

    def __is_line_exists(self, line2d):
        bucket_n = self.__get_bucket(line2d)
        for l in self.buckets[bucket_n]:
            if line2d.a.distanceToSquared(l.a) < self.norm \
                and line2d.b.distanceToSquared(l.b) < self.norm:
                return True
        return False

    def add_line(self, line2d):
        line2d = self.__normalize(line2d)
        if not self.__is_line_exists(line2d):
            bucket_n = self.__get_bucket(line2d)
            self.buckets[bucket_n].append(line2d)

    def is_line_exists(self, line2d):
        return self.__is_line_exists(self.__normalize(line2d))

    def next(self):
        while self.n < self.n_buckets:
            if self.i < len(self.buckets[self.n]):
                break
            else:
                self.i = 0
                self.n += 1
        else:
            raise StopIteration
        i = self.i
        self.i += 1
        return self.buckets[self.n][i]


def break_rect(rect_w, rect_h, n_fragments):
    voronoi = Voronoi()
    x_range = BiasedFloatRange(0, rect_w, IMPACT.x(), 0.3)
    y_range = BiasedFloatRange(0, rect_h, IMPACT.y(), 0.3)

    for i in range(n_fragments):
        voronoi.addPoint(Vec2D(x_range.pickRandom(), y_range.pickRandom()))

    bounds = Rect(0, 0, rect_w, rect_h)
    clipper = SutherlandHodgemanClipper(bounds)

    fragments = []
    for region in voronoi.getRegions():
        fragments.append(clipper.clipPolygon(region))

    return fragments

def ease(t):
    return (t - 1) ** 3 + 1

def ease_in_out_cubic(t):
    t *= 2
    if t < 1:
        return 0.5 * t*t*t
    t -= 2
    return 0.5 * (t*t*t + 2)


def draw_(i):
    background(BG_COLOR)
    filename = 'png/' + nf(i, 4) + '.png'
    img = loadImage(filename)

    image(img, 0, 0)

    img.loadPixels()
    loadPixels()
    for i, pix in enumerate(pixels):
        x, y = int(i % W), int(i // W)
        for j, fragment in enumerate(fragments):
            if fragment.containsPoint(Vec2D(x, y)):
                offset = offsets[j]
                a = int(constrain(x + offset[0], 0, W - 1))
                b = int(constrain(y + offset[1], 0, H - 1))
                pixels[i] = img.pixels[a + b * W]
                break
    updatePixels()

    stroke(33,27,45)
    noFill()

    strokeWeight(1.8)
    for line2d in resolver:
        line(line2d.a.x(), line2d.a.y(), line2d.b.x(), line2d.b.y())

    stroke(35)
    rect(0, 0, width, height)


def setup():
    global resolver
    global offsets
    global fragments

    size(W, H)
    frameRate(FPS)

    fragments = break_rect(W, H, 20)

    resolver = LineResolver(10)

    offsets = []
    for fragment in fragments:
        offsets.append((random(20) - 10, random(20) - 10))

    for fragment in fragments:
        for i, v in enumerate(fragment.vertices[:-1]):
            resolver.add_line(Line2D(v, fragment.vertices[i + 1]))
        resolver.add_line(Line2D(fragment.vertices[-1], fragment.vertices[0]))

def draw():
    i = (frameCount - 1) % N_FRAMES + 1
    draw_(i)

    if RECORD:
        if frameCount <= N_FRAMES:
            saveFrame('gif/####.gif')
        else:
            exit()
