import sys,os
import socket
import struct


try:

	for a in sys.argv[1:]:

		try:
	
			porto=int(a)
	
		except ValueError:
	
			print("Só é válido un número de porto en formato numérico, non textual")
		
		except IndexError:
		
			print("Non se introduciron suficientes datos por terminal")
		

	socketReceptor=socket.socket(socket.AF_INET,socket.SOCK_DGRAM, 0, fileno=None)

	try:

		socketReceptor.bind(('',porto))

	except OSError:

		print("Non foi posible realizar a conexión do receptor")

	while True:

		mensaxe_textual,direcion=socketReceptor.recvfrom(1024)
	
		mensaxe_float,direcion=socketReceptor.recvfrom(1024)
	
	
		print("Enviouse: ", mensaxe_textual.decode()," desde ",direcion[1])
	
	
		try:
			print("Enviouse: ",struct.unpack(str(int(len(mensaxe_float)/8))+'d',mensaxe_float)," desde ",direcion[1])
	
		except struct.error:
	
			print("Erro o desempacar os datos enviados polo emisor")
			socketReceptor.close()
			sys.exit()
	
		if mensaxe_textual!='':
	
			break;
		
	socketReceptor.close()
	
except KeyboardInterrupt:

	print("A execucion foi rematada polo usuario")
