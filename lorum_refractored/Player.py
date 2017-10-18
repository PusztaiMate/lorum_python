''' Player '''

#TODO: chose_card()

class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, index):
        return self.cards[index]

    def get_card(self, card):
        '''puts the given card into its own list'''
        self.cards.append(card)

    def chose_card(self, handler):
        '''the game calls this function when the its the players turn.
        Returns the chosen card'''
        pass

    def print_cards(self, **kwargs):
        '''prints the cards in hand to the console'''
        for i, card in enumerate(self.cards):
            print(i, ':', card, **kwargs)

    def clear_hand(self):
        '''deletes every card the player owns'''
        self.lapok.clear()

    def is_legal_card(self, card, game_handler):
        '''checks if the given card is a legal move'''
        legal_cards = game_handler.legal_cards()
        if card in legal_cards:
            return True
        return False


