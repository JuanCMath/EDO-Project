import numpy as np
from scipy.integrate import odeint
import sympy as sp

def euler_improved(f, x0, y0, h, n):
    x_values = [x0]
    y_values = [y0]

    for i in range(n):
        t = x_values[-1]
        y = y_values[-1]

        k1 = f(t, y)
        y_predict = y + h * k1

        k2 = f(t + h, y_predict)
        y_corrected = y + (h / 2) * (k1 + k2)

        x_values.append(t + h)
        y_values.append(y_corrected)

    return x_values, y_values

def runge_kutta_4(f, x0, y0, h, n):
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
        
        x_values.append(t + h)
        y_values.append(y_next)
    
    return x_values, y_values

def plot_isoclines(f, x_range, y_range, num_points=30):
    t, y = np.meshgrid(np.linspace(x_range[0], x_range[1], num_points), np.linspace(y_range[0], y_range[1], num_points))
    f = f(t, y)

    u = np.ones_like(f)
    v = f / np.sqrt(1 + f**2)

    return t, y, u, v

def exact_solution(f, x0, y0, step):

    x_values = np.arange(-25, 25 + step, step)

    x = sp.symbols('x')
    y = sp.Function('y')(x)
    
    edo = sp.Eq(y.diff(x), f(x, y))
    sol = sp.dsolve(edo, y)
    
    C = sp.symbols('C')
    particular_sol = sol.subs('C1', C)
    C_value = sp.solve(particular_sol.rhs.subs(x, x0) - y0, C)[0]
    particular_sol = particular_sol.subs(C, C_value)
    
    y_values = [round(particular_sol.rhs.subs(x, val).evalf(), 5) for val in x_values]
    
    return x_values, y_values