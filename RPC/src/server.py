import os
import platform
import xmlrpc.server
import sys
import random

MAX_CARDS = 100
MIN_CARDS = 1
COUNT_CARDS = 40


#---------------------------------------- UTILITARIOS ----------------------------------------#
def getRandomValue(min, max, level):
    rand = random.randint(min, max)

    i = 1
    while i < level:
        rand += random.randint(min, max)
        i += 1
    
    return rand // level

def changeCurentPlayer():
    global currentPlayer
    currentPlayer = 2 if currentPlayer == 1 else 1
#---------------------------------------- UTILITARIOS ----------------------------------------#

#--------------------------------------- AÇÕES DO JOGO ---------------------------------------#
def newGame():
    cards = []
    i = 0
    while i < COUNT_CARDS:
        cards.append(None)
        i = i + 1

    i = 0
    while i < COUNT_CARDS // 2:
        card = {
            "value": 0,
            "found": False
        }
        
        contains = True
        while contains:
            card["value"] = getRandomValue(MIN_CARDS,MAX_CARDS,10)

            contains = False
            for c in cards:
                if c != None and c["value"] == card["value"]:
                    contains = True
                    break

            
        added = 0
        while added < 2:
            index = getRandomValue(0,(COUNT_CARDS-1),1)

            print

            if cards[index] == None:
                cards[index] = card
                added = added + 1

        i += 1

    gabaritoStr = 'Gabarito: ['
    for c in cards:
        gabaritoStr += str(c["value"]) + ','
    gabaritoStr = gabaritoStr[0:len(gabaritoStr)-1] + ']'
    #print(gabaritoStr)

    return cards

def guessValidate(guess):
    global cards

    if guess < MIN_CARDS or guess > COUNT_CARDS:
        return -1
    
    if cards[guess-1]["found"]:
        return -1
    
    if guess == currentGuess[0]:
        return -1
        
    return guess

def processGuess():
    if currentGuess[0] > 0 and currentGuess[1] > 0 and currentGuess[0] != currentGuess[1] and cards[currentGuess[0]-1]["value"] == cards[currentGuess[1]-1]["value"] and not cards[currentGuess[0]-1]["found"] and not cards[currentGuess[1]-1]["found"]:
        cards[currentGuess[0]]["found"] = True
        cards[currentGuess[1]]["found"] = True
        playersScore[currentPlayer-1] += 1
        return 2
    
    return 1

#--------------------------------------- AÇÕES DO JOGO ---------------------------------------#

#---------------------------------------- COMUNICAÇÃO ---------------------------------------#

def connect():
    global clientsCouter
    
    if clientsCouter > 1:
        return 0
    else:
        clientsCouter += 1

    return clientsCouter
    
def getCurrenPlayer():
    global currentPlayer
    global clientsCouter

    if clientsCouter < 2:
        return 0

    return currentPlayer

def sendGuess(playerId, guess):
    global currentPlayer
    global currentGuess
    global currentGuessRead

    if playerId != currentPlayer:
        return 0

    if currentGuessRead < 3 and currentGuess[1] != 0:
        return 0

    if currentGuessRead == 3 and currentGuess[1] != 0:
        currentGuess = [0,0]
        currentGuessRead = 0

    print("Recebi: ", guess, " | ", playerId)
    _guess = guessValidate(int(guess))

    if _guess == -1:
        changeCurentPlayer()
        currentGuess = [0,0]
        return -1

    if currentGuess[0] == 0:
        currentGuess[0] = _guess
    else:
        if currentGuess[1] == 0:
            currentGuess[1] = _guess
            res = processGuess()
            if res != 2:
                changeCurentPlayer()


    # print(currentGuess)
    return 1

def getCurrentGame(playerId):
    global currentGuess
    global currentGuessRead
    global cards

    print(currentGuess)

    jogoStr = '['
    for i, c in enumerate(cards):
        if ((currentGuess[0] != 0 and currentGuess[0] == i) or (currentGuess[1] != 0 and currentGuess[1] == i)):
            jogoStr += str(c["value"]) + ','
        else:
            jogoStr += 'X,' if not c["found"] else  str(c["value"]) + ','
    jogoStr = jogoStr[0:len(jogoStr)-1] + ']'
        
    if currentGuess[1] == 0:
        return jogoStr

    if currentGuessRead < 3 and currentGuessRead != playerId:
        currentGuessRead += playerId

    return jogoStr


#---------------------------------------- COMUNICAÇÃO ---------------------------------------#

if platform.system() == "Windows":
    os.system("cls")
else:
    os.system("clear")

if len(sys.argv) != 2:
    print("$s <porta>" % sys.argv[0])
    sys.exit(0)

porta = int(sys.argv[1])

servidor = xmlrpc.server.SimpleXMLRPCServer(("", porta))
servidor.register_multicall_functions()


cards = newGame()

clientsCouter = 0

currentGuess = [0,0]
currentGuessRead = 0

currentPlayer = 1
playersScore = [0,0]


servidor.register_function(connect, "connect")
servidor.register_function(getCurrenPlayer, "getCurrenPlayer")
servidor.register_function(getCurrentGame, "getCurrentGame")
servidor.register_function(sendGuess, "sendGuess")


servidor.serve_forever()