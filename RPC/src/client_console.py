import xmlrpc.client
import sys


if len(sys.argv) != 3:
    print("$s <host> <porta>" % sys.argv[0])
    sys.exit(0)

host = sys.argv[1]
porta = sys.argv[2]

server = xmlrpc.client.ServerProxy("http://" + host + ":" + porta)

playerId = server.connect()
print("ID: %s" % playerId )

if playerId == 0:
    exit()

currentPlayer = server.getCurrenPlayer()
while (currentPlayer < 3):
    if playerId == currentPlayer:
        print("sendGuess: ", server.sendGuess(playerId, 5))

    else:
        print("getCurrentguess: ", server.getCurrentguess(playerId))

    currentPlayer = server.getCurrenPlayer()
