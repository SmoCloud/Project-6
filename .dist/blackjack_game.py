"""
Student: Mikel Cox
Instructor: Prof. Dietrich
Class: CS 353
Project: Project 2
Date: 2/15/2024

Notes:
  I'm not sure why, but I could not get easygui to work at home in replit, so I used VS Code to copy over the code to test it. I figured you would want it in replit so you could see our keylog. The only resource I used was the EasyGui library and a google search on why the image wasn't working to learn about needing to install PIL. The diagnosis in the output window says that replit might be blocked by my ISP. I'm not sure if it's a replit issue or my ISP. It's worked before, so I'm not sure.
"""
#in pyproject.toml, add under [tool.ruff]: line_length = 120
#install PIL library (pip install pillow) for blackjack image, no need to import
import easygui
from random import randint

#the title of the game
gameTitle = "Blackjack"

#this class handles all logic related to the deck of cards
class Deck:

  #construct the suits and ranks of the cards
  def __init__(self):
    self.suitTypes = ["Spades", "Hearts", "Diamonds", "Clubs"]
    self.spades = Suit("Spades")
    self.hearts = Suit("Hearts")
    self.clubs = Suit("Clubs")
    self.diamonds = Suit("Diamonds")
    self.deck = [self.spades, self.hearts, self.clubs, self.diamonds]

  #this function draws a card of random rank and suit from the deck and removes it in the process
  def drawCard(self):
    suitToDrawFrom = randint(0, 3)
    cardNames = self.deck[suitToDrawFrom].suit.keys()
    cardList = []
    for card in cardNames:
      cardList.append(card)
    cardToDraw = cardList[randint(0, len(cardList) - 1)]
    return {cardToDraw: self.deck[suitToDrawFrom].draw(cardToDraw)}

  #this function rebuilds the deck
  def newDeck(self):
    self.deck.clear()
    self.spades.newSuit()
    self.hearts.newSuit()
    self.clubs.newSuit()
    self.diamonds.newSuit()
    self.deck = [self.spades, self.hearts, self.clubs, self.diamonds]

#this class handles all logic related to the suits of the cards
class Suit:

  #constructs a suit of cards of the type given as an argument
  def __init__(self, type):
    self.type = type
    self.suit = {
        f'Ace of {self.type}': 11,
        f'Two of {self.type}': 2,
        f'Three of {self.type}': 3,
        f'Four of {self.type}': 4,
        f'Five of {self.type}': 5,
        f'Six of {self.type}': 6,
        f'Seven of {self.type}': 7,
        f'Eight of {self.type}': 8,
        f'Nine of {self.type}': 9,
        f'Ten of {self.type}': 10,
        f'Jack of {self.type}': 10,
        f'Queen of {self.type}': 10,
        f'King of {self.type}': 10
    }

  #this function draws a card of random rank from the suit of cards and removes it in the process
  def draw(self, card):
    return self.suit.pop(card)

  #this function rebuilds the suit of cards
  def newSuit(self):
    self.suit.clear()
    self.suit = {
        f'Ace of {self.type}': 11,
        f'Two of {self.type}': 2,
        f'Three of {self.type}': 3,
        f'Four of {self.type}': 4,
        f'Five of {self.type}': 5,
        f'Six of {self.type}': 6,
        f'Seven of {self.type}': 7,
        f'Eight of {self.type}': 8,
        f'Nine of {self.type}': 9,
        f'Ten of {self.type}': 10,
        f'Jack of {self.type}': 10,
        f'Queen of {self.type}': 10,
        f'King of {self.type}': 10
    }

#this class handles all logic related to the cards held in the hands of each player
class Hand:

  #constructs an empty hand of cards
  def __init__(self):
    self.hand = {}
    self.hasAce = False
    self.total = 0

  #this function shows the cards in the hand
  def show(self, player):
    handList = self.hand.keys()
    hand = player + " Hand: "
    for card in handList:
      hand += card + "\n"
    hand += f'\nScore: {self.total}'
    easygui.msgbox(hand, gameTitle, "Got it!")

  #this function draws a card from a deck and adds it to the hand
  def hit(self, Deck):
    newCard = Deck.drawCard()
    card = "".join(newCard.keys())
    if(newCard[card] == 11):
      self.hasAce = True
    self.hand.update(newCard)
    if(newCard[card] + self.total > 21 and self.hasAce):
      self.total -= 10
      self.hasAce = False
    self.total += self.hand[card]

  #this function empties the hand
  def newHand(self):
    self.hand.clear()
    self.total = 0

#main handles the game logic
def main():
  goAgane = True #boolean variable determines if game continues, set by player response to a replay message
  
  games = 0 #total games played
  playerWins = 0 #total player wins
  compWins = 0 #total computer wins
  
  gameDeck = Deck() #build a deck
  playerHand = Hand() #create player's hand
  compHand = Hand() #create computer's hand

  #various strings used for communicating with the player
  replayMsg = ""
  blackjack = "blackjack.jpg"
  gameMsg = "Welcome to Blackjack!"

  #introduce the game, prompt the player to play
  easygui.msgbox(gameMsg, gameTitle, "Play!", image = blackjack)

  #game loop
  while goAgane:
    gameEnd = False #boolean variable determines when a game has reached an end condition
    
    games += 1 #iterate games played

    #strings used for constructing more flavorful responses
    whoWon = ""
    okayMsg = ""

    #while no end condition is reached
    while(not gameEnd):

      #computer hits if their total score is beneath 19, show their hand to player
      if(compHand.total < 19):
        compHand.hit(gameDeck)
      
      compHand.show("Computer")

      #condition for computer busting
      if(compHand.total > 21):
        gameEnd = True
        playerWins += 1
        whoWon = "Computer Bust! You win!"
        replayMsg = f'Player wins: {playerWins} - {playerWins * 100 / games}%\nComputer wins: {compWins} - {compWins * 100 / games}%\nGames Tied: {(games - playerWins - compWins) * 100 / games}%\nGames played: {games}\nPlay again?'
        okayMsg = "Great!"

      #if computer didn't bust
      if not gameEnd:

        #prompt player to hit or stand
        turnChoice = easygui.buttonbox("Would you like to hit or stand?", gameTitle, ["Hit", "Stand"])

        #if player chose to hit, then hit and show player hand
        if turnChoice == "Hit":
          playerHand.hit(gameDeck)
        
        playerHand.show("Player")

        #condition for player busting
        if(playerHand.total > 21):
          gameEnd = True
          compWins += 1
          whoWon = "You Bust! Computer wins!"
          replayMsg = f'Player wins: {playerWins} - {playerWins * 100 / games}%\nComputer wins: {compWins} - {compWins * 100 / games}%\nGames Tied: {(games - playerWins - compWins) * 100 / games}%\nGames played: {games}\nPlay again?'
          okayMsg = "Damn!"

        #if player chose to stand
        elif turnChoice == "Stand":

          #condition for player winning
          if (playerHand.total > compHand.total):
            gameEnd = True
            playerWins += 1
            whoWon = f'You win!\nYour Score: {playerHand.total}\nComputer Score: {compHand.total}\n'
            replayMsg = f'Player wins: {playerWins} - {playerWins * 100 / games}%\nComputer wins: {compWins} - {compWins * 100 / games}%\nGames Tied: {(games - playerWins - compWins) * 100 / games}%\nGames played: {games}\nPlay again?'
            okayMsg = "Cool!"

          #condition for player losing
          elif (playerHand.total < compHand.total):
            gameEnd = True
            compWins += 1
            whoWon = f'You lose!\nYour Score: {playerHand.total}\nComputer Score: {compHand.total}\n'
            replayMsg = f'Player wins: {playerWins} - {playerWins * 100 / games}%\nComputer wins: {compWins} - {compWins * 100 / games}%\nGames Tied: {(games - playerWins - compWins) * 100 / games}%\nGames played: {games}\nPlay again?'
            okayMsg = "Crap!"

          #condition for a tie
          else:
            gameEnd = True
            whoWon = f'Tie!\nYour Score: {playerHand.total}\nComputer Score: {compHand.total}\n'
            replayMsg = f'Player wins: {playerWins} - {playerWins * 100 / games}%\nComputer wins: {compWins} - {compWins * 100 / games}%\nGames Tied: {(games - playerWins - compWins) * 100 / games}%\nGames played: {games}\nPlay again?'
            okayMsg = "Seriously?"

    #show the winner and prompt the player to play again
    easygui.msgbox(whoWon, gameTitle, okayMsg) 
    goAgane = easygui.ynbox(replayMsg, gameTitle)

    #rebuild deck and hands
    gameDeck.newDeck()
    playerHand.newHand()
    compHand.newHand()

if (__name__ == "__main__"):
  main()