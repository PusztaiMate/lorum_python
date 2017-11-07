''' ... '''

import sys
import pygame

from Deck import HungarianDeck
from Game import Game

WWIDTH = 1200
WHEIGHT = 900

HUMANPLAYER = 3

GREEN = (30, 140, 30)
BLACK = (0, 0, 0)

FPS = 30
FONT = 'comicsansms'
FONTSIZE_BUY = 20


def wait_yes_no(screen, msg):
    '''renders a question and waits for keyboard input'''
    font = pygame.font.SysFont(FONT, 72, True)
    text = font.render(msg + '(y/n)', True, pygame.Color('black'))
    while True:
        screen.fill(GREEN)
        screen.blit(text, ((WWIDTH - text.get_width()) // 2,
                           (WHEIGHT - text.get_height()) // 2))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if event.key == pygame.K_y or event.key == pygame.K_z:
                    return True
                elif event.key == pygame.K_n:
                    return False
        pygame.display.flip()


class Graphics:
    '''lorum game class'''

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WWIDTH, WHEIGHT))
        self.screen_rect = self.screen.get_rect()
        self.deck = []
        self.fpsclock = pygame.time.Clock()
        self.fill_up_deck()

    def fill_up_deck(self):
        '''fills up self.deck with Card images'''
        deck = HungarianDeck()
        for card in deck.cards:
            self.deck.append(CardImage(self.screen, card))

    def buy_sell_surface(self, game_handler, history):
        '''creates a surface to draw buying/selling'''
        state_dict = game_handler.get_current_state()
        self.draw_points(state_dict['points'])
        for i, row in enumerate(history):
            tmpText = "{}'s offer: {}".format(row[0], row[1])
            self.draw_text(tmpText, (100, 25 * i), 20)
        self.flip_display()

    def handle_buy(self, game_handler):
        '''handles the buying process'''
        game_handler.starter = game_handler.starter % 4  # just to be sure..
        game_handler.on_turn = game_handler.starter
        players = game_handler.players
        human_player = players[HUMANPLAYER]
        seller = players[game_handler.starter]
        print(seller.name)
        buyers = []
        for i in range(1, 4):
            buyers.append(players[(game_handler.starter + i) % 4])
        highest_bid = 0
        history = []
        while len(buyers) > 1:
            # this comes back as 0 if the bot doesn't want to buy for price
            # this high
            # text_position = 10, 100
            for buyer in buyers:
                if buyer == human_player:
                    bid = self.bid_human(highest_bid)
                else:
                    bid = buyer.bid(highest_bid)
                if bid == 0 or bid < highest_bid:
                    buyers.remove(buyer)
                    continue
                highest_bid = bid
                history.append((buyer.name, bid))
                self.buy_sell_surface(game_handler, history)
                pygame.time.wait(500)
        if seller is not human_player:
            while not seller.is_selling(highest_bid):
                text = '{}: I decline this offer'.format(seller.name)
                self.draw_text(text, (0, 200), FONTSIZE_BUY)
                self.flip_display()
                if buyers[0] == human_player:
                    highest_bid = self.bid_human(highest_bid)
                else:
                    highest_bid = buyers[0].bid(highest_bid)
                if highest_bid == 0:
                    return
        elif seller is human_player:
            print('seller is human')
            while not self.is_player_selling():
                highest_bid = buyers[0].bid(highest_bid)
                if highest_bid == 0:
                    return
                history.append((buyers[0].name, highest_bid))
                self.buy_sell_surface(game_handler, history)
        buyer = buyers[0]
        seller.points += highest_bid
        buyer.points -= highest_bid
        game_handler.on_turn = game_handler.players.index(buyer)
        game_handler.succesful_buys += 1

    def clear_input_history(self):
        '''just to catch input that is already typed in'''
        for event in pygame.event.get():
            continue

    def wait_for(self, milliseconds):
        '''wrapper for pygame.time.wait'''
        pygame.time.wait(milliseconds)

    def is_player_selling(self):
        self.wait_for(100)
        self.clear_input_history()
        self.draw_text('Do you want to sell?', (300, 300))
        self.flip_display()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_y:
                        return True
                    elif event.key == pygame.K_n:
                        return False

    def get_input(self, prompt):
        pygame.time.wait(250)
        curr_string = []
        rubber = pygame.Rect(400, 400, 450, 100)
        pygame.draw.rect(self.screen, GREEN, rubber)
        text = prompt + ''.join(curr_string)
        self.draw_text(text, (400, 400))
        self.flip_display()
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                continue
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN:
                        return ''.join(curr_string)
                    if event.key == pygame.K_BACKSPACE:
                        if curr_string:
                            rubber = pygame.Rect(400, 400, 450, 100)
                            pygame.draw.rect(self.screen, GREEN, rubber)
                            curr_string = curr_string[0:-1]
                            text = prompt + ''.join(curr_string)
                            self.draw_text(text, (400, 400))
                            self.flip_display()
                        else:
                            # ughhhh
                            rubber = pygame.Rect(400, 400, 450, 60)
                            pygame.draw.rect(self.screen, GREEN, rubber)
                    else:
                        curr_string.append(chr(event.key))
                        text = prompt + ''.join(curr_string)
                        self.draw_text(text, (400, 400))
                        self.flip_display()

    def bid_human(self, highest_bid):
        '''handles graphical biddig for human player'''
        for event in pygame.event.get():
            continue
        ans = None
        while True:
            prompt = 'Your offer (Return=pass): '.format(highest_bid)
            ans = self.get_input(prompt)
            print('ans:', ans, '(', type(ans), ')')
            if ans == '' or ans is None:
                # pass
                return 0
            try:
                ans = int(ans)
                print('ans:', ans, '(', type(ans), ')')
                break
            except:
                continue
        print('ans before returning:', ans)
        return ans

    def run(self):
        ''' runs the game '''
        game_handler = Game()
        player_name = 'Máté'
        game_handler.setup_players(player_name)
        not_over = True
        while not_over:
            game_handler.deal()
            game_handler.players[HUMANPLAYER].sort_cards()
            self.setup_player_cards(game_handler)
            self.draw_current_state(game_handler)
            self.handle_buy(game_handler)
            if game_handler.is_first_card:
                self.handle_first_card(game_handler)
                game_handler.is_first_card = False
            self.run_one_hand(game_handler)
            game_handler.evaluate_points()
            game_handler.starter += 1
            # not_over = wait_yes_no(self.screen, 'Do you want to continue?')
            if not_over:
                self.player_cards = []
                for pile in game_handler.piles:
                    pile.clear_cards()
                    pile.starting_num = None
                game_handler.is_first_card = True
                for player in game_handler.players:
                    player.clear_hand()

    def run_one_hand(self, game_handler):
        '''from deal to someone winning'''
        while True:
            self.draw_current_state(game_handler)
            if game_handler.on_turn == HUMANPLAYER:
                card = self.wait_for_move(game_handler)
                game_handler.put_card_on_deck(card)
                if not game_handler.players[HUMANPLAYER]:
                    return
            else:
                game_handler.on_turn = game_handler.on_turn % 4
                curr_player = game_handler.players[game_handler.on_turn]
                card = curr_player.choose_card(game_handler)
                game_handler.put_card_on_deck(card)
                pygame.time.wait(250)
                if not curr_player:
                    return
            game_handler.on_turn = game_handler.next_player_index()

    def handle_first_card(self, gh):
        '''handles the first round of the game (g.)'''
        # if the human player is on turn
        # gh.on_turn = gh.on_turn % 4
        if gh.on_turn == HUMANPLAYER:
            print('handle_firs_card -> human_player')
            card = self.wait_for_move(gh)
            print('card -> ', card)
        else:
            card = gh.players[gh.on_turn].choose_card(gh)
            print('handle_firs_card -> bot')
            print('card -> ', card)
        for pile in gh.piles:
            if card is None:
                print('??')
            if pile.suit == card.suit:
                pile.get_card(card)
            pile.starting_num = card.number
        gh.on_turn = (gh.on_turn + 1) % gh.NUMBER_OF_PLAYERS

    def draw_current_state(self, game_handler):
        '''draws the current gamestate on the screen'''
        state_dict = game_handler.get_current_state()
        self.screen.fill(GREEN)
        top_cards = state_dict['piles']
        points = state_dict['points']
        self.draw_pile_cards(top_cards)
        self.draw_player_cards()
        self.draw_bot_cards_number(game_handler)
        self.draw_points(points)
        self.flip_display()

    def draw_points(self, points):
        '''draws the points to the left upper corner'''
        font = pygame.font.SysFont(FONT, 14)
        texts_to_render = []
        offset_index = 0
        for k, v in points.items():
            pos = offset_index * 15
            texts_to_render.append((pos, '{}: {}'.format(k, v)))
            offset_index += 1
        for item in texts_to_render:
            text = item[1]
            pos = item[0]
            rendered = font.render(text, True, BLACK)
            self.screen.blit(rendered, (5, pos))

    def draw_pile_cards(self, top_cards):
        '''draws the top cards on the piles'''
        MARGIN = 15
        left = (WWIDTH - 4 * CardImage.CARDWITH - 3 * MARGIN) // 2
        top = WHEIGHT // 2 - 0.5 * CardImage.CARDHEIGHT
        pos = 0
        for card in self.deck:
            if card in top_cards:
                card.blit_me(left + (CardImage.CARDWITH + MARGIN) * pos, top)
                pos += 1

    def draw_player_cards(self):
        '''draws the cards the player have'''
        left = self.get_leftmost_card_x(len(self.player_cards))
        top = WHEIGHT - CardImage.CARDHEIGHT - 100
        for i, card in enumerate(self.player_cards):
            card.blit_me(left + CardImage.CARDWITH * i, top)

    def setup_player_cards(self, game_handler):
        self.player_cards = []
        for card in self.deck:
            if card in game_handler.players[HUMANPLAYER].cards:
                self.player_cards.append(card)

    def wait_for_move(self, game_handler):
        '''waits for the player to pick a card'''
        self.draw_current_state(game_handler)
        player = game_handler.players[HUMANPLAYER]
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    mousex, mousey = event.pos
                    card = self.get_card(mousex, mousey)
                    if card is None:
                        continue
                    if self.check_card(game_handler, card):
                        player.cards.remove(card)
                        for cardImg in self.player_cards:
                            # print(cardImg.name)
                            # print(card.name)
                            if cardImg.name == card.name:
                                self.player_cards.remove(cardImg)
                                break
                        return card
                    else:
                        # print('Not a legal move')
                        continue
                elif event.type == pygame.QUIT:
                    ans = wait_yes_no(self.screen,
                                      msg='Do you really want to quit?')
                    if ans:
                        pygame.quit()
                        sys.exit()
                    else:
                        self.draw_current_state(game_handler)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p or event.key == pygame.K_RETURN:
                        if player.possible_moves(game_handler):
                            # print('You have legal move(s)')
                            # print('Hint:', end=' ')
                            for card in player.possible_moves(game_handler):
                                print(card)
                            continue
                        elif game_handler.is_first_card:
                            continue
                        return None

    def get_card(self, mousex, mousey):
        for card in self.player_cards:
            if card.rect.collidepoint(mousex, mousey):
                return card
        else:
            return None

    @staticmethod
    def get_leftmost_card_x(num_cards):
        '''gives the x coordinate of the leftmost card in the player hands'''
        sWidth = WWIDTH
        coord_x = (sWidth - num_cards * CardImage.CARDWITH) / 2
        return coord_x

    def check_card(self, game_handler, card):
        '''checks if the card is a legal move'''
        if game_handler.is_first_card:
            return True
        if card in game_handler.legal_cards():
            return True
        return False

    def draw_bot_cards_number(self, game_handler):
        MARGIN_X = 20
        FONTSIZE = 10
        screen_rect = self.screen.get_rect()
        players = game_handler.players
        pos = 0, 0
        for i in range(3):
            if i == 0:
                posx = screen_rect.left + MARGIN_X
                posy = screen_rect.bottom // 2 - FONTSIZE // 2
                pos = posx, posy
            elif i == 1:
                posx = screen_rect.right // 2 - 10  # width of text
                posy = screen_rect.top + FONTSIZE // 2
                pos = posx, posy
            elif i == 2:
                posx = screen_rect.right - 150  # fix later
                posy = screen_rect.bottom // 2 - FONTSIZE // 2
                pos = posx, posy
            player = players[i]
            text = '{} cards left'.format(len(player))
            self.draw_text(text, pos)

    def flip_display(self):
        '''flips display'''
        pygame.display.flip()
        self.fpsclock.tick(FPS)

    def draw_text(self, text, pos, size=25):
        font = pygame.font.SysFont('comicsansms', size, True)
        rendered = font.render(text, True, BLACK)
        self.screen.blit(rendered, pos)


class CardImage:
    '''image for the cards'''
    SZIV = 0
    TOK = 1
    LEVEL = 2
    MAKK = 3
    BACK = 4

    CARDWITH = int(1024 / 8)
    CARDHEIGHT = int(806 / 4)

    def __init__(self, screen, card):
        self.screen = screen

        self.name = str(card)
        self.suit, self.number = self.name.split(' ')
        self.image = self.get_card_image()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = 100, 100

    def blit_me(self, left, top):
        '''draw onto surface in its current location'''
        self.rect.left = left
        self.rect.top = top
        self.screen.blit(self.image, self.rect)

    def get_card_image(self):
        '''gets the single card image from the cards/ directory'''
        image_name = self.suit.lower() + '_' + self.number.lower()
        return pygame.image.load('cards/%s.bmp' % image_name).convert()


if __name__ == '__main__':
    g = Graphics()
    g.run()
