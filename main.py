import flet as ft
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from flet.matplotlib_chart import MatplotlibChart
from Graficador import Euler_Runge_Kutta

# Global figures and axes
fig, ax = plt.subplots()

def plot_results(ax, t_values_exact, y_values_exact, t_values_euler, y_values_euler, t_values_runge_kutta, y_values_runge_kutta):
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
    t, y, u, v = Euler_Runge_Kutta.plot_isoclines(f, (-25, 25), (-25, 25))
    ax.quiver(t, y, u, v, color='gray', alpha=0.5)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Solución de EDO")
    ax.grid(True)
    ax.legend()
    ax.autoscale()
    ax.set_xlim(-25, 25)
    ax.set_ylim(-25, 25)

def precision_tester(derivative_as_string, x_condition, y_condition, h_step, ax):

    x, y = sp.symbols('x y')
    user_function = sp.sympify(derivative_as_string)
    f = sp.lambdify((x, y), user_function, 'numpy')

    n = 40

    euler_errors = []
    rk4_errors = []
    steps = []

    current_x = float(x_condition)
    y_condition = float(y_condition)
    h_step = float(h_step)

    x_euler, y_euler = Euler_Runge_Kutta.euler_improved(f, current_x, y_condition, h_step, n)
    x_rk4, y_rk4 = Euler_Runge_Kutta.runge_kutta_4(f, current_x, y_condition, h_step, n)
    x_exact, y_exact = Euler_Runge_Kutta.exact_solution(f, x_condition, y_condition)

    for i in range (n):
        error_euler = abs(y_euler[i] - y_exact[i])
        error_rk4 = abs(y_rk4[i] - y_exact[i])

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
        ax.text(step, rk4_error, f'{rk4_error:.2e}', fontsize=10, vertical_alignment='bottom', horizontal_alignment='center', color='red')
        ax.text(step, euler_error, f'{euler_error:.2e}', fontsize=10, vertical_alignment='top', horizontal_alignment='center', color='blue')
        
def main(page: ft.Page):
    page.title = "Calculador de Ecuaciones Diferenciales Ordinarias de 1er grado"

    def solving(derivative_as_string, x_condition_as_string, y_condition_as_string, h_step_as_string, amount_of_steps_as_string):
        x, y = sp.symbols('x y')
        user_function = sp.sympify(derivative_as_string)
        f = sp.lambdify((x, y), user_function, 'numpy')

        x_val = float(x_condition_as_string)
        y_val = float(y_condition_as_string)
        h = float(h_step_as_string)
        n = int(amount_of_steps_as_string)

        t_values_exact, y_values_exact = Euler_Runge_Kutta.exact_solution(f, x_val, y_val)
        t_values_euler, y_values_euler = Euler_Runge_Kutta.euler_improved(f, x_val, y_val, h, n)
        t_values_runge_kutta, y_values_runge_kutta = Euler_Runge_Kutta.runge_kutta_4(f, x_val, y_val, h, n)

        plot_results(ax, t_values_exact, y_values_exact, t_values_euler, y_values_euler, t_values_runge_kutta, y_values_runge_kutta)
        graph_container.content = MatplotlibChart(fig, expand=True)
        page.update()

    def on_graphing_click(derivative_as_string):
        x, y = sp.symbols('x y')
        user_function = sp.sympify(derivative_as_string)
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
        ax.clear()
        precision_tester(derivative_as_string, x_condition_as_string, y_condition_as_string, h_step_as_string, ax)
        graph_container.content = MatplotlibChart(fig, expand=True)
        page.update()


    tb1 = ft.TextField(label="f(x,y)", width=400)
    tb2 = ft.TextField(label="x0", width=400)
    tb3 = ft.TextField(label="y0", width=400)
    tb4 = ft.TextField(label="Paso h", width=400)
    tb5 = ft.TextField(label="Cantidad de pasos", width=400)

    solving_button = ft.ElevatedButton(text="Resolver", 
                                       on_click = lambda ignored_parameter: solving(tb1.value, tb2.value, tb3.value, tb4.value, tb5.value))

    graphing_button = ft.ElevatedButton(text="Graficar", 
                                        on_click = lambda ignored_parameter: on_graphing_click(tb1.value))

    reset_button = ft.ElevatedButton(text="Reset", 
                                     on_click=lambda ignored_parameter: reset_graph())

    precision_button = ft.ElevatedButton(text="Mostrar Precisión", 
                                         on_click=lambda ignored_parameter: show_precision_tester(tb1.value, float(tb2.value), float(tb3.value), float(tb4.value)))

    graph_container = ft.Container(width=1000, height=700, alignment=ft.alignment.center)

    input_column = ft.Column([tb1, tb2, tb3, tb4, tb5, solving_button, graphing_button,  precision_button, reset_button], 
                             width=300, spacing=10)

    main_row = ft.Row([input_column, ft.Container(content=graph_container, expand=True, alignment=ft.alignment.center)],
                       expand=True, alignment="spaceBetween")

    page.add(main_row)
    create_graph(ax)

ft.app(main)
