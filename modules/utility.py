import os
import tkinter as tk
import game_card as gc
import game_play as gp
from PIL import Image, ImageTk




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
    folder_name = '\\assets\\cards\\'
    folder_path = cur_dir + folder_name
    atk_cards = []
    def_cards = []
    sup_cards = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # if file extension is '.png' and extract card info
            if os.path.splitext(file)[1] == ".png":
                card_str = os.path.splitext(file)[0]    # take file name without extension
                file_path = os.path.join(root, file)
                # based on different number of attribute to store different card
                if len(card_str.split(',')) == 6:
                    atk_cards.append((card_str, file_path))
                elif len(card_str.split(',')) == 3:
                    def_cards.append((card_str, file_path))
                elif len(card_str.split(',')) == 2:
                    sup_cards.append((card_str, file_path))
    
    return atk_cards, def_cards, sup_cards

def display_card_list(card_list):
    var_name = [name for name, value in globals().items() if value is card_list][0]
    print('-' * 5 + f' list name: {var_name} ' + '-' * 5)
    print('-' * 5 + f'{len(card_list)} cards' + '-' * 5)
    for itr, _ in card_list:
        print(itr)
    print('-' * 15)

def convert_to_atk_card(atk_cards):
    res = []
    for itr, img_path in atk_cards:
        res.append(gc.GameCardAtk(itr, img_path))
    return res

def convert_to_def_card(def_cards):
    res = []
    for itr, img_path in def_cards:
        res.append(gc.GameCardDef(itr, img_path))
    return res

def convert_to_sup_card(sup_cards):
    res = []
    for itr, img_path in sup_cards:
        res.append(gc.GameCardSup(itr, img_path))
    return res

def display_image(path):
    pass

def load_card_back():
    size_w, size_h = gp.GameGrid.CARD_SIZE
    img_path = 'd:\\Documents\\Code\\2024Fall\\CS122_Project\\The-Apathy-of-Kings-main\\modules\\assets\\bin\\card_back.png'
    original_image = Image.open(img_path)
    resized_image = original_image.resize((size_w, size_h), Image.LANCZOS)
    image = ImageTk.PhotoImage(resized_image)
    return image



# test
if __name__ == "__main__":
    root = tk.Tk()
    root.title('Image Display Test')
    root.geometry("600x400")  


    print('-' * 10 + ' Test ' + '-' * 10)
    
    # Create a canvas 
    root.canvas = tk.Canvas(root, width=1000, height=960)
    root.canvas.grid(row=0, column=0, rowspan=2, padx=10, pady=10)
    
    # size_w, size_h = 100, 150 # card size
    # original_image = load_card_back()
    # resized_image = original_image.resize((size_w, size_h), Image.LANCZOS)
    # image = ImageTk.PhotoImage(resized_image)
    image = load_card_back()
    root.canvas.create_image(100, 100, image=image, anchor="nw")

    print('-' * 10 + ' End ' + '-' * 10)

    root.mainloop()
