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
from cmu_term_project import *


def appStarted(app):
    app.onHomePage = True
    app.onInstructions = False
    app.onGame = False
    app.onBot = False
    app.onMonteCarlo = False
    app.needsPlayers = True
    app.needsDeck = True
    app.onWinnerScreen = False
    app.printHandStrength = False
    app.numPlayers=0
    app.currentAction=""
    app.AIgoes = False
    app.currentPot=0
    app.players=[]
    app.deck=Deck()
    app.currGame=0
    app.blinds=(0, 0)
    app.button=0
    #I had nothing to do with the creation of this image
    #https://www.onlinecasinos.co.uk/blog/best-poker-hands-rankings.htm that is the link
    app.image = app.loadImage('./imagesfromWEB/card-images.png')
    app.image1 = app.scaleImage(app.image, 4/10)

def playMoves(app, moveTuple):
    print("\n")
    print("POT IS AT " + str(app.currGame.totalPotSize))
    print("CURRENTLY ON PLAYER " + str(app.currGame.currPlayerIndex + 1))
    print("PLAYER STACK IS " + 
            str(app.currGame.players[app.currGame.currPlayerIndex].numChips))
    print("PLAYER HAND IS \n" + 
            str(app.currGame.players[app.currGame.currPlayerIndex].hand[0]))
    print(str(app.currGame.players[app.currGame.currPlayerIndex].hand[1]))
    if (app.currGame.betSize == 0):
        print("NO BETS ON THE TABLE")
    else:
        print("CURRENT BET SIZE IS " + str(app.currGame.betSize))
    move = moveTuple
    if (move[0] == "check"):
        app.currGame.check()
    elif (move[0] == "bet"):
        app.currGame.bet(move[1])
    elif (move[0] == "raise"):
        app.currGame.raiseBet(move[1])
    elif (move[0] == "fold"):
        app.currGame.fold()
    elif (move[0] == "shove"):
        app.currGame.shove()
    elif (move[0] == "call"):
        app.currGame.callBet()

def mousePressed(app, event):
    if(app.onHomePage):
        if(event.x>=app.width//2-app.width//10 
        and event.x<=app.width//2+app.width//10
        and event.y<=app.height//2 - 2*app.height//10 
        and event.y>=app.height//2-3*app.height//10):
            app.onHomePage=False
            app.onGame=True
        elif(event.x>=app.width//2-app.width//10 
        and event.x<=app.width//2+app.width//10
        and event.y<=app.height//2 
        and event.y>=app.height//2-1*app.height//10):
            app.onHomePage=False
            app.onInstructions=True
        elif(event.x>=app.width//2-app.width//10 
        and event.x<=app.width//2+app.width//10
        and event.y<=app.height//2 + 2*app.height//10 
        and event.y>=app.height//2+1*app.height//10):
            app.onHomePage=False
            app.onBot=True
        elif(event.x>=app.width//2-app.width//10 
        and event.x<=app.width//2+app.width//10
        and event.y<=app.height//2 + 4*app.height//10 
        and event.y>=app.height//2+3*app.height//10):
            app.onHomePage=False
            app.onMonteCarlo=True
    
    elif(app.onBot==True or app.onMonteCarlo==True or app.onInstructions==True):
        if(event.x>=(app.width-app.width//30)
        and event.x<=app.width
        and event.y<=app.height//30 
        and event.y>=0):
            app.onGame=False
            app.onBot=False
            app.onMonteCarlo=False
            app.onInstructions=False
            app.onHomePage=True
    elif(app.onGame==True):
        if(app.needsDeck):
            app.deck = Deck()
            app.deck.shuffle()
            app.deck.setFlopTurnRiver()
            app.needsDeck=False
        if(app.needsPlayers):
            app.numPlayers = int(app.getUserInput('How many players 2-6?'))
            app.players = []
            for i in range(app.numPlayers):
                newPlayerBuyin = int(app.getUserInput("Player " + str(i + 1) 
                            + " Buy in: "))
                newPlayerHand = app.deck.dealHand()
                playerN = Player(newPlayerHand, newPlayerBuyin)
                app.players.append(playerN)
            smallBlind = int(app.getUserInput("Enter small blind: "))
            bigBlind = int(app.getUserInput("Enter big blind: "))
            app.blinds = (smallBlind, bigBlind)
            app.button = 0
            app.needsPlayers=False

        elif(event.x>=(app.width-app.width//30)
        and event.x<=app.width
        and event.y<=app.height//30 
        and event.y>=0):
            app.onGame=False
            app.onBot=False
            app.onMonteCarlo=False
            app.onInstructions=False
            app.onHomePage=True
        else:
            # start new game
            if (app.currGame == 0):
                app.currGame = Game(app.blinds, app.button, app.players, app.deck)
            else:
                #game in progress
                testBool = app.currGame.isRoundEnded()
                if (not testBool):
                    if(event.x>=app.width-app.width//10 and event.y>=app.height-app.height//10 
                    and event.x<= app.width and event.y<= app.height):
                        app.currentAction="fold"
                        move = ("fold", 0)
                        playMoves(app, move)
                    elif(event.x>=app.width-app.width//10 and event.y>=app.height-3*app.height//10 
                    and event.x<= app.width and event.y<= app.height-2*app.height//10):
                        app.currentAction="call"
                        move = ("call", 0)
                        playMoves(app, move)
                    elif(event.x>=app.width-app.width//10 and event.y>=app.height-2*app.height//10 
                    and event.x<= app.width and event.y<= app.height-1*app.height//10):
                        app.currentAction="check"
                        move = ("check", 0)
                        playMoves(app, move)
                    elif(event.x>=app.width-2*app.width//10 and event.y>=app.height-app.height//10 
                    and event.x<= app.width-app.width//10 and event.y<= app.height):
                        app.currentAction="shove"
                        app.currGame.betSize = app.currGame.players[
                                app.currGame.currPlayerIndex].numChips
                        move = ("shove", 0)
                        playMoves(app, move)
                    elif(event.x>=app.width-2*app.width//10 and event.y>=app.height-3*app.height//10 
                    and event.x<= app.width-app.width//10 and event.y<= app.height-2*app.height//10 ):
                        app.currentAction="raise"
                        amount = int(app.getUserInput("Enter raise size: "))
                        if (app.currGame.players[app.currGame.currPlayerIndex].numChips < amount
                           and amount >= app.currGame.betSize*2):
                            print("Raise must be double, try again")
                        if (app.currGame.betSize != 0) :
                            move = ("raise", amount)
                            playMoves(app, move)
                        else:
                            print("Can't raise")
                    elif(event.x>=app.width-2*app.width//10 and event.y>=app.height-2*app.height//10 
                    and event.x<= app.width-app.width//10 and event.y<= app.height-app.height//10 ):
                        app.currentAction="bet"
                        amount = int(app.getUserInput("Enter bet size: "))
                        if (app.currGame.players[app.currGame.currPlayerIndex].numChips < amount):
                            print("Bet was too big, try again")
                        if (app.currGame.betSize == 0):
                            move = ("bet", amount)
                            playMoves(app, move)
                        else:
                            print("Can't bet")

                    elif(event.x>=app.width-3*app.width//10 and event.y>=app.height-app.height//10 
                    and event.x<= app.width-2*app.width//10 and event.y<= app.height):
                        app.AIgoes=True
                        move = app.currGame.botDecision()
                        playMoves(app, move)
                    
                    elif(event.x>=app.width-3*app.width//10 and event.y>=app.height-2*app.height//10 
                    and event.x<= app.width-2*app.width//10 and event.y<= app.height-app.height//10):
                        app.printHandStrength = not app.printHandStrength
                    
                    testBool = app.currGame.isRoundEnded()
                    if (testBool):
                        app.onWinnerScreen = True
                        if(event.x>=0 and event.y>=0 and event.x<=app.width//5 and event.y<app.height):
                            app.onWinnerScreen = False
                            restartGame(app)     
                else:
                    print("Game ended!")
                    if(event.x>=0 and event.y>=0 and event.x<=app.width//5 and event.y<app.height):
                            app.onWinnerScreen = False
                            restartGame(app)

def restartGame(app):
    app.needsDeck = True
    app.currGame = 0
    app.needsPlayers = True


def drawWinner(app, canvas):
    canvas.create_rectangle(app.width//2-app.width//20, 
        app.height//2+2*app.height//20, app.width//2+app.width//20, 
        app.height//2+5*app.height//20, fill="white")
    canvas.create_text(app.width//2, (app.height//2)+3*app.height//20+15,
            text=f'Player {app.currGame.winningPlayerIndex + 1} won with \
                {app.currGame.players[app.currGame.winningPlayerIndex].hand[0]} \
                {app.currGame.players[app.currGame.winningPlayerIndex].hand[1]}')
    canvas.create_text(app.width//2, (app.height//2)+3*app.height//20-15,
            text=f'bottom left to restart')
    canvas.create_rectangle(0,app.height-3*app.height//20,app.width//7,app.height,fill="black")

def drawPlayers(app,canvas):
    for i in range(app.numPlayers):
        angle = math.pi/2 - 2*math.pi*i/app.numPlayers
        currX = app.width//2 + app.width//3 * math.cos(angle)
        currY = app.height//2 - app.height//3 * math.sin(angle)
        canvas.create_rectangle(currX-app.width//20, currY-app.height//20, 
        currX+app.width//20, currY+app.height//20, fill="white")
        if (app.currGame != 0):
            if (i == app.currGame.currPlayerIndex):
                canvas.create_text(currX, currY-25, 
                text=f'{app.currGame.players[i].hand[0]}')
                canvas.create_text(currX, currY-10, 
                text=f'{app.currGame.players[i].hand[1]}')
                canvas.create_text(currX, currY+10, 
                text=f'stack size is{app.currGame.players[i].numChips}')
                if(app.printHandStrength):
                   # if (app.currGame.players[i].handStrength == 0):
                        if(app.currGame.currTurn==0):
                            x=app.currGame.strengthPlayerPre(app.currGame.players[i])
                            canvas.create_text(currX, currY+25, 
                            text=f'Hand Strength is {x}')
                        else:
                            x=app.currGame.strengthPlayerFlop(app.currGame.players[i], app.currGame.currTurn)
                            canvas.create_text(currX, currY+25, 
                        text=f'Hand Strength is {x}')
                

def drawCenter(app,canvas):
    if (app.currGame != 0):
        canvas.create_rectangle(app.width//2-app.width//20, 
        app.height//2-app.height//20, app.width//2+app.width//20, 
        app.height//2+app.height//20, fill="white")
        if (app.currGame.isFlop()):
            canvas.create_text(app.width//2, (app.height//2)-40,
            text=f'{app.currGame.deck.flop[0]}')
            canvas.create_text(app.width//2, app.height//2-25,
            text=f'{app.currGame.deck.flop[1]}')
            canvas.create_text(app.width//2, app.height//2-10,
            text=f'{app.currGame.deck.flop[2]}')
        if (app.currGame.isTurn()):
            canvas.create_text(app.width//2, (app.height//2)-40,
            text=f'{app.currGame.deck.flop[0]}')
            canvas.create_text(app.width//2, app.height//2-25,
            text=f'{app.currGame.deck.flop[1]}')
            canvas.create_text(app.width//2, app.height//2-10,
            text=f'{app.currGame.deck.flop[2]}')
            canvas.create_text(app.width//2, app.height//2+5,
            text=f'{app.currGame.deck.turn}')
        if (app.currGame.isRiver()):
            canvas.create_text(app.width//2, (app.height//2)-40,
            text=f'{app.currGame.deck.flop[0]}')
            canvas.create_text(app.width//2, app.height//2-25,
            text=f'{app.currGame.deck.flop[1]}')
            canvas.create_text(app.width//2, app.height//2-10,
            text=f'{app.currGame.deck.flop[2]}')
            canvas.create_text(app.width//2, app.height//2+5,
            text=f'{app.currGame.deck.turn}')
            canvas.create_text(app.width//2, app.height//2+20,
            text=f'{app.currGame.deck.river}')
        canvas.create_text(app.width//2, app.height//2+40,
        text=f'Size of Pot is {app.currGame.totalPotSize}')
        

def drawHomePage(app,canvas):
    #background is grey
    canvas.create_rectangle(0,0,app.width,app.height,fill="lightgrey")
    
    #box to play the game
    canvas.create_rectangle(app.width//2-app.width//10,
    app.height//2-3*app.height//10,
    app.width//2+app.width//10,app.height//2 - 2*app.height//10,
    fill="lightgreen")
    #creates the text for the game
    canvas.create_text(app.width/2, int(app.height//2-(2.58)*app.height//10),
    text='Press here if you would like to ')
    canvas.create_text(app.width/2, int(app.height//2-(2.42)*app.height//10),
    text='play the game')
    
    #first box for general instruction
    canvas.create_rectangle(app.width//2-app.width//10,
    app.height//2-app.height//10,
    app.width//2+app.width//10,app.height//2,fill="lightgreen")
    #creates the text for instruction
    canvas.create_text(app.width/2, int(app.height//2-(0.58)*app.height//10),
    text='Press here if you would like to ')
    canvas.create_text(app.width/2, int(app.height//2-(0.42)*app.height//10),
    text='learn how to play Texas Hold Em')
    
    #second box for Bot/strategy
    canvas.create_rectangle(app.width//2-app.width//10,
    app.height//2+app.height//10,
    app.width//2+app.width//10,app.height//2 + 2*app.height//10,
    fill="lightgreen")
    #creates the text for Bot
    canvas.create_text(app.width/2, int(app.height//2+1.42*app.height//10),
    text='Press here if you would like to ')
    canvas.create_text(app.width/2, int(app.height//2+1.58*app.height//10),
    text='learn about the Bot and general strategy')

    #third box for Monte Carlo instruction and hand rankings
    canvas.create_rectangle(app.width//2-app.width//10,
    app.height//2+3*app.height//10,
    app.width//2+app.width//10,app.height//2+4*app.height//10,
    fill="lightgreen")
    #creates the text for Monte Carlo
    canvas.create_text(app.width/2, int(app.height//2+3.42*app.height//10),
    text='Press here if you would like to ')
    canvas.create_text(app.width/2, int(app.height//2+3.58*app.height//10),
    text='learn about the simulations/hands')

def drawGame(app,canvas):
    #background is grey
    canvas.create_rectangle(0,0,app.width,app.height,fill="lightgrey")

    #create the table
    canvas.create_oval(app.width//2-3*app.width//8, 
    app.height//2-3*app.height//8, 
    app.width//2+3*app.width//8, app.height//2+3*app.height//8, fill='green')
    
    #drawing the X to go back to Home screen
    canvas.create_rectangle(app.width-app.width//30,0,app.width,app.width//30,
    fill="lightgrey")
    canvas.create_line(app.width-app.width//35,5,app.width-5,app.width//35,
    fill="black")
    canvas.create_line(app.width-app.width//35,app.width//35,app.width-5,5,
    fill="black")
    #will need to do the rest later

    if(app.needsPlayers==False):
        canvas.create_rectangle(app.width-app.width//10,app.height-app.height//10,app.width,app.height,
        fill="white")
        canvas.create_text(app.width-app.width//20, app.height-app.height//20,
        text='FOLD',font="Arial 18")
        canvas.create_rectangle(app.width-app.width//10,app.height-3*app.height//10,app.width,app.height-2*app.height//10,
        fill="white")
        canvas.create_text(app.width-app.width//20, app.height-5*app.height//20,
        text='CALL',font="Arial 18")
        canvas.create_rectangle(app.width-app.width//10,app.height-4*app.height//20,app.width,app.height-2*app.height//20,
        fill="white")
        canvas.create_text(app.width-app.width//20, app.height-3*app.height//20,
        text='CHECK',font="Arial 18")
        canvas.create_rectangle(app.width-2*app.width//10,app.height-app.height//10,app.width-1*app.width//10,app.height,
        fill="white")
        canvas.create_text(app.width-3*app.width//20, app.height-app.height//20,
        text='SHOVE',font="Arial 18")
        canvas.create_rectangle(app.width-2*app.width//10,app.height-2*app.height//10,app.width-app.width//10,app.height-1*app.height//10,
        fill="white")
        canvas.create_text(app.width-3*app.width//20, app.height-3*app.height//20,
        text='BET',font="Arial 18")
        canvas.create_rectangle(app.width-2*app.width//10,app.height-3*app.height//10,app.width-app.width//10,app.height-2*app.height//10,
        fill="white")
        canvas.create_text(app.width-3*app.width//20, app.height-5*app.height//20,
        text='Raise',font="Arial 18")
        canvas.create_rectangle(app.width-3*app.width//10,app.height-app.height//10,app.width-2*app.width//10,app.height,
        fill="white")
        canvas.create_text(app.width-5*app.width//20, app.height-app.height//20,
        text='AI MOVE',font="Arial 18")
        canvas.create_rectangle(app.width-3*app.width//10,app.height-2*app.height//10,app.width-2*app.width//10,app.height-app.height//10,
        fill="white")
        if(app.printHandStrength):
            canvas.create_text(app.width-5*app.width//20, app.height-3*app.height//20,
            text='HAND STRENGTH OFF',font="Arial 15")
        else:
            canvas.create_text(app.width-5*app.width//20, app.height-3*app.height//20,
            text='HAND STRENGTH ON',font="Arial 15")

def drawInstructions(app,canvas):
    #background is white
    canvas.create_rectangle(0,0,app.width,app.height,fill="white")

#drawing the X to go back to Home screen
    canvas.create_rectangle(app.width-app.width//30,0,app.width,app.width//30,
    fill="lightgrey")
    canvas.create_line(app.width-app.width//35,5,app.width-5,app.width//35,
    fill="black")
    canvas.create_line(app.width-app.width//35,app.width//35,app.width-5,5,
    fill="black")

#create the center box that is light grey
    canvas.create_rectangle(app.width//4,app.height//2-7*app.height//16,
    3*app.width//4,app.height//2+7*app.height//16,fill="lightgrey")

#creates the title
    canvas.create_text(app.width/2, int(app.height//2-6.6*app.height//16),
    text='HERE ARE THE RULES OF POKER',font="Arial 30")

#main rules
    canvas.create_text(app.width/2, int(app.height//2-4.6*app.height//16),
    text='Poker is played with 2-9 players at one table',font="Arial 18")

    canvas.create_text(app.width/2, int(app.height//2-4.2*app.height//16),
    text='1. Every player has 2 cards in their hand, and 5 community cards'
    ,font="Arial 18")
    canvas.create_text(app.width/2, int(app.height//2-3.8*app.height//16),
    text='2. The point of the game is to make the best 5 card hand'
    ,font="Arial 18")

    canvas.create_text(app.width/2, int(app.height//2-3.2*app.height//16),
    text='3. There are 4 opportunities for every player to put in money '
    ,font="Arial 18")
    canvas.create_text(app.width/2, int(app.height//2-2.8*app.height//16),
    text='4. Before the flop, after the flop, after the turn, and after the river'
    ,font="Arial 18")
    canvas.create_text(app.width/2, int(app.height//2-2.2*app.height//16),
    text='5. The flop is the first three community cards, the turn and river are'
    ,font="Arial 18")
    canvas.create_text(app.width/2, int(app.height//2-1.8*app.height//16),
    text='the fourth and fifth respectively'
    ,font="Arial 18")

    canvas.create_text(app.width/2, int(app.height//2-1.2*app.height//16),
    text='6. There are 5 possible moves in poker: bet, check, call, raise, and fold'
    ,font="Arial 18")
    
    canvas.create_text(app.width/2, int(app.height//2-0.8*app.height//16),
    text='To bet means to put money in the pot that other players need to match in order to continue'
    ,font="Arial 18")
    
    canvas.create_text(app.width/2, int(app.height//2-0.4*app.height//16),
    text='To call means to match another players bet'
    ,font="Arial 18")
    
    canvas.create_text(app.width/2, int(app.height//2-0*app.height//16),
    text='To fold means to throw your cards away because you do not want to match a bet'
    ,font="Arial 18")
    
    canvas.create_text(app.width/2, int(app.height//2+0.4*app.height//16),
    text='To raise means to see another players bet and put in at least double that amount'
    ,font="Arial 18")

    canvas.create_text(app.width/2, int(app.height//2+0.8*app.height//16),
    text='Finally checking means to not put any money in, but still continue'
    ,font="Arial 18")

    canvas.create_text(app.width/2, int(app.height//2+1.6*app.height//16),
    text='7. Before the flop there are two players that are forced to put in a small bet'
    ,font="Arial 18")
    
    canvas.create_text(app.width/2, int(app.height//2+2.0*app.height//16),
    text='This bet is known as a blind'
    ,font="Arial 18")

    canvas.create_text(app.width/2, int(app.height//2+2.6*app.height//16),
    text='8. The player who is forced to put in the big blind acts last before the flop'
    ,font="Arial 18")

    canvas.create_text(app.width/2, int(app.height//2+3.0*app.height//16),
    text='9. The player who has the dealer button acts last after the flop'
    ,font="Arial 18")

def drawBot(app,canvas):
    #background is white
    canvas.create_rectangle(0,0,app.width,app.height,fill="white")

#drawing the X to go back to Home screen
    canvas.create_rectangle(app.width-app.width//30,0,app.width,app.width//30,
    fill="lightgrey")
    canvas.create_line(app.width-app.width//35,5,app.width-5,app.width//35,
    fill="black")
    canvas.create_line(app.width-app.width//35,app.width//35,app.width-5,5,
    fill="black")

#create the center box that is light grey
    canvas.create_rectangle(app.width//4,app.height//2-7*app.height//16,
    3*app.width//4,app.height//2+7*app.height//16,fill="lightgrey")

#creates the title
    canvas.create_text(app.width/2, int(app.height//2-6.6*app.height//16),
    text='Here is the general strategy for poker',font="Arial 30")

#bot/strategy 
    canvas.create_text(app.width/2, int(app.height//2-4.6*app.height//16),
    text='1. It is helpful to act last in poker. This means you should play more hands',font="Arial 18")

    canvas.create_text(app.width/2, int(app.height//2-4.2*app.height//16),
    text='preflop if you are going to act last'
    ,font="Arial 18")
    canvas.create_text(app.width/2, int(app.height//2-3.6*app.height//16),
    text='2. Oftentimes, if players have the same hands, then ties are settled by higher cards.'
    ,font="Arial 18")
    canvas.create_text(app.width/2, int(app.height//2-3.2*app.height//16),
    text='Thus, players should play higher cards more often'
    ,font="Arial 18")
    canvas.create_text(app.width/2, int(app.height//2-2.6*app.height//16),
    text='3. Players should also play cards that are the same suit because they '
    ,font="Arial 18")
    canvas.create_text(app.width/2, int(app.height//2-2.2*app.height//16),
    text='are more likely to get a flush'
    ,font="Arial 18")
    canvas.create_text(app.width/2, int(app.height//2-1.8*app.height//16),
    text='Additionally, they should also play hands that are close together to get a straight'
    ,font="Arial 18")
    canvas.create_text(app.width/2, int(app.height//2-1.4*app.height//16),
    text='Playing hands that are both suited and close together is especially beneficial'
    ,font="Arial 18")
    
    canvas.create_text(app.width/2, int(app.height//2-0.8*app.height//16),
    text='4. To be profitable in many gambeling games the player needs to have a positive'
    ,font="Arial 18")
    
    canvas.create_text(app.width/2, int(app.height//2-0.4*app.height//16),
    text='reward to risk ratio'
    ,font="Arial 18")
    
    canvas.create_text(app.width/2, int(app.height//2-0*app.height//16),
    text='5. This means that if you need to risk 10 dollars to win a pot of 50 dollars'
    ,font="Arial 18")
    
    canvas.create_text(app.width/2, int(app.height//2+0.4*app.height//16),
    text='you only need to win that pot 20 percent of the time'
    ,font="Arial 18")

    canvas.create_text(app.width/2, int(app.height//2+0.8*app.height//16),
    text='6. Poker is all about keeping a balence of betting, calling, and raising. '
    ,font="Arial 18")

    canvas.create_text(app.width/2, int(app.height//2+1.2*app.height//16),
    text='If you do any one of those options too often, you will be exploitable'
    ,font="Arial 18")
    
    canvas.create_text(app.width/2, int(app.height//2+1.8*app.height//16),
    text='7. As you start learning to play poker you should see if the AI makes '
    ,font="Arial 18")

    canvas.create_text(app.width/2, int(app.height//2+2.2*app.height//16),
    text='the same move as you'
    ,font="Arial 18")

    canvas.create_text(app.width/2, int(app.height//2+2.8*app.height//16),
    text='8. Overtime, you will get better and better'
    ,font="Arial 18")



def drawMonteCarlo(app,canvas):
    #background is white
    canvas.create_rectangle(0,0,app.width,app.height,fill="white")

#drawing the X to go back to Home screen
    canvas.create_rectangle(app.width-app.width//30,0,app.width,app.width//30,
    fill="lightgrey")
    canvas.create_line(app.width-app.width//35,5,app.width-5,app.width//35,
    fill="black")
    canvas.create_line(app.width-app.width//35,app.width//35,app.width-5,5,
    fill="black")

#create the center box that is light grey
    canvas.create_rectangle(app.width//4,app.height//2-7*app.height//16,
    3*app.width//4,app.height//2+7*app.height//16,fill="lightgrey")

#creates the title
    canvas.create_text(app.width/2, int(app.height//2-6.6*app.height//16),
    text='Here are the hand rankings of poker',font="Arial 30")

#Here are the hands
    canvas.create_image(app.width//2, app.height//2, image=ImageTk.PhotoImage(app.image1))

def redrawAll(app, canvas):
    if(app.onHomePage):
        drawHomePage(app,canvas)
    elif(app.onGame):
        drawGame(app,canvas)
        if(app.onWinnerScreen):
            drawWinner(app,canvas)
        if(app.needsPlayers==False):
            drawPlayers(app,canvas)
            drawCenter(app,canvas)
    elif(app.onInstructions):
        drawInstructions(app,canvas)
    elif(app.onBot):
        drawBot(app,canvas)
    elif(app.onMonteCarlo):
        drawMonteCarlo(app,canvas)
    
runApp(width=1600, height=900)

