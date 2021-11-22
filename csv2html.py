#!/usr/bin/env python
import sys
import csv
import fileinput

def q(s):
    return (s.
            replace('&','&amp;').
            replace('>','&gt;').
            replace('<','&lt;').
            replace('"','&#34;').
            replace("'",'&#39;'))

def sel(row, cols):
    if not cols:
        return row
    else:
        return [ row[i] for i in cols ]

def main(argv):
    import getopt
    def usage():
        print(f'usage: {argv[0]} [-H] [-C encoding] [-T title] [-c cols] [files ...]')
        return 100
    try:
        (opts, args) = getopt.getopt(argv[1:], 'HC:T:c:')
    except getopt.GetoptError:
        return usage()
    header = True
    encoding = 'utf-8'
    title = ' '.join(args)
    selection = []
    for (k, v) in opts:
        if k == '-H': header = False
        elif k == '-C': encoding = v
        elif k == '-T': title = v
        elif k == '-c':
            for c in v.split(','):
                if '-' in c:
                    (c1,_,c2) = c.partition('-')
                    for i in range(int(c1), int(c2)+1):
                        selection.append(i)
                else:
                    selection.append(int(c))
    fp = fileinput.input(args, openhook=(lambda path, mode: open(path, mode, encoding=encoding)))
    print(f'<html><head><title>{q(title)}</title><style>')
    print('table { border-collapse: collapse; }')
    print('</style></head><body><table border>')
    for row in csv.reader(fp):
        if header:
            cols = ( f'<th>{q(col)}</th>' for col in sel(row, selection) )
            header = False
        else:
            cols = ( f'<td class=c{i}>{q(col)}</td>' for (i,col) in enumerate(sel(row, selection)) )
        print(f'<tr>{"".join(cols)}</tr>')
    print('</table></body></html>')
    return 0

if __name__ == '__main__': sys.exit(main(sys.argv))
