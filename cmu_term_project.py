#################################################
# cmu_term_project.py
#
# Your name:David Fletcher
# Your andrew id:dfletche
#
#################################################

import cs112_f21_week6_linter
import math, copy, random
import sys
from random import randint
from cmu_112_graphics import * 

class Game(object):
    def __init__(self, blinds, button, players, deck):
        # array of players who havent busted yet
        self.playersNoBust = players
        # array of player object
        self.players = players
        # tuple containing small and big blinds
        self.blinds = blinds 
        # index of current player
        self.currPlayerIndex = 0 
        # current player bet size
        self.betSize = 0
        # current pot size
        self.totalPotSize = self.blinds[0] + self.blinds[1]
        self.currTurn = 0 # current turn 0, 1, 2, 3
        self.button = button
        self.playersLeft = len(players)
        # set current board deck to deck
        self.deck = deck
        self.winningPlayerIndex = 0

    def incrPlayerCounter(self):
        self.currPlayerIndex = (1 + self.currPlayerIndex) % len(self.players)

    def isPreflop(self):
        if self.currTurn == 0:
            return True
        return False

    def isFlop(self):
        if self.currTurn == 1:
            return True
        return False

    def isTurn(self):
        if self.currTurn == 2:
            return True
        return False

    def isRiver(self):
        if self.currTurn == 3:
            return True
        return False
#all of the is functions return a 5 card hand
    def isStraightFlush(self, hand):
        suitDict = {
            'Clubs': [],
            'Diamonds': [],
            'Spades': [],
            'Hearts': []
        }
        for card in hand:
            suitDict[card.suit].append(card.rank)
        for key in suitDict:
            if(len(suitDict[key])>=5):
                suitDict[key].sort()
                if((suitDict[key][4]-suitDict[key][0])==4):
                    return suitDict[key]
                elif(len(suitDict[key])==6):
                    if((suitDict[key][5]-suitDict[key][1])==4):
                        return suitDict[key][1:6]
                elif(len(suitDict[key])==7):
                    if((suitDict[key][6]-suitDict[key][2])==4):
                        return suitDict[key][2:7]
        return None

    def isQuads(self, hand):   
        rankDict={2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[],11:[],12:[],13:[],14:[]}
        finalList=[]
        for card in hand:
            rankDict[card.rank].append(card.suit)
        for key in rankDict:
            if(len(rankDict[key])==4):
                finalList=4*[key]
                finalList+=[]
                for i in range(14,1,-1):
                    if(i!=finalList[0] and len(rankDict[key])>0):
                        finalList.append(key)
                        return finalList
        return None

    def isFullHouse(self, hand):
        rankDict={2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0}
        finalList=[]
        for card in hand:
            rankDict[card.rank]+=1
        for i in range(14,1,-1):
            if(rankDict[i]==3):
                finalList=3*[i]
                finalList+=[]
                for j in range(14,1,-1):
                    if(rankDict[j]>=2 and i!=j):
                        finalList.append(j)
                        finalList.append(j)
                        return finalList
        return None

    def isFlush(self, hand):
        suitDict = {
            'Clubs': [],
            'Diamonds': [],
            'Spades': [],
            'Hearts': []
        }
        for card in hand:
            suitDict[card.suit].append(card.rank)
        for key in suitDict:
            if(len(suitDict[key])>=5):
                suitDict[key].sort(reverse=True)
                return suitDict[key][0:4]

    
    def isStraight(self, hand):
        suitSet = set()
        suitList = []
        for card in hand:
            suitSet.add(card.rank)
        suitList = list(suitSet)
        suitList.sort()
        if (len(suitList) >= 7):
            if (suitList[6] - suitList[2] == 4):
                return suitList[2:7]
        if (len(suitList) >= 6):
            if (suitList[5] - suitList[1] == 4):
                return suitList[1:6]
        if (len(suitList) >= 5):
            if (suitList[4] - suitList[0] == 4):
                return suitList[0:5]
        return None
            
        
    def isTrips(self, hand):
        rankDict={2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0}
        finalList=[]
        for card in hand:
            rankDict[card.rank]+=1
        for i in range(14,1,-1):
            if(rankDict[i]==3):
                finalList=3*[i]
                finalList+=[]
                for j in range(14,1,-1):
                    if(rankDict[j]==1 and j!=i):
                        finalList+=[j]
                        if(len(finalList)==5):
                            return finalList
        return None

    def isTwoPair(self, hand):
        rankDict={2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0}
        finalList=[]
        for card in hand:
            rankDict[card.rank]+=1
        for i in range(14,1,-1):
            if(rankDict[i]==2):
                finalList=2*[i]
                finalList+=[]
                for j in range(i-1,1,-1):
                    if(rankDict[j]==2 and j!=i):
                        finalList+=2*[j]
                        for k in range(14,1,-1):
                            if(k!=i and k!=j):
                                finalList.append(k)
                                return finalList
        return None

    def isPair(self, hand):
        rankDict={2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0}
        finalList=[]
        for card in hand:
            rankDict[card.rank]+=1
        for i in range(14,1,-1):
            if(rankDict[i]==2):
                finalList=2*[i]
                finalList+=[]
                for j in range(14,1,-1):
                    if(rankDict[j]==1 and j!=i):
                        finalList+=[j]
                        if(len(finalList)==5):
                            return finalList
        return None

    def isHighCard(self, hand):
        suitList = []
        for card in hand:
            suitList.append(card.rank)
        suitList.sort()
        return suitList[0:5]

    def revealFlop(self):
        print("The flop is... \n" 
        + str(self.deck.flop[0]) + "\n" +
            str(self.deck.flop[1]) +  "\n" +
            str(self.deck.flop[2]))
    
    def revealTurn(self):
        print("The turn is... \n" +
            str(self.deck.turn))

    def revealRiver(self):
        print("The river is... \n" +
            str(self.deck.river))

#reveals the next center card
    def nextTurn(self):
        self.currTurn += 1
        self.currPlayerIndex = 0
        self.playersLeft = len(self.players)
        self.betSize = 0
        for player in self.players:
            player.roundBetSize = 0
            player.handStrength = 0
        # case on turn
        if (self.isFlop()):
            self.revealFlop()
        elif (self.isTurn()):
            self.revealTurn()
        elif (self.isRiver()):
            self.revealRiver()
#decides what the bot will do
    def botDecision(self):
        betSize = self.betSize
        potSize = self.totalPotSize
        currPlayer = self.players[self.currPlayerIndex]
        stackSize=currPlayer.numChips
        handStrength = 0
        if (self.currTurn > 0):
            handStrength = self.strengthPlayerFlop(currPlayer,self.currTurn)
        else:
            handStrength = self.strengthPlayerPre(currPlayer)
        if(self.currTurn==0):
            if(betSize==0):
                if(handStrength>50):
                    return ("bet", int(((handStrength-35)//15)*potSize))
                else:
                    return ("check",0)
            else:
                if(handStrength >= int(200*betSize/potSize) and betSize*2<stackSize and handStrength>70):
                    return ("raise",min(betSize*2,stackSize))
                elif(handStrength >= int(70*betSize/potSize)):
                    return ("call",0)
                else:
                    return ("fold",0)

        elif(self.currTurn==1):
            if(betSize==0):
                if(handStrength>50):
                    return ("bet", min(int(((handStrength-30)/100)*potSize)+2,stackSize))
                else:
                    return ("check",0)
            else:
                if(handStrength >= int(180*betSize/potSize) and betSize*2<stackSize and handStrength>75):
                    return ("raise",min(betSize*2,stackSize))
                elif(handStrength >= int(120*betSize/potSize) and handStrength>60):
                    return ("call",0)
                else:
                    return ("fold",0)

        elif(self.currTurn==2):
            if(betSize==0):
                if(handStrength>60):
                    return ("bet", min(int(((handStrength-45)/100)*potSize)+2,stackSize))
                else:
                    return ("check",0)
            else:
                if(handStrength >= int(200*betSize/potSize) and betSize*2<stackSize and handStrength>80):
                    return ("raise",min(betSize*2,stackSize))
                elif(handStrength >= int(200*betSize/potSize) and handStrength >= 65):
                    return ("call",0)
                else:
                    return ("fold",0)

        elif(self.currTurn==3):
            if(betSize==0):
                if(handStrength>70):
                    return ("bet", min(int(((handStrength-45)/100)*potSize)+2,stackSize))
                else:
                    return ("check",0)
            else:
                if(handStrength >= int(200*betSize/potSize) and betSize*2<stackSize and handStrength>90):
                    return ("raise",min(betSize*2,stackSize))
                elif(handStrength >= int(300*betSize/potSize) and handStrength >= 75):
                    return ("call",0)
                else:
                    return ("fold",0)
#determines a players strength preflop
    def strengthPlayerPre(self, player):
        strength1=0
        card1=player.hand[0]
        card2=player.hand[1]
        strength1+=(card1.rank+card2.rank)
        if(card1.rank>=10 and card2.rank>=10):
            strength1+=(card1.rank+card2.rank)
        if(abs(card1.rank-card2.rank)<=4):
            strength1+=((6-abs(card1.rank-card2.rank))**2)
        if(card1.rank==card2.rank):
            strength1+=10
        if(card1.suit==card2.suit and abs(card1.rank-card2.rank)<=3):
            strength1+=(5-abs(card1.rank-card2.rank))**2
        player.strength=strength1
        print(strength1)
        return strength1
#determines a players strength post flop
    def strengthPlayerFlop(self, player,x):
        strength1=0
        total=10000
        totalWins=0
        playerFiveCardHand=[player.hand[0]]
        playerFiveCardHand.append(player.hand[1])
        playerFiveCardHand.extend(self.deck.flop)
        #need to debug
        if(x==2):
            playerFiveCardHand.append(self.deck.turn)
        if(x==3):
            playerFiveCardHand.append(self.deck.river)
        playersCards = self.rankAndOrder(playerFiveCardHand)
        for i in range(total):
            randomFiveCardHand=copy.copy(self.deck.flop)
            twoRandomCards=self.deck.dealTestHand()
            randomFiveCardHand.append(twoRandomCards[0])
            randomFiveCardHand.append(twoRandomCards[1])
            if(x==2):
                randomFiveCardHand.append(self.deck.turn)
            if(x==3):
                randomFiveCardHand.append(self.deck.river)
            testingHand=self.rankAndOrder(randomFiveCardHand)
            if(playersCards[0]>testingHand[0]):
                totalWins+=1
            elif(playersCards[0]==testingHand[0]):
                if(playersCards[1][0]>testingHand[1][0]):
                    totalWins+=1
                elif(playersCards[1][0]==testingHand[1][0]):
                    totalWins+=0.5
        strength1=totalWins//(total//100)
        player.handStrength=strength1
        print(strength1)
        return strength1

    #ranks and orders the cards
    def rankAndOrder(self, Cards):
        straightFlush = self.isStraightFlush(Cards)
        quads = self.isQuads(Cards)
        fullHouse = self.isFullHouse(Cards)
        flush = self.isFlush(Cards)
        straight = self.isStraight(Cards)
        trips = self.isTrips(Cards)
        twoPair = self.isTwoPair(Cards)
        pair = self.isPair(Cards)
        highCard = self.isHighCard(Cards)
        
        theIndex=0
        theCards=[]

        if straightFlush != None:
                theIndex = 8
                theCards = straightFlush

        elif quads != None:
            theIndex = 7
            theCards = quads
 
        elif fullHouse != None:
            theIndex = 6

        elif flush != None:
            theIndex = 5
            theCards = flush

        elif straight != None:
            theIndex = 4
            theCards = straight

        elif trips != None:
            theIndex = 3
            theCards = trips

        elif twoPair != None:
            theIndex = 2
            theCards = twoPair

        elif pair != None:
            theIndex = 1
            theCards = pair

        elif highCard != None:
            theIndex = 0
            theCards = highCard
        return [theIndex,theCards]

            #figures out what the card hand is
    def setIndices(self):
        # go through each player and calculate index
        for player in self.players:
            seven_card_hand =  []
            seven_card_hand.extend(self.deck.flop)
            seven_card_hand.append(self.deck.turn)
            seven_card_hand.append(self.deck.river)
            seven_card_hand.append(player.hand[0])
            seven_card_hand.append(player.hand[1])

            straightFlush = self.isStraightFlush(seven_card_hand)
            quads = self.isQuads(seven_card_hand)
            fullHouse = self.isFullHouse(seven_card_hand)
            flush = self.isFlush(seven_card_hand)
            straight = self.isStraight(seven_card_hand)
            trips = self.isTrips(seven_card_hand)
            twoPair = self.isTwoPair(seven_card_hand)
            pair = self.isPair(seven_card_hand)
            highCard = self.isHighCard(seven_card_hand)

            if straightFlush != None:
                player.handIndex = 8
                player.finalHand = straightFlush
                print("Straight flush!")
            elif quads != None:
                player.handIndex = 7
                player.finalHand = quads
                print("Quads!")
            elif fullHouse != None:
                player.handIndex = 6
                player.finalHand = fullHouse
                print("Full House!")
            elif flush != None:
                player.handIndex = 5
                player.finalHand = flush
                print("Flush!")
            elif straight != None:
                player.handIndex = 4
                player.finalHand = straight
                print("Straight!")
            elif trips != None:
                player.handIndex = 3
                player.finalHand = trips
                print("Trips")
            elif twoPair != None:
                player.handIndex = 2
                player.finalHand = twoPair
                print("Two pair!")
            elif pair != None:
                player.handIndex = 1
                player.finalHand = pair
                print("Pair!")
            elif highCard != None:
                player.handIndex = 0
                player.finalHand = highCard
                print("High Card!")

    def compareEqualPlayers(self, players):
        bestHand = players[0].finalHand
        bestPlayer = players[0]
        for player in players:
            for index, card in enumerate(player.finalHand):
                if (card > bestHand[index]):
                    bestHand = player.finalHand
                    bestPlayer = player
                    break
                elif (card < bestHand[index]):
                    break
        return bestPlayer

    def comparePlayerIndices(self):
        maxHandIndex = 0
        maxIndexPlayers = []
        for player in self.players:
            if player.handIndex > maxHandIndex:
                maxHandIndex = player.handIndex
                maxIndexPlayers = [player]
            elif player.handIndex == maxHandIndex:
                maxIndexPlayers.append(player)
        if len(maxIndexPlayers) == 1:
            return maxIndexPlayers[0]
        else:
            # length is greater than 2
            return self.compareEqualPlayers(maxIndexPlayers)

    def isRoundEnded(self):       
        if len(self.players) == 1:
            print("Final board " + str(self.deck.flop) + ' ' + 
        str(self.deck.turn) + ' ' + str(self.deck.river))
            self.winningPlayerIndex = self.currPlayerIndex
            self.players[self.currPlayerIndex].numChips += self.totalPotSize
            return True
        elif(self.isRiver() and self.playersLeft == 0):
            print("Final board " + str(self.deck.flop) + ' ' + 
        str(self.deck.turn) + ' ' + str(self.deck.river))
            self.setIndices()
            player = self.comparePlayerIndices()
            self.winningPlayerIndex = self.players.index(player)
            self.players[self.winningPlayerIndex].numChips += self.totalPotSize
            print("This player wins!!!! " + str(self.players.index(player) + 1))
            return True
        return False

    def check(self):
        if(self.betSize==0):
            self.incrPlayerCounter()
            self.playersLeft -= 1
            if (self.playersLeft == 0 and self.currTurn <= 2):
                print("Here comes the new ca!!")
                self.nextTurn()
        else:
            print("Can't check need to call raise or fold")

    def bet(self, amt):
        # ask for amount
        amount = amt
        self.betSize = amount
        self.totalPotSize+=amount
        self.playersLeft = len(self.players) - 1
        self.players[self.currPlayerIndex].numChips -= amount
        self.players[self.currPlayerIndex].roundBetSize = amount
        self.incrPlayerCounter()

    def callBet(self):
        if (self.players[self.currPlayerIndex].numChips < (self.betSize-self.players[self.currPlayerIndex].roundBetSize)):
            print("Not enough chips to call!")
            self.fold()
        else:
            self.totalPotSize+=(self.betSize-self.players[self.currPlayerIndex].roundBetSize)
            self.playersLeft -= 1
            self.players[self.currPlayerIndex].numChips -= (self.betSize-self.players[self.currPlayerIndex].roundBetSize)
            self.players[self.currPlayerIndex].roundBetSize = self.betSize
            self.incrPlayerCounter()
            if (self.playersLeft == 0 and self.currTurn <= 2):
                print("Here comes the new cards!!!!")
                self.nextTurn()


    def raiseBet(self, amt):
        amount = amt
        stackSize = self.players[self.currPlayerIndex].numChips
        if (self.betSize == 0 and amount <= stackSize):
            self.bet(amount)
        elif (self.betSize == 0 and amount > stackSize):
            self.fold()
        elif (amount > stackSize):
            if (self.betSize <= stackSize):
                self.callBet()
            else:
                self.fold()
        elif (amount < self.betSize*2):
            if (self.betSize <= stackSize):
                self.callBet()
            else:
                self.fold()
        else:
            self.betSize = amount
            self.totalPotSize += amount
            self.playersLeft = len(self.players) - 1
            self.players[self.currPlayerIndex].numChips -= (amount-self.players[self.currPlayerIndex].roundBetSize)
            self.players[self.currPlayerIndex].roundBetSize=amount
            self.incrPlayerCounter()

    def fold(self):
        self.players.pop(self.currPlayerIndex)
        if (self.currPlayerIndex == len(self.players)):
            self.currPlayerIndex = 0
        self.playersLeft -= 1
        if (self.playersLeft == 0):
            self.nextTurn()

    def shove(self):
        if (self.betSize != 0):
            amount = self.players[self.currPlayerIndex].numChips
            self.betSize = amount
            self.totalPotSize += amount
            self.playersLeft = len(self.players) - 1
            self.players[self.currPlayerIndex].numChips = 0
            self.players[self.currPlayerIndex].roundBetSize = amount
            self.incrPlayerCounter()
        else:
            print("Raising zero bet!")
            return

    def playerMove(self):
        print("\n")
        print("POT IS AT " + str(self.totalPotSize))
        print("CURRENTLY ON PLAYER " + str(self.currPlayerIndex + 1))
        print("PLAYER STACK IS " + 
                str(self.players[self.currPlayerIndex].numChips))
        print("PLAYER HAND IS \n" + 
                str(self.players[self.currPlayerIndex].hand[0]))
        print(str(self.players[self.currPlayerIndex].hand[1]))
        if (self.betSize == 0):
            print("NO BETS ON THE TABLE")
        else:
            print("CURRENT BET SIZE IS " + str(self.betSize))
        move = input("Enter check, bet, raise, fold, call, or shove: ")
        if (move == "check"):
            self.check()
        elif (move == "bet"):
            self.bet()
        elif (move == "raise"):
            self.raiseBet()
        elif (move == "fold"):
            self.fold()
        elif (move == "shove"):
            self.shove()
        elif (move == "call"):
            self.callBet()
    
    
class Player(object): 
    def __init__(self, hand, numChips):
        self.hand = hand
        self.numChips = numChips
        # 0 - 8 0 is high card 8 is straight flush
        self.handIndex = 0
        self.finalHand = []
        self.handStrength = 0
        self.roundBetSize = 0
    

class Card(object):
    def __init__(self,suit,rank):  
        self.suit=suit
        self.rank=rank

    def __repr__(self):
        if(self.rank<11):
            final=self.rank
        elif(self.rank==11):
            final="Jack"
        elif(self.rank==12):
            final="Queen"
        elif(self.rank==13):
            final="King"
        elif(self.rank==14):
            final="Ace"
        else:
            final="Error"
        return f"{final} of {self.suit}"


class Deck(object):
    def __init__(self):
        self.deck=[]
        for s in ['Spades','Hearts','Diamonds','Clubs']:
            for i in range(2,15):
                self.deck.append(Card(s,i))
        self.flop=[]
        self.turn=[]
        self.river=[]

    
    def __repr__(self):
        deck_string=""
        for card in self.deck:
            deck_string=deck_string+str(card)+"\n"
        return deck_string

    def shuffle(self):
        random.shuffle(self.deck)

    def setFlopTurnRiver(self):
        self.flop = self.deck[0:3]
        self.turn = self.deck[3]
        self.river = self.deck[4]
        self.deck.pop(0)
        self.deck.pop(0)
        self.deck.pop(0)
        self.deck.pop(0)
        self.deck.pop(0)
    
    def dealHand(self):
        card1 = self.deck.pop(0)
        card2 = self.deck.pop(0)
        return (card1, card2)

    def dealTestHand(self):
        index1=randint(0,len(self.deck)-1)
        index2=randint(0,len(self.deck)-1)
        while(index1==index2):
            index2=randint(0,len(self.deck)-1)
        card1=self.deck[index1]
        card2=self.deck[index2]
        return (card1, card2)
        

def newGame():
    deck1=Deck()
    deck1.shuffle()
    deck1.setFlopTurnRiver()
    
    numPlayers = int(input(("STARTING NEW GAME! HOW MANY PLAYERS? ")))

    players = []
    for i in range(numPlayers):
        newPlayerBuyin = int(input("Player " + str(i + 1) 
                    + " Buy in: "))
        newPlayerHand = deck1.dealHand()
        playerN = Player(newPlayerHand, newPlayerBuyin)
        players.append(playerN)

    smallBlind = int(input("Enter small blind: "))
    bigBlind = int(input("Enter big blind: "))

    blinds = (smallBlind, bigBlind)
    button = 0
    firstGame = Game(blinds, button, players, deck1)

    # straightDraw = [Card('Spades', 2), Card('Spades', 3), Card('Spades', 4), 
    #     Card('Hearts', 5), Card('Spades', 6), Card('Spades', 7), Card('Spades', 11)]
    # testStraight = firstGame.isStraight(straightDraw)
    # print(testStraight)
    while (not (firstGame.isRoundEnded())):
        firstGame.playerMove()
    print("End of round, create new game now...")
