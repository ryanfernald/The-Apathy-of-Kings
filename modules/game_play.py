import random
from . import utility as util


class GamePlay:

    def __init__(self):
        self.__info = {'player1': {'hand': [], 'deck': []},
                       'player2': {'hand': [], 'deck': []}
                       }
        
        # load card from \asset\card
        card_atk_list, card_def_list, card_sup_list = util.load_cards_name_from_assets()
        game_card_atk = util.convert_to_atk_card(card_atk_list)
        game_card_def = util.convert_to_def_card(card_def_list)
        game_card_sup = util.convert_to_sup_card(card_sup_list)

        # set up card for player1
        self.add_card(4, game_card_atk.copy(), self.__info['player1'])
        self.add_card(2, game_card_def.copy(), self.__info['player1'])
        self.add_card(1, game_card_sup.copy(), self.__info['player1'])
        # set up card for player2
        self.add_card(4, game_card_atk.copy(), self.__info['player2'])
        self.add_card(2, game_card_def.copy(), self.__info['player2'])
        self.add_card(1, game_card_sup.copy(), self.__info['player2'])

    @property
    def info(self):
        return self.__info

    def add_card(self, num: int, cards: list, player: dict):
        for itr in range(num):
            drawn_card = random.choice(cards)
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


