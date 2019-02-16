#!/usr/bin/env python
##
##  Simple HTTP server + Range request (iOS audio tag support)
##

import sys
import os
import re
from http import HTTPStatus
from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler

class RangeHTTPRequestHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        rs = self.headers.get('Range')
        if rs:
            z = self.send_head_partial(rs)
            if z:
                (f,offset,nbytes) = z
                try:
                    f.seek(offset)
                    data = f.read(nbytes)
                    self.wfile.write(data)
                finally:
                    f.close()
        else:
            SimpleHTTPRequestHandler.do_GET(self)
        return

    def do_HEAD(self):
        rs = self.headers.get('Range')
        if rs:
            z = self.send_head_partial(rs)
            if z:
                z[0].close()
        else:
            SimpleHTTPRequestHandler.do_HEAD(self)
        return

    RANGE = re.compile(r'bytes=(\d+)(-\d+)?', re.I)

    def send_head_partial(self, rs):
        m = self.RANGE.match(rs)
        if not m:
            self.send_error(HTTPStatus.BAD_REQUEST)
            return None
        (s,e) = m.groups()
        if e is None:
            e = s
        else:
            e = e[1:]
        s = int(s)
        e = int(e)
        path = self.translate_path(self.path)
        ctype = self.guess_type(path)
        try:
            f = open(path, 'rb')
        except OSError:
            self.send_error(HTTPStatus.NOT_FOUND)
            return None
        fs = os.fstat(f.fileno())
        length = fs[6]
        if s < 0:
            s += length
        if e < 0:
            e += length
        nbytes = e+1-s
        try:
            self.send_response(HTTPStatus.PARTIAL_CONTENT)
            self.send_header('Content-Type', ctype)
            self.send_header('Content-Length', str(nbytes))
            self.send_header('Content-Range', 'bytes %d-%d/%d' % (s,e,length))
            self.send_header('Last-Modified', self.date_time_string(fs.st_mtime))
            self.end_headers()
        except:
            f.close()
            raise
        return (f, s, nbytes)

    def end_headers(self):
        self.send_header('Accept-Ranges', 'bytes')
        SimpleHTTPRequestHandler.end_headers(self)
        return

def main(argv):
    server_address = ('', 8000)
    RangeHTTPRequestHandler.protocol_version = 'HTTP/1.1'
    with HTTPServer(server_address, RangeHTTPRequestHandler) as httpd:
        sa = httpd.socket.getsockname()
        serve_message = 'Serving HTTP on {host} port {port} (http://{host}:{port}/) ...'
        print(serve_message.format(host=sa[0], port=sa[1]))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\nKeyboard interrupt received, exiting.')
    return

if __name__ == '__main__': sys.exit(main(sys.argv))
