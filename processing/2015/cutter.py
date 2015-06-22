from toxi.geom.mesh2d import Voronoi
from toxi.geom import SutherlandHodgemanClipper
from toxi.geom import Vec2D
from toxi.geom import Line2D
from toxi.geom import Polygon2D
from toxi.geom import Rect
from toxi.util.datatypes import BiasedFloatRange
from toxi.processing import ToxiclibsSupport


W = H = 500
FPS = 20.0
DURATION = 5
N_FRAMES = DURATION * FPS
N_SAMPLES = 1
RECT_W = RECT_H = 300
IMPACT = Vec2D(RECT_W / 2, 2 * RECT_H / 3)
N_FRAGMENTS = 380
MAIN_COLOR = color(21, 20, 18)
BLUR_COLOR = color(235, 161, 14)
BG_COLOR = color(0)
RECORD = False


class Fragments:
    def __init__(self, rectangle_width=None, rectangle_height=None,
        n_fragments=None):
        self.inner = []
        self.outer = []

        if rectangle_width and rectangle_height and n_fragments:
            self.rectangle_width = rectangle_width
            self.rectangle_height = rectangle_height
            self.n_fragments = n_fragments

            voronoi = Voronoi()
            x_range = BiasedFloatRange(0, self.rectangle_width, IMPACT.x(), 0.7)
            y_range = BiasedFloatRange(0, self.rectangle_height, IMPACT.y(), 0.7)

            for i in range(n_fragments):
                voronoi.addPoint(Vec2D(x_range.pickRandom(), y_range.pickRandom()))

            bounds = Rect(0, 0, self.rectangle_width, self.rectangle_height)
            clipper = SutherlandHodgemanClipper(bounds)

            for region in voronoi.getRegions():
                self.inner.append(clipper.clipPolygon(region))

    def __getattr__(self, name):
            return None

    def __iter__(self):
        if self.cutter:
            return self.cutter

    def cut(self):
        if self.cutter:
            next(self.cutter)

    def copy(self):
        new_inner = []
        new_outer = []
        for fragment in self.inner:
            new_fragment = Polygon2D()
            for v in fragment:
                new_fragment.add(v.copy())
            new_inner.append(new_fragment)
        for fragment in self.outer:
            new_fragment = Polygon2D()
            for v in fragment:
                new_fragment.add(v.copy())
            new_outer.append(new_fragment)
        new_fragments = Fragments()
        new_fragments.inner = new_inner
        new_fragments.outer = new_outer
        if self.poly:
            new_fragments.set_poly(self.poly)
        return new_fragments

    def poly_cutter(self):
        tmp_fragments = self.inner[:]
        for fragment in tmp_fragments:
            for _point in fragment:
                if self.poly.containsPoint(_point):
                    break
            else:
                for poly_point in self.poly:
                    if fragment.containsPoint(poly_point):
                        break
                else:
                    self.inner.remove(fragment)
                    self.outer.append(fragment)
                    yield

        tmp_fragments = self.inner[:]
        for fragment in tmp_fragments:
            inner_frag = Polygon2D()
            outer_frag = Polygon2D()
            first_intersection = True
            for _point in fragment:
                if not self.poly.containsPoint(_point):
                    break
            else:
                continue
            for i, _point in enumerate(fragment):
                i_point = None
                p_point = None
                frag_edge = Line2D(_point, fragment.vertices[(i+1)%len(fragment.vertices)])
                for j, poly_point in enumerate(self.poly):
                    poly_edge = Line2D(poly_point, self.poly.vertices[(j+1)%len(self.poly.vertices)])
                    intersection = frag_edge.intersectLine(poly_edge)
                    if intersection.getType().toString() == 'INTERSECTING':
                        i_point = intersection.getPos()
                        break
                if first_intersection and i_point:
                    for poly_point in self.poly:
                        if fragment.containsPoint(poly_point):
                            p_point = poly_point
                    first_intersection = False
                if self.poly.containsPoint(_point):
                    inner_frag.add(_point)
                    if i_point:
                        inner_frag.add(i_point.copy())
                        if p_point:
                            inner_frag.add(p_point.copy())
                            outer_frag.add(p_point.copy())
                        outer_frag.add(i_point.copy())
                else:
                    outer_frag.add(_point)
                    if i_point:
                        outer_frag.add(i_point.copy())
                        if p_point:
                            outer_frag.add(p_point.copy())
                            inner_frag.add(p_point.copy())
                        inner_frag.add(i_point.copy())
            self.inner.remove(fragment)
            if inner_frag.getNumPoints() != 0:
                self.inner.append(inner_frag)
            if outer_frag.getNumPoints() != 0:
                self.outer.append(outer_frag)
            yield

    def set_poly(self, poly):
        self.poly = poly
        self.cutter = self.poly_cutter()

def ease(t):
    return (t - 1) ** 3 + 1


def polar2cart(r, theta):
    return r * cos(theta), r * sin(theta)

def draw_(t, reset=False, sample=0):
    global fragments_active
    global debris

    background(BG_COLOR)
    strokeWeight(1)
    pushMatrix()
    translate(W / 2, H / 2)
    scale(1 + 2 * t + t ** 2)
    translate(100 - W / 2, 100 - H / 2)

    if reset:
        fragments_active = fragments.copy()
        debris.clear()

    for i in range(3):
        try:
            fragments_active.cut()
        except StopIteration:
            if t < 0.7:
                poly = Polygon2D()
                for j in range(3):
                    x1, y1 = polar2cart(RECT_W / 8, j / 3.0 * 2 * PI + PI / 6)
                    x1 += RECT_W / 2
                    y1 += RECT_W / 2
                    poly.add(Vec2D(x1, y1))

                new_fragments = Fragments()
                new_fragments.inner = fragments_active.inner
                new_fragments.set_poly(poly)
                fragments_active = new_fragments

    for fragment in fragments_active.outer:
        debris.add(fragment)

    for fragment in debris:
        centroid = fragment.getCentroid()
        target_dir = centroid.sub(IMPACT).normalize()
        target_dir.scaleSelf(3 + 3 * (t ** 2))
        for v in fragment.vertices:
            v.set(v.addSelf(target_dir))

    for i, col in enumerate([BLUR_COLOR, MAIN_COLOR]):
        stroke(col)
        fill(col)
        for fragment in fragments_active.inner:
            sup.polygon2D(fragment)
        for fragment in debris:
            sup.polygon2D(fragment)
        if i == 0: filter(BLUR, 1 + 3 * t)

    popMatrix()

def setup():
    global sup
    global fragments
    global fragments_active
    global debris

    size(W, H)
    frameRate(FPS)
    sup = ToxiclibsSupport(this)

    poly = Polygon2D()
    for i in range(3):
        x1, y1 = polar2cart(RECT_W / 2, i / 3.0 * 2 * PI + PI / 6)
        x1 += RECT_W / 2
        y1 += RECT_W / 2
        poly.add(Vec2D(x1, y1))

    fragments = Fragments(RECT_W, RECT_H, N_FRAGMENTS)
    fragments.set_poly(poly)
    for i in fragments:
        pass
    fragments.outer = []

    poly = Polygon2D()
    for i in range(3):
        x1, y1 = polar2cart(RECT_W / 4, i / 3.0 * 2 * PI + PI / 2)
        x1 += RECT_W / 2
        y1 += RECT_W / 2
        poly.add(Vec2D(x1, y1))
    fragments.set_poly(poly)

    fragments_active = fragments.copy()
    debris = set()

def draw():
    global N_SAMPLES
    t = (frameCount / float(N_FRAMES)) % 1.0
    t = (frameCount / float(N_FRAMES)) % 1.0
    draw_(t, reset=(t < ((frameCount - 1) / float(N_FRAMES)) % 1.0))
    if RECORD:
        if frameCount <= N_FRAMES:
            saveFrame('gif/####.gif')
        else:
            exit()
