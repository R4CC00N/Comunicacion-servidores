from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
# "bind" accion de ligar o ajustar a ese puerto la recepcion del mensaje
# '' el mensaje vacio hace referencia a ti mismo en relacion a la IP
print("El servidor esta listo para ser usado")
while True: # un bucle infinito
    mensaje, dirCliente = serverSocket.recvfrom(2048)
    mensj_mod = mensaje.decode().upper() # decodifica y actua sobre el mensaje
    if mensj_mod == "PE": #ineccesario
        mensaje_fin = "CECILIA DEJA DE DECIR "+ mensj_mod
        serverSocket.sendto(mensaje_fin.encode(), dirCliente)
    serverSocket.sendto(mensj_mod.encode(), dirCliente)
    # dirClient almacena la IP y el puerto
