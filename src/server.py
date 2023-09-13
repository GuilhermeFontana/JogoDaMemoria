import sys
import socket
import random
import time
import os

if len(sys.argv) != 2:
    print("%s <porta>" % sys.argv[0])
    sys.exit(0)

os.system("cls")

#---------------------------------------- UTILITARIOS ----------------------------------------#
def getRandomValue(min, max, level):
    rand = random.randint(min, max)

    i = 1
    while i < level:
        rand += random.randint(min, max)
        i += 1
    
    return rand // level

class Card:
    value = 0
    found = False
#---------------------------------------- UTILITARIOS ----------------------------------------#

#--------------------------------------- AÇÕES DO JOGO ---------------------------------------#
def newGame():
    cards = []
    i = 0
    while i < 10:
        cards.append(None)
        i = i + 1

    i = 0
    while i < 5:
        card = Card()
        
        contains = True
        while contains:
            card.value = getRandomValue(1,27,10)

            contains = False
            for c in cards:
                if c != None and c.value == card.value:
                    contains = True
                    break

            
        added = 0
        while added < 2:
            index = getRandomValue(0,9,1)

            print

            if cards[index] == None:
                cards[index] = card
                added = added + 1

        i += 1

    gabaritoStr = 'Gabarito: ['
    for c in cards:
        gabaritoStr += str(c.value) + ','
    gabaritoStr = gabaritoStr[0:len(gabaritoStr)-1] + ']'
    print(gabaritoStr)

    return cards

def getGame(cards):
    jogoStr = '['
    for c in cards:
        jogoStr += 'X,' if not c.found else  str(c.value) + ','
    jogoStr = jogoStr[0:len(jogoStr)-1] + ']'

    return jogoStr

def guessValidate(guess):
    if guess < 1 or guess > 10:
        return -1
        
    return guess

def getGuess(soc1, soc2, currentPlayer, cards):
    if currentPlayer == 1:
        data = soc1.recv(1024).decode('utf-8')
        print("Recebi 1: %s" % data)
    else:
        data = soc2.recv(1024).decode('utf-8')
        print("Recebi 2: %s" % data)
    
    guess = guessValidate(int(data))
    
    if guess == -1:
        soc1.send(str(guess)+"-0".encode('utf-8'))
        soc2.send(str(guess)+"-0".encode('utf-8'))
        return -1

    cardValue = cards[guess-1].value
    soc1.send((str(guess)+"-"+str(cardValue)).encode('utf-8'))
    soc2.send((str(guess)+"-"+str(cardValue)).encode('utf-8'))
    
    return guess

def endGameValidate(cards):
    for c in cards:
        if not c.found:
            return False
        
    return True
#--------------------------------------- AÇÕES DO JOGO ---------------------------------------#


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = '127.0.0.1'
porta = int(sys.argv[1])

server_socket.bind((ip, porta))
server_socket.listen(10)

print("Aguardando os jogadores...")

soc1, client1 = server_socket.accept()
print(client1)
soc1.send('1'.encode('utf-8'))
print("Aguardando o segundo jogador...")

soc2, client2 = server_socket.accept()
print(client2)
soc2.send('2'.encode('utf-8'))

currentPlayer = 1
playersScore = [0,0]
cards = newGame()

while not endGameValidate(cards):
    msg = getGame(cards)
    soc1.send(str(currentPlayer).encode('utf-8'))
    soc2.send(str(currentPlayer).encode('utf-8'))

    time.sleep(0.5)

    soc1.send(msg.encode('utf-8'))
    soc2.send(msg.encode('utf-8'))

    guess1 = getGuess(soc1, soc2, currentPlayer, cards) -1
    guess2 = getGuess(soc1, soc2, currentPlayer, cards) -1

    if guess1 > -1 and guess1 != guess2 and cards[guess1].value == cards[guess2].value and not cards[guess1].found and not cards[guess2].found:
        cards[guess1].found = True
        cards[guess2].found = True
        playersScore[currentPlayer-1] += 1

    currentPlayer = 2 if currentPlayer == 1 else 1

    print(playersScore)

soc1.send('0'.encode('utf-8'))
soc2.send('0'.encode('utf-8'))

placar = ' Placar: '+str(playersScore[0])+'x'+str(playersScore[1])
if playersScore[0] == playersScore[1]:
    soc1.send(('O jogo empatou'+placar).encode('utf-8'))
    soc2.send(('O jogo empatou'+placar).encode('utf-8'))

if playersScore[0] >= playersScore[1]:
    soc1.send(('Você ganhou.'+placar).encode('utf-8'))
    soc2.send(('Você perdeu.'+placar).encode('utf-8'))
else:
    soc1.send(('Você perdeu.'+placar).encode('utf-8'))
    soc2.send(('Você ganhou.'+placar).encode('utf-8'))

soc1.close()
soc2.close()

print('Fim de jogo. '+placar)