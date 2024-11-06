import numpy as np  
from scipy.integrate import odeint
import matplotlib.pyplot as plt  

# Definición de la función derivada  
def f(t, y):  
    return y + t  

# Solución exacta  
def exact_solution(t):  
    return np.exp(t) - t - 1  

# Método de Euler Mejorado  
def euler_improved(f, t0, y0, h, n):  
    t_values = [t0]  
    y_values = [y0]  
    
    for i in range(n):  
        t = t_values[-1]  
        y = y_values[-1]  
        
        # Predicción  
        k1 = f(t, y)  
        y_predict = y + h * k1  
        
        # Corrección  
        k2 = f(t + h, y_predict)  
        y_corrected = y + (h / 2) * (k1 + k2)  
        
        t_values.append(t + h)  
        y_values.append(y_corrected)  
    
    return t_values, y_values  

# Método de Runge-Kutta de 4º Orden  
def runge_kutta_4(f, t0, y0, h, n):  
    t_values = [t0]  
    y_values = [y0]  
    
    for i in range(n):  
        t = t_values[-1]  
        y = y_values[-1]  
        
        k1 = f(t, y)  
        k2 = f(t + h / 2, y + h * k1 / 2)  
        k3 = f(t + h / 2, y + h * k2 / 2)  
        k4 = f(t + h, y + h * k3)  
        
        y_next = y + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)  
        
        t_values.append(t + h)  
        y_values.append(y_next)  
    
    return t_values, y_values  

# Función para graficar el campo de isoclinas
def plot_isoclines(f, t_range, y_range, num_points=50):
    t = np.linspace(t_range[0], t_range[1], num_points)
    y = np.linspace(y_range[0], y_range[1], num_points)
    T, Y = np.meshgrid(t, y)
    F = f(T, Y)

    # Normalize the arrows
    U = np.ones_like(F)
    V = F / np.sqrt(1 + F**2)

    return T, Y, U, V


# Función para determinar la solución exacta de la EDO
def exact_solution(f, t0, y0, t_values=np.linspace(-10, 10, 100)):

    def wrapper(y, t):
        return f(t, y)

    y_values = odeint(wrapper, y0, t_values)
    return t_values, y_values.flatten()