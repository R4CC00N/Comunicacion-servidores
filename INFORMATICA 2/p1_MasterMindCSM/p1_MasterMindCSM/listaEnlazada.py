# Creamos la clase node
class nodo:
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next


# Creamos la clase linked_list
class listaEnlazada:
    def __init__(self):
        self.head = None

    # Método para agregar elementos en el frente de la linked list
    def aniadir_frente(self, data):
        self.head = nodo(data=data, next=self.head)

        # Método para verificar si la estructura de datos esta vacia

    def vacio(self):
        return self.head == None

    # Método para agregar elementos al final de la linked list
    def aniadir_fin(self, data):
        if not self.head:
            self.head = nodo(data=data)
            return
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = nodo(data=data)

    def primero(self):
        return self.head

    # Método para eleminar nodos
    def eliminar(self, key):
        curr = self.head
        prev = None
        while curr and curr.data != key:
            prev = curr
            curr = curr.next
        if prev is None:
            self.head = curr.next
        elif curr:
            prev.next = curr.next
            curr.next = None

    # Método para obtener el ultimo nodo
    def ultimo(self):
        temp = self.head
        while (temp.next is not None):
            temp = temp.next
        return temp.data

    # Método para imprimir la lista de nodos
    def mostrar(self):
        node = self.head
        while node != None:
            print(node.data, end=" => ")
            node = node.next

'''
s = listaEnlazada()  # Instancia de la clase
s.aniadir_frente(5)  # Agregamos un elemento al frente del nodo
s.aniadir_fin(8)  # Agregamos un elemento al final del nodo
s.aniadir_frente(9)  # Agregamos otro elemento al frente del nodo

s.mostrar()  # Imprimimos la lista de nodos
'''

