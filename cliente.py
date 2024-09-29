import socket
import tkinter as tk
from tkinter import messagebox

# Función para registrar usuario
def registrar_usuario():
    # Obtener datos del formulario
    nombre = entry_nombre.get()
    correo = entry_correo.get()
    contraseña = entry_contraseña.get()
    
    # Validar que los campos no estén vacíos
    if not nombre or not correo or not contraseña:
        messagebox.showwarning("Error", "Todos los campos son obligatorios.")
        return
    
    # Enviar los datos al servidor
    try:
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect(('localhost', 12345))
        datos = f"{nombre},{correo},{contraseña}"
        cliente_socket.send(datos.encode('utf-8'))
        
        # Recibir la respuesta del servidor
        respuesta = cliente_socket.recv(1024).decode('utf-8')
        
        # Mostrar resultado en mensaje emergente
        if "registrado con éxito" in respuesta:
            messagebox.showinfo("Éxito", respuesta)
            limpiar_campos()  # Limpiar campos si se registró correctamente
        else:
            messagebox.showwarning("Error", respuesta)
        
        # Cerrar la conexión
        cliente_socket.close()
    except Exception as e:
        messagebox.showerror("Error de Conexión", f"No se pudo conectar al servidor.\n{e}")

# Función para listar usuarios
def listar_usuarios():
    try:
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect(('localhost', 12345))
        cliente_socket.send("LIST".encode('utf-8'))
        
        # Recibir la lista de usuarios del servidor
        lista_usuarios = cliente_socket.recv(1024).decode('utf-8')
        messagebox.showinfo("Usuarios Registrados", lista_usuarios)
        
        # Cerrar la conexión
        cliente_socket.close()
    except Exception as e:
        messagebox.showerror("Error de Conexión", f"No se pudo conectar al servidor.\n{e}")

# Función para cerrar el servidor al cerrar la ventana
def cerrar_ventana():
    try:
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect(('localhost', 12345))
        cliente_socket.send("CLOSE".encode('utf-8'))
        
        # Recibir la respuesta del servidor
        respuesta = cliente_socket.recv(1024).decode('utf-8')
        print(f"Servidor: {respuesta}")  # Mostrar en consola que el servidor fue cerrado
        
        # Cerrar la conexión
        cliente_socket.close()
    except Exception as e:
        print(f"No se pudo conectar al servidor para cerrarlo: {e}")
    
    # Finalmente cerrar la ventana
    ventana.destroy()

# Función para limpiar los campos del formulario
def limpiar_campos():
    entry_nombre.delete(0, tk.END)
    entry_correo.delete(0, tk.END)
    entry_contraseña.delete(0, tk.END)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Registro de Usuario")

# Labels y campos de entrada
label_nombre = tk.Label(ventana, text="Nombre de Usuario:")
label_nombre.grid(row=0, column=0, padx=10, pady=10)
entry_nombre = tk.Entry(ventana)
entry_nombre.grid(row=0, column=1, padx=10, pady=10)

label_correo = tk.Label(ventana, text="Correo Electrónico:")
label_correo.grid(row=1, column=0, padx=10, pady=10)
entry_correo = tk.Entry(ventana)
entry_correo.grid(row=1, column=1, padx=10, pady=10)

label_contraseña = tk.Label(ventana, text="Contraseña:")
label_contraseña.grid(row=2, column=0, padx=10, pady=10)
entry_contraseña = tk.Entry(ventana, show="*")
entry_contraseña.grid(row=2, column=1, padx=10, pady=10)

# Botones para registrar y listar usuarios
btn_registrar = tk.Button(ventana, text="Registrar", command=registrar_usuario)
btn_registrar.grid(row=3, column=0, padx=10, pady=10)

btn_listar = tk.Button(ventana, text="Usuarios", command=listar_usuarios)
btn_listar.grid(row=3, column=1, padx=10, pady=10)

# Asignar el cierre de la ventana a la función cerrar_ventana
ventana.protocol("WM_DELETE_WINDOW", cerrar_ventana)

# Ejecutar la ventana
ventana.mainloop()
