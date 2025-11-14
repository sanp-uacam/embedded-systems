
from http_parser import parse_http_request, build_http_response
import socket
import os

class SimpleHTTPServer:
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port
        self.routes = {}
        
    def route(self, path):
        def decorator(handler):
            self.routes[path] = handler
            return handler
        return decorator
    
    def handle_request(self, request_data):
        try:
            request = parse_http_request(request_data)
            print(f"Procesando: {request['method']} {request['path']}")
            
            # Buscar handler para la ruta
            handler = self.routes.get(request['path'], self.not_found_handler)
            return handler(request)
            
        except Exception as e:
            return build_http_response(500, f"Error del servidor: {str(e)}")
    
    def not_found_handler(self, request):
        return build_http_response(404, "Página no encontrada")
    
    @route('/')
    def root_handler(self, request):
        html_content = """
        <html>
            <head><title>Raspberry Pi Server</title></head>
            <body>
                <h1>¡Servidor HTTP Funcionando!</h1>
                <p>Este es un servidor HTTP implementado desde cero en Raspberry Pi Zero</p>
                <ul>
                    <li><a href="/info">Información del Sistema</a></li>
                    <li><a href="/time">Hora Actual</a></li>
                </ul>
            </body>
        </html>
        """
        return build_http_response(200, html_content, 'text/html')
    
    @route('/info')
    def info_handler(self, request):
        import subprocess
        # Obtener información del sistema
        cpu_temp = subprocess.getoutput("vcgencmd measure_temp")
        uptime = subprocess.getoutput("uptime -p")
        
        info_html = f"""
        <html>
            <head><title>Información del Sistema</title></head>
            <body>
                <h1>Información de Raspberry Pi</h1>
                <p><strong>Temperatura CPU:</strong> {cpu_temp}</p>
                <p><strong>Tiempo activo:</strong> {uptime}</p>
                <a href="/">Volver al inicio</a>
            </body>
        </html>
        """
        return build_http_response(200, info_html, 'text/html')
    
    @route('/time')
    def time_handler(self, request):
        from datetime import datetime
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return build_http_response(200, f"Hora actual: {current_time}")
    
    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        
        print(f"Servidor avanzado escuchando en http://{self.host}:{self.port}")
        
        try:
            while True:
                client_socket, client_address = server_socket.accept()
                
                # Recibir solicitud
                request_data = client_socket.recv(4096).decode('utf-8')
                
                if request_data:
                    # Procesar solicitud y generar respuesta
                    response = self.handle_request(request_data)
                    client_socket.send(response.encode('utf-8'))
                
                client_socket.close()
                
        except KeyboardInterrupt:
            print("\nCerrando servidor...")
        finally:
            server_socket.close()

if __name__ == "__main__":
    server = SimpleHTTPServer()
    server.start()