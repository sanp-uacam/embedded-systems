# server_basic.py
import socket

def start_basic_server():
    # Crear socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Configurar dirección y puerto
    host = '0.0.0.0'  # Escuchar en todas las interfaces
    port = 8080
    
    # Vincular socket
    server_socket.bind((host, port))
    server_socket.listen(5)
    
    print(f"Servidor escuchando en {host}:{port}")
    
    try:
        while True:
            # Aceptar conexión
            client_socket, client_address = server_socket.accept()
            print(f"Conexión aceptada de {client_address}")
            
            # Recibir datos del cliente
            request_data = client_socket.recv(1024).decode('utf-8')
            print(f"Solicitud recibida:\n{request_data}")
            
            # Enviar respuesta básica
            response = "HTTP/1.1 200 OK\r\n\r\nHola Mundo desde Raspberry Pi!"
            client_socket.send(response.encode('utf-8'))
            
            # Cerrar conexión
            client_socket.close()
            
    except KeyboardInterrupt:
        print("\nCerrando servidor...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_basic_server()