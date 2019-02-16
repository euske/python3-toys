#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# sortby.py - sort files/directories by size/date.
#
# Usage:
#   $ sortby.py {-t|-s} [-r] [-q] [-a] [-D] [-f format] [path ...]
#
# Options:
#   -t: sort by last modified time (mtime).
#   -s: sort by file size.
#   -r: reverse order.
#   -q: only show file names.
#   -a: show files and directories.
#   -D: show directories only.
#   -f format: specify date format (default: %Y/%m/%d %H:%M:%S)
#
import sys
import os
import os.path
import stat
import time

def main(argv):
    import getopt
    def usage():
        print('usage: %s {-t|-s} [-r] [-q] [-a] [-D] [-f format] [path ...]' % argv[0])
        return 100
    try:
        (opts, args) = getopt.getopt(argv[1:], 'tsrqaDf:')
    except getopt.GetoptError:
        return usage()
    rev = False
    dirok = False
    fileok = True
    verbose = 1
    format = '%Y/%m/%d %H:%M:%S'
    fvalue = (lambda path: os.stat(path)[stat.ST_MTIME])
    fdisp = (lambda value: time.strftime(format, time.localtime(value)))
    for (k, v) in opts:
        if k == '-r': rev = True
        elif k == '-s':
            fvalue = (lambda path: os.stat(path)[stat.ST_SIZE])
            fdisp = str
        elif k == '-q': verbose -= 1
        elif k == '-a': (dirok, fileok) = (True, True)
        elif k == '-D': (dirok, fileok) = (True, False)
        elif k == '-f': format = v
    files = []
    def rec(path):
        if os.path.exists(path):
            if os.path.islink(path): return
            if (fileok and os.path.isfile(path)) or (dirok and os.path.isdir(path)):
                files.append((fvalue(path), path))
            if os.path.isdir(path):
                try:
                    for fname in os.listdir(path):
                        rec(os.path.join(path, fname))
                except OSError:
                    pass
        else:
            print('File does not exist: %r' % path, file=sys.stderr)
    for path in (args or ['.']):
        rec(path)
    for (value,fname) in sorted(files, reverse=rev):
        if verbose:
            print(fdisp(value), fname)
        else:
            print(fname)
    return

if __name__ == '__main__': sys.exit(main(sys.argv))
