import sys,socket
from time import sleep

porto=0
portoDestino=0

try:

	porto=int(sys.argv[1:][0])
	portoDestino=int(sys.argv[1:][2])
	

except ValueError:

	print("Non se poden introducir os portos como texto, só como número")
	
except IndexError:

	print("Insuficientes elementos proporcionados o programa")
	

try: 

	IP_destino=int(sys.argv[1:][1])
	nomeFicheiro=int(sys.argv[1:][3])
	
except ValueError:

	IP_destino=sys.argv[1:][1]
	nomeFicheiro=sys.argv[1:][3]
	
except IndexError:

	print("Insuficientes elementos proporcionados o programa")


try:
	socketCliente=socket.socket(socket.AF_INET,socket.SOCK_DGRAM,0,fileno=None)
	
except AttributeError:

	print("Socket non conta con ese atributo, imposible crear o socket")
	sys.exit()
	
except OSError:

	print("Non se puido crear o socket correctamente")
	
except SyntaxError:

	print("Algún parámetro incorrecto na creación do socket")


try:
	socketCliente.bind(('',porto))
except OSError:

	print("Non se puido conectar o socket o porto")
	sys.exit()

try:
	arquivo=open(nomeFicheiro+'.txt',"r")
	
except FileNotFoundError:

	print("Arquivo non atopado")
	socketCliente.close()
	sys.exit()
	
lineas=[]

for a in arquivo:

	lineas.append(a)
	
arquivo.close()

ficheiroDestino=nomeFicheiro.upper()

try:
	escritura=open(ficheiroDestino+'.txt',"w")

except FileNotFoundError:
	print("Non se atopou o arquivo introducido")
	socketCliente.close()
	sys.exit()

lineas_mayusculas=''
i=0


while len(lineas_mayusculas)<len(lineas):

	envio_linea=lineas[i]

	sleep(2)
	try:
		tamanho=socketCliente.sendto(envio_linea.encode(),(IP_destino,portoDestino))
		
		print("Tamaño de datos enviados: ",tamanho)
		
	except:
		print("Houbo un erro enviando os datos")
		break
	
	try:
		lineas_mayusculas=socketCliente.recvfrom(1024)[0].decode()
	
	except:
	
		print("Houbo un erro recibindo os datos")
		
	print(lineas_mayusculas)
	
	
	try:
		escritura.write(lineas_mayusculas)
		
	except TypeError:
	
		print("Non é o tipo correcto para escribir no arquivo")
	i+=1
	

escritura.close()

linea_final=''
try:
	socketCliente.sendto(linea_final.encode(),(IP_destino,portoDestino))
	
except:

	print("Erro enviando os datos")
	socketCliente.close()
	sys.exit()
	
socketCliente.close()
