import socket
import csv
import os

# Función para verificar si el correo ya está registrado
def verificar_usuario_existente(correo):
    if not os.path.exists('usuarios.csv'):
        return False  # El archivo no existe, así que el usuario no puede estar registrado
    with open('usuarios.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] == correo:  # Comparar el correo (índice 1)
                return True
    return False

# Función para registrar el usuario si no está registrado
def registrar_usuario(datos_usuario):
    correo = datos_usuario[1]
    if verificar_usuario_existente(correo):
        return "Error: El correo ya está registrado."
    else:
        with open('usuarios.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(datos_usuario)
            return "Usuario registrado con éxito."

# Función para listar los usuarios registrados
def listar_usuarios():
    if not os.path.exists('usuarios.csv'):
        return "No hay usuarios registrados."
    
    usuarios = []
    with open('usuarios.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            usuarios.append(f"Nombre: {row[0]}, Correo: {row[1]}")
    
    if usuarios:
        return "\n".join(usuarios)
    else:
        return "No hay usuarios registrados."

# Configuración del servidor
def servidor():
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.bind(('localhost', 12345))
    servidor_socket.listen(5)
    
    print("Servidor escuchando en el puerto 12345...")
    
    while True:
        cliente_socket, direccion = servidor_socket.accept()
        print(f"Conexión establecida con {direccion}")
        
        # Recibir datos del cliente
        datos = cliente_socket.recv(1024).decode('utf-8')
        print(f"Datos recibidos: {datos}")
        
        # Procesar los comandos especiales o registrar usuario
        if datos == "CLOSE":
            cliente_socket.send("Servidor cerrado.".encode('utf-8'))
            cliente_socket.close()
            break  # Terminar el bucle del servidor
        elif datos == "LIST":
            lista_usuarios = listar_usuarios()
            cliente_socket.send(lista_usuarios.encode('utf-8'))
        else:
            usuario_info = datos.split(',')
            resultado = registrar_usuario(usuario_info)
            cliente_socket.send(resultado.encode('utf-8'))
        
        # Cerrar la conexión con el cliente
        cliente_socket.close()

    servidor_socket.close()  # Cerrar el servidor cuando se recibe el comando CLOSE
    print("Servidor cerrado.")

if __name__ == "__main__":
    servidor()
