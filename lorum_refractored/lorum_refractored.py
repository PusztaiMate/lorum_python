from Deck import HungarianDeck, Card
from Player import Player
from TableDeck import TableDeck


p = Player('Máté')
d = HungarianDeck()
for i in range(8):
    p.get_card(d.draw())

p.print_cards()
