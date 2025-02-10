# EDO Graphic Calculator
```{warning}
No somos responsables de lo que pueda llegar a hacer este proyecto
```

## Instalacion
Para instalar esta aplicacion necesita ejecutar el siguiente comando:

```{code-block}
(.venv) pip install -r requirements 
```

## Uso
### Parametros
- `f(x,y)` Funcion de la EDO
- `x0` Condicion inicial para x
- `y0`Condicion inicial para y
- `h` Largo del paso a elegir para metodos numericos
- `Cantidad de Pasos` Cantidad de pasos a tomar para ejecutar un buen RK

### Funcionalidades

- **Resolver**: Resuelve de forma analítica la EDO.
- **Graficar**: Grafica el campo de isoclinas.
- **Mostrar Precisión**: Muestra una gráfica de comparación entre la precisión de RK y la solución exacta.
- **Mostrar Interpolación**: Muestra la función solución usando RK + interpolación de Newton.
- **Mostrar Tabla**: Muestra la tabla de errores entre RK y la solución exacta.

## Funciones

### main.py
```{eval-rst}
.. admonition:: Funciones de main.py
   :class: note

   .. autofunction:: main.reset
   .. autofunction:: main.inputs_changed
   .. autofunction:: main.solving
   .. autofunction:: main.on_graphing_click
   .. autofunction:: main.show_precision_tester
   .. autofunction:: main.show_table
   .. autofunction:: main.show_newton_interpolation
   .. autofunction:: main.main
```

### Metodos de Resolucion de las EDOs
```{eval-rst}
.. admonition:: Métodos de Resolución de las EDOs
   :class: note

   .. autofunction:: Modulo1.Resolution_Algorithms.euler_improved
   .. autofunction:: Modulo1.Resolution_Algorithms.runge_kutta_4
   .. autofunction:: Modulo1.Resolution_Algorithms.calculate_isoclines
   .. autofunction:: Modulo1.Resolution_Algorithms.solve_edo
   .. autofunction:: Modulo1.Resolution_Algorithms.analitic_solution
   .. autofunction:: Modulo1.Resolution_Algorithms.NewtonInterpol
   .. autofunction:: Modulo1.Resolution_Algorithms.diferencias_divididas
   .. autofunction:: Modulo1.Resolution_Algorithms.evaluar_polinomio_newton_extendido
```

### Metodos de ayuda para la aplicacion
```{eval-rst}
.. admonition:: Métodos de ayuda para la aplicación
   :class: note

   .. autofunction:: Modulo1.Main_Methods.plot_results
   .. autofunction:: Modulo1.Main_Methods.create_graph
   .. autofunction:: Modulo1.Main_Methods.plot_isoclines
   .. autofunction:: Modulo1.Main_Methods.precision_tester
   .. autofunction:: Modulo1.Main_Methods.validate_inputs
   .. autofunction:: Modulo1.Main_Methods.plot_newton_interpolation
```

