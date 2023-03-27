#!/usr/bin/env python
import sys
import os.path
import logging
from html.parser import HTMLParser

SINGLE_TAGS = {'meta', 'hr', 'br', 'img'}

class Checker(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.name = None
        self.lineno = None
        self._tagstack = []
        return

    def error(self, s):
        print(f'{self.name}:{self.lineno}: {s}')
        return

    def handle_starttag(self, tag, attrs):
        if tag in SINGLE_TAGS:
            return
        self._tagstack.append((self.lineno, tag))
        return

    def handle_startendtag(self, tag, attrs):
        return

    def handle_endtag(self, tag):
        if not self._tagstack:
            self.error(f'</{tag}>')
            return
        if tag not in { tag for (_,tag) in self._tagstack }:
            self.logger.error(f'{self.name}:{self.lineno} invalid </{tag}>')
            return
        while self._tagstack:
            (lineno, prev) = self._tagstack.pop()
            if prev == tag: break
            self.logger.info(f'{self.name}:{lineno} <{prev}> closed by </{tag}>')
        return

    def close(self):
        HTMLParser.close(self)
        for (lineno, tag) in self._tagstack:
            self.logger.error(f'{self.name}:{lineno} remain <{tag}>')
        return

def htmlint(args):
    for path in args:
        name = os.path.basename(path)
        with open(path) as fp:
            p = Checker()
            p.name = name
            for (lineno, line) in enumerate(fp):
                p.lineno = lineno
                p.feed(line)
            p.close()
    return 0

def main(argv):
    import getopt
    def usage():
        print('usage: %s [-v] [file ...]' % argv[0])
        return 100
    try:
        (opts, args) = getopt.getopt(argv[1:], 'v')
    except getopt.GetoptError:
        return usage()
    level = logging.ERROR
    for (k, v) in opts:
        if k == '-v': level = logging.INFO
    if not args: return usage()

    logging.basicConfig(format='%(levelname)s %(message)s', level=level)

    return htmlint(args)

if __name__ == '__main__': sys.exit(main(sys.argv))
