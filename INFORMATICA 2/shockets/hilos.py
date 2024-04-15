# import threading


# class MiHilo(threading.Thread):
#     def __init__(self, hilo):
#         threading.Thread.__init__(self)
#         self.numero = hilo

#     def run(self):
#         contador = 1
#         while contador <= 10:
#             print('ejecutando el Hilo ', self.numero, "run", contador) # se pisan los procesos uno a otro debido al print ya que no es un proceso atomico y trabaja a la misma velocidad que los hilos
#             contador += 1


# for numero in range(10):
#     hilo = MiHilo(numero)
#     hilo.start()

import threading

lista = []
lock = threading.Lock() # instancia un candado


def anyadir(obj): #añade a una lista propia los objetos
    lock.acquire() # permite acceder a un hilo uno a uno
    lista.append(obj) # añade ojbetos a la lista
    lock.release() # libera el candado para el siguiente hilo


def obtener():
    lock.acquire()
    obj = lista.pop()
    lock.release()
    return obj
