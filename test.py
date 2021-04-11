import unittest
import game

'''
    Game of Snap Test Units

    Author: Danielis Golubovskis
    Date last modified: 30-04-2020
    Python version: Python 3.7.7 64-bit
'''


class TestPlayerClassMethods(unittest.TestCase):

    def setUp(self):
        '''
        2 of Hearts is the top card in deck
        after building the deck
        '''
        self.player = game.Player("Bob")
        self.pile = game.Pile()
        self.deck = game.Deck()
        # Drew 2 of Hearts (top card)
        self.player.draw(self.deck, self.pile)

    # Test value and suit of drawn card in pile
    def test_pile_after_draw(self):
        card = self.pile.cards[0]
        self.assertTrue(card.value == 2 and card.suit == "Hearts")

    # deck size should go down to 51
    def test_deck_after_draw(self):
        self.assertEqual(len(self.deck.cards), 51)


class TestPileClassMethods(unittest.TestCase):

    def setUp(self):
        self.testPile = game.Pile()
        self.card_one = game.Card("Hearts", "Ace")
        self.card_two = game.Card("Spades", "Ace")
        self.testPile.cards.append(self.card_one)
        self.testPile.cards.append(self.card_two)
        self.topCards = self.testPile.getTopCards()

    # hasMatched should return true
    def testHasMatched(self):
        self.assertTrue(self.testPile.hasMatched())

    # hasMatch should return false
    def testHasMatched2(self):
        self.testPile.cards.append(game.Card("Hearts", 2))
        self.assertFalse(self.testPile.hasMatched())

    # Top card should be the Ace of Spades since it was
    # added last
    def testGetTopCards(self):
        self.assertEqual(self.topCards[-1].suit, "Spades")

    # Second from top should be the Ace of Hearts
    def testGetTopCards2(self):
        self.assertEqual(self.topCards[-2].suit, "Hearts")


class TestDeckClassMethods(unittest.TestCase):

    def setUp(self):
        self.deck = game.Deck()

    # Deck size should be 52 after being generated
    def testDeckBuild(self):
        self.assertEqual(len(self.deck.cards), 52)

    # Top card should be 2 of hearts
    def testDeckBuild2(self):
        topCard = self.deck.cards[-1]
        self.assertTrue(topCard.value == 2 and topCard.suit == "Hearts")

    # Top card should not be 2 of hearts
    # The shuffling algorithm ensures this top card
    # Won't stay in the same position
    def testDeckBuild3(self):
        self.deck.shuffle()
        topCard = self.deck.cards[-1]
        self.assertFalse(topCard.value == 2 and topCard.suit == "Hearts")

    '''
    I won't be testing UInterface since it
    only contains methods that have simple
    print statements and the methods that
    the class uses are already tested above

    Same goes for the Card class. It only has
    two fields and a simple print method to print
    its suit and value
    '''


if __name__ == '__main__':
    unittest.main(verbosity=2)
