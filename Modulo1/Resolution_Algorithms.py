import numpy as np
import sympy as sp

last_derivative, last_sol = None, None


def euler_improved(f, x0, y0, h, n):
    """
    Resuelve una EDO usando el método de Euler mejorado.

    :param f: Función que representa la derivada de la EDO.
    :param x0: Condición inicial para x.
    :param y0: Condición inicial para y.
    :param h: Tamaño del paso.
    :param n: Número de pasos.
    :return: Tuple (x_values, y_values) con los valores de x e y calculados.
    """
    x_values, y_values = [x0], [y0]

    for i in range(n):
        x = x_values[-1]
        y = y_values[-1]

        k1 = f(x, y)  # Calcula la pendiente en el punto inicial
        y_predict = y + h * k1  # Predice el valor de y en el siguiente paso

        k2 = f(x + h, y_predict)  # Calcula la pendiente en el punto predicho
        y_corrected = y + (h / 2) * (k1 + k2)  # Corrige el valor de y usando el promedio de las pendientes

        x_values.append(round(x + h, 3))  # Agrega el nuevo valor de x a la lista
        y_values.append(y_corrected)  # Agrega el nuevo valor de y a la lista

    return x_values, y_values


def runge_kutta_4(f, x0, y0, h, n):
    """
    Resuelve una EDO usando el método de Runge-Kutta de 4º orden.

    :param f: Función que representa la derivada de la EDO.
    :param x0: Condición inicial para x.
    :param y0: Condición inicial para y.
    :param h: Tamaño del paso.
    :param n: Número de pasos.
    :return: Tuple (x_values, y_values) con los valores de x e y calculados.
    """
    x_values, y_values = [x0], [y0]
    
    for i in range(n):
        x, y = x_values[-1], y_values[-1]

        k1 = f(x, y)  # Calcula la pendiente en el punto inicial
        k2 = f(x + h/2, y + h*k1/2)  # Calcula la pendiente en el punto medio usando k1
        k3 = f(x + h/2, y + h*k2/2)  # Calcula la pendiente en el punto medio usando k2
        k4 = f(x + h, y + h*k3)  # Calcula la pendiente en el punto final usando k3
        
        y_next = y + (h/6) * (k1 + 2*k2 + 2*k3 + k4)  # Calcula el valor de y en el siguiente paso
        
        x_values.append(round(x + h, 3))  # Agrega el nuevo valor de x a la lista
        y_values.append(y_next)  # Agrega el nuevo valor de y a la lista
    
    return x_values, y_values


def calculate_isoclines(f, x_range, y_range, num_points=30):
    """
    Calcula y grafica las isoclinas de una EDO.

    :param f_sympy: Función simbólica que representa la derivada de la EDO.
    :param x_range: Rango de valores para x.
    :param y_range: Rango de valores para y.
    :param num_points: Número de puntos para la malla.
    :return: Tuple (x, y, u, v) con los valores calculados para graficar las isoclinas.
    """

    x, y = sp.symbols('x y')# Define las variables simbólicas

    x_vals, y_vals = np.meshgrid(np.linspace(x_range[0], x_range[1], num_points), np.linspace(y_range[0], y_range[1], num_points))# Crea una malla de puntos

    f_vals = np.zeros_like(x_vals, dtype=float)# Evalúa la función simbólica en cada punto de la malla

    for i in range(x_vals.shape[0]):
        for j in range(x_vals.shape[1]):
            f_vals[i, j] = float(f.subs({x: x_vals[i, j], y: y_vals[i, j]}))

    u = np.ones_like(f_vals)# Crea una matriz de unos con la misma forma que f_vals
    v = f_vals / np.sqrt(1 + f_vals**2)# Normaliza los valores de f para obtener las direcciones de las isoclinas

    return x_vals, y_vals, u, v


def solve_edo(derivative_as_string, f, x0, y0):
    """
    Resuelve una EDO de forma analítica.

    :param f: Función que representa la derivada de la EDO.
    :param x0: Condición inicial para x.
    :param y0: Condición inicial para y.
    :return: Solución particular de la EDO o un mensaje indicando que no existe solución.
    """

    global last_derivative
    global last_sol

    x = sp.symbols('x')  # Define el símbolo x
    y = sp.Function('y')(x)  # Define la función y(x)
    
    if last_derivative is None or last_derivative != derivative_as_string:
        print("calculating now")
        edo = sp.Eq(y.diff(x), f(x, y))  # Crea la ecuación diferencial
        try:
            sol = sp.dsolve(edo, y)  # Intenta resolver la ecuación diferencial
        except:
            sol = None
            return False  # Retorna False si no se puede resolver
        
        last_derivative = derivative_as_string
        last_sol = sol
    else:
        print("calculated before, skipping it")
        sol = last_sol

    try:
        # Intenta calcular la solución particular con las condiciones iniciales
        C = sp.symbols('C')  # Define el símbolo de la constante de integración
        particular_sol = sol.subs('C1', C)
        C_value = sp.solve(particular_sol.rhs.subs(x, x0) - y0, C)[0]
        return particular_sol.subs(C, C_value)
    except:
        return False  # Retorna False si no se puede encontrar la solución particular


def analitic_solution(derivative_as_string, f, x0, y0, step):
    """
    Calcula la solución analítica de una EDO en un rango de valores.

    :param f: Función que representa la derivada de la EDO.
    :param x0: Condición inicial para x.
    :param y0: Condición inicial para y.
    :param step: Tamaño del paso.
    :return: Tuple (x_values, y_values) con los valores de x e y calculados.
    """
    x_values = [x0]

    # "Metodo para generar los valores de x"
    helper = x0
    while (helper > -25):
        helper -= step
        x_values.append(round(helper, 3))  # Agrega los valores de x hacia la izquierda
    helper = x0
    while (helper < 25):
        helper += step
        x_values.append(round(helper, 3))  # Agrega los valores de x hacia la derecha
    x_values.sort()  # Ordena los valores de x

    particular_sol = solve_edo(derivative_as_string, f, x0, y0)  # Obtiene la solución particular

    if isinstance(particular_sol, bool) and not particular_sol:  # Retorna un mensaje de error si no se encuentra solución
        return False, f"No se pudo encontrar una solución analítica para la EDO en ({x0},{y0})."  
    

    y_values = []
    valid_x_values = []
    for val in x_values:
        try:
            y_val = particular_sol.rhs.subs(sp.symbols('x'), val).evalf()
            if y_val.is_real:
                y_values.append(round(y_val, 5))
                valid_x_values.append(val)
            else:
                print(f"Error: La función no está definida en x = {val}")
        except:
            print(f"Error: Funcion {particular_sol} no definida en x = {val}")
    
    return valid_x_values, y_values  # Retorna los valores de x e y válidos

def NewtonInterpol(x, y, x_eval):
    k = len(x)
    diferencias = diferencias_divididas(x, y)
    resultado = diferencias[0]
    for i in range(1, k):
        termino = diferencias[i]
        for j in range(i):
            termino *= (x_eval - x[j])
        resultado += termino
    return resultado

def diferencias_divididas(x, y):
    n = len(x)
    F = [[0] * n for _ in range(n)]
    for i in range(n):
        F[i][0] = y[i]
    for j in range(1, n):
        for i in range(n - j):
            F[i][j] = (F[i+1][j-1] - F[i][j-1]) / (x[i+j] - x[i])
    return [F[0][i] for i in range(n)]

def evaluar_polinomio_newton_extendido(x, y, x_vals):
    return [NewtonInterpol(x, y, xi) for xi in x_vals]