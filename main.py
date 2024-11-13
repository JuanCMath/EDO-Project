import flet as ft
import matplotlib.pyplot as plt
import numpy as np
from flet.matplotlib_chart import MatplotlibChart
from Graficador import Euler_Runge_Kutta
import sympy as sp

# Global figures and axes
fig, ax = plt.subplots()
fig_precision, ax_precision = plt.subplots()

def plot_results(ax, t_values_exact, y_values_exact, t_values_euler, y_values_euler, t_values_runge_kutta, y_values_runge_kutta):
    ax.plot(t_values_exact, y_values_exact, label='Solucion Exacta', color='green', linewidth=2)
    ax.plot(t_values_euler, y_values_euler, label='Euler Mejorado', marker='o', markersize=4, linestyle='--', color='blue')
    ax.plot(t_values_runge_kutta, y_values_runge_kutta, label='Runge-Kutta 4º Orden', marker='x', markersize=6, linestyle=':', color='red')
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Solución de EDO")
    ax.grid(True)
    ax.legend()
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)

def create_graph(ax):
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
    T, Y, U, V = Euler_Runge_Kutta.plot_isoclines(f, (-10, 10), (-10, 10))
    ax.quiver(T, Y, U, V, color='gray', alpha=0.5)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Solución de EDO")
    ax.grid(True)
    ax.legend()
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)

def precision_tester(derivative_as_string, x_condition, y_condition, h_step, ax_precision):

    x, y = sp.symbols('x y')
    user_function = sp.sympify(derivative_as_string)
    f = sp.lambdify((x, y), user_function, 'numpy')

    
    n = 20

    euler_errors = []
    rk4_errors = []
    steps = []

    current_t = float(x_condition)
    y_condition = float(y_condition)
    h_step = float(h_step)

    for i in range (n):
        t_euler, y_euler = Euler_Runge_Kutta.euler_improved(f, current_t, y_condition, h_step, n)
        t_rk4, y_rk4 = Euler_Runge_Kutta.runge_kutta_4(f, current_t, y_condition, h_step, n)
        t_exact, y_exact = Euler_Runge_Kutta.exact_solution(f, current_t + h_step * n, y_condition)

        error_euler = abs(y_euler[-1] - y_exact[-1])
        error_rk4 = abs(y_rk4[-1] - y_exact[-1])

        euler_errors.append(error_euler)
        rk4_errors.append(error_rk4)
        steps.append(current_t + h_step * n)

        h_step /= 2
        n *= 2
        current_t += h_step * n

    # Crear la tabla de precisión
    precision_data = {
        "Paso h": steps,
        "Error Euler": euler_errors,
        "Error RK4": rk4_errors
    }

    # Mostrar la tabla en la consola (o en el formato que se use en Tester.py)
    for i in range(len(steps)):
        print(f"Paso h: {steps[i]:.6f}, Error Euler: {euler_errors[i]:.12f}, Error RK4: {rk4_errors[i]:.12f}")

    # Graficar los errores
    ax_precision.plot(steps, euler_errors, label='Error Método de Euler', color='blue', marker='o', linestyle='-', markersize=6)
    ax_precision.plot(steps, rk4_errors, label='Error Método RK4', color='red', marker='s', linestyle='--', markersize=6)
    ax_precision.set_yscale('log')
    ax_precision.set_xlabel('Paso h')
    ax_precision.set_ylabel('Error')
    ax_precision.set_title('Errores de precisión de los métodos numéricos')
    ax_precision.legend()
    ax_precision.grid(True, which="both", linestyle='--', linewidth=0.5)
    

    # Agregar anotaciones de texto en la gráfica
    for step, euler_error, rk4_error in zip(steps, euler_errors, rk4_errors):
        ax_precision.text(step, rk4_error, f'{rk4_error:.2e}', fontsize=10, verticalalignment='bottom', horizontalalignment='center', color='red')
        ax_precision.text(step, euler_error, f'{euler_error:.2e}', fontsize=10, verticalalignment='top', horizontalalignment='center', color='blue')

def main(page: ft.Page):
    page.title = "Calculador de Ecuaciones Diferenciales Ordinarias"

    def solving(derivative_as_string, x_condition_as_string, y_condition_as_string, h_step_as_string):
        x, y = sp.symbols('x y')
        user_function = sp.sympify(derivative_as_string.value)
        f = sp.lambdify((x, y), user_function, 'numpy')

        x_val = float(x_condition_as_string.value)
        y_val = float(y_condition_as_string.value)
        h = float(h_step_as_string.value)

        t_values_exact, y_values_exact = Euler_Runge_Kutta.exact_solution(f, x_val, y_val)
        t_values_euler, y_values_euler = Euler_Runge_Kutta.euler_improved(f, x_val, y_val, h, 40)
        t_values_runge_kutta, y_values_runge_kutta = Euler_Runge_Kutta.runge_kutta_4(f, x_val, y_val, h, 40)

        plot_results(ax, t_values_exact, y_values_exact, t_values_euler, y_values_euler, t_values_runge_kutta, y_values_runge_kutta)
        graph_container.content = MatplotlibChart(fig, expand=True)
        page.update()

    def on_graphing_click(derivative_as_string):
        x, y = sp.symbols('x y')
        user_function = sp.sympify(derivative_as_string.value)
        f = sp.lambdify((x, y), user_function, 'numpy')
        plot_isoclines(ax, f)
        graph_container.content = MatplotlibChart(fig, expand=True)
        page.update()

    def reset_graph():
        ax.clear()
        create_graph(ax)
        graph_container.content = MatplotlibChart(fig, expand=True)
        page.update()

    def show_precision_tester(derivative_as_string, x_condition_as_string, y_condition_as_string, h_step_as_string):
        ax_precision.clear()
        precision_tester(derivative_as_string, x_condition_as_string, y_condition_as_string, h_step_as_string, ax_precision)
        precision_graph_container.content = MatplotlibChart(fig_precision, expand=True)
        page.update()

    tb1 = ft.TextField(label="f(x,y)", width=400)
    tb2 = ft.TextField(label="x0", width=400)
    tb3 = ft.TextField(label="y0", width=400)
    tb4 = ft.TextField(label="Paso h", width=400)

    solving_button = ft.ElevatedButton(
        text="Resolver", 
        on_click=lambda ignored_parameter: solving(tb1, tb2, tb3, tb4)
    )
    graphing_button = ft.ElevatedButton(
        text="Graficar",
        on_click=lambda ignored_parameter: on_graphing_click(tb1),
    )
    reset_button = ft.ElevatedButton(
        text="Reset",
        on_click=lambda ignored_parameter: reset_graph(),
    )
    precision_button = ft.ElevatedButton(
        text="Mostrar Precisión",
        on_click=lambda ignored_parameter: show_precision_tester(tb1.value, float(tb2.value), float(tb3.value), float(tb4.value)),
    )

    graph_container = ft.Container(width=1000, height=700, alignment=ft.alignment.center)
    precision_graph_container = ft.Container(width=1000, height=700, alignment=ft.alignment.center)

    input_column = ft.Column(
        [
            tb1, tb2, tb3, tb4, solving_button, graphing_button,  precision_button, reset_button,
        ],
        width=300,
        spacing=10,
    )

    main_row = ft.Column(
        [
            ft.Row(
                [
                    input_column,
                    ft.Container(content=graph_container, expand=True, alignment=ft.alignment.center)
                ],
                expand=True,
                alignment="spaceBetween",
            ),
            ft.Container(content=precision_graph_container, expand=True, alignment=ft.alignment.center)
        ],
        expand=True,
        alignment="spaceBetween",
    )

    page.add(main_row)
    create_graph(ax)

ft.app(main)