import sys
import socket

if len(sys.argv) != 3:
    print("%s <ip> <porta>" % sys.argv[0])
    sys.exit(0)

ip = sys.argv[1]
porta = int(sys.argv[2])

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ip,porta))

playerId = int(client_socket.recv(1024).decode('utf-8'))
if playerId == 1:
    print("Aguardando seu adversário...")

while(True):
    currentPlayer = int(client_socket.recv(1024).decode('utf-8'))
    data = client_socket.recv(1024).decode('utf-8')
    
    print(data)

    if playerId == currentPlayer:
        print("Sua vez. Escolha a primeira carta")
        userGuess = input()
        client_socket.send(userGuess.encode('utf-8'))

    print(client_socket.recv(1024).decode('utf-8'))
        
    if playerId == currentPlayer:
        print("Escolha a segunda carta")
        userGuess = input()
        client_socket.send(userGuess.encode('utf-8'))
        
    print(client_socket.recv(1024).decode('utf-8'))
