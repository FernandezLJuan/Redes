import sys,os
import socket


porto=0

try:

	for a in sys.argv[1:]:

		try:
		
			porto=int(a)
		
		except ValueError:
		
			print("Só é válido un número de porto en formato numérico, non textual")
			
		except IndexError:
		
			print("Non se introduciron suficientes datos por terminal")
			
	try:
		socketServidor=socket.socket(socket.AF_INET,socket.SOCK_DGRAM,0,fileno=None)
		
	except AttributeError:

		print("A librería socket non posee ese atributo")
		
	except SyntaxError:

		print("Algún parámetro incorrecto na creación do socket")
		
	except OSError:

		print("Protocolo non soportado para o socket")
		

	try:
		socketServidor.bind(('',porto))
		
	except OSError:

		print("Non foi posible conectar o socket o porto introducido")
		socketServidor.close()
		sys.exit()
		

	linea_recibida='a'
	recibidos=0

	while True:

		try:
			linea_recibida,direcion=socketServidor.recvfrom(1024)
			
		except ValueError:
			print("Non é posible establecer ese tamaño de buffer")
			socketServidor.close()
			sys.exit()
		
		try:
			linea_recibida=linea_recibida.decode()
			
		except AttributeError:
		
			print("Non se puido descodificar a mensaxe recibida")
			socketServidor.close()
			sys.exit()
			

		print("Mensaxe recibida desde a direcion: ",direcion[0]," con porto: ",direcion[1]," de tamaño: ",len(linea_recibida))	
		
		print(linea_recibida)
		
		
		try:
			linea_recibida=str(linea_recibida)
			linea_recibida=linea_recibida.upper()
			
		except:
		
			print("Non foi posible convertir a liña a maiúscula")
			socketServidor.close()
			sys.exit()
		
		
		try:
			linea_recibida=str(linea_recibida)
			socketServidor.sendto(linea_recibida.encode(),(direcion[0],direcion[1]))
			
		except AttributeError:
		
			print("Non é posible codificar un número enteiro")
			socketServidor.close()
			sys.exit()
			
		except OSError:
		
			print("Non se puido enviar a liña")
			socketServidor.close()
			sys.exit()
		
		
		if linea_recibida=='':
		
			recibidos+=1
			
		if recibidos==2:
		
			break
		
		
	socketServidor.close()

except KeyboardInterrupt:

	sys.exit()
