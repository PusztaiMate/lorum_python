'''the deck that collects the cards'''

from Deck import Card, Deck, HungarianDeck, TooManyCards, InvalidCard

class Pile(Deck):
    def __init__(self, suit):
        Deck.__init__(self)
        self.suit = suit
        self.starting_num = None
    
    def __len__(self):
        return len(self.cards)

    def __bool__(self):
        if self.cards:
            return True
        return False
 
    def get_card(self, card):
        if len(self) == 8:
            raise TooManyCards()
        next_c = self.next_card()
        if next_c is None or next_c == card:
            self.cards.append(card)
        else:
            print('Problem with: ', card)
            print('next_c', next_c)
            raise InvalidCard()

    def curr_card(self):
        if self.cards:
            return self.cards[len(self) - 1]
        return None

    def next_card(self):
        if len(self) == 0 and self.starting_num is None:
            return None
        if len(self) == 0 and self.starting_num is not None:
            return Card(self.suit, self.starting_num)
        if len(self) == 8:
            return None
        curr = self.curr_card()
        return HungarianDeck.next_card(curr)

    def clear_cards(self):
        '''deleting the cards. right now just simply creating a new list'''
        self.starting_num = None
        self.cards.clear()

