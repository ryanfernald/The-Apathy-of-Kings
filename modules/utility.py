import os
import game_card as gc


def load_cards_name_from_assets():
    """
    Reads the 'assets' folder and its subfolders to load card names from PNG file names.
    
    This function traverses the 'assets' directory, looks for PNG files, and extracts
    card information from their file names. Based on the number of attributes in the
    file name (comma-separated values), the card names are categorized into attack cards,
    defense cards, and support cards.

    Returns:
        tuple: A tuple containing three lists:
            - atk_card (list): A list of attack card names (file names with 6 attributes).
            - def_card (list): A list of defense card names (file names with 3 attributes).
            - sup_card (list): A list of support card names (file names with 2 attributes).
    
    Example:
        If the file name is 'Blazing Will,1,4,2,1100,900.png', it will be categorized 
        as an attack card since it contains 6 attributes.
    """
    cur_dir = os.path.dirname(__file__)
    folder_name = '\\assets\\'
    folder_path = cur_dir + folder_name
    atk_cards = []
    def_cards = []
    sup_cards = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # if file extension is '.png' and extract card info
            if os.path.splitext(file)[1] == ".png":
                card_str = os.path.splitext(file)[0]    # take file name without extension
                # based on different number of attribute to store different card
                if len(card_str.split(',')) == 6:
                    atk_cards.append(card_str)
                elif len(card_str.split(',')) == 3:
                    def_cards.append(card_str)
                elif len(card_str.split(',')) == 2:
                    sup_cards.append(card_str)
    
    return atk_cards, def_cards, sup_cards

def display_card_list(card_list):
    var_name = [name for name, value in globals().items() if value is card_list][0]
    print('-' * 5 + f' list name: {var_name} ' + '-' * 5)
    print('-' * 5 + f'{len(card_list)} cards' + '-' * 5)
    for itr in card_list:
        print(itr)
    print('-' * 15)

def convert_to_atk_card(atk_cards):
    game_card_atk = []
    for itr in atk_cards:
        game_card_atk.append(gc.GameCard(itr))
    return game_card_atk

# test
if __name__ == "__main__":
    print('-' * 10 + ' Test ' + '-' * 10)
    
    '''
    cur_dir = os.path.dirname(__file__)
    folder_name = '\\assets\\'
    folder_path = cur_dir + folder_name
    card_atk_list = []
    card_def_list = []
    card_sup_list = []
    for root, dirs, files in os.walk(folder_path):
        #print(f'root: {root}')
        #print(f'dirs: {dirs}')
        #print(f'files: {files}')
        for file in files:
            # if file extension is '.png' and extract card info
            if os.path.splitext(file)[1] == ".png":
                card_str = os.path.splitext(file)[0]
                if len(card_str.split(',')) == 6:
                    card_atk_list.append(card_str)
                elif len(card_str.split(',')) == 3:
                    card_def_list.append(card_str)
                elif len(card_str.split(',')) == 2:
                    card_sup_list.append(card_str)
    '''
    
    card_atk_list, card_def_list, card_sup_list = load_cards_name_from_assets()
    
    '''display_card_list(card_atk_list)
    display_card_list(card_def_list)
    display_card_list(card_sup_list)'''

    game_card_atk = convert_to_atk_card(card_atk_list)
    for itr in game_card_atk:
        itr.display()
    #print(f'{len(card_atk_list)} vs {len(game_card_atk)}')
    print('-' * 10 + ' End ' + '-' * 10)

