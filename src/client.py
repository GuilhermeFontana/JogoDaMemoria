import socket
import sys

if len(sys.argv) != 3:
    print("%s <ip> <porta>" % sys.argv[0])
    sys.exit(0)

ip = sys.argv[1]
porta = int(sys.argv[2])

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ip,porta))

data = client_socket.recv(1024).decode()

print("Recebi; %s" % data)
