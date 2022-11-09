import socket
import os,sys
from time import sleep

for i in sys.argv[1:]:

	porto=int(i)

servidor=socket.socket(socket.AF_INET,socket.SOCK_STREAM, 0, fileno=None)
servidor.bind(('0.0.0.0',porto))

servidor.listen(4)
s,direcion=servidor.accept()

while True:

	mensaje=s.recv(4096)
	mensaje=mensaje.decode()
	
	if len(mensaje)==0:
		print("Mensaje vacío, terminando conexión")
		break;

	s.send(mensaje.upper().encode())

	
s.close()
servidor.close()
