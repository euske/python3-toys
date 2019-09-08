#!/usr/bin/env python
##
##  dtree.py
##
##  Training:
##    $ dtree.py -k prop input.feats > out.tree
##
##  Testing:
##    $ dtree.py -k prop -f out.tree input.feats
##
import sys
from math import log2


# calcetp: calculates an entropy.
def calcetp(values):
    """
    >>> calcetp([1.0])
    0.0
    >>> calcetp([1.0, 0.5])
    0.9182958340544894
    """
    n = sum(values)
    etp = sum( v*log2(n/v) for v in values ) / n
    return etp

# countkeys: counts the number of keys.
def countkeys(keys):
    """
    >>> countkeys(['A', 'B', 'B'])
    {'A': 1, 'B': 2}
    """
    d = {}
    for k in keys:
        if k in d:
            d[k] += 1
        else:
            d[k] = 1
    return d

# argmax: chooses the e
def argmax(keys):
    """
    >>> argmax({'A':3, 'B':2, 'C':4})
    'C'
    """
    maxkey = None
    maxv = 0
    for (k,v) in keys.items():
        if maxkey is None or maxv < v:
            maxkey = k
            maxv = v
    assert maxkey is not None
    return maxkey

# entetp: compute the entropy of a given set of entries.
def entetp(ents, keyprop):
    return calcetp(countkeys( e[keyprop] for e in ents ).values())


##  Feature
##  Abstract class for features.
##
class Feature:

    class InvalidSplit(ValueError): pass

    def __init__(self, name, attr):
        self.name = name
        self.attr = attr
        return

    def __repr__(self):
        return ('<%s: %s>' % (self.__class__.__name__, self.name))

    # _get: returns a corresponding value for this feature.
    def _get(self, e):
        return e[self.attr]

    # ident: identify an entry for this feature.
    def ident(self, arg, e):
        raise NotImplementedError

    # split: split entries into multiple lists.
    def split(self, ents, keyprop):
        raise NotImplementedError

##  DiscreteFeature
##
class DiscreteFeature(Feature):

    def __init__(self, attr, prefix='DF:'):
        Feature.__init__(self, prefix+attr, attr)
        return

    def ident(self, arg, e):
        return self._get(e)

    def split(self, ents, keyprop):
        assert 2 <= len(ents)
        d = {}
        for e in ents:
            v = self._get(e)
            if v in d:
                d[v].append(e)
            else:
                d[v] = [e]
        if len(d) < 2: raise self.InvalidSplit
        n = len(ents)
        avgetp = sum( len(es) * entetp(es, keyprop) for es in d.values() ) / n
        split = list(d.items())
        return (avgetp, None, split)

DF = DiscreteFeature

##  DiscreteFeatureOne
##
class DiscreteFeatureOne(DiscreteFeature):

    def __init__(self, attr, index=0):
        self.index = index
        DiscreteFeature.__init__(self, attr, 'DF%d:' % index)
        return

    def _get(self, e):
        v = e[self.attr]
        if v is None: return None
        f = v.split(',')
        if len(f) <= self.index: return None
        return f[self.index]

DF1 = DiscreteFeatureOne

##  MembershipFeature
##
class MembershipFeature(Feature):

    def __init__(self, attr, prefix='MF:'):
        Feature.__init__(self, prefix+attr, attr)
        return

    def _get(self, e):
        v = e[self.attr]
        if v is None: return []
        return v.split(',')

    def ident(self, arg, e):
        return arg in self._get(e)

    def split(self, ents, keyprop):
        assert 2 <= len(ents)
        d = {}
        for e in ents:
            for v in self._get(e):
                if v in d:
                    es = d[v]
                else:
                    es = d[v] = set()
                es.add(e)
        if len(d) < 2: raise self.InvalidSplit
        n = len(ents)
        minsplit = minetp = None
        for (v,es) in d.items():
            nes = [ e for e in ents if e not in es ]
            if not nes: continue
            avgetp = (len(es)*entetp(es, keyprop) +
                      len(nes)*entetp(nes, keyprop)) / n
            if minsplit is None or avgetp < minetp:
                minetp = avgetp
                minsplit = (v, nes)
        if minsplit is None: raise self.InvalidSplit
        (arg, nes) = minsplit
        split = [(True, list(d[arg])), (False, nes)]
        return (minetp, arg, split)

MF = MembershipFeature

##  MembershipFeatureOne
##
class MembershipFeatureOne(MembershipFeature):

    def __init__(self, attr, nmems=1):
        self.nmems = nmems
        MembershipFeature.__init__(self, attr, 'MF%d:' % nmems)
        return

    def _get(self, e):
        v = e[self.attr]
        if v is None: return []
        return v.split(',')[:self.nmems]

MF1 = MembershipFeatureOne

##  QuantitativeFeature
##
class QuantitativeFeature(Feature):

    def __init__(self, attr, prefix='QF:'):
        Feature.__init__(self, prefix+attr, attr)
        return

    def ident(self, arg, e):
        v = self._get(e)
        if v is None:
            return 'un'
        elif v < arg:
            return 'lt'
        else:
            return 'ge'

    def split(self, ents, keyprop):
        assert 2 <= len(ents)
        pairs = []
        undefs = []
        for e in ents:
            v = self._get(e)
            if v is None:
                undefs.append(e)
            else:
                pairs.append((e, v))
        if not pairs: raise self.InvalidSplit
        pairs.sort(key=(lambda ev: ev[1]))
        es = [ e for (e,_) in pairs ]
        vs = [ v for (_,v) in pairs ]
        n = len(pairs)
        minsplit = minetp = None
        v0 = vs[0]
        for i in range(1, n):
            v1 = vs[i]
            if v0 == v1: continue
            v0 = v1
            avgetp = (i * entetp(es[:i], keyprop) +
                      (n-i) * entetp(es[i:], keyprop)) / n
            if minsplit is None or avgetp < minetp:
                minetp = avgetp
                minsplit = i
        if minsplit is None: raise self.InvalidSplit
        arg = vs[minsplit]
        split = [('lt', es[:minsplit]), ('ge', es[minsplit:])]
        if undefs:
            split.append(('un', undefs))
        return (minetp, arg, split)

QF = QuantitativeFeature


##  TreeBranch
##
class TreeBranch:

    def __init__(self, feature, arg, default, children):
        self.feature = feature
        self.arg = arg
        self.default = default
        self.children = children
        return

    def __repr__(self):
        return ('<TreeBranch(%r, %r)>' %
                (self.feature, self.arg))

    def test(self, e):
        v = self.feature.ident(self.arg, e)
        try:
            branch = self.children[v]
            return branch.test(e)
        except KeyError:
            #print ('Unknown value: %r: %r' % (self.feature, v))
            return self.default

    def dump(self, depth=0):
        ind = '  '*depth
        print ('%sBranch %r: %r, default=%r' %
               (ind, self.feature, self.arg, self.default))
        for (v,branch) in self.children.items():
            print ('%s Value: %r ->' % (ind, v))
            branch.dump(depth+1)
        return

# export_tree
def export_tree(tree):
    if isinstance(tree, TreeBranch):
        children = [ (v, export_tree(branch))
                     for (v,branch) in tree.children.items() ]
        return (tree.feature.name, tree.arg, tree.default, children)
    else:
        return (tree.key)


##  TreeLeaf
##
class TreeLeaf:

    def __init__(self, key):
        self.key = key
        return

    def __repr__(self):
        return ('<TreeLeaf(%r)>' % (self.key))

    def test(self, e):
        return self.key

    def dump(self, depth=0):
        ind = '  '*depth
        print ('%sLeaf %r' % (ind, self.key))
        return


##  TreeBuilder
##
class TreeBuilder:

    def __init__(self, minkeys=10, minetp=0.10, debug=1):
        self.keyprop = None
        self.features = {}
        self.minkeys = minkeys
        self.minetp = minetp
        self.debug = debug
        return

    def addfeat(self, feat):
        self.features[feat.name] = feat
        return

    def import_tree(self, tree):
        if isinstance(tree, tuple) or isinstance(tree, list):
            (name, arg, default, children) = tree
            children = { v: self.import_tree(branch) for (v,branch) in children }
            return TreeBranch(self.features[name], arg, default, children)
        else:
            return TreeLeaf(tree)

    def build(self, ents, depth=0):
        keys = countkeys( e[self.keyprop] for e in ents )
        etp = calcetp(keys.values())
        ind = '  '*depth
        if self.debug:
            print ('%sBuild: %r, etp=%.3f' % (ind, keys, etp))
        if etp < self.minetp:
            if self.debug:
                print ('%s Too little entropy. Stopping.' % ind)
            return None
        if len(ents) < self.minkeys:
            if self.debug:
                print ('%s Too few keys. Stopping.' % ind)
            return None
        minbranch = minetp = None
        for feat in self.features.values():
            try:
                (etp, arg, split) = feat.split(ents, self.keyprop)
            except Feature.InvalidSplit:
                continue
            if minbranch is None or etp < minetp:
                minetp = etp
                minbranch = (feat, arg, split)
        if minbranch is None:
            if self.debug:
                print ('%s No discerning feature. Stopping.' % ind)
            return None
        (feat, arg, split) = minbranch
        if self.debug:
            print ('%sFeature: %r, arg=%r, etp=%.3f' % (ind, feat, arg, etp))
        default = argmax(keys)
        children = {}
        for (i,(v,es)) in enumerate(split):
            if 2 <= self.debug:
                r = [ (e[feat.attr], e.key) for e in es ]
                print ('%s Split%d (%d): %r, %r' % (ind, i, len(r), v, r))
            if self.debug:
                print ('%s Value: %r ->' % (ind, v))
            branch = self.build(es, depth+1)
            if branch is None:
                keys = countkeys( e[self.keyprop] for e in es )
                best = argmax(keys)
                if self.debug:
                    print ('%s Leaf: %r -> %r' % (ind, v, best))
                branch = TreeLeaf(best)
            children[v] = branch
        return TreeBranch(feat, arg, default, children)


##  Setup Features
##
def setup(builder):
    builder.keyprop = 'Decision'
    builder.addfeat(DF('Outlook'))
    builder.addfeat(DF('Temp'))
    builder.addfeat(DF('Humidity'))
    builder.addfeat(DF('Wind'))
    return

# main
def main(argv):
    import json
    import getopt
    import fileinput
    def usage():
        print('usage: %s [-d] [-C] [-f feats] [-m minkeys] [file ...]' %
              argv[0])
        return 100
    try:
        (opts, args) = getopt.getopt(argv[1:], 'dCf:m:')
    except getopt.GetoptError:
        return usage()
    debug = 0
    usecsv = False
    feats = None
    minkeys = 1
    for (k, v) in opts:
        if k == '-d': debug += 1
        elif k == '-C': usecsv = True
        elif k == '-f': feats = v
        elif k == '-m': minkeys = int(v)

    builder = TreeBuilder(minkeys=minkeys, debug=debug)
    setup(builder)

    ents = []
    fp = fileinput.input(args)
    if usecsv:
        import csv
        props = None
        for row in csv.reader(fp):
            if props is None:
                props = row
            else:
                e = dict(zip(props, row))
                ents.append(e)
    else:
        for line in fp:
            e = json.loads(line)
            ents.append(e)

    if feats is None:
        # Training
        root = builder.build(ents)
        if debug:
            print()
            root.dump()
        print(json.dumps(export_tree(root)))

    else:
        # Testing
        with open(feats) as fp:
            data = json.loads(fp.read())
        tree = builder.import_tree(data)
        keys = {}     # given keys
        resp = {}     # given responses
        correct = {}  # correct responses
        keyprop = builder.keyprop
        for e in ents:
            ref = e[keyprop]
            keys[ref] = keys.get(ref,0)+1
            key = tree.test(e)
            resp[key] = resp.get(key,0)+1
            if e[keyprop] == key:
                correct[key] = correct.get(key,0)+1
        # Compute the precision and recall.
        for (k,v) in correct.items():
            prec = v/resp[k]
            recl = v/keys[k]
            f = 2*(prec*recl)/(prec+recl)
            print ('%s: prec=%.3f(%d/%d), recl=%.3f(%d/%d), F=%.3f' %
                   (k, prec, v, resp[k], recl, v, keys[k], f))
        print ('%d/%d' % (sum(correct.values()), sum(keys.values())))
    return 0

if __name__ == '__main__': sys.exit(main(sys.argv))
