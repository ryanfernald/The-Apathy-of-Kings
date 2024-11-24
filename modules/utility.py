import os
import tkinter as tk
from PIL import Image, ImageTk
from . import game_card as gc
from . import game_play as gp


def cur_dir():
    """
    Get the current directory of the file where this function is defined.

    This function returns the directory path of the current file (__file__). 
    It is useful when you need to reference files or resources that are located 
    in the same directory as this script.

    Returns:
    str: The absolute path of the directory containing the current file.
    This utility.py is in the 'modules' folder
    """
    return os.path.dirname(__file__)

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
    '''
    Debug purpose
    '''
    var_name = [name for name, value in globals().items() if value is card_list][0]
    print('-' * 5 + f' list name: {var_name} ' + '-' * 5)
    print('-' * 5 + f'{len(card_list)} cards' + '-' * 5)
    for itr, _ in card_list:
        print(itr)
    print('-' * 15)

def convert_to_atk_card(atk_cards):
    """
    Converts a list of attack card data into a list of GameCardAtk objects.
    
    Args:
        atk_cards (list): A list of tuples where each tuple contains 
                          (card info string, img_path) representing attack card data.
                          
    Returns:
        list: A list of GameCardAtk objects.
    """
    return [gc.GameCardAtk(card_info, img_path) for card_info, img_path in atk_cards]

def convert_to_def_card(def_cards):
    """
    Converts a list of attack card data into a list of GameCardDef objects.
    
    Args:
        def_cards (list): A list of tuples where each tuple contains 
                          (card info string, img_path) representing attack card data.
                          
    Returns:
        list: A list of GameCardDef objects.
    """
    return [gc.GameCardDef(card_info, img_path) for card_info, img_path in def_cards]

def convert_to_sup_card(sup_cards):
    """
    Converts a list of attack card data into a list of GameCardSup objects.
    
    Args:
        def_cards (list): A list of tuples where each tuple contains 
                          (card info string, img_path) representing attack card data.
                          
    Returns:
        list: A list of GameCardSup objects.
    """
    return [gc.GameCardSup(card_info, img_path) for card_info, img_path in sup_cards]


def load_card_back(card_size = (100, 150)):
    size_w, size_h = card_size

    img_path = cur_dir() + '\\assets\\bin\\card_back.png'
    original_image = Image.open(img_path)
    resized_image = original_image.resize((size_w, size_h), Image.LANCZOS)
    image = ImageTk.PhotoImage(resized_image)
    return image

def resize_image(imgPath, argW = 440, argH = 660, tiny_imgPath = None, **kwargs):
    """
    Resize an image and optionally add a smaller image at the top-right corner.

    This function resizes an input image to the specified width and height. Optionally,
    if a `tiny_imgPath` is provided, it will resize the second image to 1/6th of the
    specified dimensions and paste it in the top-right corner of the resized original.

    Parameters:
    imgPath (str): The file path to the original image that needs to be resized.
    argW (int): The width to which the original image will be resized. Default is 440 pixels.
    argH (int): The height to which the original image will be resized. Default is 660 pixels.
    tiny_imgPath (str, optional): The file path to an additional image that will be resized
                                  and pasted onto the top-right corner of the main image.
                                  Default is None, meaning no image will be pasted.

    Returns:
    ImageTk.PhotoImage: A Tkinter-compatible image of the resized original, with an optional smaller
                        image pasted on top. Suitable for use in Tkinter interfaces.
    """
    original_image = Image.open(imgPath)
    resized_img = original_image.resize((argW, argH), Image.LANCZOS)
    if tiny_imgPath:
        tiny_size = (int(argW / 6), int(argH / 6))
        tiny_image = Image.open(tiny_imgPath)
        tiny_resized = tiny_image.resize(tiny_size, Image.LANCZOS)
        position = (int(argW - tiny_size[0]), 0)  # Add a small padding of 10 pixels from top-right
        resized_img.paste(tiny_resized, position, mask=tiny_resized if 'A' in tiny_resized.getbands() else None)

    return ImageTk.PhotoImage(resized_img)


def resize_image_w_bg(imgPath, coord=(440, 660), player='player1'):
    """
    Resize an image and paste it onto a plain colored background, centered.

    This function resizes an image to 90% of the given dimensions and then pastes it onto 
    a plain color background of the specified width and height, with the resized image centered.
    The background color is determined based on the player parameter.

    Parameters:
    imgPath (str): The file path to the image that needs to be resized and pasted.
    argW (int): The width of the background image.
    argH (int): The height of the background image.
    player (str): The player identifier used to determine the background color ('player1', 'player2', etc.).

    Returns:
    ImageTk.PhotoImage: The resulting image, which is the original image resized and centered on a colored background.
                        This output is suitable for use in Tkinter interfaces.
    """
    # background color based on player
    bg_color = player_color(player)
    # Create the plain color background image
    background = Image.new('RGB', coord, color=bg_color)

    # Open and resize the original image
    img_size = (int(coord[0] * 0.9), int(coord[1] * 0.9))
    original_image = Image.open(imgPath)
    resized_img = original_image.resize(img_size, Image.LANCZOS)

    # Calculate the position to paste the resized image centered on the background
    img_width, img_height = img_size
    img_x = (coord[0] - img_width) // 2
    img_y = (coord[1] - img_height) // 2

    # Paste the resized image on the background
    background.paste(resized_img, (img_x, img_y), mask=resized_img if 'A' in resized_img.getbands() else None)

    return ImageTk.PhotoImage(background)

def player_color(player):
    """
    Get the RGB color associated with a given player.

    This function returns a specific RGB color based on the player identifier. It is useful
    for providing consistent colors for different players in a game.

    Parameters:
    player (str): A string representing the player identifier. Accepted values are 'player1' and 'player2'.
                  Any other value will return a default color.

    Returns:
    tuple: An (R, G, B) tuple representing the color associated with the given player.
           - For 'player1', it returns (20, 10, 180) (a shade of blue).
           - For 'player2', it returns (180, 10, 20) (a shade of red).
           - For any other value, it returns (0, 0, 0) (black).
    """
    if player == 'player1':
        return (20, 10, 180)
    elif player == 'player2':
        return (180, 10, 20)
    else:
        return (0, 0, 0)

# test
if __name__ == "__main__":
    root = tk.Tk()
    root.title('Image Display Test')
    root.geometry("600x400")  


    print('-' * 10 + ' Test ' + '-' * 10)
    
    # Create a canvas 
    root.canvas = tk.Canvas(root, width=1000, height=960)
    root.canvas.grid(row=0, column=0, rowspan=2, padx=10, pady=10)
    
    game1 = gp.GamePlay()
    card1 = game1.info['player1']['hand'][0]
    img_path = cur_dir() + '\\assets\\bin\\card_back.png'

    image = resize_image(card1.imgPath, 100, 150, img_path)
    #image = load_card_back()
    root.canvas.create_image(70, 100, image=image, anchor="nw")

    image1 = resize_image_w_bg(card1.imgPath, 100, 150)
    root.canvas.create_image(280, 100, image=image1, anchor="nw")

    image2 = resize_image_w_bg(card1.imgPath,  100, 150, 'player2')
    root.canvas.create_image(420, 100, image=image2, anchor="nw")

    print('-' * 10 + ' End ' + '-' * 10)

    root.mainloop()
