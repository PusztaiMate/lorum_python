from abc import ABC, abstractmethod

class PlayerABC(ABC):
    '''abstract base class for Player and Bot(s)'''

    def __init__(self, name):
        self._name = name
        self._cards = []
        self._points = 0
    
    @abstractmethod
    def bid(self):
        '''bid for the right to start'''
        pass

    @abstractmethod
    def choose_card(self, handler):
        '''the game calls this function when the its the players turn.
        Returns the chosen card'''
        pass

    @abstractmethod
    def is_selling(self, highest_bid):
        pass

    @property
    @abstractmethod
    def name(self):
        return self._name

    @abstractmethod
    def get_card(self, card):
        '''puts the given card into its own list'''
        pass

    @abstractmethod
    def clear_hand(self):
        '''deletes every card that the player holds'''
        pass
