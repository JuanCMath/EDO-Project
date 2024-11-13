def create_table_of_errors(derivative_as_string, x_condition_as_string, y_condition_as_string, h_step_as_string, amount_of_steps_as_string):
        table = ft.DataTable(
            columns=[
            ft.DataColumn(ft.Text("X")),
            ft.DataColumn(ft.Text("Solucion Exacta")),
            ft.DataColumn(ft.Text("Solucion con Euler")),
            ft.DataColumn(ft.Text("Solucion con Runge-Kutta")),
            ft.DataColumn(ft.Text("Error Euler")),
            ft.DataColumn(ft.Text("Error Runge-Kutta")),
            ],
            rows=[
            ft.DataRow(
                cells=[
                ft.DataCell(ft.Text("")),
                ft.DataCell(ft.Text("")),
                ft.DataCell(ft.Text("")),
                ft.DataCell(ft.Text("")),
                ft.DataCell(ft.Text("")),
                ft.DataCell(ft.Text("")),
                ]
            )
            ],
        )

        x, y = sp.symbols('x y')
        user_function = sp.sympify(derivative_as_string.value)
        f = sp.lambdify((x, y), user_function, 'numpy')

        x_val = float(x_condition_as_string.value)
        y_val = float(y_condition_as_string.value)
        h = float(h_step_as_string.value)
        n = int(amount_of_steps_as_string.value)

        x_values_exact, y_values_exact = Euler_Runge_Kutta.exact_solution(f, x_val, y_val)
        x_values_euler, y_values_euler = Euler_Runge_Kutta.euler_improved(f, x_val, y_val, h, n)
        x_values_runge_kutta, y_values_runge_kutta = Euler_Runge_Kutta.runge_kutta_4(f, x_val, y_val, h, n)


        euler_errors = []
        rk4_errors = []
        steps = []

        for i in range (n):
            error_euler = abs(y_values_euler[i] - y_values_exact[i])
            error_rk4 = abs(y_values_runge_kutta[i] - y_values_exact[i])

            euler_errors.append(error_euler)
            rk4_errors.append(error_rk4)
            steps.append(x_val + h * i)

        page.add(table)