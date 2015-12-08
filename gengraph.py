#!/usr/bin/env python
import sys
import math
import random

def crossline(linea, lineb):
    ((xa0,ya0),(xa1,ya1)) = linea
    ((xb0,yb0),(xb1,yb1)) = lineb
    vxa = xa1-xa0
    vya = ya1-ya0
    vxb = xb1-xb0
    vyb = yb1-yb0
    dx = xb0-xa0
    dy = yb0-ya0
    det = vxb*vya - vxa*vyb
    if det == 0:
        if vya*dx != vxa*dy: return False
        if (max(xa0,xa1) <= min(xb0,xb1) or
            max(xb0,xb1) <= min(xa0,xa1) or
            max(ya0,ya1) <= min(yb0,yb1) or
            max(yb0,yb1) <= min(ya0,ya1)): return False
    else:
        ta = vxb*dy - vyb*dx
        tb = vxa*dy - vya*dx
        if 0 < det:
            if (ta <= 0 or det <= ta or
                tb <= 0 or det <= tb): return False
        else:
            if (ta <= det or 0 <= ta or
                ta <= det or 0 <= tb): return False
    return True
assert crossline(((0,0),(1,1)), ((0,0),(1,1)))
assert crossline(((0,0),(1,2)), ((0,0),(2,4)))
assert crossline(((1,1),(2,3)), ((1,1),(3,5)))
assert crossline(((0,0),(2,2)), ((1,1),(3,3)))
assert crossline(((0,0),(2,4)), ((1,2),(3,6)))
assert not crossline(((0,0),(1,1)), ((0,1),(1,2)))
assert not crossline(((0,0),(1,1)), ((2,2),(3,3)))
assert crossline(((0,0),(2,2)), ((0,1),(2,1)))
assert crossline(((1,0),(1,2)), ((0,0),(2,2)))
assert crossline(((0,0),(1,1)), ((0,1),(1,0)))
assert not crossline(((0,0),(2,2)), ((2,1),(3,1)))
assert not crossline(((0,0),(2,2)), ((1,2),(1,3)))
assert not crossline(((2,2),(0,0)), ((2,1),(3,1)))
assert not crossline(((2,2),(0,0)), ((1,2),(1,3)))
assert crossline(((0,1),(1,0)), ((0,0),(1,1)))
assert crossline(((10,90),(90,10)), ((10,10),(90,90)))

class Point:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lines = []
        return

    def add(self, line):
        self.lines.append(line)
        return

    def dist(self, p):
        dx = self.x-p.x
        dy = self.y-p.y
        return dx*dx+dy*dy

class Line:
    
    def __init__(self, p1, p2):
        self.pts = (p1, p2)
        return

    def draw(self):
        for p in self.pts:
            p.add(self)
        return

    def cross(self, line):
        (p0,p1) = self.pts
        (q0,q1) = line.pts
        return crossline(
            ((p0.x, p0.y), (p1.x, p1.y)),
            ((q0.x, q0.y), (q1.x, q1.y))
            )

class LineSet:
    
    def __init__(self, size):
        self.size = size
        self.pts = []
        self.lines = []
        return

    def add(self, p):
        self.pts.append(p)
        return

    def findNear(self, p0, dist=1):
        for p1 in self.pts:
            d = p0.dist(p1)
            if d <= dist: return p1
        return None

    def run(self, maxout=4):
        lines = []
        for (i,p0) in enumerate(self.pts):
            for p1 in self.pts[i+1:]:
                lines.append(Line(p0,p1))
        random.shuffle(lines)
        for line in lines:
            if maxout <= max( len(p.lines) for p in line.pts ): continue
            cross = self.findCross(line)
            if cross is None:
                line.draw()
                self.lines.append(line)
        return
                
    def findCross(self, line0):
        for line1 in self.lines:
            if line1.cross(line0): return line1
        return None

    def dump(self):
        (w,h) = self.size
        print('<svg xmlns="http://www.w3.org/2000/svg"'
              ' xmlns:xlink="http://www.w3.org/1999/xlink"'
              ' version="1.1" width="%d" height="%d">' % (w,h))
        print('<g fill="none" stroke="black" stroke-width="2">')
        for line in self.lines:
            (p0,p1) = line.pts
            print(' <line x1="%d" y1="%d" x2="%d" y2="%d" />' %
                  (p0.x,p0.y, p1.x,p1.y))
        print('</g>')
        print('<g fill="white" stroke="black">')
        for p in self.pts:
            if p.lines:
                print(' <circle cx="%d" cy="%d" r="4" />' %
                      (p.x, p.y))
        print('</g>')
        print('<g text-anchor="middle">')
        for line in self.lines:
            (p0,p1) = line.pts
            x = (p0.x+p1.x)/2
            y = (p0.y+p1.y)/2
            d = int(math.sqrt(p0.dist(p1)))//20
            print('<text x="%d" y="%d">%d</text>' % (x,y,d))
        print('</g>')
        print('</svg>')
        return

n = 10
w = h = 200
margin = 10
dist = w*h//20
ls = LineSet((w,h))
ls.add(Point(margin, margin))
ls.add(Point(w-margin, h-margin))
for _ in range(n):
    while True:
        x = random.randrange(margin, w-margin)
        y = random.randrange(margin, h-margin)
        p = Point(x,y)
        if ls.findNear(p, dist) is None:
            ls.add(p)
            break
ls.run()
ls.dump()
