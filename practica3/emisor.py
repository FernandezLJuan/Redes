import sys,os
import socket
import struct

try:
	socketEmisor=socket.socket(socket.AF_INET,socket.SOCK_DGRAM, 0, fileno=None)
	try:
		
		porto_propio=int(sys.argv[1:][0])
		porto_destinatario=int(sys.argv[1:][1])
		
	except ValueError:
		
		print("Só é válido un número de porto en formato numérico, non textual")
		
	except IndexError:
		
		print("Non se introduciron suficientes elementos por terminal")
		

	try:

		IP=int(sys.argv[1:][2])
		

	except ValueError:

		IP=sys.argv[1:][2]
		
	except IndexError:

		print("Non se introduciron suficientes elementos por terminal")
		
		
	try:


		socketEmisor.bind(('',porto_propio))
		
	except OSError:

		print("Erro á hora de conectar o emisor")
		sys.exit()


	mensaje="CONEXION ESTABLECIDA"

	try:
		mensaxe_float=struct.pack('ddd',3.1415,1.2,3.8)
		
	except struct.error:

		print("Erro empacando os datos a enviar")
		socketEmisor.close()
		sys.exit()
	try:
		socketEmisor.sendto(mensaje.encode(),('',porto_destinatario))
		socketEmisor.sendto(mensaxe_float,('',porto_destinatario))
		
	except ValueError:

		print("Tipo de dato da mensaxe incorrecto, deben ser bytes")
		socketEmisor.close()
		sys.exit()
	socketEmisor.close()

except KeyboardInterrupt:

	print("Execución rematada polo usuario")
