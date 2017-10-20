''' Player '''

#TODO: chose_card()

class Player:
    '''Human player. Maybe base class for bots?'''
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.points = 0

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, index):
        return self.cards[index]

    def __bool__(self):
        if self.cards:
            return False
        return True

    def bid(self):
        '''bid for the right to start'''
        print(self.name, ':')
        self.print_cards(end=' | ')
        bid = input('Ajánlat a kezdésért >> ')
        try:
            bid = int(bid)
        except ValueError:
            return 0
        except TypeError:
            return 0
        return bid

    def get_card(self, card):
        '''puts the given card into its own list'''
        self.cards.append(card)

    def choose_card(self, handler):
        '''the game calls this function when the its the players turn.
        Returns the chosen card'''
        print(self.name, ':')
        self.print_cards(end=' | ')
        print('\nCurrent cards: ', end=' ')
        for card in handler.current_cards():
            print(card, end=' || ')
        while True:
            answer = input('\nChosen card (empty = pass): ')
            try:
                if answer is None or answer == '':
                    return None
                elif int(answer) in range(len(self)):
                    chosen_card = self.cards[int(answer)]
                    if handler.legal_cards()[0] is None:  # first turn
                        self.cards.remove(chosen_card)
                        return chosen_card
                    elif chosen_card in handler.legal_cards():
                        self.cards.remove(chosen_card)
                        return chosen_card
                    else:
                        print('A kártya nem rakható le, próbálj meg egy másikat.')
                        continue
            except Exception:
                continue
            else:
                print('Kérlek próbáld újra\n Választott index: ')
                continue

    def print_cards(self, **kwargs):
        '''prints the cards in hand to the console'''
        self.sort_cards()
        for i, card in enumerate(self.cards):
            print(i, ':', card, **kwargs)

    def clear_hand(self):
        '''deletes every card the player owns'''
        self.cards.clear()

    def is_legal_card(self, card, game_handler):
        '''checks if the given card is a legal move'''
        legal_cards = game_handler.legal_cards()
        if card in legal_cards or legal_cards is None:
            return True
        return False

    def is_selling(self, bid):
        self.print_cards(end=' | ')
        ans = input('Do you want to sell the right to start for {}?'.format(bid))
        if ans.lower() == 'y' or ans.lower() == 'yes':
            return True
        return False

    def sort_cards(self):
        '''sorting the cards'''
        self.cards = sorted(self.cards)
