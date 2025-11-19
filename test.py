from main import cantidad_ceros_fil_col, ocultar_celdas
from main import X

valorUno = X(0, (0,0),oculto=False)
valorDos = X(0, (0,1), oculto=False)   
valorTres = X(0, (1,0), oculto=True)
valorCuatro = X(0, (1,1),oculto=False)
matriz = [valorUno, valorDos, valorTres, valorCuatro]
#0 0
#A 0

print("Probando funcion cantidad ceros fil col")
cantidad_ceros_fil_col_result = cantidad_ceros_fil_col(matriz=matriz)

print(cantidad_ceros_fil_col(matriz=matriz))
print(ocultar_celdas(matriz=matriz,diccionario_fila_col={0:2},fila=True))
print(cantidad_ceros_fil_col(matriz=matriz))

