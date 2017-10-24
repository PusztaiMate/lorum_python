''' the module that consists the bot for the game '''
from collections import OrderedDict
from random import choice
from PlayerABC import PlayerABC
from Deck import HungarianDeck, Card

class BotLevel1(PlayerABC):
    '''basic bot for the game.
    Doesn't sell or buy, randomly
    makes a legal move'''
    def __init__(self, name):
        super().__init__(name)
        self.cards = []
        self.points = 0

    def __len__(self):
        return len(self.cards)

    def bid(self):
        self.me_says('Fuck you, I dont want to fucking start!')
        return 0

    def choose_card(self, handler):
        legal_cards = handler.legal_cards()
        # legal_cards = [legal_cards.copy()[i] for i in range(len(legal_cards))
        # if legal_cards[i] is not None]
        lc_tmp = []
        for i, card in enumerate(legal_cards):
            if legal_cards[i] is not None:
                lc_tmp.append(card)
        legal_cards = lc_tmp

        for card in legal_cards:
            if card is None:
                legal_cards.remove(card)
        own_legal_moves = []
        if handler.is_first_card:
            chosen_card = choice(self.cards)
            self.cards.remove(chosen_card)
            handler.is_first_card = False
            return chosen_card
        for card in self.cards:
            if card in legal_cards:
                own_legal_moves.append(card)

        if own_legal_moves:
            chosen_card = choice(own_legal_moves)
            self.cards.remove(chosen_card)
            answ = 'Card played: ' + str(chosen_card) + ', card left: '
            answ += str(len(self.cards))
            self.me_says(answ)
            return chosen_card
        self.me_says('Pass! Cards left:' + str(len(self.cards)))
        return None

    def clear_hand(self):
        self.cards.clear()

    @property
    def name(self):
        return super().name

    def get_card(self, card):
        self.cards.append(card)

    def is_selling(self, highest_bid):
        self.me_says('No points are enough!')
        return False

    def me_says(self, message, **kwargs):
        '''printing the bots name as part of the msg '''
        print(self.name, ':', message, **kwargs)


class BotLevel2(PlayerABC):
    '''level 2 bot'''
    def __init__(self, name):
        super().__init__(name)
        self.cards = []
        self.points = 0

    def __len__(self):
        return len(self.cards)

    def bid(self):
        '''returns the number of points the bot is willing to give
        to have the right to start'''
        possible_holes =  self.calculate_sum_dist(self.get_starting_card())
        self.say('I give', 20 - possible_holes, 'for the right to start!')
        return 20 - possible_holes

    @property
    def name(self):
        return super().name

    def get_starting_card(self):
        '''chooses the starting card and returns it'''
        best_cards = self.best_starting_cards()
        # remove if we only have one card of the suit & it's not a big diff
        # TODO: get statistics about this and have a better guess
        lonely_suits = []
        for suit, num_of_cards in self.cards_per_suit().items():
            if num_of_cards == 1:
                lonely_suits.append(suit)
        # TODO: this one below
        # ~the amount of less points if we start with lonely card:
        # LONELY = 3
        # since best_cards is an OrderedDict we can do this:
        examined_card = None
        while True:
            examined_card = best_cards.popitem(last=False)[0]
            suit = examined_card.split(' ')[0]
            if suit not in lonely_suits:
                break
        return Card.from_string(examined_card)

    def get_possible_cards(self, handler):
        '''returns the cards that can be played out'''
        nexts_on_pile = handler.legal_cards()
        pos_crds = [card for card in nexts_on_pile if card in self.cards]
        return pos_crds

    def choose_card(self, handler):
        '''chooses a legal card from the hand and gives it to the handler'''
        if handler.is_first_card:
            return self.get_starting_card()
        # if it's not the first round:
        possible_cards = self.get_possible_cards(handler)
        # if the bot has no options
        if not possible_cards:
            msg = choice(('Pass!', 'Go on without me!', "Resting this round"))
            self.say(msg)
            return None
        # if we have only one option:
        if len(possible_cards) == 1:
            chosen_card = possible_cards[0]
            self.cards.remove(chosen_card)
            self.say('playing out:', chosen_card)
            return chosen_card

        chosen_card = self.pick_best_card(possible_cards)
        self.say('playing out:', chosen_card)
        self.cards.remove(chosen_card)
        return chosen_card

    def pick_best_card(self, possible_cards):
        '''picks wich card to play out and returns it'''
        cards_p_suit = self.cards_per_suit()
        chosen_card = possible_cards[0]
        for ccard in possible_cards:
            if cards_p_suit[ccard.suit] > cards_p_suit[chosen_card.suit]:
                chosen_card = ccard
        return chosen_card

    def clear_hand(self):
        '''clear the remaining cards from the hand'''
        self.cards.clear()

    def say(self, *msg, **kwargs):
        '''appends '"NAME": ... in front of the message'''
        print(self.name + ':', *msg, **kwargs)

    def get_card(self, card):
        self.cards.append(card)

    def is_selling(self, highest_bid):
        if highest_bid > 10:
            return True
        return False

    def cards_per_suit(self):
        '''returns a dict: dict[suit]==number of cards per suit'''
        card_p_suit = {}
        for suit in HungarianDeck.suits:
            num = 0
            for card in self.cards:
                if card.suit == suit:
                    num += 1
            card_p_suit[suit] = num
        return card_p_suit

    def calculate_sum_dist(self, starting_card):
        '''calculates the number of holes with given starting card'''
        HDeck = HungarianDeck
        cards_p_suit = self.cards_per_suit()
        num_of_holes = 0
        for suit in HungarianDeck.suits:
            # Temporary starting card for calculation
            tmp_card = Card(suit, starting_card.number)
            # Every cards distance from the starting card
            # 0 if not same suit, distance if same
            dists = [HDeck.distance(tmp_card, card) for card in self.cards]
            # number of holes given a suit. max of the list created above
            # minus the number of cards in that suit
            num_of_holes += max(dists) - cards_p_suit[suit]
            # if the starting card is not in our hand we add that one to
            # the number aswell (because we created a temporary card)
            if cards_p_suit[suit] != 0:
                num_of_holes += 1
        return num_of_holes

    def best_starting_cards(self):
        '''gives the 3 "best" starting option'''
        holes = dict()
        for card in self.cards:
            holes[str(card)] = self.calculate_sum_dist(card)
        ordered_hpc = OrderedDict(sorted(holes.items(), key=lambda t: t[1]))
        return ordered_hpc
