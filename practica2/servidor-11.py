import socket
import sys,os

porto=sys.argv[1:]

socketServer=socket.socket(socket.AF_INET,socket.SOCK_STREAM, 0, fileno=None)

cadea='Hola mundo'

socketServer.bind(('0.0.0.0',int(porto[0])))

socketServer.listen(4)

while True:

	socketConexion,direcion=socketServer.accept()
	print("Conexion aceptada do cliente con direción: ",direcion[0])
	mensaxe1='Hola, este es el servidor,'
	mensaxe2=' la conexion ha sido establecida correctamente'

	socketConexion.send(mensaxe1.encode())
	socketConexion.send(mensaxe2.encode())
	
	mensaxe_recibida=socketConexion.recv(8)

	print("Mensaxe recibida do servidor {}".format(mensaxe_recibida.decode()))


print('Cerramos la conexión')
socketConexion.close()
socketServer.close()
