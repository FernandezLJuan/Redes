import socket
import os,sys
from time import sleep

cliente=socket.socket(socket.AF_INET,socket.SOCK_STREAM, 0, fileno=None)
cliente.connect(('',1234))

archivo=open("mensaje_servidor.txt","r")
lineas=[]

for a in archivo:

	lineas.append(a)

archivo.close()

archivo=open("mensaje_servidor_CAP.txt","w")

lineas_mayusculas=[]
i=0

while len(lineas_mayusculas)<=len(lineas)-1:

	cliente.send(lineas[i].encode())
	mensaje=cliente.recv(4096).decode()
	
	lineas_mayusculas.append(mensaje)
	archivo.write(lineas_mayusculas[i])
	
	i+=1
	
archivo.close()
cliente.send(''.encode())
cliente.close()
