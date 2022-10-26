import socket
import sys,os

socketServer=socket.socket(socket.AF_INET,socket.SOCK_STREAM, 0, fileno=None)

cadea='Hola mundo'

socketServer.bind(('',37001))

socketServer.listen(4)

while 1:

	socketConexion,direcion=socketServer.accept()
	print("Conexion aceptada do cliente con direción: ",direcion[0])
	socketServer.close()
