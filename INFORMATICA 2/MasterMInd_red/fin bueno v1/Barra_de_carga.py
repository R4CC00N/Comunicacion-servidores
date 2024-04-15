import time

limite = 40


def barra_segmento(segmento, total, longitud):
    porcentaje = segmento / total
    completado = int(porcentaje * longitud)
    restante = longitud - completado
    barra = f"[{'#' * completado}{'^' * restante}{porcentaje:.2%}]"
    return barra


def funcionamiento_barra():
    for i in range(limite + 1):
        time.sleep(0.05)
        print(barra_segmento(i, limite, 40), end="\r")


