#!/usr/bin/env python
import random

def genmaze2(w, h):
    dirs = [(1,0,'-'), (-1,0,'-'), (0,1,'|'), (0,-1,'|')]
    def add(p):
        return
    m = []
    for i in range(h):
        m.append([' ']*w)
    m[1][1] = '+'
    root = []
    for d in dirs:
        root.append(((1,1), d))
    while 0 < len(root):
        i = random.randrange(len(root))
        ((x0,y0),(vx,vy,c)) = root[i]
        del root[i]
        (x1,y1) = (x0+vx, y0+vy)
        (x2,y2) = (x1+vx, y1+vy)
        if (0 <= x2 and x2 < w and
            0 <= y2 and y2 < h and
            m[y1][x1] == ' '):
            if m[y2][x2] == ' ':
                m[y1][x1] = c
                m[y2][x2] = '+'
                for d in dirs:
                    root.append(((x2,y2), d))
            elif m[y2][x2] == '+':
                (x3,y3) = (x2+vx, y2+vy)
                (x4,y4) = (x3+vx, y3+vy)
                (x3a,y3a) = (x2+vy, y2-vx)
                (x3b,y3b) = (x2-vy, y2+vx)
                if (0 <= x4 and x4 < w and
                    0 <= y4 and y4 < h and
                    m[y3][x3] == ' ' and
                    m[y4][x4] == ' ' and
                    m[y3a][x3a] != ' ' and
                    m[y3b][x3b] != ' '):
                    m[y1][x1] = c
                    m[y2][x2] = c
                    m[y3][x3] = c
                    m[y4][x4] = '+'
                    for d in dirs:
                        root.append(((x4,y4), d))
    return m

m = genmaze2(15, 15)
for row in m:
    print(''.join(row))
