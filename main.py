import streamlit as st
import pandas as pd
from pprint import pprint as pp
from functools import reduce
import copy
import pandas as pd
from models import X


def data_frame_a_lista(df):
    matriz = []
    for i in range(len(df)):
        for j in range(len(df.columns)):
            valor = df.iloc[i, j]
            try:
                valor = int(valor)
            except:
                valor = 0
            matriz.append(X(num=valor, posicion=(i, j)))
    return matriz


#  lista de X → DataFrame
def lista_a_data_frame(matriz_X):
    if not matriz_X:
        return pd.DataFrame()

    n_filas = max(x.posicion[0] for x in matriz_X) + 1
    n_cols = max(x.posicion[1] for x in matriz_X) + 1

    df_data = [[0 for _ in range(n_cols)] for _ in range(n_filas)]
    for x in matriz_X:
        df_data[x.posicion[0]][x.posicion[1]] = x.num

    return pd.DataFrame(df_data)


def matriz_estilos_ocultos(matriz_X):
    if not matriz_X:
        return pd.DataFrame()

    n_filas = max(x.posicion[0] for x in matriz_X) + 1
    n_cols = max(x.posicion[1] for x in matriz_X) + 1

    estilos = pd.DataFrame([["" for _ in range(n_cols)] for _ in range(n_filas)])

    for x in matriz_X:
        if x.oculto:
            estilos.iloc[x.posicion[0], x.posicion[1]] = (
                "background-color: red; color: white;"
            )

    return estilos


# asignamos color verde a las celdas que forman parte de ciertas coordenadas
def matriz_estilos_resultado(matriz_X, coordenadas: list[tuple[int, int]]):
    if not matriz_X:
        return pd.DataFrame()

    n_filas = max(x.posicion[0] for x in matriz_X) + 1
    n_cols = max(x.posicion[1] for x in matriz_X) + 1

    estilos = pd.DataFrame([["" for _ in range(n_cols)] for _ in range(n_filas)])

    for x in matriz_X:
        if x.posicion in coordenadas:
            estilos.iloc[x.posicion[0], x.posicion[1]] = (
                "background-color: green; color: white;"
            )

    return estilos


def buscar_menor_fila(matriz: list[X]) -> list[int]:
    longitud_matriz = int(len(matriz) ** (1 / 2))
    valores_menores: list[int] = [0] * longitud_matriz
    contador_fila: int = 0
    for x in matriz:
        if x.posicion[0] != contador_fila:
            contador_fila += 1
        if x.posicion[1] == 0:
            valores_menores[contador_fila] = x.num
        if x.posicion[0] == contador_fila:
            if valores_menores[contador_fila] > x.num:
                valores_menores[contador_fila] = x.num
    return valores_menores


def buscar_menor_columna(matriz: list[X]) -> list[int]:
    longitud_matriz = int(len(matriz) ** (1 / 2))
    valores_menores: list[X] = []
    for x in matriz:
        if x.posicion[0] == 0:
            valores_menores.append(x.num)

    for i in range(longitud_matriz):
        for x in matriz:
            if x.posicion[1] == i:
                if valores_menores[i] > x.num:
                    valores_menores[i] = x.num
    return valores_menores


def restar_valor_menor(
    valores_menores: list[int], matriz: list[X], fila: bool = False
) -> list[X]:
    matriz_aux = copy.deepcopy(matriz)
    contador_fila = 0
    if fila:
        for x in range(len(matriz_aux)):
            if contador_fila != matriz_aux[x].posicion[0]:
                contador_fila += 1
            if contador_fila == matriz_aux[x].posicion[0] and matriz_aux[x].num != 0:
                matriz_aux[x].num -= valores_menores[contador_fila]
        return matriz_aux
    else:

        contador_columna = 0
        for i in range(len(valores_menores)):
            for x in matriz_aux:
                if i == x.posicion[1] and x.num != 0:
                    x.num -= valores_menores[i]
        return matriz_aux


def cantidad_ceros_fil_col(matriz: list[X]) -> dict:
    lineas_filas = dict()
    lineas_columnas = dict()
    tamano_matriz = int(len(matriz) ** (1 / 2))
    # se construye un diccionario donde se guarda cuantos ceros tiene cada linea
    for i in range(tamano_matriz):
        lineas_filas[i] = 0
        lineas_columnas[i] = 0

    contador_fila = 0
    for x in matriz:
        if x.posicion[0] != contador_fila:
            contador_fila += 1
        if x.posicion[0] == contador_fila and x.num == 0 and x.oculto == False:
            lineas_filas[contador_fila] += 1

    for i in range(tamano_matriz):
        for x in matriz:
            if x.posicion[1] == i and x.num == 0 and x.oculto == False:
                lineas_columnas[i] += 1

    cantidad_ceros_total = reduce(
        lambda x, y: x + y, list(map(lambda x: lineas_columnas[x], lineas_columnas))
    )
    return lineas_filas, lineas_columnas, cantidad_ceros_total


def cantidad_ceros_no_asig_fil_col(matriz: list[X]) -> dict:
    lineas_filas = dict()
    lineas_columnas = dict()
    tamano_matriz = int(len(matriz) ** (1 / 2))
    # se construye un diccionario donde se guarda cuantos ceros tiene cada linea
    for i in range(tamano_matriz):
        lineas_filas[i] = 0
        lineas_columnas[i] = 0

    contador_fila = 0
    for x in matriz:
        if x.posicion[0] != contador_fila:
            contador_fila += 1
        if x.posicion[0] == contador_fila and x.num == 0 and x.asignado == False:
            lineas_filas[contador_fila] += 1

    for i in range(tamano_matriz):
        for x in matriz:
            if x.posicion[1] == i and x.num == 0 and x.asignado == False:
                lineas_columnas[i] += 1

    cantidad_ceros_total = reduce(
        lambda x, y: x + y, list(map(lambda x: lineas_columnas[x], lineas_columnas))
    )
    return lineas_filas, lineas_columnas, cantidad_ceros_total


# 1. Contar la cantidad de ceros en cada fila, cade columna y el total de la matriz
# 2. Contador de ceros
# 3. Mientras el contador sea menor a la cantidad de ceros totales de la matriz:
# 2. Sacar el valor mayor de la fila y de la columna en cuanto a la cantidad de ceros.
# 3. Vamos a comparar el mayor numero de ceros de la fila y de las columnas.
# 4. Si hay empate se oculta la fila:
# Se sumara la cantidad de ceros de la fila oculta  al contador
# Se sumara 1 a la marca de la celda
# 5. Si no se oculta la columna:
#   # Se sumara la cantidad de ceros de la columna que se esta ocultando.
#   # Se sumara 1 a la marca de la celda
# 6. Se obtendra el menor numero de las filas que no estan ocultas.
# 7. A las celdas que no tengan ninguna marca y no esten ocultas se les restara el minimo numero obtenido en el paso anterior
# 8. Se sumara el menor numero obtenido en el paso 6 a las celdas que esten marcadas 2 veces
# 9. Se le asignara un cero a cada maquina y se


def max_dict(diccionario: dict) -> int:
    return int(max(list(map(lambda x: diccionario[x], diccionario))))


def ocultar_celdas(
    diccionario_fila_col: dict, matriz: list[X], fila: bool = False
) -> list[X]:
    if fila:
        for numero_posicion in diccionario_fila_col:
            for x in matriz:
                if x.posicion[0] == numero_posicion:
                    x.oculto = True
                    x.marcar()
    else:
        for numero_posicion in diccionario_fila_col:
            for x in matriz:
                if numero_posicion == x.posicion[1]:
                    x.oculto = True
                    x.marcar()
    return matriz


def dibujar_lineas(matriz: list[X], tupla: tuple) -> list[X]:
    contador_ceros = 0
    diccionario_fila = tupla[0]
    diccionario_col = tupla[1]
    cantidad_ceros_total = tupla[2]

    while contador_ceros < cantidad_ceros_total:
        valor_maximo_fila = max_dict(diccionario_fila)
        valor_maximo_col = max_dict(diccionario_col)

        if valor_maximo_fila >= valor_maximo_col:
            diccionario_fila_ocultar = dict(
                filter(lambda x: x[1] == valor_maximo_fila, diccionario_fila.items())
            )

            matriz = ocultar_celdas(
                diccionario_fila_col=diccionario_fila_ocultar, matriz=matriz, fila=True
            )
            contador_ceros += valor_maximo_fila * len(diccionario_fila_ocultar)
        else:
            diccionario_col_ocultar = dict(
                filter(lambda x: x[1] == valor_maximo_col, diccionario_col.items())
            )

            matriz = ocultar_celdas(
                diccionario_fila_col=diccionario_col_ocultar, matriz=matriz, fila=False
            )
            contador_ceros += valor_maximo_col * len(diccionario_col_ocultar)

        diccionario_fila, diccionario_col, _ = cantidad_ceros_fil_col(matriz)

    return matriz


def terminado_o_no_v3(matriz: list[X]) -> bool | list[tuple[int, int]]:

    lista_columnas_asignadas = set()
    lista_filas_asignadas = set()
    lista_asignaciones = []

    for x in matriz:
        x.asignado = False

    tamano = int(len(matriz) ** 0.5)

    while True:
        asignacion_realizada = False

        for fila in range(tamano):
            if fila in lista_filas_asignadas:
                continue
            ceros_fila = [
                x
                for x in matriz
                if x.posicion[0] == fila
                and x.num == 0
                and x.posicion[1] not in lista_columnas_asignadas
            ]
            if len(ceros_fila) == 1:
                x = ceros_fila[0]
                x.asignado = True
                lista_asignaciones.append(x.posicion)
                lista_filas_asignadas.add(x.posicion[0])
                lista_columnas_asignadas.add(x.posicion[1])
                asignacion_realizada = True

        for col in range(tamano):
            if col in lista_columnas_asignadas:
                continue
            ceros_col = [
                x
                for x in matriz
                if x.posicion[1] == col
                and x.num == 0
                and x.posicion[0] not in lista_filas_asignadas
            ]
            if len(ceros_col) == 1:
                x = ceros_col[0]
                x.asignado = True
                lista_asignaciones.append(x.posicion)
                lista_filas_asignadas.add(x.posicion[0])
                lista_columnas_asignadas.add(x.posicion[1])
                asignacion_realizada = True

        if not asignacion_realizada:
            break

    if len(lista_filas_asignadas) == tamano and len(lista_columnas_asignadas) == tamano:
        return lista_asignaciones
    else:
        return False


def encontrar_menor_no_marcado(matriz: list[X]):
    lista_aux = []
    for x in matriz:
        if x.marcado == 0:
            lista_aux.append(x.num)
    return min(lista_aux)


def restar_valores_no_marcados_y_sumar_los_marcados(
    matriz: list[X], valor_menor: int
) -> list[X]:
    for x in matriz:
        if x.marcado == 0:
            x.num -= valor_menor
        elif x.marcado == 2:
            x.num += valor_menor

    return matriz


def funcion_objetivo(matriz_original: list[X], coordenadas: list[tuple]) -> int:
    tamano_matriz = int(len(matriz_original) ** (1 / 2))
    resultado = dict()
    for i in range(tamano_matriz):
        resultado[f"empresa_{i}"] = 0
    for x in matriz_original:
        if x.posicion in coordenadas:
            resultado[f"empresa_{x.posicion[0]}"] += x.num
    resultado["valor_objetivo"] = reduce(
        lambda x, y: x + y, list(map(lambda x: x[1], resultado.items()))
    )
    resultado["coordenadas"] = coordenadas
    return resultado


def limpiar_matriz(matriz: list[X]) -> list[X]:
    for x in matriz:
        x.oculto = False
        x.marcado = 0
        x.asignado = False

    return matriz


def procesar_matriz(matriz_X: list[X]) -> list[X]:

    valores_menores_fila = buscar_menor_fila(matriz=matriz_X)

    matriz_filas_restadas = restar_valor_menor(
        matriz=matriz_X,
        valores_menores=valores_menores_fila,
        fila=True,
    )
    valores_menores_columna = buscar_menor_columna(matriz=matriz_filas_restadas)
    matriz_columnas_restadas = restar_valor_menor(
        matriz=matriz_filas_restadas,
        valores_menores=valores_menores_columna,
    )

    n_ceros_col_fil = cantidad_ceros_fil_col(matriz_columnas_restadas)

    dibujar = dibujar_lineas(matriz=matriz_columnas_restadas, tupla=n_ceros_col_fil)

    valor_menor = encontrar_menor_no_marcado(matriz=dibujar)

    matriz_restada = restar_valores_no_marcados_y_sumar_los_marcados(
        matriz=dibujar, valor_menor=valor_menor
    )

    terminado = terminado_o_no_v3(matriz=matriz_restada)
    # terminado = terminado_o_no(matriz=matriz_restada)

    # dibujar = dibujar_lineas(matriz=matriz_restada, tupla=n_ceros_col_fil)
    while not terminado:
        n_ceros_col_fil = cantidad_ceros_fil_col(matriz_restada)
        dibujar = dibujar_lineas(matriz=matriz_restada, tupla=n_ceros_col_fil)
        valor_menor = encontrar_menor_no_marcado(matriz=dibujar)
        matriz_restada = restar_valores_no_marcados_y_sumar_los_marcados(
            matriz=dibujar, valor_menor=valor_menor
        )
        terminado = terminado_o_no_v3(matriz=matriz_restada)
        # terminado = terminado_o_no(matriz=matriz_restada)

    resultado = funcion_objetivo(matriz_original=matriz_X, coordenadas=terminado)

    return dibujar, resultado


# # #     # return dibujar, {}
