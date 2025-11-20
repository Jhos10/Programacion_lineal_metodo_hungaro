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

    st.title("Resultados")
    # mostramos la matriz original con los resultados resaltados
    df_original = lista_a_data_frame(matriz_original)
    estilos_resultados = matriz_estilos_resultado(
        matriz_X, coordenadas=resultado["coordenadas"]
    )
    st.dataframe(df_original.style.apply(lambda _: estilos_resultados, axis=None))
    st.write(f"Valor optimo de la funcion objetivo: {resultado['valor_objetivo']}")

if st.button("Procesar matriz 14 x 14"):
    st.write("Procesando...")

    progress_bar = st.progress(0)
    for i in range(101):
        time.sleep(0.03)
        progress_bar.progress(i)

    st.success("¡Proceso completado!")

    # convertimos el data frame ingresado a una matriz de X
    matriz_X = copy.deepcopy(matriz_14_14)
    matriz_original = copy.deepcopy(matriz_X)
    try:
        # Aplicamos el algoritmo hungaro (devuelve matriz_X modificada)
        matriz_X, resultado = procesar_matriz(matriz_X)

        # convertimos la matriz de X a data frame para mostrar
        df_resultado = lista_a_data_frame(matriz_X)

        st.title("Resultados")
        # mostramos la matriz original con los resultados resaltados
        df_original = lista_a_data_frame(matriz_original)
        estilos_resultados = matriz_estilos_resultado(
            matriz_X, coordenadas=resultado["coordenadas"]
        )
        st.dataframe(df_original.style.apply(lambda _: estilos_resultados, axis=None))
        st.write(f"Valor optimo de la funcion objetivo: {resultado['valor_objetivo']}")
    except Exception as e:
        st.error(
            "No se pudo encontrar una solucion con este metodo para la matriz dada."
        )
