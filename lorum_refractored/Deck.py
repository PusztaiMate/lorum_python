''' Card & Deck '''

import random

class TooManyCards(Exception):
    pass

class InvalidCard(Exception):
    pass

class Card:
    '''Card'''

    card_id = 0  # to comput how 'far' 2 cards are from eachother

    def __init__(self, suit=None, number=None):
        self.suit = suit
        self.number = number
        self.c_id = Card.card_id
        Card.card_id += 1

    def __str__(self):
        return self.suit + ' ' + self.number

    def __eq__(self, other):
        return (self.suit == other.suit and self.number == other.number)

    def __lt__(self, other):
        return (self.c_id < other.c_id)

    def __sub__(self, other):
        if self.suit != other.suit:
            return 0
        else:
            return self.c_id - other.c_id



class Deck:
    def __init__(self):
        self.cards = []

    def __getitem__(self, index):
        return self.cards[index]

    def __len__(self):
        return len(self.cards)

    def __bool__(self):
        return len(self.cards) != 0

    def draw(self):
        return self.cards.pop(random.randint(0, len(self) - 1))

    def print_cards(self, **kwargs):
        for card in self.cards:
            print(card, **kwargs)

class HungarianDeck(Deck):
    '''Hungarian deck with 32 cards'''
    suits = 'Tökk Makk Levél Szív'.split(' ')
    numbers = 'VII VIII IX X Alsó Felső Király Ász'.split(' ')

    def __init__(self):
        Deck.__init__(self)
        self.cards = [Card(suit, number) for suit in HungarianDeck.suits 
                      for number in HungarianDeck.numbers]


    @classmethod
    def next_card(cls, card):
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

if __name__ == '__main__':
    print('in main')
    d = HungarianDeck()
    for card in d:
        print(card)


