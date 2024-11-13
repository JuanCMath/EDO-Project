import numpy as np  
import matplotlib.pyplot as plt  
import Graficador.Euler_Runge_Kutta as ERK
import sympy as sp

# Método de Euler  
def euler_method(f, t0, y0, h, n):  
    y = y0  
    t = t0  
    for _ in range(n):  
        y += h * f(t, y)  
        t += h  
    return y  

# Método de Runge-Kutta de 4º Orden  
def runge_kutta_4(f, t0, y0, h, n):  
    y = y0  
    t = t0  
    for _ in range(n):  
        k1 = f(t, y)  
        k2 = f(t + h / 2, y + h * k1 / 2)  
        k3 = f(t + h / 2, y + h * k2 / 2)  
        k4 = f(t + h, y + h * k3)  
        y += (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)  
        t += h  
    return y  

def precision_tester(input):  

    x, y = sp.symbols('x y')
    user_function = sp.sympify(input)
    f = sp.lambdify((x, y), user_function, 'numpy')

    t0 = 0  
    y0 = 1  
    
    h = 0.01  # Tamaño de paso más pequeño  
    n = 20    # Número inicial de pasos aumentado  

    euler_errors = []  
    rk4_errors = []  
    steps = []  
    
    current_t = t0  

    for i in range(n):  
        y_euler = ERK.euler_improved(f, current_t, y0, h, n)  
        y_rk4 = ERK.runge_kutta_4(f, current_t, y0, h, n)  
        
        y_exact = ERK.exact_solution(f, t0, y0)  

        error_euler = abs(y_euler[-1][-1] - y_exact[-1][-1])  
        error_rk4 = abs(y_rk4[-1][-1] - y_exact[-1][-1])  

        euler_errors.append(error_euler)  
        rk4_errors.append(error_rk4)  
        steps.append(current_t + h * n)  

        #print(f"t = {current_t + h * n:.2f} | Euler: {y_euler:.12f}, Error Euler: {error_euler:.12f}")  
        #print(f"t = {current_t + h * n:.2f} | RK4: {y_rk4:.12f}, Error RK4: {error_rk4:.12f}")  

        h /= 2  
        n *= 2  
        current_t += h * n  

    plt.figure(figsize=(12, 8))  
    plt.plot(steps, euler_errors, label='Error Método de Euler', color='blue', marker='o', linestyle='-', markersize=6)  
    plt.plot(steps, rk4_errors, label='Error Método RK4', color='red', marker='s', linestyle='--', markersize=6)  

    plt.yscale('log')  
    plt.xlabel('t', fontsize=14)  
    plt.ylabel('Error', fontsize=14)  
    plt.title('Errores de precisión de los métodos numéricos', fontsize=16)  
    plt.xticks(fontsize=12)  
    plt.yticks(fontsize=12)  
    plt.legend(fontsize=12)  
    plt.grid(True, which="both", linestyle='--', linewidth=0.5)  

    # Anotar los errores en la gráfica  
    for step, euler_error, rk4_error in zip(steps, euler_errors, rk4_errors):  
        plt.text(step, rk4_error, f'{rk4_error:.2e}', fontsize=10, verticalalignment='bottom', horizontalalignment='center', color='red')  
        plt.text(step, euler_error, f'{euler_error:.2e}', fontsize=10, verticalalignment='top', horizontalalignment='center', color='blue')  

    plt.show()  

# Ejecuta el tester  
precision_tester("x+y")


#TODO : parte aparte de decimal 

#lista = [1e100, 1e83, 1e83, 1e83, 1e83, 1e83, 1e83, 1e83, 1e83, 1e83, 1e83]
#from decimal import Decimal, getcontext  

#def sumar_con_precision(numeros):  
    # Establecer la precisión deseada  
#    getcontext().prec = 17  # Puedes ajustar la precisión según sea necesario  
    #ordeno de menor a mayor para que sea aún más la precisión 
#    numeros.sort()
    # Convertir la lista de números a Decimal y sumarlos  
#    suma = 0
#    for numero in numeros:
#        suma += Decimal(numero)
#    return suma

# Llamar al método de suma  
#resultado_preciso = sumar_con_precision(lista)
#print(resultado_preciso)