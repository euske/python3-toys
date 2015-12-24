#!/usr/bin/env python
import sys
import socket
import asyncore

class Session(asyncore.dispatcher):

    bufsize = 4096
    delim = b'\n'

    def __init__(self, sock, name):
        asyncore.dispatcher.__init__(self, sock)
        self.name = name
        self.rbuf = b''
        self.wbuf = b''

    def readable(self):
        return True

    def writable(self):
        return (0 < len(self.wbuf))

    def handle_close(self):
        print('%s: disconnected' % self.name)

    def handle_read(self):
        data = self.recv(self.bufsize)
        if not data:
            self.close()
            return
        (data,t,left) = data.partition(self.delim)
        self.rbuf += data
        if t:
            self.wbuf = self.process(self.rbuf)
            self.rbuf = left

    def handle_write(self):
        nbytes = self.send(self.wbuf)
        self.wbuf = self.wbuf[nbytes:]

    def process(self, data):
        print('%s: recv: %r' % (self.name, data))
        return b'you said "%s"\r\n' % data.strip()

class Server(asyncore.dispatcher):

    def __init__(self, host='', port=8000):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind((host, port))
        self.listen(5)
        print('listening at %s:%r...' % (host, port))

    def handle_accepted(self, sock, addr):
        (host, port) = addr
        name = '%s:%d' % (host, port)
        print('%s: conntected' % name)
        Session(sock, name)

def main(argv):
    import getopt
    def usage():
        print ('usage: %s [-d] [host [port]]' % argv[0])
        return 100
    try:
        (opts, args) = getopt.getopt(argv[1:], 'd')
    except getopt.GetoptError:
        return usage()
    host = ''
    port = 8000
    debug = 0
    for (k, v) in opts:
        if k == '-d': debug += 1
    if args:
        host = args.pop(0)
    if args:
        port = int(args.pop(0))
    Server(host, port)
    asyncore.loop()
    return

if __name__ == '__main__': sys.exit(main(sys.argv))
