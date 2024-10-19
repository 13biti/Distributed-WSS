import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()

port = 8001 

client_socket.connect((host, port))

client_socket.send("Hello".encode())

response = client_socket.recv(1024).decode()
print(f"Received response from server: {response}")

client_socket.close()

