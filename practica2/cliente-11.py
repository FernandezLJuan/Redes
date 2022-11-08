import socket
import sys,os
from time import sleep

IP=0
porto=0

for i in sys.argv[1:]:
	try:
	
		porto=int(i)
		
	except ValueError:
	
		IP=i
		
socketCliente=socket.socket(socket.AF_INET,socket.SOCK_STREAM,fileno=None)
socketCliente.connect(('',porto))

sleep(1)
print(socketCliente.recv(1024).decode())

print("Rematado")
mensaje='AAAAAAAA AAAAAA'
socketCliente.send(mensaje.encode())
socketCliente.close()
