import numpy as np
from scipy.integrate import odeint
import sympy as sp
import inspect

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

        k1 = f(x, y)
        y_predict = y + h * k1

        k2 = f(x + h, y_predict)
        y_corrected = y + (h / 2) * (k1 + k2)

        x_values.append(round(x + h, 3))
        y_values.append(y_corrected)

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
        t = x_values[-1]
        y = y_values[-1]
        
        k1 = f(t, y)
        k2 = f(t + h / 2, y + h * k1 / 2)
        k3 = f(t + h / 2, y + h * k2 / 2)
        k4 = f(t + h, y + h * k3)
        
        y_next = y + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
        
        x_values.append(round(t + h, 3))
        y_values.append(y_next)
    
    return x_values, y_values

def plot_isoclines(f, x_range, y_range, num_points=30):
    """
    Calcula y grafica las isoclinas de una EDO.

    :param f: Función que representa la derivada de la EDO.
    :param x_range: Rango de valores para x.
    :param y_range: Rango de valores para y.
    :param num_points: Número de puntos para la malla.
    :return: Tuple (t, y, u, v) con los valores calculados para graficar las isoclinas.
    """
    t, y = np.meshgrid(np.linspace(x_range[0], x_range[1], num_points), np.linspace(y_range[0], y_range[1], num_points))
    f = f(t, y)

    u = np.ones_like(f)
    v = f / np.sqrt(1 + f**2)

    return t, y, u, v

def solve_edo(f, x0, y0):
    """
    Resuelve una EDO de forma analítica.

    :param f: Función que representa la derivada de la EDO.
    :param x0: Condición inicial para x.
    :param y0: Condición inicial para y.
    :return: Solución particular de la EDO.
    """
    x = sp.symbols('x')
    y = sp.Function('y')(x)
    edo = sp.Eq(y.diff(x), f(x, y))
    sol = sp.dsolve(edo, y)
    C = sp.symbols('C')
    particular_sol = sol.subs('C1', C)
    C_value = sp.solve(particular_sol.rhs.subs(x, x0) - y0, C)[0]
    return particular_sol.subs(C, C_value)

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
    helper = x0

    while (helper > -25):
        helper -= step
        x_values.append(round(helper, 3))

    helper = x0

    while (helper < 25):
        helper += step
        x_values.append(round(helper, 3))
    
    x_values.sort()

    particular_sol = solve_edo(f, x0, y0)
    y_values = [round(particular_sol.rhs.subs(sp.symbols('x'), val).evalf(), 5) for val in x_values]
    return x_values, y_values