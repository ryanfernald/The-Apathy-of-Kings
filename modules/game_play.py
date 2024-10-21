import tkinter as tk
import random
from PIL import Image, ImageTk
import game_card as gc
import utility as util

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

class ImageMoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Image Display Test')
        self.root.geometry("600x400")
        
        # Create a canvas
        self.canvas = tk.Canvas(root, width=600, height=400)
        self.canvas.pack()
        
        # Initialize GamePlay and get card information
        game1 = GamePlay()
        game1.displayGameInfo()

        # Load and resize the image for the card in player 1's hand
        img_path = game1.player1_hand[0].imgPath
        original_image = Image.open(img_path)
        resized_image = original_image.resize((160, 240), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(resized_image)

        # Keep a reference to the image to avoid garbage collection
        self.root.image = self.image

        # Add the image to the canvas
        self.image_id = self.canvas.create_image(100, 100, image=self.image, anchor="nw")

        # Bind mouse events for dragging
        self.canvas.tag_bind(self.image_id, "<Button-1>", self.start_drag)
        self.canvas.tag_bind(self.image_id, "<B1-Motion>", self.on_drag)

    def start_drag(self, event):
        # Record the starting point of the drag
        self.start_x = event.x
        self.start_y = event.y

    def on_drag(self, event):
        # Calculate the change in position
        dx = event.x - self.start_x
        dy = event.y - self.start_y

        # Move the image by the delta
        self.canvas.move(self.image_id, dx, dy)

        # Update the starting point to the new position
        self.start_x = event.x
        self.start_y = event.y

def show_card_list(arg):
    for itr in arg:
        itr.display()

'''# test case
if __name__ == "__main__":
    root = tk.Tk()
    root.title('Image Display Test')
    root.geometry("600x400")
    
    canvas = tk.Canvas(root, width=600, height=400)
    canvas.pack()
    
    game1 = GamePlay()
    game1.displayGameInfo()

    
    image = Image.open(game1.player1_hand[0].imgPath)
    resized_image = image.resize((150, 220), Image.LANCZOS)
    image = ImageTk.PhotoImage(resized_image)

    
    canvas.create_image(200, 200, image=image)

    

    
    app = ImageMoverApp(root)
    root.mainloop()
'''

# test case to demonstrate dragging image around
if __name__ == "__main__":
    root = tk.Tk()
    root.title('Image Display Test')
    root.geometry("600x400")
    
    # Create a canvas to display the image
    canvas = tk.Canvas(root, width=600, height=400)
    canvas.pack()
    
    # Initialize GamePlay and get card information
    game1 = GamePlay()
    game1.displayGameInfo()

    # Load and resize the image for the card in player 1's hand
    img_path = game1.player1_hand[0].imgPath
    original_image = Image.open(img_path)
    resized_image = original_image.resize((150, 220), Image.LANCZOS)
    image = ImageTk.PhotoImage(resized_image)

    # Keep a reference to the image to avoid garbage collection
    root.image = image

    # Create an image on the canvas
    image_id = canvas.create_image(200, 200, image=image, anchor="nw")

    # Functions for dragging the image
    def start_drag(event):
        # Record the starting point of the drag
        start_drag.start_x = event.x
        start_drag.start_y = event.y

    def on_drag(event):
        # Calculate the change in position
        dx = event.x - start_drag.start_x
        dy = event.y - start_drag.start_y

        # Move the image by the delta
        canvas.move(image_id, dx, dy)

        # Update the starting point to the new position
        start_drag.start_x = event.x
        start_drag.start_y = event.y

    # Bind mouse events for dragging the image
    canvas.tag_bind(image_id, "<Button-1>", start_drag)
    canvas.tag_bind(image_id, "<B1-Motion>", on_drag)

    root.mainloop()



    print('\n\n' +'-'*30 + '\n')
    show_card_list(game1.player1_hand)
    print('\n\n' +'-'*30 + '\n')
    show_card_list(game1.player2_hand)