import socket
from http_parser import parse_http_request, send_http_response

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    host= '0.0.0.0'
    port= 8080
    
    server_socket.bind((host,port))
    server_socket.listen(5)
    
    def handler_path(path):
        if(path == "/"):
            return send_http_response (200, "Hola mundo desde handler" )
        return send_http_response(404,"")
    
    try:
        while True:
            client_socket, client_addres = server_socket.accept()
            print(f"Conexión exitosa con: {client_addres}")
            
            request_data = client_socket.recv(1024).decode('utf-8')
            
            parsed = parse_http_request(request_data)
            
            print(parsed)
            print(f"Ruta de la petición: {parsed.get("path")}")
            
            response = handler_path(parsed.get("path"))
            
            client_socket.send(response.encode('utf-8'))
            client_socket.close()      
    except KeyboardInterrupt:
        print("Apagando servidor")
    finally:
        server_socket.close()
        
if __name__ == "__main__":
    start_server()