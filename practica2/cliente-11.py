import socket
import sys,os

socketCliente=socket.socket(socket.AF_INET,socket.SOCK_STREAM,fileno=None)
socketCliente.connect(('',37001))

