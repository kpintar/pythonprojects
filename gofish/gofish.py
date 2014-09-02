'''
Created on Sep 2, 2014

@author: Kevin
'''
from test.pickletester import MyList

# from Adam Barr's wonderful book "Find the Bug"

''' This function draws a card from a deck and puts it into a hand. It is
meant to be part of the game Go Fish, so if the resulting hand has all four 
suits for a given card rank, those four cards are removed from the hand. 

Cards are identified by their rank and suit: the rank is one of the elements
in the list ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
and the suit is on of the elements of the list ["spades", "hearts", "diamonds", "clubs"].

A deck is a list that initially contains 52 elements. Each element of the list
is a tuple with two elements: the rank and the suit. So a single entry
in the deck might be the tuple ("K", "spades"), which is the king of spades.

A hand is a dictionary. In each element of the dictionary, the key is
the rank and the value is a list that contains the names of the suits that the hand
holds for that rank. E.g., if a hand as the 3 of spades and the 3 of hearts, and
no other 3s, then the key "3" has the value ["spades", "hearts"]. A key should not
have an empty list associated with it - if no cards of a given rank are held,
no value exists for that key.'''

import random
import sys

rankList = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
suitList = ["spades", "hearts", "diamonds", "clubs"]
GOFISH = "Go Fish"
    
def log_stdout(msg):
    '''Print msg to the screen.'''
    print(msg)

def makeDeck():
    ''' Creates a deck.
        A deck is a list that initially contains 52 elements. Each element of the list
        is a tuple with two elements: the rank and the suit. So a single entry
        in the deck might be the tuple ("K", "spades"), which is the king of spades.    
    '''
    
    deck = []
    for r in rankList:
        for s in suitList:
            deck.append([r, s])
    return deck

def getCard(deck):

    ''' Randomly remove a single card from the deck and return it. Assumes that the deck 
      is not empty.

      deck: A deck as described above

      Returns: a single card, which is a tuple with two elements, the rank and the suit

    '''
    index = random.randint(0,len(deck)-1)
    newCard = deck[index]
    del deck[index]
    return newCard

def askForCard(requestor, requestorHand, giver, giverHand  ):
    '''Asks other player for a needed rank '''
    if len(requestorHand) == 0:
        print("%s has no cards. %s" %(requestor,GOFISH))
        return

    #find the rank with maximum count
    maxKey = GOFISH
    maxCount = 0
    for key in requestorHand:
        count=len(requestorHand.get(key))
        if count > maxCount:
            maxKey = key
            maxCount = count
    
    if len(giverHand) == 0:
        print("%s has requested %s but %s has no cards. %s" %(requestor,maxKey,giver,GOFISH))
        return GOFISH
    
    received = giverHand.get(maxKey,GOFISH)
    print("%s asked %s for %s and the answer was %s" %(requestor,giver, maxKey,received))
    
    if received == GOFISH:
        return GOFISH
    for value in received:
        requestorHand[maxKey].append(value)
    del giverHand[maxKey]
    return received
    

def drawCard(name, deck, hand):

    ''' Draw a new card from the deck and add it to the hand. If the hand now holds the rank
      in all four suits, then remove them from the hand.

      name: A string with the name of the playerHand, used only for display purposes.
      deck: A deck as described above
      hand: A hand dictionary as described above

      Returns: None.
    '''

    if len(deck) > 0:  # protect against empty deck
        newCard = getCard(deck)
        cardRank = newCard[0]
        cardSuit = newCard[1]
    else:
        return

    if cardRank in hand:
        # append this suit to the result
        hand[cardRank].append(cardSuit)
    else:
        # first of this suit, create a list with one element
        hand[cardRank] = [ cardSuit ]

def initHand(deck,hand,numberOfCards):
    for i in range(numberOfCards):
        newCard=getCard(deck)
        cardRank = newCard[0]
        cardSuit = newCard[1]
        testList = hand.get(cardRank,"notAsuitSuit")
        if testList == "notAsuitSuit":
            hand[cardRank]=[cardSuit]
        else:
            hand[cardRank].append(cardSuit)

def playHand(name,hand):
    played=False
    for r in rankList:
        cardSuits=hand.get(r,"notAsuitSuit")
        if len(cardSuits) == 4:
            print('%s %s %s' % (name, "lay down", r + "s"))
            del hand[r]
            played=True
    if not played:
        print("player %s has nothing to play" %(name)) 
        
class GoFish:
    ''' Play a game of Go Fish!
    '''
    def __init__(self, playerList=["DefaultPlayer1", "DefaultPlayer2"]):
        if (len(playerList)>0):
            tempPlayers = playerList
        else:
            tempPlayers = ["DefaultPlayer1", "DefaultPlayer2"]
        self.deck=makeDeck()
        self.players={}
        initCardCount=7       
        if (len(tempPlayers)>4):
            initCardCount=5
        for name in tempPlayers:
            self.players[name]={}
            initHand(self.deck, self.players[name], initCardCount)

    def autoPlay(self):
        '''Plays a game of GoFish'''
        notDone = True
        roundNumber = 0
        whoToAsk={}
        while notDone:
            roundNumber+=1
            print('Round %i !' % (roundNumber))
            for player in self.players:
                playersHand = self.players.get(player)
                print('player %s is now playing and has %i ranks' % (player,len(playersHand)))        
                
                temp = whoToAsk.get(player,GOFISH)
                if (temp == GOFISH) or (len(temp)==0):
                    whoToAsk[player]=[]
                    for temp in self.players:
                        if temp != player:
                            whoToAsk[player].append(temp)
                            
                giver = whoToAsk[player].pop(0)
                giverHand = self.players.get(giver)
                received = askForCard(player, playersHand, giver, giverHand)
                if received == GOFISH:
                    if len(self.deck) == 0:
                        print("nothing to draw. moving along.  will ask another player next round")
                        #for debugPlayer in self.players:
                        #    print("player %s has the following cards %s" %(debugPlayer,self.players.get(debugPlayer)))
                        #notDone=False
                        #continue
                    else:
                        drawCard(player, self.deck, playersHand)
                playHand(player, playersHand)
                if len(playersHand) <= 0:
                    print('player %s has won!' %(player))
                    notDone=False
                    continue
        print("game over")
        
# Main
if __name__ == '__main__':
    '''Plays a Go Fish with the players passed as arguments'''
    #ToDo - add interactive mode
    players = []
    count = 0
    for p in sys.argv[1:]:
        players.append(p)
        count += 1

    game = GoFish(playerList=players)
    game.autoPlay()
            
