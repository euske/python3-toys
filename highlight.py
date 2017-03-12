#!/usr/bin/env python
import sys
import io
import re

STYLES = (
    'font-weight:bold; background:yellow; color:red;',
    'font-weight:bold; background:yellow; color:blue',
    'font-weight:bold; background:yellow; color:green',
    'font-weight:bold; background:black; color:yellow',
    'font-weight:bold; background:black; color:cyan',
)

# q(s)
def q(s):
    return (s.
            replace('&','&amp;').
            replace('>','&gt;').
            replace('<','&lt;').
            replace('"','&#34;').
            replace("'",'&#39;'))

# highlight(s, pats)
def highlight(s, pats):
    r = []
    for (pid,pat) in enumerate(pats):
        for m in pat.finditer(s):
            if m.start(0) < m.end(0):
                r.append((m.start(0), +(pid+1)))
                r.append((m.end(0), -(pid+1)))
    r.sort()
    (i0,pat0) = (0,None)
    a = set()
    for (i,p) in r:
        if 0 < p:
            a.add(p-1)
        else:
            a.remove(-p-1)
        if a:
            pat = pats[min(a)]
        else:
            pat = None
        if pat0 is not pat:
            if i0 < i:
                yield (pat0, s[i0:i])
            (i0,pat0) = (i,pat)
    assert not a and pat0 is None
    yield (pat0, s[i0:])
    return

# main
def main(argv):
    import getopt
    def usage():
        print ('usage: %s [-c cin] [-C cout] [pat ...]' % argv[0])
        return 100
    try:
        (opts, args) = getopt.getopt(argv[1:], 'c:C:')
    except getopt.GetoptError:
        return usage()
    cin = 'utf-8'
    cout = 'utf-8'
    for (k, v) in opts:
        if k == '-c': cin = v
        elif k == '-C': cout = v
    pats = []
    styles = []
    hmap = {None: '%s'}
    for (cid,arg) in enumerate(args):
        pat = re.compile(arg)
        cls = 'p_%s' % cid
        fmt = '<span class="%s">%%s</span>' % cls
        pats.append(pat)
        styles.append((cls, STYLES[cid % len(STYLES)]))
        hmap[pat] = fmt
    fin = io.TextIOWrapper(sys.stdin.buffer, encoding=cin)
    fout = io.TextIOWrapper(sys.stdout.buffer, encoding=cout)
    fout.write('<html><head><style>\n')
    for (cls,style) in styles:
        fout.write('.%s { %s }\n' % (cls, style))
    fout.write('</style></head><body><pre>')
    for line in fin:
        line = ''.join( (hmap[pat] % s) for (pat,s) in highlight(line, pats) )
        fout.write(line)
    fout.write('</pre></body></html>\n')
    return

if __name__ == '__main__': sys.exit(main(sys.argv))
