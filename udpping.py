#!/usr/bin/env python
import io
import sys
import logging
import socket
import time

def server(lport, maxsize=65536):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', lport))
    logging.info('server: listening: lport=%r' % lport)
    while True:
        (data, addr) = sock.recvfrom(maxsize)
        logging.info('server: received: data=%r, addr=%r' % (len(data), addr))
        sock.sendto(data, addr)
    return

def client(host, port, maxsize=65536, delay=1, timeout=1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    addr1 = (host, port)
    size = maxsize
    while True:
        data1 = b'\xcc' * size
        sock.sendto(data1, addr1)
        logging.info('client: sent: data=%r, addr=%r' % (len(data1), addr1))
        (data2, addr2) = sock.recvfrom(maxsize)
        logging.info('client: recv: data=%r, addr=%r' % (len(data2), addr2))
        time.sleep(delay)
    return

# main
def main(argv):
    import getopt
    def usage():
        print('usage: %s [-d] [-l lport] [-m maxsize] [-L delay] [host port]' % argv[0])
        return 100
    try:
        (opts, args) = getopt.getopt(argv[1:], 'dl:m:L:')
    except getopt.GetoptError:
        return usage()
    level = logging.INFO
    lport = None
    maxsize = 30000
    delay = 1
    for (k, v) in opts:
        if k == '-d': level = logging.DEBUG
        elif k == '-l': lport = int(v)
        elif k == '-m': maxsize = int(v)
        elif k == '-L': delay = int(v)
    if lport is None and len(args) < 2: return usage()

    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=level)
    if lport is not None:
        server(lport, maxsize=maxsize)
    else:
        host = args.pop(0)
        port = int(args.pop(0))
        client(host, port, maxsize=maxsize, delay=delay)
    return 0

if __name__ == '__main__': sys.exit(main(sys.argv))
