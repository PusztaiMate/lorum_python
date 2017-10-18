'''the deck that collects the cards'''

from Deck import Deck, HungarianDeck, TooManyCards, InvalidCard

class TableDeck(Deck):
    def __init__(self, suit):
        Deck.__init__(self)
        self.suit = suit
        self.starting_num = None
 
    def get_card(self, card):
        if len(self) == 8:
            raise TooManyCards()
        next_c = self.next_card()
        if next_c is None or next_c == card:
            self.cards.append(card)
        else:
            raise InvalidCard()

    def curr_card(self):
        if len(self) > 0:
            return self.cards[len(self) - 1]
        return None

    def next_card(self):
        if len(self) == 0 and self.starting_num is None:
            return None#
        if len(self) == 0 and self.starting_num is not None:
            return Card(self.suit, self.starting_num)
        if len(self) == 8:
            return None
        curr = self.curr_card()
        return HungarianDeck.next_card(curr)


