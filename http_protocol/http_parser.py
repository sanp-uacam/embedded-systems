def parse_http_request(request):
    
    lines = request.split('\r\n')
    
    request_line = lines[0]
    method, path, version = request_line.split(' ')
    
    return {
        'method': method,
        'path': path,
        'version': version,
    }

def send_http_response(status_code, content, content_type='text/plain'):
    status_messages = {
        200: 'OK',
        404: 'Not Found',
        500: 'Internal Server Error'
    }
    
    response = f"HTTP/1.1 {status_code} {status_messages.get(status_code)}\r\n"
    response += f"Content-Type: {content_type}\r\n"
    response += f"Content-Length: {len(content)}\r\n"
    response += f"\r\n"
    response += content
    
    return response