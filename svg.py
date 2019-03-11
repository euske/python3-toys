#!/usr/bin/env python
import sys
from xml.etree.ElementTree import tostring, Element, ElementTree


##  misc. functions
##
def tolist(x):
    if x is None:
        return []
    elif isinstance(x, str):
        return x.split(' ')
    else:
        return list(x)

def flatten(seq):
    a = []
    for x in seq:
        if isinstance(x, list) or isinstance(x, tuple):
            a += flatten(x)
        else:
            a.append(x)
    return a

def nsplit(n, seq):
    a = []
    v = []
    for x in seq:
        v.append(x)
        if n <= len(v):
            a.append(v)
            v = []
    return a

def getbounds(pts):
    (x0,y0,x1,y1) = (sys.maxsize, sys.maxsize, -sys.maxsize, -sys.maxsize)
    for (x,y) in pts:
        x0 = min(x0, x)
        y0 = min(y0, y)
        x1 = max(x1, x)
        y1 = max(y1, y)
    return (x0,y0,x1,y1)


##  SVGItem
##
class SVGItem:

    TAG = None

    def __init__(self, **attrs):
        self.fill = attrs.pop('fill', None)
        self.stroke = attrs.pop('stroke', None)
        self.stroke_width = attrs.pop('stroke_width', None)
        self.transforms = tolist(attrs.pop('transform', None))
        self.styles = tolist(attrs.pop('style', None))
        self.marker0 = attrs.pop('marker0', None)
        self.marker1 = attrs.pop('marker1', None)
        self.attrs = attrs
        return

    def __getitem__(self, k):
        return self.attrs.get(k)

    def __setitem__(self, k, v):
        self.attrs[k] = v
        return

    def translate(self, x, y):
        self.transforms.append('translate(%d,%d)' % (x,y))
        return self

    def get(self, k, v=None):
        return self.attrs.get(k, v)

    def set(self, k, v):
        self.attrs[k] = v
        return

    def copy(self, src=None):
        if src is None:
            src = SVGItem()
        src.fill = self.fill
        src.stroke = self.stroke
        src.stroke_width = self.stroke_width
        src.transforms = self.transforms.copy()
        src.marker0 = self.marker0
        src.marker1 = self.marker1
        src.attrs = self.attrs
        return src

    def bbox(self, parent=None):
        return None

    def defs(self):
        a = []
        if self.marker0 is not None:
            a.append(self.marker0)
        if self.marker1 is not None:
            a.append(self.marker1)
        return a

    def toxml(self):
        elem = Element(self.TAG)
        for (k,v) in self.attrs.items():
            k = k.replace('_','-')
            if v is None:
                elem.set(k, 'none')
            elif isinstance(v, list) or isinstance(v, tuple):
                elem.set(k, ' '.join(map(str, flatten(v))))
            else:
                elem.set(k, str(v))
        if self.fill is not None:
            elem.set('fill', self.fill)
        if self.stroke is not None:
            elem.set('stroke', self.stroke)
        if self.stroke_width is not None:
            elem.set('stroke-width', str(self.stroke_width))
        if self.transforms:
            elem.set('transform', ' '.join(self.transforms))
        if self.styles:
            elem.set('style', ' '.join(self.styles))
        if self.marker0 is not None:
            elem.set('marker-begin', 'url(#'+self.marker0.id+')')
        if self.marker1 is not None:
            elem.set('marker-end', 'url(#'+self.marker1.id+')')
        return elem

    def tostring(self):
        return tostring(self.toxml())


##  SVGGroup
##
class SVGGroup(SVGItem):

    TAG = 'g'

    def __init__(self, *children, **attrs):
        SVGItem.__init__(self, **attrs)
        if len(children) == 1 and isinstance(children[0], list):
            children = children[0]
        else:
            children = list(children)
        self.children = children
        return

    def __len__(self):
        return len(self.children)

    def __iter__(self):
        return iter(self.children)

    def copy(self, src=None):
        if src is None:
            children = [ c.copy() for c in self.children ]
            src = SVGGroup(*children)
        return SVGItem.copy(self, src)

    def add(self, obj):
        self.children.append(obj)
        return

    def remove(self, obj):
        self.children.remove(obj)
        return

    def bbox(self, parent=None):
        ok = False
        (x0,y0,x1,y1) = (sys.maxsize, sys.maxsize, -sys.maxsize, -sys.maxsize)
        for c in self.children:
            b = c.bbox(self)
            if b is not None:
                ok = True
                x0 = min(x0, b[0])
                y0 = min(y0, b[1])
                x1 = max(x1, b[2])
                y1 = max(y1, b[3])
        if ok:
            return (x0,y0,x1,y1)
        else:
            return None

    def defs(self):
        a = []
        for c in self.children:
            a.extend(c.defs())
        return a

    def toxml(self):
        elem = SVGItem.toxml(self)
        for c in self.children:
            elem.append(c.toxml())
        return elem

Group = SVGGroup


##  SVGCanvas
##
class SVGCanvas(SVGGroup):

    TAG = 'svg'

    def __init__(self, width=None, height=None, version='1.1', **attrs):
        self.width = attrs.pop('width', width)
        self.height = attrs.pop('height', height)
        self.version = attrs.pop('version', version)
        SVGGroup.__init__(self, **attrs)
        return

    def toxml(self):
        elem = SVGGroup.toxml(self)
        elem.set('xmlns', 'http://www.w3.org/2000/svg')
        elem.set('xmlns:xlink', 'http://www.w3.org/1999/xlink')
        b = self.bbox(self)
        elem.set('width', str(self.width or b[2]))
        elem.set('height', str(self.height or b[3]))
        elem.set('version', self.version)
        defs = self.defs()
        if defs:
            e = Element('defs')
            for d in set(defs):
                e.append(d.toxml())
            elem.insert(0, e)
        return elem

    def dump(self, fp=sys.stdout.buffer, decl=False):
        if decl:
            fp.write(b'<?xml version="1.0" encoding="UTF-8"?>')
        fp.write(self.tostring())
        fp.flush()
        return

SVG = SVGCanvas


##  Line
##
class Line(SVGItem):

    TAG = 'line'

    def __init__(self, *args, **attrs):
        self.x1 = attrs.pop('x1', None)
        self.y1 = attrs.pop('y1', None)
        self.x2 = attrs.pop('x2', None)
        self.y2 = attrs.pop('y2', None)
        if len(args) == 2:
            ((self.x1,self.y1), (self.x2,self.y2)) = args
        elif len(args) == 4:
            (self.x1,self.y1,self.x2,self.y2) = args
        if self.x1 is None: raise SyntaxError('x1 not defined')
        if self.y1 is None: raise SyntaxError('y1 not defined')
        if self.x2 is None: raise SyntaxError('x2 not defined')
        if self.y2 is None: raise SyntaxError('y2 not defined')
        self.p1 = (self.x1, self.y1)
        self.p2 = (self.x2, self.y2)
        SVGItem.__init__(self, **attrs)
        return

    def copy(self, src=None):
        src = Line(self.x1, self.y1, self.x2, self.y2)
        return SVGItem.copy(self, src)

    def move(self, dx, dy):
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy
        self.p1 = (self.x1, self.y1)
        self.p2 = (self.x2, self.y2)
        return self

    def bbox(self, parent=None):
        if parent is None:
            sw = self.stroke_width or 0
        else:
            sw = parent.stroke_width or 0
        return (self.x1-sw, self.y1-sw,
                self.x2+sw, self.y2+sw)

    def toxml(self):
        elem = SVGItem.toxml(self)
        elem.set('x1', str(self.x1))
        elem.set('y1', str(self.y1))
        elem.set('x2', str(self.x2))
        elem.set('y2', str(self.y2))
        return elem


##  Rect
##
class Rect(SVGItem):

    TAG = 'rect'

    def __init__(self, *args, **attrs):
        self.x = attrs.pop('x', None)
        self.y = attrs.pop('y', None)
        self.width = attrs.pop('width', None)
        self.height = attrs.pop('height', None)
        if len(args) == 2:
            ((self.x,self.y), (self.width,self.height)) = args
        elif len(args) == 4:
            (self.x,self.y,self.width,self.height) = args
        if self.x is None: raise SyntaxError('x not defined')
        if self.y is None: raise SyntaxError('y not defined')
        if self.width is None: raise SyntaxError('width not defined')
        if self.height is None: raise SyntaxError('height not defined')
        self.topleft = (self.x, self.y)
        self.bottomright = (self.x+self.width, self.y+self.height)
        SVGItem.__init__(self, **attrs)
        return

    def copy(self, src=None):
        src = Rect(self.x, self.y, self.width, self.height)
        return SVGItem.copy(self, src)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        return self

    def bbox(self, parent=None):
        if parent is None:
            sw = self.stroke_width or 0
        else:
            sw = parent.stroke_width or 0
        return (self.x-sw, self.y-sw,
                self.x+self.width+sw, self.y+self.height+sw)

    def toxml(self):
        elem = SVGItem.toxml(self)
        elem.set('x', str(self.x))
        elem.set('y', str(self.y))
        elem.set('width', str(self.width))
        elem.set('height', str(self.height))
        return elem


##  Circle
##
class Circle(SVGItem):

    TAG = 'circle'

    def __init__(self, *args, **attrs):
        self.cx = attrs.pop('cx', None)
        self.cy = attrs.pop('cy', None)
        self.r = attrs.pop('r', None)
        if len(args) == 2:
            ((self.cx,self.cy), self.r) = args
        elif len(args) == 3:
            (self.cx,self.cy,self.r) = args
        if self.cx is None: raise SyntaxError('cx not defined')
        if self.cy is None: raise SyntaxError('cy not defined')
        if self.r is None: raise SyntaxError('r not defined')
        SVGItem.__init__(self, **attrs)
        return

    def copy(self, src=None):
        src = Circle(self.cx, self.cy, self.r)
        return SVGItem.copy(self, src)

    def move(self, dx, dy):
        self.cx += dx
        self.cy += dy
        return self

    def bbox(self, parent=None):
        if parent is None:
            sw = self.stroke_width or 0
        else:
            sw = parent.stroke_width or 0
        return (self.cx-self.r-sw, self.cy-self.r-sw,
                self.cx+self.r+sw, self.cy+self.r+sw)

    def toxml(self):
        elem = SVGItem.toxml(self)
        elem.set('cx', str(self.cx))
        elem.set('cy', str(self.cy))
        elem.set('r', str(self.r))
        return elem


##  Polygon
##
class Polygon(SVGItem):

    TAG = 'polygon'

    def __init__(self, *args, **attrs):
        points = flatten(attrs.pop('points', args))
        self.points = nsplit(2, points)
        if not self.points: raise SyntaxError('points not defined')
        SVGItem.__init__(self, **attrs)
        return

    def add(self, *args):
        if len(args) == 1:
            p = args[0]
        elif len(args) == 2:
            p = args
        else:
            raise SyntaxError('invalid args: %r' % args)
        self.points.append(p)
        return self

    def copy(self, src=None):
        src = self.__class__(*self.points)
        return SVGItem.copy(self, src)

    def move(self, dx, dy):
        self.points = [ (x+dx,y+dy) for (x,y) in self.points ]
        return self

    def bbox(self, parent=None):
        if parent is None:
            sw = self.stroke_width or 0
        else:
            sw = parent.stroke_width or 0
        (x0,y0,x1,y1) = getbounds(self.points)
        return (x0-sw, y0-sw, x1+sw, y1+sw)

    def toxml(self):
        elem = SVGItem.toxml(self)
        a = []
        for (x,y) in self.points:
            a.append('%r,%r' % (x,y))
        elem.set('points', ' '.join(a))
        return elem


##  Polyline
##
class Polyline(Polygon):

    TAG = 'polyline'


##  Path
##
class Path(SVGItem):

    TAG = 'path'

    def __init__(self, *args, **attrs):
        self.d = attrs.pop('d', args)
        if not self.d: raise SyntaxError('d not defined')
        SVGItem.__init__(self, **attrs)
        return

    def add(self, *args):
        self.d.extend(args)
        return self

    def copy(self, src=None):
        src = Path(*self.d)
        return SVGItem.copy(self, src)

    def toxml(self):
        elem = SVGItem.toxml(self)
        elem.set('d', ' '.join(map(str, flatten(self.d))))
        return elem


##  Text
##
class Text(SVGItem):

    TAG = 'text'

    def __init__(self, *args, **attrs):
        self.x = attrs.pop('x', None)
        self.y = attrs.pop('y', None)
        text = attrs.pop('text', None)
        if len(args) == 2:
            ((self.x,self.y), self.text) = args
        elif len(args) == 3:
            (self.x,self.y,self.text) = args
        else:
            raise SyntaxError(args)
        if self.x is None: raise SyntaxError('x not defined')
        if self.y is None: raise SyntaxError('y not defined')
        if self.text is None: raise SyntaxError('text not defined')
        SVGItem.__init__(self, **attrs)
        return

    def copy(self, src=None):
        src = Text(self.x, self.y, self.text)
        return SVGItem.copy(self, src)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        return self

    def bbox(self, parent=None):
        return (self.x, self.y, self.x, self.y)

    def toxml(self):
        elem = SVGItem.toxml(self)
        elem.set('x', str(self.x))
        elem.set('y', str(self.y))
        elem.text = self.text
        return elem


##  Marker
##
class Marker(SVGGroup):

    TAG = 'marker'

    def __init__(self, id=None, **attrs):
        self.id = attrs.pop('id', id)
        if self.id is None: raise SyntaxError('id not defined')
        self.orient = attrs.pop('orient', 'auto')
        self.viewBox = None
        SVGGroup.__init__(self, **attrs)
        return

    def add(self, obj):
        SVGGroup.add(self, obj)
        (x0,y0,x1,y1) = self.bbox()
        self.viewBox = (x0, y0, x1-x0, y1-y0)
        return

    def defs(self):
        return [self]

    def toxml(self):
        elem = SVGGroup.toxml(self)
        elem.set('id', self.id)
        elem.set('orient', self.orient)
        elem.set('viewBox', '%r %r %r %r' % self.viewBox)
        return elem


##  Symbol
##
class Symbol(SVGGroup):

    TAG = 'symbol'

    def __init__(self, id=None, **attrs):
        self.id = attrs.pop('id', id)
        if self.id is None: raise SyntaxError('id not defined')
        self.viewBox = None
        SVGGroup.__init__(self, **attrs)
        return

    def add(self, obj):
        SVGGroup.add(self, obj)
        (x0,y0,x1,y1) = self.bbox()
        self.viewBox = (x0, y0, x1-x0, y1-y0)
        return

    def defs(self):
        return [self]

    def toxml(self):
        elem = SVGGroup.toxml(self)
        elem.set('id', self.id)
        elem.set('viewBox', '%r %r %r %r' % self.viewBox)
        return elem


##  Use
##
class Use(SVGItem):

    def __init__(self, item=None, *args, **attrs):
        self.item = attrs.pop('item', item)
        if self.item is None: raise SyntaxError('item not defined')
        SVGItem.__init__(self, *args, **attrs)
        return

    def bbox(self, parent=None):
        return self.item.bbox(parent)

    def toxml(self):
        elem = SVGGroup.toxml(self)
        elem.set('id', self.item.id)
        return elem


##  Arrow
##
class Arrow(Line):

    ARROW = Marker(id='arrow')
    ARROW.add(Polygon([(-5,-5), (5,0), (-5,5)], fill='black', stroke=None))

    def __init__(self, *args, **attrs):
        Line.__init__(self, *args, **attrs)
        self.marker1 = self.ARROW
        return


# run
def run():
    svg = SVG(400,200)
    w = h = 100
    g = Group(stroke='black', fill='none',
              stroke_width=2, transform='translate(10,10)')
    g.add(Arrow(0,10+h,0,0))
    g.add(Arrow(-10,h,10+w,0+h))
    g.add(Text(-10,h-10,'0', stroke='none',fill='black',
               text_anchor='middle',dy='0.5em'))
    a = [5,9,4,0,7,3,1,8,6,2]
    dx = 10
    dy = 10
    for (x,y) in enumerate(a):
        g.add(Rect(x*dx,100-y*dy, dx,y*dy, fill='red'))
    g.add(Polyline([ (x*dx+dx/2,100-y*dy) for (x,y) in enumerate(a) ],
                     stroke='green'))
    g.add(Text(w/2,10,'title', stroke='none',fill='black',
               text_anchor='middle', style='font-size:16px'))
    svg.add(g)
    svg.dump()

if __name__ == '__main__': run()
