# view.py
import streamlit as st
import pandas as pd
import copy
from main import (
    data_frame_a_lista,
    lista_a_data_frame,
    matriz_estilos_ocultos,
    procesar_matriz,
    matriz_estilos_resultado,
    X,
)
from dataclasses import dataclass
import time


st.title("Metodo Hungaro")
# Condigo para produccion
# Capturamos el tamaño del que el usuario quiere la matriz
st.write(
    "### Esta aplicacion usa el metodo hungaro para resolver el problema de asignacion, cada celda de la matriz representa un costo, cada fila un trabajador o empresa y cada columna una tarea o proyecto. "
)


st.warning(
    "Nota: La matriz debe ser cuadrada es decir que el numero de filas y columnas deben ser iguales."
)
tamano_matriz = st.number_input(
    "Elige el amaño de la matriz (n x n)", min_value=1, max_value=15, step=1
)

# Creamos matriz vacia inicial
# df = pd.DataFrame([["" for i in range(tamano_matriz)] for x in range(tamano_matriz)])
df = pd.DataFrame(
    [["" for _ in range(tamano_matriz)] for _ in range(tamano_matriz)],
    index=[f"Empresa {i+1}" for i in range(tamano_matriz)],
    columns=[f"Central {i+1}" for i in range(tamano_matriz)],
)
st.write("### Edita la matriz:")
st.warning(
    "Las celdas deben contener numeros enteros y positivos, las vacias se toman como 0."
)
matriz_editable = st.data_editor(df, key="editor", num_rows="dynamic")

# procesamos la matriz al presionar el boton
if st.button("Procesar matriz"):
    st.write("Procesando...")

    progress_bar = st.progress(0)
    for i in range(101):
        time.sleep(0.03)
        progress_bar.progress(i)

    st.success("¡Proceso completado!")

    # convertimos el data frame ingresado a una matriz de X
    matriz_X = data_frame_a_lista(matriz_editable)
    matriz_original = copy.deepcopy(matriz_X)

    # Aplicamos el algoritmo hungaro (devuelve matriz_X modificada)
    matriz_X, resultado = procesar_matriz(matriz_X)

    # convertimos la matriz de X a data frame para mostrar
    df_resultado = lista_a_data_frame(matriz_X)

    # creamos data frame de estilos  (para que las celdas ocultas salgan en rojo )
    estilos = matriz_estilos_ocultos(matriz_X)

    # Mostramos el resultado procesado con estilos
    st.write("### Resultado del procesamiento:")
    st.dataframe(df_resultado.style.apply(lambda _: estilos, axis=None))

    st.title("Resultados")
    # mostramos la matriz original con los resultados resaltados
    df_original = lista_a_data_frame(matriz_original)
    estilos_resultados = matriz_estilos_resultado(
        matriz_X, coordenadas=resultado["coordenadas"]
    )
    st.dataframe(df_original.style.apply(lambda _: estilos_resultados, axis=None))
    st.write(f"Valor optimo de la funcion objetivo: {resultado['valor_objetivo']}")


#
# Codigo para probar en desarollo
# valorUno = X(10, (0, 0))
# valorDos = X(9, (0, 1))
# valorTres = X(5, (0, 2))
# valorCuatro = X(9, (1, 0))
# valorCinco = X(8, (1, 1))
# valorSeis = X(3, (1, 2))
# valorSiete = X(6, (2, 0))
# valorOcho = X(4, (2, 1))
# valorNueve = X(7, (2, 2))

# fila1_pos1 = X(45, (0, 0))
# fila1_pos2 = X(60, (0, 1))
# fila1_pos3 = X(75, (0, 2))
# fila1_pos4 = X(60, (0, 3))
# fila1_pos5 = X(50, (0, 4))

# fila2_pos1 = X(25, (1, 0))
# fila2_pos2 = X(85, (1, 1))
# fila2_pos3 = X(90, (1, 2))
# fila2_pos4 = X(50, (1, 3))
# fila2_pos5 = X(55, (1, 4))

# fila3_pos1 = X(50, (2, 0))
# fila3_pos2 = X(72, (2, 1))
# fila3_pos3 = X(85, (2, 2))
# fila3_pos4 = X(65, (2, 3))
# fila3_pos5 = X(45, (2, 4))

# fila4_pos1 = X(55, (3, 0))
# fila4_pos2 = X(78, (3, 1))
# fila4_pos3 = X(80, (3, 2))
# fila4_pos4 = X(70, (3, 3))
# fila4_pos5 = X(52, (3, 4))

# fila5_pos1 = X(52, (4, 0))
# fila5_pos2 = X(65, (4, 1))
# fila5_pos3 = X(95, (4, 2))
# fila5_pos4 = X(68, (4, 3))
# fila5_pos5 = X(48, (4, 4))

# matriz_1 = [
#     fila1_pos1,
#     fila1_pos2,
#     fila1_pos3,
#     fila1_pos4,
#     fila1_pos5,
#     fila2_pos1,
#     fila2_pos2,
#     fila2_pos3,
#     fila2_pos4,
#     fila2_pos5,
#     fila3_pos1,
#     fila3_pos2,
#     fila3_pos3,
#     fila3_pos4,
#     fila3_pos5,
#     fila4_pos1,
#     fila4_pos2,
#     fila4_pos3,
#     fila4_pos4,
#     fila4_pos5,
#     fila5_pos1,
#     fila5_pos2,
#     fila5_pos3,
#     fila5_pos4,
#     fila5_pos5,
# ]


# matriz_2 = [
#     valorUno,
#     valorDos,
#     valorTres,
#     valorCuatro,
#     valorCinco,
#     valorSeis,
#     valorSiete,
#     valorOcho,
#     valorNueve,
# ]


# # ------------------------------
# # 1. Elegir tamaño de la matriz
# # ------------------------------
# # n = st.number_input("Tamaño de la matriz (n x n)", min_value=1, max_value=15, step=1)

# # Creamos DataFrame editable inicial vacío
# # df = pd.DataFrame([["" for _ in range(n)] for _ in range(n)])

# # st.write("### Edita la matriz:")
# # matriz_editable = st.data_editor(df, key="editor", num_rows="dynamic")

# # ------------------------------
# # 2. Procesar matriz al presionar botón
# # ------------------------------
# if st.button("Procesar matriz 2"):

#     # Convertir DataFrame ingresado a una matriz de X
#     # matriz_X = dataframe_to_Xlist(matriz_editable)
#     # matriz_original = copy.deepcopy(matriz_X)
#     matriz_X = matriz_2
#     # Aplicamos tu algoritmo (devuelve matriz_X modificada)
#     matriz_X = procesar_matriz(matriz_X)

#     # Convertimos la matriz de X a DataFrame para mostrar
#     df_resultado = lista_a_data_frame(matriz_X)

#     # Creamos DataFrame de estilos (celdas ocultas en rojo)
#     estilos = matriz_estilos_ocultos(matriz_X)

#     # Mostrar resultado procesado con estilos
#     st.write("### Resultado del procesamiento matriz 2:")
#     st.dataframe(df_resultado.style.apply(lambda _: estilos, axis=None))

# if st.button("Procesar matriz 1"):

#     # Convertir DataFrame ingresado a una matriz de X
#     # matriz_X = dataframe_to_Xlist(matriz_editable)
#     # matriz_original = copy.deepcopy(matriz_X)
#     matriz_X = matriz_1
#     # Aplicamos tu algoritmo hungaro que devuelve matriz_x modificado
#     matriz_X = procesar_matriz(matriz_X)

#     # Convertimos la matriz de X a dataFrame para mostrar
#     df_resultado = lista_a_data_frame(matriz_X)

#     # Creamos DataFrame de estilos (celdas ocultas en rojo
#     estilos = matriz_estilos_ocultos(matriz_X)

#     # Mostrar resultado procesado con estilos
#     st.write("### Resultado del procesamiento matriz 2:")
#     st.dataframe(df_resultado.style.apply(lambda _: estilos, axis=None))
