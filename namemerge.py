#!/usr/bin/env python
##
##  namemerge.py - merge organization names.
##

import re

FULLWIDTH = (
    '　！”＃＄％＆’（）＊＋，\uff0d\u2212．／０１２３４５６７８９：；＜＝＞？'
    '＠ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ［＼］＾＿'
    '‘ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ｛｜｝'
)
HALFWIDTH = (
    ' !\"#$%&\'()*+,--./0123456789:;<=>?'
    '@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_'
    '`abcdefghijklmnopqrstuvwxyz{|}'
)
Z2HMAP = dict( (ord(zc), ord(hc)) for (zc,hc) in zip(FULLWIDTH, HALFWIDTH) )

def zen2han(s):
    return s.translate(Z2HMAP)


##  NameMerger
##
class NameMerger:

    def __init__(self, short_threshold=0.9, long_threshold=0.3):
        self.short_threshold = short_threshold
        self.long_threshold = long_threshold
        self.items = []
        self.ss = {}
        return

    def add(self, key, *args):
        if not args:
            args = key
        key = zen2han(re.sub(r'\W', '', key))
        pid = len(self.items)
        self.items.append((key, args))
        for n in range(1, len(key)+1):
            for i in range(len(key)-n+1):
                s = key[i:i+n]
                if s in self.ss:
                    a = self.ss[s]
                else:
                    a = self.ss[s] = []
                a.append(pid)
        return

    def fixate(self):
        clusters = []
        belongs = {}
        for (s,a) in sorted(self.ss.items(), key=lambda x: len(x[0])):
            for (i,pid1) in enumerate(a):
                (key1,_) = self.items[pid1]
                prop1 = len(s)/len(key1)
                for pid2 in a[i+1:]:
                    (key2,_) = self.items[pid2]
                    prop2 = len(s)/len(key2)
                    if max(prop1, prop2) < self.short_threshold: continue
                    if min(prop1, prop2) < self.long_threshold: continue
                    if pid1 in belongs:
                        c1 = belongs[pid1]
                        if pid2 in belongs:
                            # merge: c1 <- c2, erase: c2.
                            c2 = belongs[pid2]
                            if c1 is not c2:
                                c1.extend(c2)
                                for pid in c2:
                                    belongs[pid] = c1
                                clusters.remove(c2)
                        else:
                            # join: c1 <- pid2.
                            c1.append(pid2)
                            belongs[pid2] = c1
                    elif pid2 in belongs:
                        # join: c2 <- pid1.
                        c2 = belongs[pid2]
                        c2.append(pid1)
                        belongs[pid1] = c2
                    else:
                        # new cluster
                        c = [pid1, pid2]
                        clusters.append(c)
                        belongs[pid1] = c
                        belongs[pid2] = c
        clusters.sort(key=len, reverse=True)
        for pid in range(len(self.items)):
            if pid not in belongs:
                clusters.append([pid])
        for c in clusters:
            yield [ self.items[pid][1] for pid in c ]
        return

if __name__ == '__main__':
    import fileinput
    m = NameMerger()
    for line in fileinput.input():
        m.add(line.strip())
    for c in m.fixate():
        print(len(c), c)
