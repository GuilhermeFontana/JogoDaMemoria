import sys
import socket
import random

if len(sys.argv) != 2:
    print("%s <porta>" % sys.argv[0])
    sys.exit(0)

#-------------------------------------- GERAÇÃO DO JOGO --------------------------------------#
class Card:
    value = 0
    found = 'N'

cards = []
i = 0
while i < 10:
    cards.append(None)
    i = i + 1

i = 0
while i < 5:
    card = Card()
    
    card.value = random.randint(1,27)
    card.value += random.randint(1,27)
    card.value = card.value // 2


    added = 0
    while added < 2:
        index = random.randint(0,9)
        index = index + random.randint(0,9)
        index = index // 2

        if cards[index] == None:
            cards[index] = card
            added = added + 1

    i = i + 1

gabaritoStr = 'Gabarito: ['
for c in cards:
    gabaritoStr += str(c.value) + ','
gabaritoStr = gabaritoStr[0:len(gabaritoStr)-1] + ']'
print(gabaritoStr)
#-------------------------------------- GERAÇÃO DO JOGO --------------------------------------#


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = 'localhost'
porta = int(sys.argv[1])

server_socket.bind((ip, porta))
server_socket.listen(10)

soc1, client1 = server_socket.accept()
print(client1)
soc1.send('1'.encode('utf-8'))
soc2, client2 = server_socket.accept()
print(client2)
soc2.send('2'.encode('utf-8'))

currentPlayer = 1
playersScore = [0,0]

while True:
    jogoStr = '['
    for c in cards:
        jogoStr += 'X,' if c.found == 'N' else  str(c.value) + ','
    jogoStr = jogoStr[0:len(jogoStr)-1] + ']'


    msg = jogoStr
    soc1.send(str(currentPlayer).encode('utf-8'))
    soc2.send(str(currentPlayer).encode('utf-8'))

    soc1.send(msg.encode('utf-8'))
    soc2.send(msg.encode('utf-8'))

    if currentPlayer == 1:
        data = soc1.recv(1024).decode('utf-8')
        print("Recebi 1: %s" % data)
    else:
        data = soc2.recv(1024).decode('utf-8')
        print("Recebi 2: %s" % data)

    guess1 = int(data.split(',')[0]) -1
    guess2 = int(data.split(',')[1]) -1

    if guess1 != guess2 and guess1 >= 0 and guess2 >= 0 and guess1 <= 10 and guess2 <= 10: 

        if cards[guess1].value == cards[guess2].value:
            cards[guess1].found = 'S'
            cards[guess2].found = 'S'
            playersScore[currentPlayer-1] += 1

    currentPlayer = 2 if currentPlayer == 1 else 1

    print(playersScore)

s.close()