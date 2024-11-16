import numpy as np
import sympy as sp
from Modulo1 import Resolution_Algorithms

def plot_results(ax, t_values_exact, y_values_exact, t_values_euler, y_values_euler, t_values_runge_kutta, y_values_runge_kutta):
    """
    Grafica los resultados de las soluciones exacta, Euler mejorado y Runge-Kutta.

    :param ax: Ejes de Matplotlib donde se graficarán los resultados.
    :param t_values_exact: Valores de tiempo de la solución exacta.
    :param y_values_exact: Valores de y de la solución exacta.
    :param t_values_euler: Valores de tiempo de la solución de Euler mejorado.
    :param y_values_euler: Valores de y de la solución de Euler mejorado.
    :param t_values_runge_kutta: Valores de tiempo de la solución de Runge-Kutta.
    :param y_values_runge_kutta: Valores de y de la solución de Runge-Kutta.
    """
    ax.plot(t_values_exact, y_values_exact, label='Solucion Exacta', color='green', linewidth=2)
    ax.plot(t_values_euler, y_values_euler, label='Euler Mejorado', marker='o', markersize=4, linestyle='--', color='blue')
    ax.plot(t_values_runge_kutta, y_values_runge_kutta, label='Runge-Kutta 4º Orden', marker='x', markersize=6, linestyle=':', color='red')
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Solución de EDO")
    ax.grid(True)
    ax.legend()
    ax.set_xlim(-25, 25)
    ax.set_ylim(-25, 25)

def create_graph(ax):
    """
    Crea un gráfico inicial con una línea horizontal en y=0.

    :param ax: Ejes de Matplotlib donde se creará el gráfico.
    """
    x = np.linspace(-100, 100, 500)
    y = x - x
    ax.plot(x, y, color="blue")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Campo Direccional: ")
    ax.axhline(0, color="black", lw=1)
    ax.axvline(0, color="black", lw=1)
    ax.grid(True)
    ax.legend()

def plot_isoclines(ax, f):
    """
    Grafica las isoclinas de la EDO.

    :param ax: Ejes de Matplotlib donde se graficarán las isoclinas.
    :param f: Función que representa la derivada de la EDO.
    """
    t, y, u, v = Resolution_Algorithms.plot_isoclines(f, (-25, 25), (-25, 25))
    ax.quiver(t, y, u, v, color='gray', alpha=0.5)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Solución de EDO")
    ax.grid(True)
    ax.legend()
    ax.autoscale()
    ax.set_xlim(-25, 25)
    ax.set_ylim(-25, 25)

def precision_tester(derivative_as_string, x_condition, y_condition, h_step, amount_of_steps_as_string, ax):
    """
    Calcula y grafica los errores de los métodos de Euler y Runge-Kutta.

    :param derivative_as_string: Derivada de la EDO en formato de cadena.
    :param x_condition: Condición inicial para x.
    :param y_condition: Condición inicial para y.
    :param h_step: Tamaño del paso.
    :param amount_of_steps_as_string: Número de pasos.
    :param ax: Ejes de Matplotlib donde se graficarán los errores.
    """
    x, y = sp.symbols('x y')
    user_function = sp.sympify(derivative_as_string)
    f = sp.lambdify((x, y), user_function, 'numpy')

    euler_errors = []
    rk4_errors = []
    steps = []

    current_x = float(x_condition)
    y_condition = float(y_condition)
    h_step = float(h_step)
    n = int(amount_of_steps_as_string)

    x_exact, y_exact = Resolution_Algorithms.analitic_solution(f, x_condition, y_condition, h_step)
    x_euler, y_euler = Resolution_Algorithms.euler_improved(f, current_x, y_condition, h_step, n)
    x_rk4, y_rk4 = Resolution_Algorithms.runge_kutta_4(f, current_x, y_condition, h_step, n)

    first_index = np.where(x_exact == x_euler[0])[0][0]
    
    for i in range (n):
        error_euler = abs(y_euler[i] - y_exact[first_index + i] )
        error_rk4 = abs(y_rk4[i] - y_exact[first_index + i])

        euler_errors.append(error_euler)
        rk4_errors.append(error_rk4)
        steps.append(current_x + h_step * i)

    # Graficar los errores
    ax.plot(steps, euler_errors, label='Error Método de Euler', color='blue', marker='o', linestyle='-', markersize=6)
    ax.plot(steps, rk4_errors, label='Error Método RK4', color='red', marker='s', linestyle='--', markersize=6)
    ax.set_yscale('log')
    ax.set_xlabel('Paso h')
    ax.set_ylabel('Error')
    ax.set_title('Errores de precisión de los métodos numéricos')
    ax.legend()
    ax.grid(True, which="both", linestyle='--', linewidth=0.5)

    # Agregar anotaciones de texto en la gráfica
    for step, euler_error, rk4_error in zip(steps, euler_errors, rk4_errors):
        ax.text(step, rk4_error, f'{float(rk4_error):.2e}', fontsize=5, va='bottom', ha='center', color='red')
        ax.text(step, euler_error, f'{float(euler_error):.2e}', fontsize=5, va='top', ha='center', color='blue')

def validate_inputs(*inputs):
    """
    Valida las entradas proporcionadas por el usuario.

    :param inputs: Entradas a validar (derivada, condiciones iniciales, tamaño del paso, número de pasos).
    :return: Tuple (bool, str) indicando si las entradas son válidas y un mensaje de error en caso de entradas inválidas.
    """
    try:
        sp.sympify(inputs[0])  
    except sp.SympifyError:
        return False, "Invalid mathematical function in f(x,y)."
    
    for i, inp in enumerate(inputs[1:], start=1):
        try:
            float(inp)  
        except ValueError:
            return False, f"Invalid numerical input in field {i}."
    
    return True, ""