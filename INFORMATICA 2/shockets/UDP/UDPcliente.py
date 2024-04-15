from socket import *

serverName = '127.0.0.1' # funciona con "localhost"
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM) # shocket_dgram para udp siempre
mensaje = input('Introduzca la frase en minusculas : ')
clientSocket.sendto(mensaje.encode(), (serverName, serverPort))
# "sendto" lo usamos para enviar un mesaje
# ".encode" para codificar el mensaje,
# luego las cabeceras se encargaran de ingresar el puerto y el IP con (serverName, serverPort)
# ".decode" decodifica el mensaje
# "dirServidor" obtiene una dupla en la que almacena el mensaje y la direccion del servidor que regreso el mensaje

mensjMod, dirServidor = clientSocket.recvfrom(2048)
# dirServidor almacena la IP y el puerto que es lo mismo que nuestro serverName y serverPort
print(mensjMod.decode())
