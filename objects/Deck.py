import random

from objects.Card import Card


class Deck:
    """
    deck class compiles a full set of 52 cards objects on creation. other methods implements what a dealer normally
    does with a deck of cards; shuffling, drawing, etc
    """
    def __init__(self):
        self.pile = []
        for i in range(52):
            self.pile.append(Card(i))

    def refresh(self):
        self.__init__()

    def check(self):
        for card in self.pile[0:10]:
            print(card.show())

    def shuffle(self):
        random.shuffle(self.pile)

    def draw(self):
        drawn = self.pile[0]
        self.pile.pop(0)

        return drawn

    def burn(self):
        self.pile.pop(0)

    def show_flop(self):

        self.burn()

        flop_cards = []
        for i in range(3):
            flop_cards.append(self.draw())

        return flop_cards

    def show_turn_river(self):

        self.burn()
        turn_river_card = self.draw()

        return [turn_river_card]
