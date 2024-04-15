import sys

mensaje = self.recibir()
codigo = mensaje.split(" ")
if "GANADO" in codigo:
    print("ADIOS")
    sys.exit()