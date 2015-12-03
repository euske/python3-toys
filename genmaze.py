#!/usr/bin/env python
import random

def genmaze(w, h):
    dirs = [(1,0), (-1,0), (0,1), (0,-1)]
    m = []
    for i in range(h):
        m.append(['#']*w)
    root = [(1,1)]
    m[1][1] = ' '
    while 0 < len(root):
        i = random.randrange(len(root))
        (x0,y0) = root[i]
        del root[i]
        for (vx,vy) in dirs:
            (x1,y1) = (x0+vx+vx, y0+vy+vy)
            if 0 <= x1 and x1 < w and 0 <= y1 and y1 < h:
                if m[y1][x1] != ' ':
                    m[y1][x1] = ' '
                    m[y0+vy][x0+vx] = ' '
                    root.append((x1,y1))
    return m

m = genmaze(15, 15)
for row in m:
    print(''.join(row))
