from collections import deque
from colorsys import rgb_to_hsv, hsv_to_rgb
from PIL import Image

# 1. Agrupar colores similares y contar sus pixeles.
def extraer_colores(imagen):
    imagen = imagen.convert('RGB')
    imagen.thumbnail((160, 160))
    grupos = {}
    for r, g, b in imagen.getdata():
        clave = (r // 32, g // 32, b // 32)
        datos = grupos.setdefault(clave, [0, 0, 0, 0])
        datos[0] += r
        datos[1] += g
        datos[2] += b
        datos[3] += 1
    total = imagen.width * imagen.height
    colores = []
    for r, g, b, frecuencia in grupos.values():
        colores.append({'rgb': (r//frecuencia, g//frecuencia, b//frecuencia),
                        'frecuencia': frecuencia, 'porcentaje': 100*frecuencia/total})
    return burbuja(colores)[:5]

# 2. Bubble Sort: ordenar de mayor a menor frecuencia.
def burbuja(colores):
    for i in range(len(colores)-1):
        for j in range(len(colores)-1-i):
            if colores[j]['frecuencia'] < colores[j+1]['frecuencia']:
                colores[j], colores[j+1] = colores[j+1], colores[j]
    return colores


def tono(rgb):
    return rgb_to_hsv(*(x/255 for x in rgb))[0]*360

# 3. Puntuacion de armonia: favorece tonos cercanos.
def armonia(a, b):
    diferencia = abs(tono(a['rgb']) - tono(b['rgb']))
    distancia = min(diferencia, 360-diferencia)
    return max(0, 30-distancia/3)

# Programacion dinamica: elegir hasta 3 colores sin repetir.
# dp[k][i] = mejor puntuacion de k colores terminando en i.
def paleta_armonica(colores):
    n = len(colores)
    if not n:
        return [], 0
    cantidad = min(3, n)
    dp = [[float('-inf')]*n for _ in range(cantidad+1)]
    anterior = [[-1]*n for _ in range(cantidad+1)]
    for i in range(n):
        dp[1][i] = colores[i]['porcentaje']
    for k in range(2, cantidad+1):
        for i in range(k-1, n):
            for j in range(k-2, i):
                puntos = dp[k-1][j] + colores[i]['porcentaje'] + armonia(colores[j], colores[i])
                if puntos > dp[k][i]:
                    dp[k][i] = puntos
                    anterior[k][i] = j
    i = max(range(n), key=lambda i: dp[cantidad][i])
    puntos = dp[cantidad][i]
    paleta = []
    for k in range(cantidad, 0, -1):
        paleta.append(colores[i])
        i = anterior[k][i]
    return paleta[::-1], puntos

# 4. Grafo circular de 12 tonos, con dos vecinos por nodo.
def bfs(inicio):
    grafo = {i: [(i-1)%12, (i+1)%12] for i in range(12)}
    cola = deque([inicio])
    visitados = {inicio}
    recorrido = []
    while cola:
        nodo = cola.popleft()
        recorrido.append(nodo)
        for vecino in grafo[nodo]:
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append(vecino)
    return recorrido


def hexadecimal(rgb):
    return '#%02X%02X%02X' % rgb

