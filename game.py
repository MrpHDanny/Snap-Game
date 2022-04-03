import random
import time
import threading
import sys

'''
    Game of Snap (2 Player AI only)

    Author: Danielis Golubovskis
    Date last modified: 30-04-2020
    Python version: Python 3.7.7 64-bit

'''


class Card:
    def __init__(self, suit, val):
        self.suit = suit
        self.value = val

    def show(self):
        print("{} of {}".format(self.value, self.suit))


class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    # Function to generate the deck
    def build(self):
        for s in ["Spades", "Clubs", "Diamonds", "Hearts"]:
            for v in ("Ace", "King", "Queen", "Jack", 10, 9, 8, 7, 6, 5, 4, 3, 2):
                self.cards.append(Card(s, v))

    def show(self):
        for c in self.cards:
            c.show()

    # Function to shuffle the deck using the Fisher Yates shuffle
    def shuffle(self):
        for i in range(len(self.cards) - 1, 0, -1):
            r = random.randint(0, i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]


class Pile:
    def __init__(self):
        self.cards = []

    def getTopCards(self):
        topCards = []
        if len(self.cards) > 1:
            # Get second card from the top
            topCards.append(self.cards[-2])
        # Get top card
        topCards.append(self.cards[-1])
        return topCards

    def hasMatched(self):
        topCards = self.getTopCards()
        return topCards[0].value == topCards[1].value


class Player:
    def __init__(self, name):
        self.name = name

    def draw(self, deck, pile):
        '''
        Simulating 'think' time by adding a random
        delay between each card draw of 0.5s - 1.0s
        Note: there is also a delay after pile
        and deck info is printed but it is constant
        '''
        delayTime = random.randint(500, 1000)/1000
        time.sleep(delayTime)
        card = deck.cards.pop()
        pile.cards.append(card)
        print("> {} drew {} of {}".format(self.name, card.value, card.suit))

    def saySnap(self):
        '''
        To simulate human reaction speed I took the fastest
        recorded reaction speed of 120ms (Needs fact checking)
        and my slowest reaction speed of 400ms as boundaries
        for how fast can the AI can call out 'Snap'
        '''
        reactionTime = random.randint(120, 401) / 1000
        threading.Timer(
            reactionTime, lambda p: print(f"> {p} : Snap! (Reaction time: {reactionTime})"), args=(self.name,)).start()
        return reactionTime


class UInterface:

    def sayWelcome(self):
        print("---------------------------")
        print("   Welcome to Snap v1.0")
        print("---------------------------")
        time.sleep(1)
        print("\nStarting the game with two players\n")
        time.sleep(1)

    def announceADraw(self):
        time.sleep(1)
        print("> The deck is out of cards and the game is a draw!!!")
        time.sleep(1)
        print("> Ending the game...")
        sys.exit()

    def printWinnerOfGame(self, player):
        time.sleep(1)
        print("> Woohoo!!! Winner of the game is: {}".format(player))
        time.sleep(1)
        print("> Ending the game...")
        sys.exit()

    def printPileAndDeck(self, deck, pile):
        topCards = pile.getTopCards()
        deckSize = len(deck.cards)
        if len(topCards) == 2:
            print("---Current top cards in pile: [{} of {} and {} of {}]".format(
                topCards[0].value, topCards[0].suit, topCards[1].value, topCards[1].suit))
            print("---Cards in deck: {}\n".format(deckSize))
        else:
            print("---Current top cards in pile: [{} of {}]".format(
                topCards[0].value, topCards[0].suit))
            print("---Cards in deck: {}\n".format(deckSize))
        time.sleep(0.5)


class Game():
    def __init__(self, player1, player2):
        self.turn = 0
        self.pile = Pile()
        self.deck = Deck()
        self.players = [player1, player2]
        self.ui = UInterface()

    def startGame(self):
        '''
        I'm probably breaking every rule of good python
        coding practice by avoiding using self.x in this
        method but I'm new to python so I'll let it slide
        '''
        turn = self.turn
        pile = self.pile
        deck = self.deck
        players = self.players
        ui = self.ui
        topCards = []  # Top cards in pile

        ui.sayWelcome()
        deck.shuffle()
        # Player 1 puts first card into pile
        players[turn].draw(deck, pile)
        ui.printPileAndDeck(deck, pile)
        turn = 1 - turn
        # Player 2 puts second card into pile
        players[turn].draw(deck, pile)
        ui.printPileAndDeck(deck, pile)
        turn = 1 - turn
        # Players start drawing until there is a match
        while len(deck.cards) > 0:
            # Check if match occured
            if pile.hasMatched():
                # Both players react as fast as they can
                p1Time = players[0].saySnap()
                p2Time = players[1].saySnap()
                time.sleep(1)
                # Player 1 won
                if p1Time < p2Time:
                    ui.printWinnerOfGame(players[0].name)
                # In the unlikely scenario both players have identical reaction times call draw
                elif p1Time == p2Time:
                    print(
                        "Wow, both players had identical reaction times... It's a draw!")
                    sys.exit()
                # Player 2 won
                else:
                    ui.printWinnerOfGame(players[1].name)
            # Keep drawing
            players[turn].draw(deck, pile)
            ui.printPileAndDeck(deck, pile)
            turn = 1 - turn
        # No winner since deck is empty
        ui.announceADraw()


if __name__ == '__main__':

    player1 = Player("Bob")
    player2 = Player("George")
    game = Game(player1, player2)
    game.startGame()  # Run the game
