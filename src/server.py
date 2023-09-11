import socket
import sys

if len(sys.argv) != 2:
    print("%s <porta>" % sys.argv[0])
    sys.exit(0)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = '172.18.41.50'
porta = int(sys.argv[1])

server_socket.bind((ip, porta))
server_socket.listen(10)

while True:
    s, client = server_socket.accept()
    s.send('Server do Gui!'.encode())
    print(client)
    s.close()