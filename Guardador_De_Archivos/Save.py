import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import io

def abrir_buscador():
    global carpeta_seleccionada
    carpeta_seleccionada = filedialog.askdirectory(title="Selecciona una carpeta")
    if carpeta_seleccionada:
        etiqueta.config(text=f'Carpeta seleccionada: {carpeta_seleccionada}')
    else:
        etiqueta.config(text='No se seleccionó ninguna carpeta.')

# Método para guardar el buffer en una ruta específica
def guardar_variable(buffer):
    global carpeta_seleccionada
    if carpeta_seleccionada:
        archivo_ruta = f"{carpeta_seleccionada}/interface_capture.png"
        
        # Guardar el contenido del buffer en el archivo
        with open(archivo_ruta, 'wb') as archivo:
            archivo.write(buffer.getbuffer())
        
        etiqueta.config(text=f'Captura de la interfaz guardada en: {archivo_ruta}')
    else:
        etiqueta.config(text='No se ha seleccionado ninguna carpeta para guardar el archivo.')

def main(buffer):
    global etiqueta, carpeta_seleccionada, ventana
    carpeta_seleccionada = None
    ventana = tk.Tk()
    ventana.title("Mi Aplicación")
    
    # Obtener el ancho de la pantalla
    screen_width = ventana.winfo_screenwidth()
    
    # Configurar la posición X para abrir a la derecha
    ventana.geometry(f"300x300+{screen_width - 310}+100")
    
    boton = tk.Button(ventana, text="Seleccionar Carpeta", command=lambda: abrir_buscador())
    boton.pack(pady=20)

    etiqueta = tk.Label(ventana, text="No se ha seleccionado ninguna carpeta.")
    etiqueta.pack(pady=20)

    # Crear un botón que ejecutará la función para guardar la captura de la interfaz
    # Usar lambda para pasar el buffer cuando se presione el botón
    boton_guardar = tk.Button(ventana, text="Guardar Captura", command=lambda: guardar_variable(buffer))
    boton_guardar.pack(pady=20)

    ventana.mainloop()