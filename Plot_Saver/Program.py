import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import io

def Folder_Selector():
    global carpeta_seleccionada
    carpeta_seleccionada = filedialog.askdirectory(title="Selecciona una carpeta")
    if carpeta_seleccionada:
        etiqueta.config(text=f'Carpeta seleccionada: {carpeta_seleccionada}')
    else:
        etiqueta.config(text='No se seleccionó ninguna carpeta.')

# Método para guardar el buffer en una ruta específica
def Plot_Saver(buffer):
    global carpeta_seleccionada, entrada_nombre
    nombre_archivo = entrada_nombre.get().strip()
    
    if carpeta_seleccionada and nombre_archivo:
        archivo_ruta = f"{carpeta_seleccionada}/{nombre_archivo}.png"

        # Guardar el contenido del buffer en el archivo
        with open(archivo_ruta, 'wb') as archivo:
            archivo.write(buffer.getbuffer())

        etiqueta.config(text=f'Captura de la interfaz guardada en: {archivo_ruta}')
        ventana.destroy()  # Cerrar la ventana después de guardar
    elif not nombre_archivo:
        etiqueta.config(text='Por favor, introduce un nombre para el archivo.')
    else:
        etiqueta.config(text='No se ha seleccionado ninguna carpeta para guardar el archivo.')

def on_entry_click(event):
    """Función para manejar el evento de clic en el campo de entrada."""
    if entrada_nombre.get() == 'Nombre del archivo':
        entrada_nombre.delete(0, tk.END)  # Eliminar el texto por defecto
        entrada_nombre.config(fg='black')
        etiqueta_nombre.place_forget()
        etiqueta_nombre.place(x=entrada_nombre.winfo_x(), y=entrada_nombre.winfo_y() - 20)

def on_focusout(event):
    """Función para manejar el evento de perder foco en el campo de entrada."""
    if entrada_nombre.get() == '':
        entrada_nombre.insert(0, 'Nombre del archivo')
        entrada_nombre.config(fg='grey')
        etiqueta_nombre.place(x=entrada_nombre.winfo_x(), y=entrada_nombre.winfo_y() - 20)
    else:
        etiqueta_nombre.place_forget()

def main(buffer):
    global etiqueta, carpeta_seleccionada, ventana, entrada_nombre, etiqueta_nombre
    carpeta_seleccionada = None

    ventana = tk.Tk()
    ventana.title("Plot Saver")

    # Obtener el ancho de la pantalla
    screen_width = ventana.winfo_screenwidth()
    # Configurar la posición X para abrir a la derecha
    ventana.geometry(f"300x300+{screen_width - 310}+100")

    boton = tk.Button(ventana, text="Seleccionar Carpeta", command=Folder_Selector)
    boton.pack(pady=20)

    etiqueta = tk.Label(ventana, text="No se ha seleccionado ninguna carpeta.")
    etiqueta.pack(pady=20)

    # Crear un campo de entrada para el nombre del archivo
    entrada_nombre = tk.Entry(ventana, fg='grey')
    entrada_nombre.insert(0, 'Nombre del archivo')
    entrada_nombre.bind('<FocusIn>', on_entry_click)
    entrada_nombre.bind('<FocusOut>', on_focusout)
    entrada_nombre.pack(pady=20)

    # Crear una etiqueta que aparecerá encima del campo de entrada
    etiqueta_nombre = tk.Label(ventana, text="Nombre del archivo", fg='grey')

    # Crear un botón que ejecutará la función para guardar la captura de la interfaz
    boton_guardar = tk.Button(ventana, text="Guardar Captura", command=lambda: Plot_Saver(buffer))
    boton_guardar.pack(pady=20)

    ventana.mainloop()