import re
import numpy as np
from scipy.optimize import milp
from scipy.optimize import LinearConstraint
from scipy import optimize

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
            int_Var = re.findall(r"\[([^\]]+)\]", linea)[0].split()
            int_Var = list(map(int, [valor.strip('[') for valor in int_Var]))
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
   
    # Convertir restricciones de integralidad
    
    integrality = np.zeros(num_variables)
    if isinstance(int_Var, int):
        int_Var = [int_Var]
    for i in int_Var:
        integrality[i-1] = 1

    c = [-1 * val for val in coef_funcion]  # Convertir a negativo para maximización
    A = [val for val in coef_matrizD]
    b_u = [val for val in term_indepD]
    b_u = np.array([valor for sublist in term_indepD for valor in sublist])
    b_l = np.full_like(b_u, -np.inf)
    A_eq = [val for val in coef_matrizI]
    b_eq = [val for val in term_indepI]
    bounds = [val for val in cotas_Var]

    # Generar tuplas bounds correctamente (PARA ESTE CASO NO SON NECESARIAS)
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


    # Convertir restricciones de desigualdad a formato scipy.optimize.LinearConstraint
    constraints = LinearConstraint(A, lb=b_l, ub=b_u)

    # Resolver el problema con scipy.optimize.milp
    res = milp(c=c, constraints=constraints, integrality=integrality)

    return res


# Ejemplo de uso
plantilla = "Problem"  # Reemplaza con el nombre de tu archivo de plantilla
datos = leer_plantilla(plantilla)

# Extraer valores del archivo
num_variables, num_restrD, num_restrI, int_Var, coef_funcion, coef_matrizD, term_indepD, coef_matrizI, term_indepI, cotas_Var = leer_plantilla(plantilla)

# Resolver el problema de programación lineal de optimización
resultado = resolver_problema(num_variables, num_restrD, num_restrI, int_Var, coef_funcion, coef_matrizD, term_indepD, coef_matrizI, term_indepI, cotas_Var)

# Mostrar información de variables y matrices
print("Número de variables:", num_variables)
print("Número de restricciones de desigualdad:", num_restrD)
print("Número de restricciones de igualdad:", num_restrI)
print("Número de restricciones de igualdad:", int_Var)
print("Coeficientes de la función objetivo:", coef_funcion)
print("Matriz de coeficientes de las restricciones de desigualdad:", coef_matrizD)
print("Términos independientes de las restricciones de desigualdad:", term_indepD)
print("Matriz de coeficientes de las restricciones de igualdad:", coef_matrizI)
print("Términos independientes de las restricciones de igualdad:", term_indepI)
print("Cotas de las variables:", cotas_Var)

# Imprimir el resultado
print("Resultado total:", resultado)
print("Solución óptima:")
print("Valor objetivo optimo:", -resultado.fun, "\nOptimo variables de decision X: ",resultado.x)
print("Optimo variables X: ", resultado.x)




