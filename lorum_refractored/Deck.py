''' Card & Deck '''

import random

class TooManyCards(Exception):
    '''exception for too many cards'''
    pass

class InvalidCard(Exception):
    '''exception for invalid cards'''
    pass

class Card:
    '''Card'''

    card_id = 0  # for sorting

    def __init__(self, suit=None, number=None):
        self.suit = suit
        self.number = number
        self.c_id = Card.card_id
        Card.card_id += 1

    @classmethod
    def from_string(cls, string):
        '''init from string (example: "Makk Ász")'''
        suit, number = string.split(' ')
        return cls(suit, number)

    def __str__(self):
        return self.suit + ' ' + self.number

    def __eq__(self, other):
        if other is None:
            return False
        return self.suit == other.suit and self.number == other.number

    def __lt__(self, other):
        return  self.c_id < other.c_id

    def __sub__(self, other):
        if self.suit != other.suit:
            return 0
        else:
            return self.c_id - other.c_id


class Deck:
    '''deck of cards'''
    def __init__(self):
        self.cards = []

    def __getitem__(self, index):
        return self.cards[index]

    def __len__(self):
        return len(self.cards)

    def __bool__(self):
        return len(self.cards) != 0

    def draw(self):
        '''draw a random card from the deck'''
        return self.cards.pop(random.randint(0, len(self) - 1))

    def print_cards(self, **kwargs):
        '''print the cards in the deck'''
        for card in self.cards:
            print(card, **kwargs)

class HungarianDeck(Deck):
    '''Hungarian deck with 32 cards'''
    suits = 'Tök Makk Levél Szív'.split(' ')
    numbers = 'VII VIII IX X Alsó Felső Király Ász'.split(' ')

    def __init__(self):
        Deck.__init__(self)
        self.cards = [Card(suit, number) for suit in HungarianDeck.suits
                      for number in HungarianDeck.numbers]

    @classmethod
    def next_card(cls, card):
        '''gives the next card. Makk Ász -> Makk VII'''
        if card is None:
            return None
        suit = card.suit
        if card.number == 'Ász':
            number = 'VII'
        else:
            index = cls.numbers.index(card.number)
            index += 1
            number = cls.numbers[index]
        return Card(suit, number)

    @classmethod
    def distance(cls, card1, card2):
        '''returns the distance of two cards.
        order doesn't matter(c1-c2 == c2-c1).
        if they are different color distance() returns 0'''
        if card1.suit != card2.suit:
            return 0
        else:
            tmp = 0
            while card1 != card2:
                card1 = HungarianDeck.next_card(card1)
                tmp += 1
            return tmp

if __name__ == '__main__':
    print('in main')
    d = HungarianDeck()
    for card in d:
        print(card)


