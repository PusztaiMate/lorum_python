''' the module that consists the bot for the game '''

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
            print('card:', card, type(card), sep='--')
            print('legal_cards', legal_cards, type(legal_cards), sep='--')
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

    def bid(self):
        pass

    @property
    def name(self):
        super().name()

    def choose_card(self, handler):
        '''chooses a legal card from the hand and gives it to the handler'''
        pass

    def clear_hand(self):
        '''clear the remaining cards from the hand'''
        self.cards.clear()

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
        hole_per_card = {str(card) : self.calculate_sum_dist(card) for card in self.cards}
        while len(hole_per_card) > 3:
            highest_val = max(hole_per_card.values())
            highest_key = None
            for kkey, vval in hole_per_card.items():
                if vval == highest_val:
                    highest_key = kkey
            hole_per_card.__delitem__(highest_key)
        return hole_per_card

if __name__ == '__main__':
    deck = HungarianDeck()
    bot = BotLevel2('Test_Bot')
    for _ in range(8):
        bot.get_card(deck.draw())
    bot.cards = sorted(bot.cards)
    for card in bot.cards:
        print(card, end=' | ')
    print()
    for card in bot.cards:
        print('Number of holes with', card, ':', bot.calculate_sum_dist(card))
    print('best_starting_cards():')
    for k, card in bot.best_starting_cards().items():
        print(k, sep=' | ', end=' ')
