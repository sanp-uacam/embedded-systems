import socket
import subprocess
from datetime import datetime

class SimpleHTTPServer:
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port
    
    def parse_http_request(self, request_data):
        """Parsea una solicitud HTTP básica"""
        if not request_data:
            return {'method': 'GET', 'path': '/'}
        
        lines = request_data.split('\r\n')
        if lines and lines[0]:
            parts = lines[0].split(' ')
            if len(parts) >= 2:
                return {'method': parts[0], 'path': parts[1]}
        
        return {'method': 'GET', 'path': '/'}
    
    def build_http_response(self, status_code, content, content_type='text/html'):
        """Construye una respuesta HTTP básica"""
        status_messages = {200: 'OK', 404: 'Not Found'}
        
        response = f"HTTP/1.1 {status_code} {status_messages.get(status_code, 'OK')}\r\n"
        response += f"Content-Type: {content_type}\r\n"
        response += f"Content-Length: {len(content)}\r\n"
        response += "\r\n"
        response += content
        
        return response
    
    def handle_request(self, path):
        """Maneja las diferentes rutas"""
        if path == '/':
            return self.root_handler()
        elif path == '/info':
            return self.info_handler()
        elif path == '/time':
            return self.time_handler()
        else:
            return self.not_found_handler()
    
    def root_handler(self):
        html = """
        <html>
            <head><title>Servidor HTTP</title></head>
            <body>
                <h1>¡Servidor Funcionando!</h1>
                <p>Servidor HTTP desde cero en Python</p>
                <ul>
                    <li><a href="/info">Info del Sistema</a></li>
                    <li><a href="/time">Hora Actual</a></li>
                </ul>
            </body>
        </html>
        """
        return self.build_http_response(200, html)
    
    def info_handler(self):
        try:
            cpu_temp = subprocess.getoutput("vcgencmd measure_temp")
        except:
            cpu_temp = "No disponible"
        
        html = f"""
        <html>
            <body>
                <h1>Información del Sistema</h1>
                <p><strong>Temperatura:</strong> {cpu_temp}</p>
                <a href="/">Inicio</a>
            </body>
        </html>
        """
        return self.build_http_response(200, html)
    
    def time_handler(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        html = f"""
        <html>
            <body>
                <h1>Hora Actual</h1>
                <p><strong>Hora:</strong> {current_time}</p>
                <a href="/">Inicio</a>
            </body>
        </html>
        """
        return self.build_http_response(200, html)
    
    def not_found_handler(self):
        html = """
        <html>
            <body>
                <h1>404 - Página No Encontrada</h1>
                <a href="/">Volver al inicio</a>
            </body>
        </html>
        """
        return self.build_http_response(404, html)
    
    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        
        print(f"Servidor escuchando en http://{self.host}:{self.port}")
        
        try:
            while True:
                client_socket, addr = server_socket.accept()
                print(f"Conexión de {addr}")
                
                request_data = client_socket.recv(1024).decode('utf-8')
                print(f"Solicitud: {request_data.splitlines()[0] if request_data else 'Empty'}")
                
                parsed = self.parse_http_request(request_data)
                response = self.handle_request(parsed['path'])
                
                client_socket.send(response.encode('utf-8'))
                client_socket.close()
                
        except KeyboardInterrupt:
            print("\nCerrando servidor...")
        finally:
            server_socket.close()

if __name__ == "__main__":
    server = SimpleHTTPServer()
    server.start()