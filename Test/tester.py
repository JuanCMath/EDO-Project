import numpy as np
import sympy as sp

def exact_solution(f, x0, y0, step):
    x_values = np.arange(-25, 25 + step, step)

    x = sp.symbols('x')
    y = sp.Function('y')(x)
    
    # Asegúrate de que las funciones trigonométricas sean reconocidas
    edo = sp.Eq(y.diff(x), f(x, y))
    sol = sp.dsolve(edo, y)
    
    C = sp.symbols('C')
    particular_sol = sol.subs('C1', C)
    C_value = sp.solve(particular_sol.rhs.subs(x, x0) - y0, C)[0]
    particular_sol = particular_sol.subs(C, C_value)
    
    print(particular_sol)
    y_values = [round(particular_sol.rhs.subs(x, val).evalf(), 6) for val in x_values]
    
    return x_values, y_values

# Ejemplo de uso
if __name__ == "__main__":
    x, y = sp.symbols('x y')
    user_function = sp.sympify("sin(x + y)")
    f = sp.lambdify((x, y), user_function, modules=['sympy'])

    x0 = 0
    y0 = 1
    step = 5

    x_values, y_values = exact_solution(f, x0, y0, step)
    print(x_values)
    print(y_values)