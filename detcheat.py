#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# detcheat.py - cheat detector for Python codes.
#
# Usage:
#   $ detcheat.py *.py
#
# Options:
#   -d: debug mode.
#   -n ntop: show top n pairs (default: 10).
#
# The algorithm in this code is explained in:
#   https://theory.stanford.edu/~aiken/publications/papers/sigmod03.pdf
#

import sys
import tokenize

def kgrams(seq, k=5):
    n = len(seq)
    if n < k:
        yield seq
    else:
        for i in range(n - k + 1):
            yield seq[i:i+k]
    return

def winnow(seq, k=5):
    kgram = kgrams(seq, k)
    hashes = [ hash(''.join(x)) for x in kgram ]
    windows = kgrams(hashes, 4)
    s = {}
    for (i,window) in enumerate(windows):
        mh = min(window)
        s[mh] = i
    return s

def common(s0, s1):
    n = 0
    for k in s0.keys():
        if k in s1:
            n += 1
    return n

T_IGNORED = frozenset([
    tokenize.NEWLINE, tokenize.NL,
    tokenize.INDENT, tokenize.DEDENT,
    tokenize.COMMENT, tokenize.ENCODING,
])

KEYWORDS = frozenset([
    'assert', 'break', 'continue', 'del', 'elif', 'else', 'except',
    'exec', 'finally', 'for', 'global', 'if', 'lambda', 'pass',
    'print', 'raise', 'return', 'try', 'while', 'yield',
    'yield', 'as', 'with', 'from', 'import', 'def', 'class',
    'in', 'not', 'and', 'or',

    '__import__', 'abs', 'all', 'any', 'apply', 'basestring', 'bin',
    'bool', 'buffer', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod',
    'cmp', 'coerce', 'compile', 'complex', 'delattr', 'dict', 'dir', 'divmod',
    'enumerate', 'eval', 'execfile', 'exit', 'file', 'filter', 'float',
    'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'hex', 'id',
    'input', 'int', 'intern', 'isinstance', 'issubclass', 'iter', 'len',
    'list', 'locals', 'long', 'map', 'max', 'min', 'next', 'object',
    'oct', 'open', 'ord', 'pow', 'property', 'range', 'raw_input', 'reduce',
    'reload', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice',
    'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type',
    'unichr', 'unicode', 'vars', 'xrange', 'zip'
])

def gettokens(fp):
    for token in tokenize.tokenize(fp.readline):
        t = token.type
        s = token.string
        if t in T_IGNORED:
            pass
        elif t is tokenize.STRING:
            yield 'STR'
        elif t is tokenize.NUMBER:
            yield s
        elif t is tokenize.NAME:
            if s in KEYWORDS:
                yield s
            else:
                yield 'ID'
        elif s:
            yield s
    return

class SimDB:

    def __init__(self, debug=0):
        self.debug = debug
        self.results = []
        return

    def add(self, key, fp):
        try:
            tokens = list(gettokens(fp))
            if self.debug:
                print('tokens:', tokens)
            self.results.append((key, winnow(tokens)))
        except tokenize.TokenError:
            pass
        except UnicodeError:
            pass
        except SyntaxError:
            pass
        return

    def getsim(self, n=0):
        a = []
        for (i,(key0,ws0)) in enumerate(self.results):
            for (key1,ws1) in self.results[i+1:]:
                c = common(ws0, ws1)
                ratio = c/max(len(ws0), len(ws1))
                a.append((ratio, key0, key1))
        a.sort(key=lambda x:x[0], reverse=True)
        if n == 0:
            n = len(a)
        return a[:n]

def main(argv):
    import getopt
    def usage():
        print('usage: %s [-d] [-n ntop] [file ...]' % argv[0])
        return 100
    try:
        (opts, args) = getopt.getopt(argv[1:], 'dn:')
    except getopt.GetoptError:
        return usage()
    debug = 0
    ntop = 10
    for (k, v) in opts:
        if k == '-d': debug += 1
        elif k == '-n': ntop = int(v)
    #
    db = SimDB(debug=debug)
    for path in args:
        sys.stderr.write('Parsing: %r\n' % path)
        sys.stderr.flush()
        with open(path, 'rb') as fp:
            db.add(path, fp)
    for (ratio, path0, path1) in db.getsim(ntop):
        print('%.2f %s %s' % (ratio, path0, path1))
        if debug:
            with open(path0, 'r') as fp:
                print(fp.read())
            with open(path1, 'r') as fp:
                print(fp.read())
    return

if __name__ == '__main__': sys.exit(main(sys.argv))
