import flet as ft
import matplotlib.pyplot as plt
import numpy as np
from flet.matplotlib_chart import MatplotlibChart
from Graficador import Euler_Runge_Kutta
import sympy as sp

def main(page: ft.Page):
    # Buttons functionality
    def solving( #TODO: Add the solution to the problem
        derivativeAsString,
        xConditionAsString,
        yConditionAsString,
        hStepAsString,
        valueToCalculateAsString,):

        solution.focus()
        solution.value = "*PERFECT SOLUTION*"  # Put the solution here
        page.update()

    def createGraph():
        # Creating generic graph
        page.title = "EDO Solver and Grapher"
        x = np.linspace(-100, 100, 500)
        y = x - x

        fig, ax = plt.subplots()
        ax.plot(x, y, color="blue")

        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title("Campo Direccional: ")
        ax.axhline(0, color="black", lw=1)
        ax.axvline(0, color="black", lw=1)
        ax.grid(True)
        ax.legend()

        # Adding the graph to the display
        graph_container.content = MatplotlibChart(fig, expand=True)
        page.update()

    def onGraphingClick(
        derivativeAsString,
        xConditionAsString,
        yConditionAsString,
        hStepAsString,
        valueToCalculateAsString,
    ):
        # Getting the function from the input
        x, y = sp.symbols('x y')
        user_function = sp.sympify(derivativeAsString.value)
        f = sp.lambdify((x, y), user_function, 'numpy')

        # Getting the inputs Value
        x_val = float(xConditionAsString.value)
        y_val = float(yConditionAsString.value)
        h = float(hStepAsString.value)
        n = float(valueToCalculateAsString.value)


        # Exact solution #TODO
        t_values_exact, y_values_exact = Euler_Runge_Kutta.exact_solution(f ,x_val, y_val)

        #Euler Improved
        t_values_euler, y_values_euler = Euler_Runge_Kutta.euler_improved(f, x_val, y_val, h, 20)

        # Runge_kutta_4
        t_values_runge_kutta, y_values_runge_kutta = Euler_Runge_Kutta.runge_kutta_4(f, x_val, y_val, h, 20)


        #Isoclinas
        T, Y, U, V = Euler_Runge_Kutta.plot_isoclines(f, (-10, 10), (-10, 10))

        # Plot the results
        fig, ax = plt.subplots()

        ax.plot(t_values_exact, y_values_exact, label='Solucion Exacta', color='green', linewidth=2)
        ax.plot(t_values_euler, y_values_euler, label='Euler Mejorado', marker='o', markersize=4, linestyle='--', color='blue')
        ax.plot(t_values_runge_kutta, y_values_runge_kutta, label='Runge-Kutta 4º Orden', marker='x', markersize=6, linestyle=':', color='red')
        ax.quiver(T, Y, U, V, color='gray', alpha=0.5)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title("Solución de EDO")
        ax.grid(True)
        ax.legend()

        # Set axis limits
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)

        # Adding the graph to the display
        graph_container.content = MatplotlibChart(fig, expand=True)
        page.update()

    # Equations input
    solution = ft.Text(value="Resultado:", width=400)
    tb1 = ft.TextField(label="y'", width=400)
    tb2 = ft.TextField(label="x0", width=400)
    tb3 = ft.TextField(label="y0", width=400)
    tb4 = ft.TextField(label="Paso h", width=400)
    tb5 = ft.TextField(label="Calcular y en x", width=400)
    solvingButton = ft.ElevatedButton(text="Resolver", on_click=solving)
    graphingButton = ft.ElevatedButton(
        text="Graficar",
        on_click=lambda ignoredParameter: onGraphingClick(tb1, tb2, tb3, tb4, tb5),
    )
    # Create a container for the graph
    graph_container = ft.Container(width=1000, height=700, alignment=ft.alignment.center)

    # Layout the components
    input_column = ft.Column(
        [
            tb1, tb2, tb3, tb4, tb5,  solvingButton, solution, graphingButton
        ],
        width=300,
        spacing=10,
    )

    main_row = ft.Row(
        [
            input_column,
            ft.Container(content=graph_container, expand=True, alignment=ft.alignment.center)
        ],
        expand=True,
        alignment="spaceBetween",
    )

    page.add(main_row)
    createGraph()

ft.app(main)
