

import re
import numpy as np
from scipy.optimize import linprog

def leer_plantilla(plantilla):
    with open(plantilla, 'r') as file:
        lineas = file.readlines()

    for linea in lineas:
        if 'num_variables' in linea:
            num_variables = int(linea.split("=")[1])
        elif 'num_restrD' in linea:
            num_restrD = int(linea.split("=")[1])
        elif 'num_restrI' in linea:
            num_restrI = int(linea.split("=")[1])
        elif 'coef_funcion' in linea:
            coef_funcion = re.findall(r"\[([^\]]+)\]", linea)[0].split()
            coef_funcion = list(map(float, [valor.strip('[') for valor in coef_funcion]))
        elif 'coef_matrizD' in linea:
            coef_matrizD = re.findall(r"\[([^\]]+)\]", linea)
            coef_matrizD = [list(map(float, fila.replace('[', '').replace(']', '').split())) for fila in coef_matrizD]
        elif 'term_indepD' in linea:
            term_indepD = re.findall(r"\[([^\]]+)\]", linea)
            term_indepD = [list(map(float, fila.replace('[', '').replace(']', '').split())) for fila in term_indepD]
        elif 'coef_matrizI' in linea:
            coef_matrizI = re.findall(r"\[([^\]]+)\]", linea)
            coef_matrizI = [list(map(float, fila.replace('[', '').replace(']', '').split())) for fila in coef_matrizI]
        elif 'term_indepI' in linea:
            term_indepI = re.findall(r"\[([^\]]+)\]", linea)
            term_indepI = [list(map(float, fila.replace('[', '').replace(']', '').split())) for fila in term_indepI]
        elif 'cotas_Var' in linea:
            cotas_Var = re.findall(r"\[([^\]]+)\]", linea)
            cotas_Var = [[float(valor) if valor != 'None' else None for valor in fila.replace('[', '').replace(']', '').split()]for fila in cotas_Var]

    return num_variables, num_restrD, num_restrI, coef_funcion, coef_matrizD, term_indepD, coef_matrizI, term_indepI, cotas_Var


def resolver_problema(num_variables, num_restrD, num_restrI, coef_funcion, coef_matrizD, term_indepD, coef_matrizI, term_indepI, cotas_Var):
    
    c = [-1 * val for val in coef_funcion]  # Convertir a negativo para maximización
    A_ub = [val for val in coef_matrizD]
    b_ub = [val for val in term_indepD]
    A_eq = [val for val in coef_matrizI]
    b_eq = [val for val in term_indepI]

    # Generar tuplas bounds correctamente
    bounds = []
    if cotas_Var:  # Verificar si cotas_Var no está vacío
        for fila in cotas_Var:
            if fila:  # Verificar si la fila no está vacía
                min_valor = min(fila) if None not in fila else 0
                max_valor = max(fila) if None not in fila else None
                bounds.append((min_valor, max_valor))
            else:
                bounds.append((0, None))  # Establecer límites predeterminados
    else:
        bounds = []  # No hay restricciones en las variables        


    # Resolver el problema de programación lineal de optimización (bajo condiciones)
        
    if not A_eq and not b_eq:  # Verificar si A_eq y b_eq son vacías
        if not A_ub and not b_ub:  # Verificar si también A_ub y b_ub son vacías
            print("Faltan restricciones para el problema de optimizacion") # Si todas las matrices de restricciones están vacías
        else:
            resultado = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs') # Si solo A_eq y b_eq están vacías
    elif not A_eq and not b_eq:  # Si solo A_ub y b_ub están vacías
        resultado = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
    else:
        resultado = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs') # Si se tienen todos los datos, ninguno es vacío

    print(resultado)
    return resultado


# Ejemplo de uso
plantilla = "Problem" # Reemplaza con el nombre de tu archivo de plantilla
datos = leer_plantilla(plantilla)

# Extraer valores del archivo
num_variables, num_restrD, num_restrI, coef_funcion, coef_matrizD, term_indepD, coef_matrizI, term_indepI, cotas_Var = leer_plantilla(plantilla)

# Resolver el problema de programación lineal de optimización
resultado = resolver_problema(num_variables, num_restrD, num_restrI, coef_funcion, coef_matrizD, term_indepD, coef_matrizI, term_indepI, cotas_Var)


# Mostrar informacion de variables y matrices
print("Número de variables:", num_variables)
print("Número de restricciones de desigualdad:", num_restrD)
print("Número de restricciones de igualdad:", num_restrI)
print("Coeficientes de la función objetivo:", coef_funcion)
print("Matriz de coeficientes de las restricciones de desigualdad:", coef_matrizD)
print("Términos independientes de las restricciones de desigualdad:", term_indepD)
print("Matriz de coeficientes de las restricciones de igualdad:", coef_matrizI)
print("Términos independientes de las restricciones de igualdad:", term_indepI)
print("Cotas de las variables:", cotas_Var)

# Imprimir el resultado
print("Resultado total:", resultado)
print("Solución óptima:")
print("Valor objetivo optimo:", -resultado.fun, "\nOptimo v ariables X: ",resultado.x)
print("Optimo variables X: ", resultado.x)



##### TIPS PARA USO CORRECTO EN PLANTILLA TXT:

# 1. Para minimizacion, los coeficientes de la funcion en la plantilla deben colcarse en negativo.

# 2. A_ub (coef_matrizD) debe contener el mismo numero de columnas que el numero de elementos de c.
    # Rellenar con ceros si es necesario, en caso de que no hayan coeficientes para las variables.

# 3. bounds = cotas_Var (cotas o limites de la variable): si no es una sola cota que especifique [0 None] -> de 0 a infinito sin limite para todo el modelo,
    # entonces debe de haber misma cantidad de bounds por cantidad de variables en la funcion de maximizacion.

# 4. Si no se tiene coeficientes de igualdad o desigualdad, no colocar nada


