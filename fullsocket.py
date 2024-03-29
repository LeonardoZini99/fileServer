__author__ = 'paolo'
# 12/2015

import socket
import struct

class FullSocket:
    def __init__(self, sock=None):
        self.MSGLEN = 4
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        else:
            self.sock = sock

    def accept(self):
        return self.sock.accept()

    def bind(self,(host, port)):
        self.sock.bind((host, port))

    def close(self):
        self.sock.close()

    def connect(self, (host, port)):
        self.sock.connect((host, port))

    def getsockname(self):
        return self.sock.getsockname()

    def listen(self,backlog):
        self.sock.listen(backlog)

    def recv(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < self.MSGLEN:
            chunk = self.sock.recv(min(self.MSGLEN - bytes_recd, 2048))
            if chunk == '':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        nstr  = ''.join(chunks)
        nsize = struct.unpack('I',nstr)
        size  = socket.ntohl(nsize[0])
        chunks = []
        bytes_recd = 0
        while bytes_recd < size:
            chunk = self.sock.recv(min(size - bytes_recd, 2048))
            if chunk == '':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return ''.join(chunks)

    def send(self, msg):
        size=len(msg)               # send msg length as unsigned integer
        nsize=socket.htonl(size)    #
        nstr=struct.pack('I',nsize)
        sizelen=len(nstr)
        totalsent = 0
        while totalsent < sizelen:
            sent = self.sock.send(nstr[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

        totalsent = 0
        while totalsent < size:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent
