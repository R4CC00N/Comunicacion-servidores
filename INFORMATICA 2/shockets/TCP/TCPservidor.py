from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("localhost", serverPort))
serverSocket.listen(1)  # Solicitudes en cola
print("El servidor esta listo para ser usado")
while True:
    clientsocket, direccion = serverSocket.accept()  # acepta la conexion del cliente
    mensaje = clientsocket.recv(1024)
    mayuscula = mensaje.decode().upper()
    clientsocket.send(mayuscula.encode())
    clientsocket.close()  # cierra la comunicacion que ha aceptado antes
