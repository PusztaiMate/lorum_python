from random import choice

from PlayerABC import PlayerABC

class Bot(PlayerABC):
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
        legal_cards = [legal_cards.copy()[i] for i in range(len(legal_cards)) if legal_cards[i] is not None]
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
            self.me_says('Card played: ' + str(chosen_card) + ', card left: ' + str(len(self.cards)))
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
        print(self.name, ':', message, **kwargs)
     