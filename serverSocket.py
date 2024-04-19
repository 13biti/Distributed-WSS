import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 19003

server_socket.bind((host, port))

server_socket.listen(5)

while True:
    client_socket, addr = server_socket.accept()
    print(f"Got connection from {addr}")

    data = client_socket.recv(1024).decode()
    print(f"Received message from client: {data}")
    client_socket.close()

