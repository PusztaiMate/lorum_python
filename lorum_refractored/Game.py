from Deck import HungarianDeck
from TableDeck import TableDeck
from Player import Player

class Game:
    """description of class"""

    NUMBER_OF_PLAYERS = 4

    def __init__(self):
        self.tabledecks = [TableDeck(suit) for suit in HungarianDeck.suits]
        self.setup_players()

    def handle_first_round(self, card):
        pass

    def handle_buy(self):
        pass

    def handle_rounds(self):
        pass

    def run(self):
        game_over = False
        while not game_over:
            deal()
            handle_buy()
            handle_rounds()
            handle_points()

    def setup_players(self):
        self.players = [Player('Player ' + str(i)) for i in range(1, 4)]

    def deal(self):
        deck = HungarianDeck()
        for player in players:
            for i in range(8):
                player.get_card(deck.draw())
