from maps.Card_Map import card_map


class Card:
    """
    card class with card value information. card serial also acts as value of the card which depends on
        1. face value
        2. suit value
    actual card value can be check from Card_Map.
    hash and some operators are overloaded to make the objects iterable and comparable.
    """
    def __init__(self, serial):
        if type(serial) == int:
            self.serial = serial
        elif type(serial) == str:
            self.serial = card_map[serial]

        self.value = int(self.serial / 4)
        self.valueliteral = ('J' if self.value == 9 else
                             'Q' if self.value == 10 else
                             'K' if self.value == 11 else
                             'A' if self.value == 12 else
                             str(self.value + 2))

        self.suitrank = self.serial % 4
        self.suit = ('C' if self.suitrank == 0 else
                     'D' if self.suitrank == 1 else
                     'H' if self.suitrank == 2 else
                     'S')

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __lt__(self, other):
        return self.serial < other.serial

    def __hash__(self):
        return hash(self.serial)

    def show(self):
        return self.valueliteral + self.suit


