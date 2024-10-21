import game_card as gc
import tkinter as tk
import utility as util
import random

class GamePlay:

    def __init__(self):
        self.__player1_deck = []
        self.__player1_hand = []
        self.__player2_deck = []
        self.__player2_hand = []
        
        # load card from \asset\card
        card_atk_list, card_def_list, card_sup_list = util.load_cards_name_from_assets()
        game_card_atk = util.convert_to_atk_card(card_atk_list)
        game_card_def = util.convert_to_def_card(card_def_list)
        game_card_sup = util.convert_to_sup_card(card_sup_list)

        # set up card for player1
        self.add_card(4, game_card_atk.copy(), self.__player1_deck, self.__player1_hand)
        self.add_card(2, game_card_def.copy(), self.__player1_deck, self.__player1_hand)
        self.add_card(1, game_card_sup.copy(), self.__player1_deck, self.__player1_hand)
        # set up card for player2
        self.add_card(4, game_card_atk.copy(), self.__player2_deck, self.__player2_hand)
        self.add_card(2, game_card_def.copy(), self.__player2_deck, self.__player2_hand)
        self.add_card(1, game_card_sup.copy(), self.__player2_deck, self.__player2_hand)

        
    @property
    def player1_deck(self):
        return self.__player1_deck
    
    @property
    def player1_hand(self):
        return self.__player1_hand
    
    @property
    def player2_deck(self):
        return self.__player2_deck
    
    @property
    def player2_hand(self):
        return self.__player2_hand

    def add_card(self, num: int, cards: list, deck: list, hand: list):
        for itr in range(num):
            drawn_card = random.choice(cards)
            hand.append(drawn_card)
            cards.remove(drawn_card)
        
        deck.extend(cards)
        random.shuffle(deck)
        
    def displayGameInfo(self):
        print(f'Player 1 hand: {len(self.__player1_hand)}')
        print(f'Player 1 deck: {len(self.__player1_deck)}')
        print(f'Player 2 hand: {len(self.__player2_hand)}')
        print(f'Player 2 deck: {len(self.__player2_deck)}')


def show_card_list(arg):
    for itr in arg:
        itr.display()

if __name__ == "__main__":
    '''root = tk.Tk()
    root.title('Image Display Test')
    root.geometry("600x400")  '''

    
    game1 = GamePlay()
    game1.displayGameInfo()

    '''print('\n\n' +'-'*30 + '\n')
    show_card_list(game1.player1_hand)
    print('\n\n' +'-'*30 + '\n')
    show_card_list(game1.player2_hand)'''

    print(game1.player1_hand[0].imgPath)


