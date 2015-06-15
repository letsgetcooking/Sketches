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
DURATION = 3
N_FRAMES = DURATION * FPS
N_SAMPLES = 1
IMPACT = Vec2D(120, 120)
RECT_W = RECT_H = 300
BG_COLOR = color(209, 67, 52)
MAIN_COLOR = color(28, 33, 48)
BLUR_COLOR = color(2, 143, 118)
STROKE_COLOR = color(179, 224, 153)
RECORD = False


def break_rect(rect_w, rect_h, n_fragments):
    voronoi = Voronoi()
    x_range = BiasedFloatRange(0, rect_w, IMPACT.x(), 0.6)
    y_range = BiasedFloatRange(0, rect_h, IMPACT.y(), 0.6)

    for i in range(n_fragments):
        voronoi.addPoint(Vec2D(x_range.pickRandom(), y_range.pickRandom()))

    bounds = Rect(0, 0, rect_w, rect_h)
    clipper = SutherlandHodgemanClipper(bounds)

    fragments = []
    for region in voronoi.getRegions():
        fragments.append(clipper.clipPolygon(region))

    return fragments

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

def copy_fragments(fragments):
    fragments_copy = []
    for fragment in fragments:
        new_fragment = Polygon2D()
        for v in fragment:
            new_fragment.add(v.copy())
        fragments_copy.append(new_fragment)
    return fragments_copy

def ease(t):
    return (t - 1) ** 3 + 1

def ease_in_out_cubic(t):
    t *= 2
    if t < 1:
        return 0.5 * t*t*t
    t -= 2
    return 0.5 * (t*t*t + 2)


def draw_(t, reset=False):
    global fragments_copy
    background(BG_COLOR)
    strokeWeight(0.3)
    fill(MAIN_COLOR)
    pushMatrix()
    translate(100, 100)
    if reset:
        fragments_copy = copy_fragments(fragments)
    if t < 0.5:
        fill(BLUR_COLOR)
        noStroke()
        sup.rect(Rect(Vec2D(-5, -5), Vec2D(RECT_W + 5, RECT_H + 5)))
        filter(BLUR, 8)
        fill(MAIN_COLOR)
        sup.rect(Rect(Vec2D(0, 0), Vec2D(RECT_W, RECT_H)))
        stroke(STROKE_COLOR)
        trace_adj_list(adj_list, int(16 * ease(2 * t)), (16 * ease(2 * t)) % 1)
    else:
        fill(MAIN_COLOR)
        noStroke()
        if t > 0.6:
            translate((-(W + RECT_W) / 2) * ease_in_out_cubic((t - 0.6) * 2.5), 0)
            fill(BLUR_COLOR)
            sup.rect(Rect(Vec2D((W + RECT_W) / 2 - 5, -5), Vec2D(RECT_W + 5 + (W + RECT_W) / 2, RECT_H + 5)))
            filter(BLUR, 8)
            fill(MAIN_COLOR)
            sup.rect(Rect(Vec2D((W + RECT_W) / 2, 0), Vec2D(RECT_W + (W + RECT_W) / 2, RECT_H)))
        for fragment in fragments_copy:
            centroid = fragment.getCentroid()
            target_dir = centroid.sub(IMPACT).normalize()
            target_dir.scaleSelf(-40 * constrain(1 - (8 * t - 4) ** 2, 0, 1))
            for v in fragment.vertices:
                v.set(v.addSelf(target_dir))
            sup.polygon2D(fragment)
    popMatrix()

def setup():
    global sup
    global adj_list
    global fragments
    global fragments_copy
    size(W, H)
    frameRate(FPS)

    sup = ToxiclibsSupport(this)
    fragments = break_rect(RECT_W, RECT_H, 100)
    fragments_copy = copy_fragments(fragments)
    adj_list = make_adj_list(fragments)

def draw():
    global N_SAMPLES
    t = (frameCount / float(N_FRAMES)) % 1.0
    N_SAMPLES = 1 if 0.45 < t < 0.7 else 4
    if not RECORD:
        t = (frameCount / float(N_FRAMES)) % 1.0
        draw_(t, reset=(t < ((frameCount - 1) / float(N_FRAMES)) % 1.0))
    else:
        result = [[0, 0, 0] for i in range(W * H)]
        for sample in range(N_SAMPLES):
            t = (frameCount + 0.2 * sample / float(N_SAMPLES)) / N_FRAMES
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
            saveFrame('gif/####.gif')
        else:
            exit()
