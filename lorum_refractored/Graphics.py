'''...'''

import pygame
import sys
import random

SZINEK = 'MAKK SZIV LEVEL TOKK'.split(' ')
SZAMOK = 'VII VIII IX X ALSÓ FELSŐ KIRÁLY ÁSZ'.split(' ')

WWIDTH = 1200
WHEIGHT = 800


class Graphics:
    '''lorum game class'''

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (WWIDTH, WHEIGHT))

    def test(self):
        '''hello'''
        GREEN = pygame.Color(30, 130, 30)
        card = CardImage(self.screen, self.settings, 'Levél VII')
        while True:
            card = Graphics.get_random_card(self.screen, self.settings)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.fill(GREEN)
            card.blit_me()
            pygame.time.wait(1000)
            pygame.display.flip()

    @staticmethod
    def get_random_card(screen, settings):
        '''just for testing. creates a random card and returns it'''
        suit = random.choice(SZINEK)
        number = random.choice(SZAMOK)
        card_name = suit + ' ' + number
        return CardImage(screen, settings, card_name)


class CardImage:
    '''image for the cards'''
    SZIV = 0
    TOK = 1
    LEVEL = 2
    MAKK = 3
    BACK = 4

    CARDWITH = int(1024 / 8)
    CARDHEIGHT = int(806 / 4)

    def __init__(self, screen, settings, card):
        self.screen = screen
        self.settings = settings

        self.name = str(card)
        posx, posy = self.register_card_pos()
        image = pygame.image.load('hungarian_deck.png').convert()
        self.cropped = image.subsurface(
            posx, posy, CardImage.CARDWITH, CardImage.CARDHEIGHT)
        self.rect = self.cropped.get_rect()
        self.rect.left, self.rect.top = 100, 100

    def blit_me(self):
        '''draw onto surface in its current location'''
        self.screen.blit(self.cropped, self.rect)

    def register_card_pos(self):
        '''gets the image for the card'''
        x, y = 0, 0
        suit = self.name.split(' ')[0].upper()  # upper, just to make sure..
        if suit.startswith('S'):
            y = CardImage.SZIV
        elif suit.startswith('T'):
            y = CardImage.TOK
        elif suit.startswith('L'):
            y = CardImage.LEVEL
        elif suit.startswith('M'):
            y = CardImage.MAKK
        else:
            y = CardImage.BACK

        number = self.name.split(' ')[1]
        if number.lower() == 'ász' or number.lower() == 'asz':
            x = 0
        elif number.lower() == 'király' or number.lower() == 'kiraly':
            x = 1
        elif number.lower() == 'felső' or number.lower() == 'felso':
            x = 2
        elif number.lower() == 'alsó' or number.lower() == 'also':
            x = 3
        elif number.lower() == 'x':
            x = 4
        elif number.lower() == 'ix':
            x = 5
        elif number.lower() == 'viii':
            x = 6
        elif number.lower() == 'vii':
            x = 7
        else:
            x = 0

        x, y = x * CardImage.CARDWITH, y * CardImage.CARDHEIGHT
        return x, y


if __name__ == '__main__':
    setts = Settings()
    g = Graphics(setts)
    g.test()
