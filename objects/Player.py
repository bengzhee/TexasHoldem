from objects.Hand import Hand


class Player:
    """
    player class holds information distributed cards and the amount of capital held. class variables are information
    visible to all players.

    added player actions like bet, check, raise. need to review again if this should be here
    """

    def __init__(self, name, capital):
        self.name = name
        self.hand = Hand()
        self.capital = capital
        self.stakes = 0

    def draw_card(self, deck):
        self.hand.draw_card(deck)

    def clear_hand(self):
        self.hand.pokerhand = []

    def clear_stakes(self):
        self.stakes = 0

    def check_cards(self):
        return [card.show() for card in self.hand.pokerhand]

    def show_hidden_cards(self):
        return ['[]' for card in self.hand.pokerhand]

    def update_score(self):
        self.hand.update_hand(self.community_cards)
        self.hand.check_score()

    def Bet(self, value):
        if value > self.capital:
            return 1

        self.capital -= value
        Player.pot += value
        self.stakes = value

        return 0

    def Check(self):
        """Check doesn't do anything."""

    def Raise(self, other, value):
        if value <= other.stakes:
            return 1
        self.capital -= value
        Player.pot += value
        self.stakes = value

    def Call(self, other):
        if other:
            if other.stakes >= self.capital:
                Player.pot += self.capital
                self.stakes = self.capital
                self.capital = 0
            else:
                self.capital -= other.stakes
                Player.pot += other.stakes
                self.stakes = other.stakes
