

import re
import numpy as np
from scipy.optimize import linprog
import pulp
import matplotlib.pyplot as plt



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
        elif 'int_Var' in linea:
            int_Var = re.findall(r"\[([^\]]+)\]", linea)
            int_Var = [list(map(float, fila.replace('[', '').replace(']', '').split())) for fila in int_Var]
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

    return num_variables, num_restrD, num_restrI, int_Var, coef_funcion, coef_matrizD, term_indepD, coef_matrizI, term_indepI, cotas_Var


def resolver_problema(num_variables, num_restrD, num_restrI, int_Var, coef_funcion, coef_matrizD, term_indepD, coef_matrizI, term_indepI, cotas_Var):
    

    # Generar tuplas bounds correctamente
    bounds = []
    if cotas_Var:  # Verificar si cotas_Var no está vacío
        for fila in cotas_Var:
            if fila:  # Verificar si la fila no está vacía
                min_valor = min(fila) if None not in fila else 0
                max_valor = max(fila) if None not in fila else None
                bounds.extend([min_valor, max_valor])
            else:
                bounds.extend([0, None])  # Establecer límites predeterminados
    else:
        bounds = []  # No hay restricciones en las variables

    # Crear un problema de optimización lineal
    linearProblem = pulp.LpProblem("Maximizing Objective", pulp.LpMaximize)

    # Declarar variables de optimización
    variables = []
    for i in range(len(coef_funcion)):
        var_name = 'x' + str(i+1)
        # Agregar cada variable por separado a la lista de variables
        var = pulp.LpVariable(var_name, lowBound=bounds[0], upBound=bounds[1])
        variables.append(var)


    # Agregar la función objetivo al problema
    objective = pulp.lpSum(coef_funcion[i] * variables[i] for i in range(num_variables))
    linearProblem += objective

    # Agregar restricciones a partir de coef_matrizD y term_indepD
    for i in range(len(coef_matrizD)):
        constraint = pulp.lpDot(variables, coef_matrizD[i]) <= term_indepD[i][0]
        linearProblem += constraint

    # Agregar restricciones a partir de coef_matrizI y term_indepI
    for i in range(len(coef_matrizI)):
        constraint = pulp.lpDot(variables, coef_matrizI[i]) == term_indepI[i][0]
        linearProblem += constraint


    # Resolver el problema
    solution = linearProblem.solve()

    return linearProblem, solution

# Ejemplo de uso
plantilla = "Problem"  # Reemplaza con el nombre de tu archivo de plantilla
datos = leer_plantilla(plantilla)

# Extraer valores del archivo
num_variables, num_restrD, num_restrI, int_Var, coef_funcion, coef_matrizD, term_indepD, coef_matrizI, term_indepI, cotas_Var = leer_plantilla(plantilla)

# Resolver el problema de programación lineal de optimización
linearProblem, resultado = resolver_problema(num_variables, num_restrD, num_restrI, int_Var, coef_funcion, coef_matrizD, term_indepD, coef_matrizI, term_indepI, cotas_Var)


# Mostrar los valores de las variables y el valor objetivo si la solución es óptima
if resultado == pulp.LpStatusOptimal:
    print(linearProblem)
    print("Valor objetivo optimo:", pulp.value(linearProblem.objective))
    for var in linearProblem.variables():   
        print(f"{var.name} = {var.varValue}")

if resultado == pulp.LpStatusOptimal:
    print(linearProblem)
