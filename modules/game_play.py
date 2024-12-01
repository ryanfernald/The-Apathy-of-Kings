import random
import copy
from . import utility as util

from . import game_card as gc
from .utility import load_dragons_from_assets


class GamePlay:

    def __init__(self):
        self.__info = {
            'player1': {'hand': [], 'deck': [], 'dragon': None},
            'player2': {'hand': [], 'deck': [], 'dragon': None},
        }
        
        # load card from \asset\card
        card_atk_list, card_def_list, card_sup_list = util.load_cards_name_from_assets()
        game_card_atk = util.convert_to_atk_card(card_atk_list)
        game_card_def = util.convert_to_def_card(card_def_list)
        game_card_sup = util.convert_to_sup_card(card_sup_list)

        # Load dragon data
        self.dragons = util.load_dragons_from_assets()
        
        # Assign dragons randomly
        self.assign_dragons(self.dragons)

        # use deepcopy to fix card.view mess because shallow copy problem
        # set up card for player1 
        self.add_card(4, copy.deepcopy(game_card_atk), self.__info['player1'])
        self.add_card(3, copy.deepcopy(game_card_def), self.__info['player1'])
        # self.add_card(1, copy.deepcopy(game_card_sup), self.__info['player1'])
        # set up card for player2
        self.add_card(4, copy.deepcopy(game_card_atk), self.__info['player2'])
        self.add_card(3, copy.deepcopy(game_card_def), self.__info['player2'])
        # self.add_card(1, copy.deepcopy(game_card_sup), self.__info['player2'])



    def assign_dragons(self, dragons):
        if len(dragons) < 2:
            raise ValueError("Not enough dragons available to assign to players!")
        random.shuffle(dragons)
        self.__info['player1']['dragon'] = self.dragons.pop()
        self.__info['player2']['dragon'] = self.dragons.pop()
        # print(f"Player 1 assigned dragon: {self.__info['player1']['dragon'].name}")
        # print(f"Player 2 assigned dragon: {self.__info['player2']['dragon'].name}")

        
    @property
    def info(self):
        return self.__info

    def add_card(self, num: int, cards: list, player: dict):
        for itr in range(num):
            drawn_card = random.choice(cards)
            drawn_card.view = gc.CardView.FRONT
            player['hand'].append(drawn_card)
            cards.remove(drawn_card)
        
        player['deck'].extend(cards)
        random.shuffle(player['deck'])
    
    # testing purpose
    def displayGameInfo(self):
        print(f'Player 1 hand: {len(self.__info["player1"]["hand"])}')
        print(f'Player 1 deck: {len(self.__info["player1"]["deck"])}')
        print(f'Player 2 hand: {len(self.__info["player2"]["hand"])}')
        print(f'Player 2 deck: {len(self.__info["player2"]["deck"])}')

# 
if __name__ == "__main__":
    game1 = GamePlay()
    game1.displayGameInfo()


