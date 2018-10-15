from objects.Deck import Deck
from objects.Player import Player


class Game:

    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.community_cards = []
        self.pot = 0

        self.players = [Player(i, 1e6) for i in range(2)]
        for player in self.players:
            player.draw_card(self.deck)
            player.draw_card(self.deck)

    def flop(self):
        self.community_cards += self.deck.show_flop()

    def turn_river(self):
        self.community_cards += self.deck.show_turn_river()
