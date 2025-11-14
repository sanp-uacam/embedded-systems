import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect(('192.168.137.10', 8080))
client_socket.connect(('localhost', 8080))

request = 'GET /api HTTP/1.1\r\nHost: localhost\r\n'
# request += 'Content-Lenght: 100\r\n'
# request += '{"user":"""}'
client_socket.send(request.encode())

response = client_socket.recv(4096).decode()
print(response)

client_socket.close()