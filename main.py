import flet as ft  # Libreria Para crear aplicaciones web
import matplotlib.pyplot as plt  # Libreria para plotear
import sympy as sp  # Libreria para manejar operaciones simbolicas
from flet.matplotlib_chart import MatplotlibChart  # Componente Flet para usar gráficos de Matplotlib
import Modulo1.Main_Methods
import Modulo1.Resolution_Algorithms # Custom module for numerical methods
from Modulo1.Main_Methods import plot_results, create_graph, plot_isoclines, precision_tester, validate_inputs # Helper functions
import io # Biblioteca para guardar como imagen la página
# Global figures and axes
fig, ax = plt.subplots()  # Crea una nueva figura y ejes para plotear

tracker ={
    "solving" : False,
    "isoclines" : False,
    "precision" : False,
    "table" : False
}

last_inputs = {
    "derivative": None,
    "x_condition": None,
    "y_condition": None,
    "h_step": None,
    "amount_of_steps": None
}

def main(page: ft.Page):
    """
    Configura y ejecuta la aplicación de Flet para resolver y graficar EDOs.

    :param page: Página de Flet donde se mostrará la aplicación.
    """
    page.title = "Calculador de Ecuaciones Diferenciales Ordinarias de 1er grado"  # Titulo de la aplicacioon

    def reset():
        """
        Resetea parametros para funcionamiento de botones.
        """
        global tracker
        global last_inputs
        tracker = { "solving" :False, "isoclines" : False, "precision" : False, "table" : False }
        last_inputs = { "derivative": None, "x_condition": None, "y_condition": None, "h_step": None, "amount_of_steps": None }

    def inputs_changed(derivative_as_string, x_condition_as_string, y_condition_as_string, h_step_as_string, amount_of_steps_as_string):

        global last_inputs
        current_inputs = {
            "derivative": derivative_as_string,
            "x_condition": x_condition_as_string,
            "y_condition": y_condition_as_string,
            "h_step": h_step_as_string,
            "amount_of_steps": amount_of_steps_as_string
        }
        if current_inputs.values == last_inputs.values:
            return False
    
        reset()
        last_inputs = current_inputs
        return True
    
    #Metodo que  resuelve la EDO y grafica sus 3 soluciones en la aplicacion
    def solving(derivative_as_string, x_condition_as_string, y_condition_as_string, h_step_as_string, amount_of_steps_as_string):
        """
        Resuelve la EDO y grafica las soluciones exacta, Euler mejorado y Runge-Kutta.

        :param derivative_as_string: Derivada de la EDO en formato de cadena.
        :param x_condition_as_string: Condición inicial para x.
        :param y_condition_as_string: Condición inicial para y.
        :param h_step_as_string: Tamaño del paso.
        :param amount_of_steps_as_string: Número de pasos.
        """
        global last_inputs
        global tracker
        # Verifica que sean validas las entradas
        is_valid, error_message = validate_inputs(derivative_as_string, x_condition_as_string, y_condition_as_string, h_step_as_string, amount_of_steps_as_string)
        if not is_valid:
            page.snack_bar = ft.SnackBar(ft.Text(error_message), open=True)  # Show an error message
            page.update()
            return
        
        if not inputs_changed(derivative_as_string, x_condition_as_string, y_condition_as_string, h_step_as_string, amount_of_steps_as_string) and tracker["solving"] == True:
            return

        # Define variables simbolicas (x e y)
        x, y = sp.symbols('x y')
        # Convierte el string en una expresion simbolica
        user_function = sp.sympify(derivative_as_string)
        # Convierte la expresion simbolica en una funcion numerica evaluable
        f = sp.lambdify((x, y), user_function, modules=['sympy'])

        # Conversion de datos de las entradas
        x_val = float(x_condition_as_string)
        y_val = float(y_condition_as_string)
        h = float(h_step_as_string)
        n = int(amount_of_steps_as_string)  

        # Resolver la EDO por los 3 metodos
        x_values_exact, y_values_exact = Modulo1.Resolution_Algorithms.analitic_solution(derivative_as_string, f, x_val, y_val, h)
        x_values_euler, y_values_euler = Modulo1.Resolution_Algorithms.euler_improved(f, x_val, y_val, h, n)
        x_values_runge_kutta, y_values_runge_kutta = Modulo1.Resolution_Algorithms.runge_kutta_4(f, x_val, y_val, h, n)

        if(x_values_exact == False): #Si no se pudo resolver la EDO con los metodos analiticos, se muestra un mensaje de error
            page.overlay.append(ft.SnackBar(ft.Text(y_values_exact), open=True))
            # Mostrar los resultados sin la solucion exacta
            plot_results(ax, [], [], x_values_euler, y_values_euler, x_values_runge_kutta, y_values_runge_kutta)
            graph_container.content = MatplotlibChart(fig, expand=True)  # Actualizar la grafica del Box
            page.update()  #Updatear la pagina para que se muestre la tabla
        else:
            # Mostrar los resultados
            plot_results(ax, x_values_exact, y_values_exact, x_values_euler, y_values_euler, x_values_runge_kutta, y_values_runge_kutta)
            graph_container.content = MatplotlibChart(fig, expand=True)  # Actualizar la grafica del Box
            page.update()  #Updatear la pagina para que se muestre la tabla

        tracker["solving"] = True

    def on_graphing_click(derivative_as_string, x_condition_as_string, y_condition_as_string, h_step_as_string, amount_of_steps_as_string):
        """
        Grafica el campo direccional de la EDO.

        :param derivative_as_string: Derivada de la EDO en formato de cadena.
        """
        global last_inputs
        global tracker
        # Verifica si las entradas son validas
        is_valid, error_message = validate_inputs(derivative_as_string, x_condition_as_string, y_condition_as_string, h_step_as_string, amount_of_steps_as_string)
        if not is_valid:
            page.snack_bar = ft.SnackBar(ft.Text(error_message), open=True)  # Show an error message
            page.update()
            return
        
        if not inputs_changed(derivative_as_string, x_condition_as_string, y_condition_as_string, h_step_as_string, amount_of_steps_as_string) and tracker["isoclines"] == True:
            return
        
        # Convierte el string entrante en una expresion simbolica
        user_function = sp.sympify(derivative_as_string)
    
        plot_isoclines(ax, user_function) #Calcula el campo Direccional y lo muestra
        graph_container.content = MatplotlibChart(fig, expand=True)  #Actualiza el contenido del Box
        page.update() #Refresca la pagina para que se muestr el resultado

        tracker["isoclines"] = True

    #Muestra usando funciones continuas como se incrementa la diferencia entre los errores producidos por Euler y RK4
    def show_precision_tester(derivative_as_string, x_condition_as_string, y_condition_as_string, h_step_as_string, amount_of_steps_as_string):
        """
        Muestra los errores de precisión de los métodos de Euler y Runge-Kutta.

        :param derivative_as_string: Derivada de la EDO en formato de cadena.
        :param x_condition_as_string: Condición inicial para x.
        :param y_condition_as_string: Condición inicial para y.
        :param h_step_as_string: Tamaño del paso.
        :param amount_of_steps_as_string: Número de pasos.
        """
        global last_inputs
        global tracker

        if not inputs_changed(derivative_as_string, x_condition_as_string, y_condition_as_string, h_step_as_string, amount_of_steps_as_string) and tracker["precision"] == True:
            return
        
        ax.clear()
        # Valida las entradas
        is_valid, error_message = validate_inputs(derivative_as_string, x_condition_as_string, y_condition_as_string, h_step_as_string, amount_of_steps_as_string)
        if not is_valid:
            page.snack_bar = ft.SnackBar(ft.Text(error_message), open=True)  # Show an error message
            page.update()
            return
        
        # Calcula los errores y los muestra
        precision_tester(derivative_as_string, x_condition_as_string, y_condition_as_string, h_step_as_string, amount_of_steps_as_string, ax)
        graph_container.content = MatplotlibChart(fig, expand=True)  # Actualiza el Box
        page.update() #Refresca la pagina

        tracker["precision"] = True

    #Muestra la tabla de soluciones para el metodo analitico y los 2 numericos junto a los errores cometidos
    def show_table(derivative_as_string, x_condition_as_string, y_condition_as_string, h_step_as_string, amount_of_steps_as_string):
        """
        Muestra una tabla con las soluciones exacta, Euler y Runge-Kutta, y sus errores.

        :param derivative_as_string: Derivada de la EDO en formato de cadena.
        :param x_condition_as_string: Condición inicial para x.
        :param y_condition_as_string: Condición inicial para y.
        :param h_step_as_string: Tamaño del paso.
        :param amount_of_steps_as_string: Número de pasos.
        """
        global last_inputs
        global tracker

        if not inputs_changed(derivative_as_string, x_condition_as_string, y_condition_as_string, h_step_as_string, amount_of_steps_as_string) and tracker["table"] == True:
            return
        
        ax.clear()
        # Valida las entradas
        is_valid, error_message = validate_inputs(derivative_as_string, x_condition_as_string, y_condition_as_string, h_step_as_string, amount_of_steps_as_string)
        if not is_valid:
            page.snack_bar = ft.SnackBar(ft.Text(error_message), open=True)  # Show an error message
            page.update()
            return

        # Define Variables (x e y)
        x, y = sp.symbols('x y')
        # Convierte el string a una expresion simbolica
        user_function = sp.sympify(derivative_as_string)
        # Convierte una expresion simbolica en una funcion evaluable
        f = sp.lambdify((x, y), user_function, modules=['sympy'])

        # Casteando las entradas en tipos de datos necesarios
        x_val = float(x_condition_as_string)
        y_val = float(y_condition_as_string)
        h = float(h_step_as_string)
        n = int(amount_of_steps_as_string)  # Convert the number of steps to int

        # Solucionar la EDO de todas las formas
        x_exact, y_exact = Modulo1.Resolution_Algorithms.analitic_solution(derivative_as_string, f, x_val, y_val, h)
        x_euler, y_euler = Modulo1.Resolution_Algorithms.euler_improved(f, x_val, y_val, h, n)
        x_rk4, y_rk4 = Modulo1.Resolution_Algorithms.runge_kutta_4(f, x_val, y_val, h, n)

        if(x_exact == False): #Si no se pudo resolver la EDO con los metodos numericos, se muestra un mensaje de error

            # Creacion de la tabla con los resultados
            table_rows = [
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(f"{x_euler[i]:.2f}")),
                    ft.DataCell(ft.Text(f"{float(y_euler[i]):.2f}")),
                    ft.DataCell(ft.Text(f"{float(y_rk4[i]):.2f}"))
               ]) for i in range(len(x_euler))
            ]

            # Creacion de la tabla en la aplicacion
            table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("X Values")),
                    ft.DataColumn(ft.Text("Euler Solution")),
                    ft.DataColumn(ft.Text("RK4 Solution")),
                ],
                rows=table_rows,
            )

            # Haciendo posible que la tabla tenga un scrollbar
            scrollable_table = ft.ListView(
                controls=[table],
                auto_scroll=True,
                width=1000,
                height=700
            )
        else:
        # Inicializacion de Arrays para guardar los errores
            euler_errors = []
            rk4_errors = []
            steps = []

            #Calculamos en que indice tenemos que empezar a comparar, 
            #(la solucion exacta toma valores -25 <= x <= 25 mientras que los metodos analiticos el usario elige un valor entre esos numeros)
            for i in range(len(x_exact)):
                if (x_exact[i] == x_euler[0]): 
                    first_index = i 
                    break

            #Calculamos los Errores Relativos a la solucion exacta de los metodos Euler y RK4
            for i in range(n):
                if (first_index + i <  len(y_exact)):
                    error_euler = abs(y_euler[i] - y_exact[first_index + i])
                    error_rk4 = abs(y_rk4[i] - y_exact[first_index + i])

                    euler_errors.append(error_euler)
                    rk4_errors.append(error_rk4)
                    steps.append(x_val + h * i)
                else:
                    break

            # Creacion de la tabla con los resultados
            table_rows = [
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(f"{step:.2f}")),
                    ft.DataCell(ft.Text(f"{float(y_exact[first_index + i]):.2f}")),
                    ft.DataCell(ft.Text(f"{float(y_euler[i]):.2f}")),
                    ft.DataCell(ft.Text(f"{float(y_rk4[i]):.2f}")),
                    ft.DataCell(ft.Text(f"{float(euler_errors[i]):.2e}")),
                    ft.DataCell(ft.Text(f"{float(rk4_errors[i]):.2e}")),
                ]) for i, step in enumerate(steps)
            ]

        # Creacion de la tabla en la aplicacion
            table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("X Values")),
                    ft.DataColumn(ft.Text("Exact Solution")),
                    ft.DataColumn(ft.Text("Euler Solution")),
                    ft.DataColumn(ft.Text("RK4 Solution")),
                    ft.DataColumn(ft.Text("Euler Error")),
                    ft.DataColumn(ft.Text("RK4 Error")),
                ],
                rows=table_rows,
            )

            # Haciendo posible que la tabla tenga un scrollbar
            scrollable_table = ft.ListView(
                controls=[table],
                auto_scroll=True,
                width=1000,
                height=700
            )

        graph_container.content = scrollable_table  # Añadiendo la tabla al Box

        page.update() # Refrescando la pagina
        tracker["table"] = True

    # Crea los campos de entrada de Texto del usuario
    tb1 = ft.TextField(label="f(x,y)", width=400)
    tb2 = ft.TextField(label="x0", width=400)
    tb3 = ft.TextField(label="y0", width=400)
    tb4 = ft.TextField(label="Paso h", width=400)
    tb5 = ft.TextField(label="Cantidad de pasos", width=400)

    # Crea los botones para resolucion de EDO en la aplicacion
    solving_button = ft.ElevatedButton(text="Resolver", 
                                       on_click = lambda ignored_parameter: solving(tb1.value, tb2.value, tb3.value, tb4.value, tb5.value))

    graphing_button = ft.ElevatedButton(text="Graficar", 
                                        on_click = lambda ignored_parameter: on_graphing_click(tb1.value, tb2.value, tb3.value, tb4.value, tb5.value))

    precision_button = ft.ElevatedButton(text="Mostrar Precisión", 
                                         on_click=lambda ignored_parameter: show_precision_tester(tb1.value, float(tb2.value), float(tb3.value), float(tb4.value), float(tb5.value)))
    
    toggle_table_button = ft.ElevatedButton(text="Mostrar Tabla", 
                                           on_click=lambda ignored_parameter: show_table(tb1.value, tb2.value, tb3.value, tb4.value, tb5.value))

    # Crea el Box donde van las graficas
    graph_container = ft.Container(width=1000, height=700, alignment=ft.alignment.center)

    # Crea una columna para los campos de entrada y botones
    input_column = ft.Column([tb1, tb2, tb3, tb4, tb5, solving_button, graphing_button, precision_button, toggle_table_button], width=300, spacing=10)

    # Crea un Box principal donde va a ir todo lo anterior para mostrarse en pantalla
    main_row = ft.Row([input_column, ft.Container(content=graph_container, expand=True, alignment=ft.alignment.center)], expand=True, alignment="spaceBetween")

    page.add(main_row)  # Añade el box principal a la aplicacion
    create_graph(ax)  # Crea el grafico inicial

ft.app(main)  # Inicia la aplicacion de Flet