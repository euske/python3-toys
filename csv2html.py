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

def main(argv):
    import getopt
    def usage():
        print('usage: %s [-h] [-c codec] [-T title] [files ...]' % argv[0])
        return 100
    try:
        (opts, args) = getopt.getopt(argv[1:], 'hc:T:')
    except getopt.GetoptError:
        return usage()
    header = False
    encoding = 'utf-8'
    title = ' '.join(args)
    for (k, v) in opts:
        if k == '-h': header = True
        elif k == '-c': encoding = v
        elif k == '-T': title = v
    fp = fileinput.input(args, openhook=(lambda path, mode: open(path, mode, encoding=encoding)))
    print('<html><head><title>%s</title><style>' % q(title))
    print('table { border-collapse: collapse; }')
    print('</style></head><body><table border>')
    for row in csv.reader(fp):
        if header:
            cols = ( '<th>%s</th>' % q(col) for col in row )
            header = False
        else:
            cols = ( '<td>%s</td>' % q(col) for col in row )
        print ('<tr>%s</tr>' % (''.join(cols)))
    print('</table></body></html>')
    return 0

if __name__ == '__main__': sys.exit(main(sys.argv))
