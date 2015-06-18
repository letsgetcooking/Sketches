from toxi.geom.mesh2d import Voronoi
from toxi.geom import SutherlandHodgemanClipper
from toxi.geom import Vec2D
from toxi.geom import Line2D
from toxi.geom import Polygon2D
from toxi.geom import Rect
from toxi.util.datatypes import BiasedFloatRange
from toxi.processing import ToxiclibsSupport


W = H = 500
FPS = 30.0
DURATION = 3.4
N_FRAMES = DURATION * FPS
N_SAMPLES = 1
RECT_W = RECT_H = 300
IMPACT = Vec2D(RECT_W / 2, 2 * RECT_H / 3)
N_FRAGMENTS = 180
SPEED = 10
CUT_SPEED = 0.2
MAIN_COLOR = color(255, 106, 90)
SECOND_COLOR = color(255, 179, 80)
BG_COLOR = color(39, 45, 77)
STROKE_COLOR = MAIN_COLOR
RECORD = False


def break_rect(rect_w, rect_h, n_fragments):
    voronoi = Voronoi()
    x_range = BiasedFloatRange(0, rect_w, IMPACT.x(), 0.8)
    y_range = BiasedFloatRange(0, rect_h, IMPACT.y(), 0.8)

    for i in range(n_fragments):
        voronoi.addPoint(Vec2D(x_range.pickRandom(), y_range.pickRandom()))

    bounds = Rect(0, 0, rect_w, rect_h)
    clipper = SutherlandHodgemanClipper(bounds)

    fragments = []
    for region in voronoi.getRegions():
        fragments.append(clipper.clipPolygon(region))

    return fragments

def copy_fragments(fragments):
    fragments_active = []
    for fragment in fragments:
        new_fragment = Polygon2D()
        for v in fragment:
            new_fragment.add(v.copy())
        fragments_active.append(new_fragment)
    return fragments_active

def ease(t):
    return (t - 1) ** 3 + 1

def ease_in_out_cubic(t):
    t *= 2
    if t < 1:
        return 0.5 * t*t*t
    t -= 2
    return 0.5 * (t*t*t + 2)

def make_adj_list(fragments):
    adj_list = dict()
    for fragment in fragments:
        for i, _vertex in enumerate(fragment):
            if not _vertex in adj_list:
                adj_list[_vertex.copy()] = set()
            adj_list[_vertex.copy()].add(fragment.vertices[(i+1)%len(fragment.vertices)].copy())
            adj_list[_vertex.copy()].add(fragment.vertices[(i-1)%len(fragment.vertices)].copy())

    adj_list = {key: list(value) for key, value in adj_list.items()}

    return adj_list

def polar2cart(r, theta):
    return r * cos(theta), r * sin(theta)

def trace_adj_list(adj_list, max_depth, end_progress):
    first = min(adj_list, key=lambda x: x.distanceTo(IMPACT))
    visited = set()
    vertices_queue = []
    vertices_queue.append(first)
    depth = max_depth

    while vertices_queue and depth:
        for i in range(len(vertices_queue)):
            head = vertices_queue.pop(0)
            visited.add(head)
            for tail in adj_list[head]:
                if not tail in visited and head.x() != tail.x() and head.y() != tail.y():
                    vertices_queue.append(tail)
                    if depth == 1:
                        sup.line(Line2D(head, tail).toRay2D().toLine2DWithPointAtDistance(
                            head.distanceTo(tail) * end_progress))
                    else:
                        sup.line(head, tail)
        depth -= 1

def triangle_cutter(fragments, triangle):
    tmp_fragments = fragments[:]
    for fragment in tmp_fragments:
        if not sum(triangle.containsPoint(_point) for _point in fragment):
            fragments.remove(fragment)
            yield

    tmp_fragments = fragments[:]
    while True:
        for fragment in tmp_fragments:
            for _point in fragment:
                if not triangle.containsPoint(_point):
                    min_distance, nearest_line = 999999, None
                    for i, v in enumerate(triangle.vertices):
                        _line = Line2D(v, triangle.vertices[(i+1)%
                            len(triangle.vertices)])
                        distance = _line.toRay2D().getDistanceToPoint(_point)
                        if distance < min_distance:
                            min_distance = distance
                            nearest_line = _line
                    closest = nearest_line.closestPointTo(_point)
                    _point.interpolateToSelf(closest, CUT_SPEED)
        yield

def draw_(t, reset=False, sample=0):
    global fragments_active
    global fragments_to_cut
    global cutter

    background(BG_COLOR)
    strokeWeight(1)
    pushMatrix()
    translate(100, 100)
    fill(MAIN_COLOR)
    stroke(MAIN_COLOR)

    if reset:
        fragments_active = copy_fragments(fragments)
        fragments_to_cut = fragments_active[:]
        cutter = triangle_cutter(fragments_to_cut, triangle)

    if t < 0.75:
        if not sample:
            try:
                next(cutter)
            except StopIteration:
                pass

        static_fragmets = []
        dynamic_fragments = []
        for fragment in fragments_active:
            if not fragment in fragments_to_cut:
                if not sample:
                    moving_fragment = fragment
                    centroid = moving_fragment.getCentroid()
                    target_dir = centroid.sub(Vec2D(W, 2 * H / 3)).normalize()
                    target_dir.scaleSelf(SPEED * (0.5 + ease(t)))
                    for v in moving_fragment.vertices:
                        v.set(v.addSelf(target_dir))
                else:
                    moving_fragment = fragment.copy()
                    for i in range(sample):
                        centroid = moving_fragment.getCentroid()
                        target_dir = centroid.sub(Vec2D(W, 2 * H / 3)).normalize()
                        target_dir.scaleSelf(SPEED / 5.0)
                        for v in moving_fragment.vertices:
                            v.set(v.addSelf(target_dir))
                dynamic_fragments.append(moving_fragment)
            else:
                static_fragmets.append(fragment)

        pushMatrix()
        fill(0, 50)
        stroke(0, 50)
        translate(5, 5)
        for fragment in static_fragmets:
            sup.polygon2D(fragment)
        popMatrix()
        fill(MAIN_COLOR)
        stroke(MAIN_COLOR)
        for fragment in static_fragmets:
            sup.polygon2D(fragment)
        sup.polygon2D(triangle)
        for fragment in dynamic_fragments:
            fill(0, 50)
            stroke(0, 50)
            sup.polygon2D(fragment)
        translate(-5, -5)
        for fragment in dynamic_fragments:
            fill(SECOND_COLOR)
            stroke(SECOND_COLOR)
            sup.polygon2D(fragment)
    else:
        fill(0, 50)
        stroke(0, 50)
        pushMatrix()
        translate(5, 5)
        translate(0, -H * ease_in_out_cubic(4 * (t - 0.75)))
        sup.polygon2D(triangle)
        translate(0, H)
        sup.rect(Rect(Vec2D(0, 0), Vec2D(RECT_W, RECT_H)))
        popMatrix()

        fill(MAIN_COLOR)
        stroke(MAIN_COLOR)
        translate(0, -H * ease_in_out_cubic(4 * (t - 0.75)))
        sup.polygon2D(triangle)
        translate(0, H)
        sup.rect(Rect(Vec2D(0, 0), Vec2D(RECT_W, RECT_H)))

    popMatrix()

def setup():
    global sup
    global adj_list
    global fragments
    global fragments_active
    global fragments_to_cut
    global triangle
    global cutter
    size(W, H)
    frameRate(FPS)
    sup = ToxiclibsSupport(this)

    triangle = Polygon2D()
    for i in range(3):
        x1, y1 = polar2cart(RECT_W / 1.75, i / 3.0 * 2 * PI + PI / 6)
        x1 += RECT_W / 2
        y1 += RECT_W / 1.7
        triangle.add(Vec2D(x1, y1))

    fragments = break_rect(RECT_W, RECT_H, N_FRAGMENTS)
    fragments = sorted(fragments, key=lambda f: f.getCentroid().sub(IMPACT),
        cmp=lambda x, y: cmp(x.angleBetween(Vec2D(1, 0), True),
            y.angleBetween(Vec2D(1, 0), True)))
    fragments_active = copy_fragments(fragments)
    fragments_to_cut = fragments_active[:]
    adj_list = make_adj_list(fragments)

    cutter = triangle_cutter(fragments_to_cut, triangle)

def draw():
    global N_SAMPLES
    t = (frameCount / float(N_FRAMES)) % 1.0
    N_SAMPLES = 1 if 0.45 < t < 0.7 else 4
    if not RECORD:
        t = (frameCount / float(N_FRAMES)) % 1.0
        draw_(t, reset=(t < ((frameCount - 1) / float(N_FRAMES)) % 1.0))
    else:
        result = [[0, 0, 0] for i in range(W * H)]
        for i, sample in enumerate(range(N_SAMPLES)):
            t = (frameCount + 0.2 * sample / float(N_SAMPLES)) / N_FRAMES
            draw_(t, sample=sample)
            loadPixels()
            for j, pix in enumerate(pixels):
                result[j][0] += red(pix)
                result[j][1] += green(pix)
                result[j][2] += blue(pix)
        loadPixels()
        for i, rgb in enumerate(result):
            pixels[i] = color(rgb[0] / N_SAMPLES, rgb[1] / N_SAMPLES, rgb[2] / N_SAMPLES)
        updatePixels()
        if frameCount <= N_FRAMES:
            saveFrame('gif/####.gif')
        else:
            exit()
