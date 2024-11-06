import flet as ft
import matplotlib.pyplot as plt
import numpy as np
from flet.matplotlib_chart import MatplotlibChart


def main(page: ft.Page):
    # Buttons functionality
    def solving(
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
        print("*Changes graph magically*")

    # Equations input
    solution = ft.TextField(label="Resultado:", read_only=True, width=400)
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
    graph_container = ft.Container(width=600, height=400, alignment=ft.alignment.center)

    # Layout the components
    input_column = ft.Column(
        [
            tb1, tb2, tb3, tb4, tb5, solution, solvingButton, graphingButton
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
