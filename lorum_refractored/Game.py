''' main game lorum '''

from random import randint

from Deck import HungarianDeck
from Pile import Pile
from Player import Player
from Bot import Bot

class Game:
    """description of class"""

    NUMBER_OF_PLAYERS = 4

    def __init__(self):
        self.piles = [Pile(suit) for suit in HungarianDeck.suits]
        self.setup_players()

        self.is_first_card = True
        self.on_turn = 0
        self.starter = randint(0, self.NUMBER_OF_PLAYERS - 1)

    def handle_first_card(self):
        '''handles the first round of the game'''
        card = self.players[self.on_turn].choose_card(self)
        for pile in self.piles:
            if pile.suit == card.suit:
                pile.get_card(card)
            pile.starting_num = card.number
        self.on_turn = (self.on_turn + 1) % self.NUMBER_OF_PLAYERS

    def handle_buy(self):
        '''handles the buying-selling of the right to start'''
        index = self.on_turn
        highest_bid = 0
        highest_bidder = (index + 1) % self.NUMBER_OF_PLAYERS
        turn_since_hb = 0

        while turn_since_hb <= self.NUMBER_OF_PLAYERS -1:
            print('self.on_turn', self.on_turn)
            index = (index + 1) % self.NUMBER_OF_PLAYERS
            turn_since_hb += 1
            if index != self.on_turn:
                player_bid = self.players[index].bid()
                if player_bid > highest_bid:
                    highest_bidder = index
                    highest_bid = player_bid
                    turn_since_hb = 0

        print('self.on_turn=', self.on_turn)
        if self.players[self.on_turn].is_selling(highest_bid):
            self.players[self.on_turn].points += highest_bid
            self.players[highest_bidder].points -= highest_bid
            self.on_turn = highest_bidder

            for player in self.players:
                print(player.name, ':', player.points, 'point(s)')


    def handle_rounds(self):
        '''handles the rest of the rounds'''
        while True:
            print(':' * 150)
            curr_player = self.players[self.on_turn]
            card = curr_player.choose_card(self)
            self.put_card_on_deck(card)
            self.on_turn = self.next_player_index()
            if len(curr_player) == 0:
                return

    def put_card_on_deck(self, card):
        '''puts the card on the correct tabledeck'''
        if card is None:
            return
        for pile in self.piles:
            if pile.suit == card.suit:
                pile.get_card(card)

    def next_player_index(self):
        '''index of the next player'''
        return (self.on_turn + 1) % self.NUMBER_OF_PLAYERS

    def evaluate_points(self):
        '''evaluates the points at the end of the game'''
        sum_card = 0
        winner = None
        for player in self.players:
            num_of_cards = len(player)
            if num_of_cards:
                player.points -= num_of_cards
                sum_card += num_of_cards
            else:
                winner = player

        winner.points += sum_card

        for player in self.players:
            print(player.name, ':', player.points, 'point(s)')
    def run_round(self):
        '''from dealing the cards to eval. the points'''
        game_over = False
        self.is_first_card = True
        while not game_over:
            self.on_turn = self.starter
            self.deal()
            self.handle_buy()
            if self.is_first_card:
                self.handle_first_card()
                self.is_first_card = False
            self.handle_rounds()
            self.evaluate_points()
            game_over = self.ask_if_over()
            self.starter = (self.starter + 1) % self.NUMBER_OF_PLAYERS
            for tdeck in self.piles:
                tdeck.clear_cards()

    def ask_if_over(self):
        '''handling exit for now'''
        ans = input('Do you want to quit? (y/n)')
        if ans.lower() == 'n':
            return False
        return True

    def setup_players(self):
        '''initialazing players and bots'''
        human_players = 0
        bot_players = self.NUMBER_OF_PLAYERS - human_players
        self.players = [Player('Player ' + str(i)) for i in range(1, 1 + human_players)]
        for i in range(1, 1 + bot_players):
            self.players.append(Bot('Bot' + str(i)))

    def deal(self):
        '''deals the cards'''
        deck = HungarianDeck()
        for player in self.players:
            player.clear_hand()
        for player in self.players:
            for _ in range(8):
                player.get_card(deck.draw())

    def legal_cards(self):
        '''cards that can be played out'''
        return [pile.next_card() for pile in self.piles]

    def current_cards(self):
        re_val = []
        for pile in self.piles:
            if pile:
                re_val.append(pile[len(pile) - 1])
        return re_val

if __name__ == '__main__':
    g = Game()
    g.run_round()
    