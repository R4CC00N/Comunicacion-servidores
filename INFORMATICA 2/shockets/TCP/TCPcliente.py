from socket import *

serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)  # sock_stream solo para TCP
clientSocket.connect((serverName, serverPort))  # realiza la conexion caracteristica en TCP

mensaje = input('Introduzca la frase en minusculas : ')
clientSocket.send(mensaje.encode())  # el "send" no necesita parametros por que ya he establecido una comunicacion

mensajeModificado = clientSocket.recv(1024)
print(" Mensaje desde el servidor : ", mensajeModificado.decode())
clientSocket.close()
