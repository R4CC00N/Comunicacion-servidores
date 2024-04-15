# clase hija
import time
from socket import *
import sys
import getopt
import Barra_de_carga
from newSocket import *


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
        self.clientSocket = newSocket(
            socket(AF_INET, SOCK_STREAM))  # lo convertimos en una variable de la clase nueva del socket
        self.clientSocket.connect((self.serverIp, self.serverPort))  # doble parentesis porque es la llamda y la tupla

        msj = "hello#MM" + "#" + str(self.clientName)
        self.send(msj)

    def send(self, msg):  # no ponemos el input pq no cumple lo que es una caja negra
        # para mandar mi nombre con el mensaje
        # el mensaje debe ser la combinacion de colores
        self.clientSocket.send(msg.encode())

    def recibir(self):
        mensajeModificado = self.clientSocket.recv(1024)  # tamaño buffer
        msg = mensajeModificado.decode()
        text = msg
        return text

    def close(self):
        self.clientSocket.close()

    def game_phase1_p1(self):
        print()
        print("TURNO DE JUGAR")
        msg = input("ingrese jugada con 'colors': ")
        if msg.split()[0] == "secretcode":
            print("Ha ingresado mal la clave, intentelo de nuevo con alguno de estos parametros: \n "
                  "*introduzca 'colors' seguido de su intento ")
            self.game_phase1_p1()
        else:
            parsemsg = self.parseMyturn(msg)  # puede estas dentro del cliente la clase importada
            if parsemsg == "0":
                print("Ha ingresado mal la clave, intentelo de nuevo con alguno de estos parametros: \n "
                      "*introduzca 'colors' seguido de su intento ")
            else:
                self.send(parsemsg)
                resultado = self.recibir()
                codigo = resultado.split(" ")
                if "perdido." in codigo:
                    print()
                    print(self.clientName)
                    print(resultado)
                    self.game_init = False
                    print("ya se deberia acabar o esperar")
                    # sys.exit()
                elif codigo[0].lower() == "terminando":
                    print()
                    print(self.clientName)
                    print(resultado)
                    self.game_init = False
                    sys.exit("cerrando...")
                elif "ganado" in codigo:
                    print()
                    print(self.clientName)
                    print(resultado)
                    msg = f"cambio#MM#{self.clientName}"
                    self.send(msg)
                    self.game_init = False
                    print("ya se deberia acabar o esperar")
                    p2_recibe = self.recibir()
                    print(p2_recibe)
                    if p2_recibe == "cambio":
                        self.game_phase1_p2()
                        mensaje_server = self.recibir()
                        print(mensaje_server)
                        if mensaje_server == "listo":
                            pass
                        else:
                            print(mensaje_server)
                else:
                    print(resultado)
                    # sys.exit()

    def game_phase1_p2(self):
        print()
        game2 = False
        msg = input("ingrese codigo secreto con 'secretcode': ")
        if msg.split()[0] == "colors":
            print("Ha ingresado mal la clave, intentelo de nuevo con alguno de estos parametros: \n*introduzca "
                  "'secretcode' seguido de la clave que va a adivinar ")
            self.game_phase1_p2()
        else:
            parsemsg = self.parseMyturn(msg)  # puede estas dentro del cliente la clase importada
            if parsemsg == "0":
                print("Ha ingresado mal la clave, intentelo de nuevo con alguno de estos parametros: \n*introduzca "
                      "'secretcode' seguido de la clave que va a adivinar ")
            else:
                self.send(parsemsg)
                resultado = self.recibir()
                codigo = resultado.split()
                if codigo[0].lower() == "terminando":
                    print()
                    print(self.clientName)
                    print(resultado)
                    self.game_init = False
                    sys.exit("cerrando...")

        while not game2:
            resultado = self.recibir()
            if resultado == "cambio":
                if self.clientSocket is None:
                    self.connet()
                res = self.recibir()
                if res == "listo":
                    game2 = True
            else:
                print(resultado)
        while game2:
            if self.clientSocket is None:
                self.connet()
            self.game_phase1_p1()

    def comunicacion(self):  # aqui hace todos los calculos
        game = False
        x = input("1. crear\n2. unirse\n3. salir\nESCOGE: ")

        if x == "1":
            print("Hola vamos a juga")
            while not self.game_init:
                game = False
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

            while not game:
                resultado = self.recibir()
                if resultado == "listo":
                    game = True

                else:
                    print(resultado)

            while game:
                print()
                if self.clientSocket is None:
                    self.connet()
                self.game_phase1_p1()

        elif x == "2":
            print("Hola vamos a unirnos a una partida")

            if self.clientSocket is None:
                self.connet()

            # Mensaje de union para recibir la lista de servidores
            msg_union = f"unirse#MM#{self.clientName}"
            self.send(msg_union)
            recive = self.recibir()
            print(recive)

            # mensaje para unirse a un servidor
            id_game = input("introduzca la partida a unirse: ")
            msj = f"id#{id_game}#{self.clientName}"
            self.send(msj)
            respuesta_p1 = self.recibir().split("#")
            print(respuesta_p1[0], respuesta_p1[1])
            self.game_phase1_p2()

        elif x == "3":
            print("Adios")
            exit(0)
        else:
            print("Porfavor digite una opcion valida")


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
