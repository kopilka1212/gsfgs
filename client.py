import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(('localhost', 12345))
def send_data():
    while True:
        print("введіть сопвіщення")
        message = input()
        client_socket.send(str(message).encode()




