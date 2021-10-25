#!/usr/bin/env python
##
##  rtspclient.py - simple RTSP client
##  (only works with GStreamer with MJPEG stream for now)
##  - RFC 7826 (RTSP)
##  - RFC 3550 (RTP)
##  - RFC 2435 (RTP JPEG)
##
##  server$ ./test-launch 'videotestsrc ! rtpjpegpay name=pay0 pt=96'
##  client$ python rtspclient.py [-v] [-l lport] rtsp://host/test
##
import io
import sys
import logging
import socket
import select
import struct
import urllib.parse
from datetime import datetime, timedelta

# NTP2POSIX: timedelta
#   NTP Epoch: 1900/1/1 00:00:00
#   UTC Epoch: 1970/1/1 00:00:00
NTP2POSIX = (datetime(1900,1,1) - datetime(1970,1,1)).total_seconds()

# cf. https://gitlab.freedesktop.org/gstreamer/gst-plugins-good/-/blob/master/gst/rtp/gstrtpjpegdepay.c
lum_dc = (
    bytes([0, 1, 5, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]), # codelen
    bytes([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]),           # symbol
)
lum_ac = (
    bytes([0, 2, 1, 3, 3, 2, 4, 3, 5, 5, 4, 4, 0, 0, 1, 0x7d]), # codelen
    bytes([                                                    # symbol
  0x01, 0x02, 0x03, 0x00, 0x04, 0x11, 0x05, 0x12,
  0x21, 0x31, 0x41, 0x06, 0x13, 0x51, 0x61, 0x07,
  0x22, 0x71, 0x14, 0x32, 0x81, 0x91, 0xa1, 0x08,
  0x23, 0x42, 0xb1, 0xc1, 0x15, 0x52, 0xd1, 0xf0,
  0x24, 0x33, 0x62, 0x72, 0x82, 0x09, 0x0a, 0x16,
  0x17, 0x18, 0x19, 0x1a, 0x25, 0x26, 0x27, 0x28,
  0x29, 0x2a, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39,
  0x3a, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x49,
  0x4a, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59,
  0x5a, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69,
  0x6a, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79,
  0x7a, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89,
  0x8a, 0x92, 0x93, 0x94, 0x95, 0x96, 0x97, 0x98,
  0x99, 0x9a, 0xa2, 0xa3, 0xa4, 0xa5, 0xa6, 0xa7,
  0xa8, 0xa9, 0xaa, 0xb2, 0xb3, 0xb4, 0xb5, 0xb6,
  0xb7, 0xb8, 0xb9, 0xba, 0xc2, 0xc3, 0xc4, 0xc5,
  0xc6, 0xc7, 0xc8, 0xc9, 0xca, 0xd2, 0xd3, 0xd4,
  0xd5, 0xd6, 0xd7, 0xd8, 0xd9, 0xda, 0xe1, 0xe2,
  0xe3, 0xe4, 0xe5, 0xe6, 0xe7, 0xe8, 0xe9, 0xea,
  0xf1, 0xf2, 0xf3, 0xf4, 0xf5, 0xf6, 0xf7, 0xf8,
  0xf9, 0xfa])
)
chm_dc = (
    bytes([0, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]), # codelen
    bytes([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]),           # symbol
)
chm_ac = (
    bytes([0, 2, 1, 2, 4, 4, 3, 4, 7, 5, 4, 4, 0, 1, 2, 0x77]), # codelen
    bytes([                                                    # symbol
  0x00, 0x01, 0x02, 0x03, 0x11, 0x04, 0x05, 0x21,
  0x31, 0x06, 0x12, 0x41, 0x51, 0x07, 0x61, 0x71,
  0x13, 0x22, 0x32, 0x81, 0x08, 0x14, 0x42, 0x91,
  0xa1, 0xb1, 0xc1, 0x09, 0x23, 0x33, 0x52, 0xf0,
  0x15, 0x62, 0x72, 0xd1, 0x0a, 0x16, 0x24, 0x34,
  0xe1, 0x25, 0xf1, 0x17, 0x18, 0x19, 0x1a, 0x26,
  0x27, 0x28, 0x29, 0x2a, 0x35, 0x36, 0x37, 0x38,
  0x39, 0x3a, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48,
  0x49, 0x4a, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58,
  0x59, 0x5a, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68,
  0x69, 0x6a, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78,
  0x79, 0x7a, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87,
  0x88, 0x89, 0x8a, 0x92, 0x93, 0x94, 0x95, 0x96,
  0x97, 0x98, 0x99, 0x9a, 0xa2, 0xa3, 0xa4, 0xa5,
  0xa6, 0xa7, 0xa8, 0xa9, 0xaa, 0xb2, 0xb3, 0xb4,
  0xb5, 0xb6, 0xb7, 0xb8, 0xb9, 0xba, 0xc2, 0xc3,
  0xc4, 0xc5, 0xc6, 0xc7, 0xc8, 0xc9, 0xca, 0xd2,
  0xd3, 0xd4, 0xd5, 0xd6, 0xd7, 0xd8, 0xd9, 0xda,
  0xe2, 0xe3, 0xe4, 0xe5, 0xe6, 0xe7, 0xe8, 0xe9,
  0xea, 0xf2, 0xf3, 0xf4, 0xf5, 0xf6, 0xf7, 0xf8,
  0xf9, 0xfa])
)

def write_huffman_header(fp, code, tableno, tablecls):
    (codelen, symbol) = code
    fp.write(b'\xff\xc4') # DHT
    fp.write(struct.pack('>HB', 3+len(codelen)+len(symbol),
                         (tablecls << 4) | tableno))
    fp.write(codelen)
    fp.write(symbol)
    return

def write_quant_header(fp, qtable, tableno):
    fp.write(b'\xff\xdb') # DQT
    fp.write(struct.pack('>HB', 3+len(qtable), tableno))
    fp.write(qtable)
    return

def write_jpeg_header(fp, typ, width, height, qtable, prec, dri):
    fp.write(b'\xff\xd8') # SOI
    size0 = (128 if (prec & 1) else 64)
    write_quant_header(fp, qtable[:size0], 0)
    size1 = (128 if (prec & 2) else 64)
    write_quant_header(fp, qtable[size0:size0+size1], 1)
    if dri != 0:
        fp.write(b'\xff\xdd') # DRI
        fp.write(struct.pack('>H', 4))
        fp.write(struct.pack('>H', dri))
    fp.write(b'\xff\xc0') # SOF
    fp.write(struct.pack('>H', 8+3*3))
    fp.write(b'\x08')
    fp.write(struct.pack('>HH', height, width))
    fp.write(b'\x03')
    if (typ & 0x3f) == 0:
        fp.write(b'\x00\x21\x00')
    else:
        fp.write(b'\x00\x22\x00')
    fp.write(b'\x01\x11\x01')
    fp.write(b'\x02\x11\x01')
    write_huffman_header(fp, lum_dc, 0, 0)
    write_huffman_header(fp, lum_ac, 0, 1)
    write_huffman_header(fp, chm_dc, 1, 0)
    write_huffman_header(fp, chm_ac, 1, 1)
    fp.write(b'\xff\xda') # SOS
    fp.write(struct.pack('>H', 6+2*3))
    fp.write(b'\x03')
    fp.write(b'\x00\x00')
    fp.write(b'\x01\x11')
    fp.write(b'\x02\x11')
    fp.write(b'\x00\x3f\x00')
    return

def depay_jpeg(packets):
    buf = io.BytesIO()
    for data in packets:
        # cf. RFC 2435. ch.3
        (offset,) = struct.unpack('>L', data[:4])
        offset &= 0xffffff
        typ = data[4]
        q = data[5]
        width = data[6]*8
        height = data[7]*8
        i = 8
        dri = 0
        if 64 <= typ:
            (dri,_) = struct.unpack('>HH', data[i:i+4])
            i += 4
        if offset == 0:
            prec = 0
            if 128 <= q:
                (mbz,prec,length) = struct.unpack('>BBH', data[i:i+4])
                assert 0 < length
                i += 4
                qtable = data[i:i+length]
                i += length
            else:
                qtable = make_table(q) # NOTIMPL
            write_jpeg_header(buf, typ, width, height, qtable, prec, dri)
        buf.write(data[i:])
    return buf.getvalue()


##  RTSPClient
##
class RTSPClient:

    BUFSIZ = 65536

    def __init__(self, lport, url):
        # Initialize parameters.
        self.logger = logging.getLogger()
        self.url = url
        (scheme,netloc,self.path,_,_) = urllib.parse.urlsplit(url)
        assert scheme == 'rtsp'
        (self.host,_,port) = netloc.partition(':')
        self.rport_rtsp = int(port or '8554')
        self.lport_rtp = lport
        self.lport_rtcp = lport+1
        self.rport_rtp = None
        self.rport_rtcp = None
        self.session_key = None
        self.logger.info(
            f'initialize: host={self.host}, '
            f'rport_rtsp={self.rport_rtsp}, '
            f'lport_rtp={self.lport_rtp}, '
            f'lport_rtcp={self.lport_rtcp}')
        # Create sockets.
        self.sock_rtp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_rtp.setblocking(False)
        self.sock_rtp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock_rtp.bind(('', self.lport_rtp))
        self.sock_rtcp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_rtcp.setblocking(False)
        self.sock_rtcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock_rtcp.bind(('', self.lport_rtcp))
        #(_,self.lport_rtcp) = self.sock_rtcp.getsockname()
        self.sock_rtsp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_rtsp.connect((self.host, self.rport_rtsp))
        self.logger.info(
            f'connect: host={self.host}, '
            f'port={self.rport_rtsp}')
        # Internal variables.
        self._cseq = 0          # RTSP CSeq.
        self._rtp_pays = None   # RTP payload packets.
        self._rtp_seqno = None  # RTP last sequence no.
        self._last_ntp = None   # Last NTP timestamp.
        self._last_rts = None   # Last RTP timestamp.
        return

    # send_req: send a RTSP request and retrive the response.
    def send_req(self, req):
        self._cseq += 1
        buf = ('\r\n'.join(req)+f'\r\nCSeq: {self._cseq}\r\n\r\n').encode('ascii')
        self.logger.debug(f'send: {buf}')
        self.sock_rtsp.send(buf)
        resp = self.sock_rtsp.recv(self.BUFSIZ)
        self.logger.debug(f'recv: {resp}')
        return resp.decode('ascii').splitlines()

    # setup: send a SETUP request to the server.
    def setup(self):
        req = (
            f'SETUP {self.url} RTSP/1.0',
            f'Transport: RTP/AVP;unicast;client_port={self.lport_rtp}-{self.lport_rtcp}'
        )
        for line in self.send_req(req):
            if line.startswith('Session:'):
                (_,_,session) = line.partition(' ')
                (self.session_key,_,_) = session.partition(';')
            elif line.startswith('Transport:'):
                (_,_,transport) = line.partition(' ')
                for v in transport.split(';'):
                    if v.startswith('server_port='):
                        (_,_,prange) = v.partition('=')
                        (p0,_,p1) = prange.partition('-')
                        self.rport_rtp = int(p0)
                        self.rport_rtcp = int(p1)
        self.logger.info(
            f'SETUP: session_key={self.session_key}, '
            f'port_rtp={self.rport_rtp}, '
            f'port_rtcp={self.rport_rtcp}')
        return

    # play: send a PLAY request to the server.
    def play(self):
        req = (
            f'PLAY {self.url} RTSP/1.0',
            f'Session: {self.session_key}',
            'Range: npt=0-'
        )
        self.send_req(req)
        self.logger.info(f'PLAY')
        return

    # run: event loop
    def run(self, timeout=None):
        self._rtp_pays = None
        self._rtp_seqno = None
        # Send the dummy packet to initiate the stream.
        data = b'\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        self.sock_rtp.sendto(data, (self.host, self.rport_rtp))
        self.sock_rtcp.sendto(data, (self.host, self.rport_rtcp))
        epoll = select.epoll()
        epoll.register(self.sock_rtp, select.POLLIN)
        epoll.register(self.sock_rtcp, select.POLLIN)
        while True:
            # Poll RTP/RTCP ports.
            for (fd,event) in epoll.poll(timeout):
                if fd == self.sock_rtp.fileno():
                    (data, addr) = self.sock_rtp.recvfrom(self.BUFSIZ)
                    self.process_rtp(data)
                elif fd == self.sock_rtcp.fileno():
                    (data, addr) = self.sock_rtcp.recvfrom(self.BUFSIZ)
                    self.process_rtcp(data)
        return

    # process_rtp: process RTP packet.
    def process_rtp(self, data):
        (flags,pt,seqno,rts,ssrc) = struct.unpack('>BBHLL', data[:12])
        self.logger.debug(
            f'process_rtp: flags={flags}, '
            f'pt={pt}, seqno={seqno}, '
            f'rts={rts}, ssrc={ssrc}')
        if self._rtp_seqno != seqno:
            # Packet drop detected. Cancelling the current payload.
            self.logger.info(f'process_rtp: DROP')
            self._rtp_pays = None
        # Append to the payload (if it's not cancelled).
        if self._rtp_pays is not None:
            cc = flags & 0x0f
            self._rtp_pays.append(data[12+cc*4:])
        if pt & 0x80:
            # Significant packet - ending the payload.
            if self._rtp_pays is not None:
                timestamp = None
                # When possible, calculate the timestamp based on the last SR.
                if self._last_ntp is not None and self._last_rts is not None:
                    # RTP timestamp is of base 90000Hz.
                    dt = (rts - self._last_rts) / 90000
                    timestamp = self._last_ntp + timedelta(seconds=dt)
                # Depayload JPEG.
                frame = depay_jpeg(self._rtp_pays)
                self.process_rtp_frame(timestamp, frame)
            self._rtp_pays = []
        self._rtp_seqno = seqno+1
        return

    # process_rtcp: process RTCP SR packet.
    def process_rtcp(self, data):
        (flags,pt,length,ssrc) = struct.unpack('>BBHL', data[:8])
        self.logger.debug(
            f'process_rtcp: flags={flags}, '
            f'pt={pt}, length={length}, ssrc={ssrc}')
        assert pt == 200 # RTCP
        # Conver the NTP timestamp to UTC.
        (ntpmsw, ntplsw, rts) = struct.unpack('>LLL', data[8:20])
        fraction = ntplsw / (1<<32)
        self._last_ntp = datetime.fromtimestamp(ntpmsw + NTP2POSIX + fraction)
        self._last_rts = rts
        self.logger.debug(
            f'process_rtcp: sync: '
            f'last_ntp={self._last_ntp}, last_rts={self._last_rts}')
        return

    # process_rtp_frame: process a frame (JPEG).
    # [Override]
    def process_rtp_frame(self, timestamp, frame):
        self.logger.info(
            f'process_rtp_frame: timestamp={timestamp}, '
            f'frame={len(frame)}')
        with open('./out.jpg', 'wb') as fp:
            fp.write(frame)
        return

# main
def main(argv):
    import getopt
    def usage():
        print(f'usage: {argv[0]} [-d] [-l lport] rtsp://host:port/path')
        return 100
    try:
        (opts, args) = getopt.getopt(argv[1:], 'dl:')
    except getopt.GetoptError:
        return usage()
    level = logging.INFO
    lport = 10000
    for (k, v) in opts:
        if k == '-d': level = logging.DEBUG
        elif k == '-l': lport = int(v)
    if not args: return usage()

    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=level)

    url = args.pop(0)
    client = RTSPClient(lport, url)
    client.setup()
    client.play()
    client.run()
    return 0

if __name__ == '__main__': sys.exit(main(sys.argv))
