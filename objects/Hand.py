import operator

from maps import Score
from objects.Card import Card


class Hand:
    """
    hand class checks and assign the score of a set of cards from the player hand and community cards.

    TODO: redefine ranking list.
    """
    def __init__(self):
        self.pokerhand = []
        self.combined_hand = self.pokerhand
        self.hand_by_value = self.rank_cardvalue()
        self.hand_by_suit = self.rank_cardsuit()
        self.score = 0
        self.best_hand = None

    def draw_card(self, deck):
        self.pokerhand.append(deck.draw())

    def update_hand(self, community_cards=None):
        if community_cards is None:
            community_cards = []

        self.combined_hand = self.pokerhand + community_cards
        self.combined_hand.sort(reverse=True)
        self.hand_by_value = self.rank_cardvalue()
        self.hand_by_suit = self.rank_cardsuit()

    def check_score(self):
        if self.has_royal_flush():
            self.best_hand = 'Royal Flush'
        elif self.has_straight_flush():
            self.best_hand = 'Straight Flush'
        elif self.has_quadruplets():
            self.best_hand = '4 of a Kind'
        elif self.has_fullhouse():
            self.best_hand = 'Full House'
        elif self.has_flush():
            self.best_hand = 'Flush'
        elif self.has_straight():
            self.best_hand = 'Straight'
        elif self.has_triplets():
            self.best_hand = '3 of a Kind'
        elif self.has_two_pairs():
            self.best_hand = '2 Pairs'
        elif self.has_pair():
            self.best_hand = 'Pairs'
        else:
            self.score = sum([card.serial for card in self.combined_hand[0:5]])
            self.best_hand = 'High Card'

    def rank_card_list(self):
        return self.combined_hand.sort(reverse=True)

    def rank_cardvalue(self, cards_list=None):
        """returns a list of sorted (cardvalue, frequency) tuples. 
        uses cards_list if given, else uses self.combined_hand"""

        if cards_list:
            value_list = [c.value for c in cards_list]
        else:
            value_list = [c.value for c in self.combined_hand]
        value_count_list = {v: value_list.count(v) for v in value_list}
        sorted_value_count_list = sorted(value_count_list.items(), key=operator.itemgetter(0), reverse=True)

        return sorted_value_count_list

    def rank_cardsuit(self, cards_list=None):
        """returns a list of sorted (cardsuit, frequency) tuples
        uses cards_list if given, else uses self.combined_hand"""

        if cards_list:
            suit_list = [c.suit for c in cards_list]
        else:
            suit_list = [c.suit for c in self.combined_hand]
        suit_count_list = {s: suit_list.count(s) for s in suit_list}
        sorted_suit_count_list = sorted(suit_count_list.items(), key=operator.itemgetter(0), reverse=True)
        return sorted_suit_count_list

    def has_pair(self):

        hand_has_pair = False
        value_with_pair = None

        for val, freq in self.hand_by_value:
            if freq >= 2:
                hand_has_pair = True
                value_with_pair = val
                break

        if hand_has_pair:
            remaining_cards = self.combined_hand.copy()
            counter = 0
            for c in self.combined_hand:
                if c.value == value_with_pair:
                    remaining_cards.remove(c)
                    counter += 1
                    if counter == 2:
                        break
            self.score = Score.pair_score
            self.score += value_with_pair * 2
            self.score += sum([card.serial for card in remaining_cards[0:3]])

        return hand_has_pair

    def has_two_pairs(self):

        hand_has_2pair = False
        value_with_1pair = None
        value_with_2pair = None

        for val, freq in self.hand_by_value:
            if freq >= 2:
                value_with_1pair = val
                break

        if value_with_1pair:
            remaining_cards = self.combined_hand.copy()
            counter = 0
            for c in self.combined_hand:
                if c.value == value_with_1pair:
                    remaining_cards.remove(c)
                    counter += 1
                    if counter == 2:
                        break

            if remaining_cards:
                remaining_by_value = self.rank_cardvalue(remaining_cards)

                for val, freq in remaining_by_value:
                    if freq >= 2:
                        hand_has_2pair = True
                        value_with_2pair = val
                        break

                if value_with_2pair:
                    remaining_cards2 = remaining_cards.copy()
                    counter = 0
                    for c in remaining_cards:
                        if c.value == value_with_2pair:
                            remaining_cards2.remove(c)
                            counter += 1
                            if counter == 2:
                                break

                    self.score = Score.two_pair_score
                    self.score += value_with_1pair * 2
                    self.score += value_with_2pair * 2
                    self.score += remaining_cards2[0].value

        return hand_has_2pair

    def has_triplets(self):

        hand_has_triplets = False
        value_with_trips = None

        for val, freq in self.hand_by_value:
            if freq >= 3:
                hand_has_triplets = True
                value_with_trips = val
                break

        if hand_has_triplets:
            remaining_cards = self.combined_hand.copy()
            counter = 0
            for c in self.combined_hand:
                if c.value == value_with_trips:
                    remaining_cards.remove(c)
                    counter += 1
                    if counter == 3:
                        break

            self.score = Score.triplets_score
            self.score += value_with_trips * 3

        return hand_has_triplets

    def has_straight(self):
        hand_has_straight = False

        for i in range(len(self.hand_by_value) - 5 + 1):
            if self.hand_by_value[i][0] == self.hand_by_value[i + 4][0] + 4:
                hand_has_straight = True
                high_card_value = self.hand_by_value[i][0]
                break

        if hand_has_straight:
            self.score = Score.straight_score
            for seq in range(high_card_value - 4, high_card_value + 1):
                for c in self.combined_hand:
                    if c.value == seq:
                        self.score += c.serial
                        break

        return hand_has_straight

    def has_flush(self):

        hand_has_flush = False
        for suit, freq in self.hand_by_suit:
            if freq >= 5:
                hand_has_flush = True
                suit_on_flush = suit
                break

        if hand_has_flush:
            self.score = Score.flush_score
            counter = 0
            for c in self.combined_hand:
                if c.suit == suit_on_flush:
                    self.score += c.serial
                    counter += 1
                    if counter == 5:
                        break

        return hand_has_flush

    def has_fullhouse(self):

        hand_has_fullhouse = False
        value_with_trips = None
        value_with_pair = None

        for val, freq in self.hand_by_value:
            if freq >= 3:
                value_with_trips = val
                break

        if value_with_trips:
            remaining_cards = self.combined_hand.copy()
            counter = 0
            for c in self.combined_hand:
                if c.value == value_with_trips:
                    remaining_cards.remove(c)
                    counter += 1
                    if counter == 3:
                        break

            remaining_by_value = self.rank_cardvalue(remaining_cards)

            for val, freq in remaining_by_value:
                if freq >= 2:
                    hand_has_fullhouse = True
                    value_with_pair = val
                    break

            if value_with_pair:
                remaining_cards2 = remaining_cards.copy()
                counter = 0
                for c in remaining_cards:
                    if c.value == value_with_pair:
                        remaining_cards2.remove(c)
                        counter += 1
                        if counter == 2:
                            break

                self.score = Score.full_house_score
                self.score += value_with_trips * 3
                self.score += value_with_pair * 2

        return hand_has_fullhouse

    def has_quadruplets(self):

        hand_has_quadruplets = False
        value_with_quads = None

        for val, freq in self.hand_by_value:
            if freq >= 4:
                hand_has_quadruplets = True
                value_with_quads = val
                break

        if value_with_quads:
            remaining_cards = self.combined_hand.copy()
            counter = 0
            for c in self.combined_hand:
                if c.value == value_with_quads:
                    remaining_cards.remove(c)
                    counter += 1
                    if counter == 4:
                        break

            self.score = Score.quads_score
            self.score += value_with_quads * 3
            self.score += remaining_cards[0].value

        return hand_has_quadruplets

    def has_straight_flush(self):

        hand_has_straight_flush = False
        suit_on_flush = None
        for suit, freq in self.hand_by_suit:
            if freq >= 5:
                suit_on_flush = suit
                break
        if suit_on_flush:
            flushed_cards = [card for card in self.combined_hand if card.suit == suit_on_flush]

            for i in range(len(flushed_cards) - 5 + 1):
                if flushed_cards[i].value == flushed_cards[i + 4].value + 4:
                    hand_has_straight_flush = True
                    high_card_value = flushed_cards[i][0]
                    break

            if hand_has_straight_flush:
                self.score = Score.straight_flush_score
                for seq in range(high_card_value - 4, high_card_value + 1):
                    for c in flushed_cards:
                        if c.value == seq:
                            self.score += c.serial
                            break

        return hand_has_straight_flush

    def has_royal_flush(self):

        hand_has_royal_flush = False
        royal_flush = {Card(c) for c in ['ten_spades', 'jack_spades', 'queen_spades', 'king_spades', 'ace_spades']}
        if royal_flush.issubset(self.combined_hand):
            hand_has_royal_flush = True
            self.score = Score.royal_flush_score

        return hand_has_royal_flush
