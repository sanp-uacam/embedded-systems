def parse_http_request(request_data):
    """
    Parsea una solicitud HTTP y extrae método, ruta y headers
    """
    lines = request_data.split('\r\n')
    
    # Parsear línea de solicitud
    request_line = lines[0]
    method, path, version = request_line.split(' ')
    
    # Parsear headers
    headers = {}
    for line in lines[1:]:
        if line == '':
            break  # Fin de headers
        if ':' in line:
            key, value = line.split(':', 1)
            headers[key.strip()] = value.strip()
    
    return {
        'method': method,
        'path': path,
        'version': version,
        'headers': headers
    }

def build_http_response(status_code, content, content_type='text/plain'):
    """
    Construye una respuesta HTTP válida
    """
    status_messages = {
        200: 'OK',
        404: 'Not Found',
        500: 'Internal Server Error'
    }
    
    response = f"HTTP/1.1 {status_code} {status_messages.get(status_code, 'Unknown')}\r\n"
    response += f"Content-Type: {content_type}\r\n"
    response += f"Content-Length: {len(content)}\r\n"
    response += "Connection: close\r\n"
    response += "\r\n"
    response += content
    
    return response