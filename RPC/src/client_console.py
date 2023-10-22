import os
import platform
import xmlrpc.client
import sys
import time


if len(sys.argv) != 3:
    print("$s <host> <porta>" % sys.argv[0])
    sys.exit(0)


if platform.system() == "Windows":
    os.system("cls")
else:
    os.system("clear")


host = sys.argv[1]
porta = sys.argv[2]

server = xmlrpc.client.ServerProxy("http://" + host + ":" + porta)

playerId = server.connect()
print("ID: %s" % playerId )

if playerId == 0:
    exit()

currentPlayer = server.getCurrenPlayer()
if playerId == 1:
    while (currentPlayer == 0):
        print("Aguardando adversário")
        time.sleep(5)
        currentPlayer = server.getCurrenPlayer()

while (currentPlayer < 3):
    currentPlayer = server.getCurrenPlayer()
    print("CP: ", currentPlayer)

    if playerId == currentPlayer:
        print("getCurrentGame: ", server.getCurrentGame(playerId))
        print("Sua vez. Escolha a primeira carta")
        userGuess = input()
        res = server.sendGuess(playerId, userGuess)
        print("getCurrentGame: ", server.getCurrentGame(playerId))

        if res == 1:
            print("Escolha a segunda carta")
            userGuess = input()
            res = server.sendGuess(playerId, userGuess)
            print("getCurrentGame: ", server.getCurrentGame(playerId))

            if res != 2:
                currentPlayer -= 1

    else:
        print("getCurrentGame: ", server.getCurrentGame(playerId))
        time.sleep(5)

