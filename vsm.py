#!/usr/bin/env python
##
##  vsm.py
##
##  Provides a Vector Space Model with TF/IDF for distance metrics.
##
import sys
import math

class VSM:

    """
>>> sp = VSM()
>>> sp.add('A', {'foo':1, 'baa':1, 'baz':2})
>>> sp.add('B', {'baa':1, 'baz':1})
>>> sp.commit()
>>> sp.calcsim({'baa':1, 'baz':1}, {'baz':2})
0
>>> list(sp.findsim('A'))
[(0, 'B')]
"""

    def __init__(self):
        self.tf = {}
        self.df = {}
        self.idf = None
        self.docs = {}
        return

    def __len__(self):
        return len(self.docs)

    def add(self, key, feats):
        a = set()
        for (k,v) in feats.items():
            if k not in self.tf:
                self.tf[k] = 0
            self.tf[k] += v
            a.add(k)
        for k in a:
            if k not in self.df:
                self.df[k] = 0
            self.df[k] += 1
        self.docs[key] = feats
        self.idf = None
        return

    def get(self, key):
        return self.docs[key]

    def commit(self):
        if self.idf is None:
            n = math.log(len(self.docs))
            self.idf = {None: n}
            for (k,v) in self.df.items():
                if v <= 1: continue
                self.idf[k] = n - math.log(v)
        return

    def calcsim(self, feats1, feats2):
        assert self.idf is not None
        D = self.idf[None]
        f1 = { k: v*self.idf.get(k,D) for (k,v) in feats1.items() }
        f2 = { k: v*self.idf.get(k,D) for (k,v) in feats2.items() }
        n1 = sum( v*v for v in f1.values() )
        n2 = sum( v*v for v in f2.values() )
        if n1 == 0 or n2 == 0: return 0
        dot = sum( v1*f2[k] for (k,v1) in f1.items() if k in f2 )
        return dot/math.sqrt(n1*n2)

    def findsim(self, k0, threshold=0):
        f0 = self.docs[k0]
        a = []
        for (k1,f1) in self.docs.items():
            if k1 == k0: continue
            sim = self.calcsim(f0, f1)
            if sim < threshold: continue
            yield (sim, k1)
        return

    def findall(self, keys=None, threshold=0, verbose=False):
        if keys is None:
            items = list(self.docs.items())
        else:
            items = [ (k,self.docs[k]) for k in keys ]
        for (i,(k0,f0)) in enumerate(items):
            for (k1,f1) in items[i+1:]:
                sim = self.calcsim(f0, f1)
                if sim < threshold: continue
                yield (sim, k0, k1)
            if verbose:
                sys.stderr.write('.'); sys.stderr.flush()
        return
