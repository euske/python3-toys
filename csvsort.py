#!/usr/bin/env python
import sys
import csv
import fileinput

def main(argv):
    import getopt
    def usage():
        print(f'usage: {argv[0]} [-H] [-C encoding] [-c cols] [-n] [-r] [files ...]')
        return 100
    try:
        (opts, args) = getopt.getopt(argv[1:], 'HC:c:nr')
    except getopt.GetoptError:
        return usage()
    header = True
    encoding = 'utf-8'
    selection = []
    reverse = False
    numeric = False
    for (k, v) in opts:
        if k == '-H': header = False
        elif k == '-C': encoding = v
        elif k == '-c':
            for c in v.split(','):
                if '-' in c:
                    (c1,_,c2) = c.partition('-')
                    for i in range(int(c1), int(c2)+1):
                        selection.append(i)
                else:
                    selection.append(int(c))
        elif k == '-n': numeric = True
        elif k == '-r': reverse = True
    def f(row):
        if numeric:
            return tuple( int(row[c]) for c in selection )
        else:
            return tuple( row[c] for c in selection )
    fp = fileinput.input(args, openhook=(lambda path, mode: open(path, mode, encoding=encoding)))
    row0 = None
    rows = []
    for row in csv.reader(fp):
        if header:
            row0 = row
            header = False
        else:
            rows.append(row)
    rows.sort(key=f, reverse=reverse)
    writer = csv.writer(sys.stdout)
    if row0 is not None:
        writer.writerow(row0)
    for row in rows:
        writer.writerow(row)
    return 0

if __name__ == '__main__': sys.exit(main(sys.argv))
