import numpy as np  # Librería para operaciones matemáticas y manejo de arreglos
import sympy as sp  # Librería para operaciones simbólicas

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
    x_values = [x0]
    y_values = [y0]

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
    x_values = [x0]
    y_values = [y0]
    
    for i in range(n):
        x = x_values[-1]
        y = y_values[-1]
        
        k1 = f(x, y)  # Calcula la pendiente en el punto inicial
        k2 = f(x + h / 2, y + h * k1 / 2)  # Calcula la pendiente en el punto medio usando k1
        k3 = f(x + h / 2, y + h * k2 / 2)  # Calcula la pendiente en el punto medio usando k2
        k4 = f(x + h, y + h * k3)  # Calcula la pendiente en el punto final usando k3
        
        y_next = y + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)  # Calcula el valor de y en el siguiente paso
        
        x_values.append(round(x + h, 3))  # Agrega el nuevo valor de x a la lista
        y_values.append(y_next)  # Agrega el nuevo valor de y a la lista
    
    return x_values, y_values

def calculate_isoclines(f_sympy, x_range, y_range, num_points=30):
    """
    Calcula y grafica las isoclinas de una EDO.

    :param f_sympy: Función simbólica que representa la derivada de la EDO.
    :param x_range: Rango de valores para x.
    :param y_range: Rango de valores para y.
    :param num_points: Número de puntos para la malla.
    :return: Tuple (x, y, u, v) con los valores calculados para graficar las isoclinas.
    """
    # Define las variables simbólicas
    x, y = sp.symbols('x y')

    # Crea una malla de puntos
    x_vals, y_vals = np.meshgrid(np.linspace(x_range[0], x_range[1], num_points), np.linspace(y_range[0], y_range[1], num_points))

    # Evalúa la función simbólica en cada punto de la malla
    f_vals = np.zeros_like(x_vals, dtype=float)
    for i in range(x_vals.shape[0]):
        for j in range(x_vals.shape[1]):
            f_vals[i, j] = float(f_sympy.subs({x: x_vals[i, j], y: y_vals[i, j]}))

    # Crea una matriz de unos con la misma forma que f_vals
    u = np.ones_like(f_vals)
    # Normaliza los valores de f para obtener las direcciones de las isoclinas
    v = f_vals / np.sqrt(1 + f_vals**2)

    return x_vals, y_vals, u, v

def solve_edo(f, x0, y0):
    """
    Resuelve una EDO de forma analítica.

    :param f: Función que representa la derivada de la EDO.
    :param x0: Condición inicial para x.
    :param y0: Condición inicial para y.
    :return: Solución particular de la EDO o un mensaje indicando que no existe solución.
    """
    x = sp.symbols('x')  # Define el símbolo x
    y = sp.Function('y')(x)  # Define la función y(x)
    edo = sp.Eq(y.diff(x), f(x, y))  # Crea la ecuación diferencial
    try:
        sol = sp.dsolve(edo, y)  # Intenta resolver la ecuación diferencial
    except Exception:
        return False  # Retorna False si no se puede resolver
    
    C = sp.symbols('C')  # Define el símbolo de la constante de integración
    try:
        # Intenta calcular la solución particular con las condiciones iniciales
        particular_sol = sol.subs('C1', C)
        C_value = sp.solve(particular_sol.rhs.subs(x, x0) - y0, C)[0]
        return particular_sol.subs(C, C_value)
    except:
        return False  # Retorna False si no se puede encontrar la solución particular

def analitic_solution(f, x0, y0, step):
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


    particular_sol = solve_edo(f, x0, y0)  # Obtiene la solución particular

    if(particular_sol is bool and not particular_sol):# Retorna un mensaje de error si no se encuentra solución
        return False, "No se pudo encontrar una solución analítica para la EDO."  
    
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
        except Exception as e:
            print(f"Error: Funcion {particular_sol} no definida en x = {val}")
    
    return valid_x_values, y_values  # Retorna los valores de x e y válidos