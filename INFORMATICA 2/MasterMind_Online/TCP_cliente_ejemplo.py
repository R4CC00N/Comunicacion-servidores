# clase hija
from socket import *
import sys
import getopt
import Barra_de_carga
import menu


class ClienteTCP:

    # constructor
    def __init__(self, name, ip, port):  # variables clave y publicas
        self.clientName = name
        self.serverIp = ip
        self.serverPort = port
        self.clientSocket = None  # usamos esto que ahora mismo no esta definido
        # debemos crear algo para crear el socket y para conectarlo
        self.game_init = False

    def parseMyturn(self, code):
        valor = 0

        if isinstance(code, int):
            valor = "init#" + str(code) + "#" + str(self.clientName)
        else:
            codigo = code.split(" ")
            # usaremos la palabra clave "colors" para pasarle por parametro al servidor nuestro intento para jugar
            if codigo[0].lower() == "colors":
                valor = "colors#" + codigo[1]
            # usaremos la palabra clave "fin" para pasarle por parametro al servidor que vamos a terminar de jugar
            elif codigo[0].lower() == "fin":
                valor = "end#" + self.clientName
            # usaremos la palabra clave "secretcode" para pasarle por parametro al servidor el codigo secreo a adivinar
            elif codigo[0].lower() == "secretcode":
                valor = "secretcode#" + codigo[1]
        # si los valores no coinciden con nada retornara 0 y en el bucle while volvera a pedir el valor
        return str(valor)

    def connet(self):
        self.clientSocket = socket(AF_INET, SOCK_STREAM)  # lo convertimos en una variable de la clase
        self.clientSocket.connect((self.serverIp, self.serverPort))  # doble parentesis porque es la llamda y la tupla

    def send(self, mensaje):  # no ponemos el input pq no cumple lo que es una caja negra
        msg = mensaje  # para mandar mi nombre con el mensaje
        # el mensaje debe ser la combinacion de colores
        self.clientSocket.send(msg.encode())

    def recibir(self):
        mensajeModificado = self.clientSocket.recv(1024)  # tamaño buffer
        msg = mensajeModificado.decode()
        text = msg
        return text

    def close(self):
        self.clientSocket.close()

    def comunicacion(self):  # aqui hace todos los calculos
        # menu.ejecutar()
        while not self.game_init:
            if self.clientSocket is None:
                self.connet()

            msg = int(input("ingrese numero de rondas: "))
            parsemsg = self.parseMyturn(msg)  # puede estas dentro del cliente la clase importada
            if parsemsg == "0":
                print("Ha ingresado mal la clave, intentelo de nuevo")
            else:
                self.send(parsemsg)
                resultado = self.recibir()
                codigo = resultado.split(" ")
                print(resultado)
                # si el el mensaje recibido coincide con el string activara el bucle en True y se iniciara el juego
                if codigo[0].lower() == "iniciando":
                    # activaremos una barra de carga por estetica
                    Barra_de_carga.funcionamiento_barra()
                    self.game_init = True

        while self.game_init:
            print()
            if self.clientSocket is None:
                self.connet()

            msg = input("ingrese jugada: ")
            parsemsg = self.parseMyturn(msg)  # puede estas dentro del cliente la clase importada

            if parsemsg == "0":
                print("Ha ingresado mal la clave, intentelo de nuevo con alguno de estos parametros: \n *introduzca 'colors' seguido de su intento\n *introduzca 'secretcode' seguido de la clave que va a adivinar ")
            else:
                self.send(parsemsg)
                resultado = self.recibir()
                codigo = resultado.split(" ")
                print(resultado)
                if "perdido." in codigo:
                    print(self.clientName)
                    self.game_init = False
                    sys.exit()
                if codigo[0].lower() == "terminando":
                    print(self.clientName)
                    self.game_init = False
                    sys.exit("cerrando...")
                if "ganado" in codigo:
                    print(self.clientName)
                    self.game_init = False
                    sys.exit()


def conseguir_argumentos():
    name = None
    ip = "127.0.0.1"
    port = 1234

    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "n:i:p:", ["name=", "ip =", "port ="])
        #  comentando esto utiliza los valores por defecto
        #  se puede modificar cualquiera de los valores en terminal y los que no cambien seguiran siendo por defecto
        # if len(argv) < 3:
        #     print("Faltan valores")
        #     sys.exit()
    except:
        print("Error en los argumentos introduzca -n NOMBRE -i IP -p PUERTO")
        sys.exit()

    for opt, arg in opts:
        if opt in ['-i', '--ip']:
            ip = arg
        elif opt in ['-n', '--name']:
            name = arg
        elif opt in ['-p', '--port']:
            port = int(arg)

    return name, ip, port


def main():
    name, ip, serverPort = conseguir_argumentos()
    var = ClienteTCP(name, ip, serverPort)
    var.connet()
    var.comunicacion()
    var.close()
    exit(1)


if __name__ == "__main__":
    main()
