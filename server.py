import sys
import socket
from threading import Thread

class Reader(Thread):
    def __init__(self, sock, fp):
        Thread.__init__(self)
        self.sock = sock
        self.fp = fp
        
    def run(self):
        while True:
            data = self.sock.recv(1024)
            if not data: break
            self.fp.write(data)
            self.fp.flush()

class Writer(Thread):
    def __init__(self, fp, sock):
        Thread.__init__(self)
        self.fp = fp
        self.sock = sock
        
    def run(self):
        while True:
            data = self.fp.read(1)
            if not data: break
            data = data.replace(b'\r', b'')
            data = data.replace(b'\n', b'\r\n')
            self.sock.send(data)
        self.sock.shutdown(socket.SHUT_WR)

def main(argv):
    args = argv[1:]
    host = '0.0.0.0'
    port = int(args.pop(0))
    print('* Listening: %s:%d...' % (host, port))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(1)
    (conn,addr) = sock.accept()
    print('* Accepted: %s:%d' % addr)
    reader = Reader(conn, sys.stdout.buffer)
    reader.start()
    writer = Writer(sys.stdin.buffer, conn)
    writer.start()
    writer.join()
    print('* Closing...')
    reader.join()
    conn.close()
    return

main(sys.argv)
