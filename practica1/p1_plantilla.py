import socket
import sys
import getopt
import binascii
import time
import argparse

#función que convirte a hexadecimal unha direción IP en forma decimal
def hexadecimal(direcion):

	try:#se é unha direción IPv4 podemos convertila directamente con binascii
		return str(binascii.hexlify(socket.inet_aton(direcion))).split("'")[1]
		
	except OSError:#no caso de ser unha direción IPv6 non será posible empregar binascii pero aproveitamos o feito de que xa está en hexadecimal e só precisamos concatenar os segmentos separados por ':'
	
		direcion=direcion.split(':')
		direcion_convertida=''
		for i in direcion:
		
			direcion_convertida+=i
			
		return direcion_convertida

#ao introducir un nome de host executase esta función
def parser_host(args):
		
	try:
		#intentamos obter as IP asociadas a ese host con getaddrinfo, ademais obtemos o nome canónico activando a flag socket.AI_CANONNAME
		addr4=socket.getaddrinfo(args.nome_host,"0",flags=socket.AI_CANONNAME)
		addr6=socket.getaddrinfo(args.nome_host,"0",socket.AF_INET6)
		
		print("Nombre canonico: ",addr4[0][3])
		
		#mostramos unha direción IPv4 e unha direción IPv6 asociadas
		print("****************************************************************")
		print("IPv4: {} {}".format(addr4[0][4][0],hexadecimal(addr4[0][4][0])))
		print("IPV6: {} {}".format(addr6[0][4][0],hexadecimal(addr6[0][4][0])))
		print("****************************************************************")

	except socket.gaierror:#en caso de qeu o host non se introducise correctamente ou se introducise un host inexistente indicaselle o usuario. Cando se introduce o host de maneira incorrecta lanzase un socket.gaierror igual que cando non existe o host, imposible diferenciar os casos
		
		print("Non hai direcións asociadas a este host")
		
		
#función que mostra o porto correspondente con un servizo
def parser_servizo(args):

	try:#o servizo debe ser unha cadea de caracteres (exemplo: http), polo tanto se ao convertilo a int non lanza unha excepción iso significa que o usuario tratou de introducir un número como servizo
		int(args.servizo)
		
		print("O servizo debe introducirse como o nome en texto")
	
	except ValueError:#se hai un erro o convertir a int o servizo entón existe a posibilidade de que se introducise un servizo válido
	
		try:
			porto=socket.getaddrinfo(None,args.servizo)
			print("****************************************************************")
			print("Servizo: {} Porto: {}".format(args.servizo,porto[0][4][1]))
			print("****************************************************************")
	
		except socket.gaierror:#se se introduciu un servizo inexistente lanzarase socket.gaierror indicando que non é válido
			print("O servizo introducido non é un servizo válido")


#indica o servizo correspondente a un porto
def parser_porto(args):

	try:#intentamos obter a información do porto con getservbyport
		print("****************************************************************")
		print("Porto: {} Servizo {}".format(args.porto,socket.getservbyport(args.porto)))
		print("****************************************************************")
			
	except OverflowError:#cando o número de porto introducido é demasiado grande (exemplo: 50000) lanzarase un OverflowError que se pode empregar para dicir o usuario que o porto que introduciu é demasiado grande
		
		print("Numero de porto demasiado longo")
		
	except OSError:#se o porto non existe facemos catch de OSError e indicamolo
	
		print("Porto non encontrado")


#proporciona información sobre unha ip introducida
def parser_ip(args):


	try:
			
		direcion=binascii.unhexlify(args.ip)#tratamos de convertir a ip introducida a binario, se lanza un binascii.Error sabemos que se introduciu en formato decimal
			
		try:#se a ip estaba en hexadecimal a operación atnerior non fallou e convertiuna a binario, primeiro tratamos de obter a conversión a decimal dunha IPv4 con inet_ntop, con esa conversión obtemos o host empregando gethostbyaddr
		
			direcion_decimal=socket.inet_ntop(socket.AF_INET,direcion)
			host=socket.gethostbyaddr(direcion_decimal)
			
			print("****************************************************************")
			print("Direcion IPV4: {}: {} : host {}".format(direcion_decimal,args.ip,host[0]))
			print("****************************************************************")

		#en caso de que a gethostbyaddr devolva un host inválido indicamos que se descoñece o host
		except socket.herror:
		
			print("Host descoñecido")

		except ValueError:#se tratamos de obter a versión decimal dunha direción ipv6 con inet_ntop e o parametro socket.AF_INET (correspondente a ipv6) entón este lanzará un ValueError, se isto ocurre sabemos que o usuario introduciu unha direción ipv6 en hexadecimal
		
			try:#obtemos a direción ipv6 en formato decimal e tamén o host
				direcion_decimal=socket.inet_ntop(socket.AF_INET6,direcion)
				host=socket.gethostbyaddr(direcion_decimal)
				
				print("****************************************************************")
				print("Direcion IPV6: {} {}: host {}".format(direcion_decimal,args.ip,host[0]))
				print("****************************************************************")
				
			except ValueError:#se inet_ntop lanza de novo un ValueError sabemos que a IP non é nin ipv4 nin ipv6, polo tanto, non é válida
			
				print("A cadea introducida non é valida")
				
			except socket.herror:
		
				print("Host descoñecido")
				
	except binascii.Error:#co binascii.Error na conversión a binario sabiamos que se introducira unha direción en formato decimal
		
		try:#tratamos de convertir a ip a hexadeximal e de obter o host
			direcion_hexadecimal=hexadecimal(args.ip)
			host=socket.gethostbyaddr(args.ip)
			

			if len(args.ip)<=12:#se a lonxitude da cadea é menor ou igual a 12 é unha direción IPv4
				
				print("****************************************************************")
				print("Direción IPv4:{} {}: host {} ".format(args.ip,hexadecimal(args.ip),host[0]))
				print("****************************************************************")
				
			else:#senón é IPv6
				print("****************************************************************")
				print("Direción IPv6:{} {}: host {} ".format(args.ip,hexadecimal(args.ip),host[0]))
				print("****************************************************************")
			
		except socket.gaierror:#non se atopou host para esa direción
		
			print("Non hai host asociado a esa direción IP")
			
		except socket.herror:#non se coñece o host
		
			print("Host descoñecido")


def main():
	#con isto preparamos para obter argumentos, a opcion --help e -h crease automáticamente
	parser = argparse.ArgumentParser(description='Práctica 1 de Redes e Comunicacións')
	#con isto engadimos argumentos, podense meter de 2 maneiras, opcion curta (con guion) e longa (con dous guions)
	#con dest damoslle un nome co que se gardara ao facer a función parse_args(), se non o poñemos o colle das opcions
	parser.add_argument('-n','--nome_host',type=str,dest='nome_host',action='store',help='Un nome de dirección de internet, coma www.usc.es') #a action='store' é o comportamnteto por defecto
	parser.add_argument('-s','--servizo',type=str,help='Un nome de sevizo, coma ssh')
	parser.add_argument('-p','--porto',type=int,help='Un numero de porto, coma 22')
	parser.add_argument('-i','--ip',type=str,help='Unha ip, en IPv4, IPv6 ou enteiro hexadecimal')
	args=parser.parse_args()

	if args.nome_host:
		
		parser_host(args)
	
	if args.servizo:
	
		parser_servizo(args)
			
	if args.porto:

		parser_porto(args)
	
	if args.ip:
		
		parser_ip(args)

	

		
if __name__ == "__main__":
    main()		
