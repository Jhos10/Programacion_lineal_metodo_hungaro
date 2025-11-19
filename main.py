# SI tiene dos lineas ENTONCES se suma, SINO SI tiene una linea no se edita el valor, SINO se resta
import streamlit as st
import pandas as pd
from dataclasses import dataclass 
from pprint import pprint as pp
from functools import reduce
import copy
import pandas as pd


#modelo de datos 
@dataclass 
class X:
  num : int 
  # (1,3) -> primera posicion fila y segunda posicion columna.
  posicion : tuple
  asignado : bool  = False
  marcado : int  = 0
  oculto : bool = False




  def marcar(self):
    self.marcado += 1 


# ------------------------------
# Lógica: convertir DataFrame a lista de X
# ------------------------------
def dataframe_to_Xlist(df):
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


# ------------------------------
# Lógica: lista de X → DataFrame
# ------------------------------
def Xlist_to_dataframe(matriz_X):
    if not matriz_X:
        return pd.DataFrame()
    
    n_filas = max(x.posicion[0] for x in matriz_X) + 1
    n_cols = max(x.posicion[1] for x in matriz_X) + 1
    
    # Crear lista de listas vacía
    df_data = [[0 for _ in range(n_cols)] for _ in range(n_filas)]
    
    for x in matriz_X:
        df_data[x.posicion[0]][x.posicion[1]] = x.num
    
    return pd.DataFrame(df_data)


# ------------------------------
# Lógica: obtener matriz de estilos (sin Streamlit)
# ------------------------------
def matriz_estilos_ocultos(matriz_X):
    if not matriz_X:
        return pd.DataFrame()
    
    n_filas = max(x.posicion[0] for x in matriz_X) + 1
    n_cols = max(x.posicion[1] for x in matriz_X) + 1
    
    estilos = pd.DataFrame([["" for _ in range(n_cols)] for _ in range(n_filas)])
    
    for x in matriz_X:
        if x.oculto:
            estilos.iloc[x.posicion[0], x.posicion[1]] = "background-color: red; color: white;"
    
    return estilos


# ------------------------------
# Aquí puedes agregar tu algoritmo húngaro, ocultar celdas, etc.
# ------------------------------






def buscar_menor_fila(matriz : list[X] ) -> list[int]:
  longitud_matriz = int(len(matriz)**(1/2))
  valores_menores : list[int] = [0] * longitud_matriz
  contador_fila : int = 0
  for x in matriz:
    if x.posicion[0] != contador_fila:
      contador_fila += 1
    if x.posicion[1] == 0:
      valores_menores[contador_fila] = x.num
    if x.posicion[0] == contador_fila :
      if valores_menores[contador_fila] > x.num:
        valores_menores[contador_fila] = x.num
  return valores_menores

def buscar_menor_columna(matriz : list[X])-> list[int]:
  longitud_matriz = int(len(matriz)**(1/2))
  valores_menores : list[X] = []
  for x in matriz:
    if x.posicion[0] == 0:
      valores_menores.append(x.num)
    
  for i in range(longitud_matriz):
    for x in matriz:
      if x.posicion[1] == i:
        if valores_menores[i] > x.num:
          valores_menores[i] = x.num
  return valores_menores





def restar_valor_menor(valores_menores : list[int], matriz : list[X], fila : bool = False)-> list[X]:
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
      


def cantidad_ceros_fil_col(matriz : list[X]) -> dict:
  lineas_filas = dict()
  lineas_columnas = dict()
  tamano_matriz = int(len(matriz)**(1/2))
  #se construye un diccionario donde se guarda cuantos ceros tiene cada linea 
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

  cantidad_ceros_total = reduce(lambda x,y: x+y, list(map(lambda x: lineas_columnas[x],lineas_columnas)))
  return lineas_filas, lineas_columnas, cantidad_ceros_total


def max_dict(diccionario : dict):
  pass


# tupla_lineas = cantidad_ceros_fil_col(matriz= matriz_columnas_restadas)
# print("numero de ceros")
# pp(tupla_lineas)

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

def max_dict(diccionario : dict)-> int:
  return int(max(list(map(lambda x : diccionario[x], diccionario))))

def ocultar_celdas(diccionario_fila_col: dict, matriz: list[X], fila: bool = False)->list[X]:
  # print(f"ocultando fila:{fila}")
  # print("diccionario usado para ocultar")
  # pp(diccionario_fila_col)
  # pp(matriz)
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

    


# def dibujar_lineas(matriz: list[X], tupla:tuple) -> list[X]:
#   contador_ceros = 0
#   diccionario_fila = tupla[0]
#   diccionario_col = tupla[1]
#   cantidad_ceros_totales = tupla[2]
#   while contador_ceros <= cantidad_ceros_totales:
#     valor_maximo_fila = max_dict(diccionario_fila)
#     valor_maximo_col = max_dict(diccionario_col)

#     # pp(contador_ceros)
#     if  valor_maximo_fila >= valor_maximo_col:
#       diccionario_fila_ocultar = dict(filter(lambda x: x[1]== valor_maximo_fila, diccionario_fila.items()))
#       matriz = ocultar_celdas(diccionario_fila_col=diccionario_fila_ocultar,matriz=matriz, fila=True)
#       contador_ceros += valor_maximo_fila*len(diccionario_fila_ocultar)
#     else:
#       diccionario_col_ocultar = dict(filter(lambda x: x[1]== valor_maximo_col, diccionario_col.items()))
#       matriz = ocultar_celdas(diccionario_fila_col=diccionario_col_ocultar,matriz=matriz)
#       contador_ceros += valor_maximo_col*len(diccionario_col_ocultar)

#     diccionario_fila = cantidad_ceros_fil_col(matriz=matriz)[0]
#     diccionario_col = cantidad_ceros_fil_col(matriz=matriz)[1]

#   return matriz

def dibujar_lineas(matriz: list[X], tupla:tuple) -> list[X]:
    contador_ceros = 0
    diccionario_fila = tupla[0]
    diccionario_col = tupla[1]
    cantidad_ceros_total = tupla[2]

    while contador_ceros < cantidad_ceros_total:
        valor_maximo_fila = max_dict(diccionario_fila)
        valor_maximo_col = max_dict(diccionario_col)

        if valor_maximo_fila >= valor_maximo_col:
            diccionario_fila_ocultar = {k:v for k,v in diccionario_fila.items() if v == valor_maximo_fila}
            matriz = ocultar_celdas(diccionario_fila_col=diccionario_fila_ocultar, matriz=matriz, fila=True)
            contador_ceros += valor_maximo_fila * len(diccionario_fila_ocultar)
        else:
            diccionario_col_ocultar = {k:v for k,v in diccionario_col.items() if v == valor_maximo_col}
            matriz = ocultar_celdas(diccionario_fila_col=diccionario_col_ocultar, matriz=matriz, fila=False)
            contador_ceros += valor_maximo_col * len(diccionario_col_ocultar)

        # 🔹 Recalcular diccionarios después de cada iteración
        diccionario_fila, diccionario_col, _ = cantidad_ceros_fil_col(matriz)

    return matriz

# def dibujar_lineas(matriz: list[X], tupla:tuple) -> list[X]:
#     contador_ceros = 0
#     diccionario_fila = tupla[0]
#     diccionario_col = tupla[1]
#     cantidad_ceros_total = tupla[2]

#     while contador_ceros < cantidad_ceros_total:
#         valor_maximo_fila = max_dict(diccionario_fila)
#         valor_maximo_col = max_dict(diccionario_col)

#         if valor_maximo_fila >= valor_maximo_col:
#             diccionario_fila_ocultar = dict(filter(lambda x: x[1]== valor_maximo_fila, diccionario_fila.items()))
#             matriz = ocultar_celdas(diccionario_fila_col=diccionario_fila_ocultar, matriz=matriz, fila=True)
#             contador_ceros += valor_maximo_fila * len(diccionario_fila_ocultar)
#         else:
#             diccionario_col_ocultar = dict(filter(lambda x: x[1]== valor_maximo_col, diccionario_col.items()))
#             matriz = ocultar_celdas(diccionario_fila_col=diccionario_col_ocultar, matriz=matriz, fila=False)
#             contador_ceros += valor_maximo_col * len(diccionario_col_ocultar)

#         # 🔹 Recalcular diccionarios después de cada iteración
#         diccionario_fila = cantidad_ceros_fil_col(matriz)[0]
#         diccionario_col = cantidad_ceros_fil_col(matriz)[1]
#         # diccionario_fila, diccionario_col = cantidad_ceros_fil_col(matriz)

#     return matriz     

      


def terminado_o_no(matriz : list[X])-> bool:
  print("Comprobando si terminamos el problema o NO!")
  lista_columnas_asignadas = []
  lista_filas_asignadas = []
  lista_asignaciones = []
  contador_empresa = 0
  for x in matriz:
    if x.num == 0 and x.posicion[1] not in lista_columnas_asignadas and x.posicion[0] not in lista_filas_asignadas:
      x.asignado = True
      contador_empresa += 1
      lista_columnas_asignadas.append(x.posicion[1])
      lista_filas_asignadas.append(x.posicion[0])
      lista_asignaciones.append(x.posicion)
  # print(lista_columnas_asignadas)
  # print(lista_asignaciones)
  return False if contador_empresa < len(matriz)**(1/2) or contador_empresa > len(matriz)**(1/2) else lista_asignaciones

# Buscar maquina con una unica posibilidad del cero, que asigne todas las que tienen una posibilidad
# 
# Marcar filas y columnas con la mayor cantidad de ceros
# Despues seguir con las menores 

def encontrar_menor_no_marcado(matriz : list[X]):
  lista_aux = []
  for x in matriz:
    if x.marcado == 0 :
      lista_aux.append(x.num)
  return min(lista_aux)

# valor_menor = encontrar_menor_no_marcado(matriz=matriz_marcada)

def restar_valores_no_marcados_y_sumar_los_marcados_dos_veces(matriz: list[X], valor_menor: int) -> list[X]:
  for x in matriz:
    if x.marcado == 0:
      x.num -= valor_menor
    elif x.marcado == 2:
      x.num += valor_menor

  return matriz

# matriz_final = restar_valores_no_marcados_y_sumar_los_marcados_dos_veces(matriz=matriz_marcada, valor_menor=valor_menor)


# coordenadas = terminado_o_no(matriz=matriz_final)

def funcion_objetivo(matriz_original: list[X],coordenadas: list[tuple]) -> int:
  tamano_matriz = int(len(matriz_original)**(1/2))
  resultado = dict()
  for i in range(tamano_matriz):
    resultado[f"empresa_{i}"] = 0
  for x in matriz_original:
    if x.posicion in coordenadas:
      resultado[f"empresa_{x.posicion[0]}"] += x.num
  resultado['valor_objetivo'] = reduce(lambda x,y: x+y, list(map(lambda x: x[1],resultado.items())))
  return resultado


# pp(funcion_objetivo(matriz_original=matriz, coordenadas=coordenadas))


def procesar_matriz(matriz_X: list[X]) -> list[X]:
  # matriz_X = reduce(lambda x,y: x+y, matriz_X)
  # print(matriz_X)
  valores_menores_fila = buscar_menor_fila(matriz=matriz_X)

  matriz_filas_restadas = restar_valor_menor(matriz=matriz_X, valores_menores=valores_menores_fila, fila=True)
  valores_menores_columna = buscar_menor_columna(matriz=matriz_filas_restadas)
  matriz_columnas_restadas = restar_valor_menor(matriz=matriz_filas_restadas,valores_menores=valores_menores_columna,)

  n_ceros_col_fil = cantidad_ceros_fil_col(matriz_columnas_restadas)
  # pp(n_ceros_col_fil)

  dibujar = dibujar_lineas(matriz=matriz_columnas_restadas,tupla=n_ceros_col_fil)
  # pp(dibujar)
 
  return dibujar



  

# if __name__ == '__main__':
#   print("Hello Hungarian Method")
  # ------------------------------
# Aquí puedes agregar tu algoritmo húngaro, ocultar celdas, etc.
# ------------------------------


  
  # fila1_pos1 = X(45, (0,0))
  # fila1_pos2 = X(60, (0,1))
  # fila1_pos3 = X(75, (0,2))
  # fila1_pos4 = X(60, (0,3))
  # fila1_pos5 = X(50, (0,4))

  # fila2_pos1 = X(25, (1,0))
  # fila2_pos2 = X(85, (1,1))
  # fila2_pos3 = X(90, (1,2))
  # fila2_pos4 = X(50, (1,3))
  # fila2_pos5 = X(55, (1,4))

  # fila3_pos1 = X(50, (2,0))
  # fila3_pos2 = X(72, (2,1))
  # fila3_pos3 = X(85, (2,2))
  # fila3_pos4 = X(65, (2,3))
  # fila3_pos5 = X(45, (2,4))

  # fila4_pos1 = X(55, (3,0))
  # fila4_pos2 = X(78, (3,1))
  # fila4_pos3 = X(80, (3,2))
  # fila4_pos4 = X(70, (3,3))
  # fila4_pos5 = X(52, (3,4))

  # fila5_pos1 = X(52, (4,0))
  # fila5_pos2 = X(65, (4,1))
  # fila5_pos3 = X(95, (4,2))
  # fila5_pos4 = X(68, (4,3))
  # fila5_pos5 = X(48, (4,4))

  # matriz = [
  #     fila1_pos1, fila1_pos2, fila1_pos3, fila1_pos4, fila1_pos5,
  #     fila2_pos1, fila2_pos2, fila2_pos3, fila2_pos4, fila2_pos5,
  #     fila3_pos1, fila3_pos2, fila3_pos3, fila3_pos4, fila3_pos5,
  #     fila4_pos1, fila4_pos2, fila4_pos3, fila4_pos4, fila4_pos5,
  #     fila5_pos1, fila5_pos2, fila5_pos3, fila5_pos4, fila5_pos5
  # ]

  
#inicia el algoritmo 
#se saca el valor menor de cada fila 
  # valores_menores_fila = buscar_menor_fila(matriz=matriz)
  # #s
  # matriz_filas_restadas = restar_valor_menor(matriz=matriz, valores_menores=valores_menores_fila, fila=True)
  # #se repite el proceso con las  valoress_menores_columna = buscar_menor_columna(matriz=matriz_filas_restadas)
  # valores_menores_columna = buscar_menor_columna(matriz=matriz_filas_restadas)
  # matriz_columnas_restadas = restar_valor_menor(matriz=matriz_filas_restadas,valores_menores=valores_menores_columna,)

  # n_ceros_col_fil = cantidad_ceros_fil_col(matriz_columnas_restadas)
  # pp(n_ceros_col_fil)

  # dibujar = dibujar_lineas(matriz=matriz_columnas_restadas,tupla=n_ceros_col_fil)
  # pp(dibujar)

  # procesar_matriz(matriz_X=dibujar)