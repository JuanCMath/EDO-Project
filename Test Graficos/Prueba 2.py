import numpy as np  
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

# Parámetros  
t0 = 0      # Valor inicial de t  
y0 = 1      # Valor inicial de y  
h = 0.5     # Tamaño del paso (aumentado para mayor diferencia)  
n = 20      # Número de pasos  

# Calcular los valores  
t_values_exact = np.linspace(t0, t0 + n * h, n + 1)  
y_values_exact = exact_solution(t_values_exact)  

t_values_euler, y_values_euler = euler_improved(f, t0, y0, h, n)  
t_values_rk4, y_values_rk4 = runge_kutta_4(f, t0, y0, h, n)  

# Graficar los resultados  
plt.figure(figsize=(10, 6))  
plt.plot(t_values_exact, y_values_exact, label='Solución Exacta', color='green', linewidth=2)  
plt.plot(t_values_euler, y_values_euler, label='Euler Mejorado', marker='o', markersize=5, linestyle='--', color='blue') # Estilo diferente  
plt.plot(t_values_rk4, y_values_rk4, label='Runge-Kutta 4º Orden', marker='x', markersize=5, linestyle=':', color='red') # Estilo diferente  

# Configuración de la gráfica  
plt.title("Comparación de Métodos de Solución de EDO")  
plt.xlabel('t')  
plt.ylabel('y')  
plt.legend()  
plt.grid()  
plt.xlim(t0, t0 + n * h)  # Configura los límites del eje x  
plt.ylim(min(min(y_values_exact), min(y_values_euler), min(y_values_rk4)) - 2,   
           max(max(y_values_exact), max(y_values_euler), max(y_values_rk4)) + 2)  # Ajuste para mejor visualización  
plt.show()