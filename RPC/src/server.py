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
        
    return guess-1

def processGuess():
    if currentGuess[0] > -1 and currentGuess[1] > -1 and currentGuess[0] != currentGuess[1] and cards[currentGuess[0]]["value"] == cards[currentGuess[1]]["value"] and not cards[currentGuess[0]]["found"] and not cards[currentGuess[1]]["found"]:
        cards[currentGuess[0]]["found"] = True
        cards[currentGuess[1]]["found"] = True
        playersScore[currentPlayer-1] += 1
    else:
        changeCurentPlayer()

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
            processGuess()

    print(currentGuess)
    return 1

def getCurrentguess(playerId):
    global currentGuess
    global currentGuessRead

    strCurrentGuess = "["
    if currentGuess[0] == 0:
        strCurrentGuess += "[0,0]"
    else:
        strCurrentGuess += "[" + str(currentGuess[0]) + "," + str(cards[currentGuess[0]]["value"]) + "], "
    if currentGuess[1] == 0:
        strCurrentGuess += "[0,0]"
    else:
        strCurrentGuess += "[" + str(currentGuess[1]) + "," + str(cards[currentGuess[1]]["value"]) + "]"
    strCurrentGuess += "]"
    
    if currentGuess[1] != 0:
        return strCurrentGuess
    
    if currentGuessRead < 3:
        if currentGuessRead != playerId:
            currentGuessRead += playerId

        return strCurrentGuess
    else:
        currentGuess = [0,0]
        currentGuessRead = 0
        return [0,0]
        

#---------------------------------------- COMUNICAÇÃO ---------------------------------------#


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
servidor.register_function(getCurrentguess, "getCurrentguess")
servidor.register_function(sendGuess, "sendGuess")


servidor.serve_forever()