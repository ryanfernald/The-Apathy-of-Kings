import tkinter as tk
import random
from PIL import Image, ImageTk
import game_card as gc
import utility as util
import game_grid as ggrid
import time
import game_control as ctrl

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
    
    # testing purpose
    def displayGameInfo(self):
        print(f'Player 1 hand: {len(self.__player1_hand)}')
        print(f'Player 1 deck: {len(self.__player1_deck)}')
        print(f'Player 2 hand: {len(self.__player2_hand)}')
        print(f'Player 2 deck: {len(self.__player2_deck)}')

class CardDisplayPanel:
    def __init__(self, root):
        # Create a canvas 
        self.canvas = tk.Canvas(root, width=1000, height=960)
        self.canvas.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

        # Info panel to display selected card details (Card Image and Info)
        self.card_display_frame = tk.Frame(root, bg="lightgrey", width=480, height=720)
        self.card_display_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Add a label and canvas to display the card image
        self.card_image_label = tk.Label(self.card_display_frame, text="Card Image", bg="lightgrey")
        self.card_image_label.pack()
        self.card_image_canvas = tk.Canvas(self.card_display_frame, width=480, height=720, bg="white")
        self.card_image_canvas.pack()

        # Add text widget to display card information
        self.card_info_text = tk.Text(self.card_display_frame, height=10, width=60)
        self.card_info_text.pack()

        # Keep a reference for the displayed image
        self.card_image_ref = None

    def display_card_info(self, game_card):
        # Clear previous information
        self.card_info_text.delete(1.0, tk.END)
        self.card_image_canvas.delete("all")

        # Display card information
        card_info = game_card.info()
        for itr in card_info:
            self.card_info_text.insert(tk.END, itr + '\n')

        # Load and display the card image
        img_path = game_card.imgPath
        original_image = Image.open(img_path)
        resized_image = original_image.resize((440, 660), Image.LANCZOS)
        card_image = ImageTk.PhotoImage(resized_image)

        # Display the image on the canvas
        self.card_image_canvas.create_image(240, 360, anchor="center", image=card_image)

        # Keep a reference to avoid garbage collection
        self.card_image_ref = card_image
        self.card_image_canvas.image = card_image


# test case 
class TestMoveImg:
    def __init__(self, root):
        self.root = root
        self.root.title('Image Display Test')
        self.root.geometry("1500x960")
        
        # Create an instance of GameGrid
        self.game_grid1 = ggrid.GameGrid()
        
        # Initialize CardDisplayPanel to handle card information display
        self.card_display_panel = CardDisplayPanel(root)
        
        # Initialize GamePlay and get card information
        game1 = GamePlay()
        #game1.displayGameInfo()    # message: show number of cards


        # Draw the card hands, decks, and battlefields on the canvas using the instance methods        
        self.game_grid1.canvas_layout(self.card_display_panel.canvas)
        self.game_grid1.canvas_battlefield(self.card_display_panel.canvas)

        # Create a dictionary to hold player data
        self.players = {
            "player1": {
                "hand_images": [],
                "deck_images": [],
                "deck_images_back": [],
                "image_idx": []
            },
            "player2": {
                "hand_images": [],
                "deck_images": [],
                "deck_images_back": [],
                "image_idx": []
            }
        }

        # Setup player 1 cards
        self.setup_player_cards(game1.player1_hand, "player1", self.game_grid1.PLAYER1_HAND, self.game_grid1.PLAYER1_DECK)

        # Setup player 2 cards (repeat similar setup for player 2)
        self.setup_player_cards(game1.player2_hand, "player2", self.game_grid1.PLAYER2_HAND, self.game_grid1.PLAYER2_DECK)

    def setup_player_cards(self, hand, player_key, hand_positions, deck_positions):
        size_w, size_h = self.game_grid1.CARD_SIZE
        
        # Setup hand cards
        for itr, card in enumerate(hand):
            # Load and resize the image for the card in the player's hand
            img_path = card.imgPath
            original_image = Image.open(img_path)
            resized_image = original_image.resize((size_w, size_h), Image.LANCZOS)
            image = ImageTk.PhotoImage(resized_image)

            # Keep a reference to the image to avoid garbage collection
            self.players[player_key]["hand_images"].append(image)

            # Add the image to the canvas
            x_position, y_position = hand_positions[itr]
            image_id = self.card_display_panel.canvas.create_image(x_position - size_w / 2, y_position - size_h / 2, image=image, anchor="nw")
            self.players[player_key]["image_idx"].append(image_id)

            # Bind mouse events for dragging using GameControl class
            self.card_display_panel.canvas.tag_bind(image_id, "<Button-1>", lambda event, img_id=image_id: ctrl.GameControl.start_drag(event, self.card_display_panel.canvas, img_id))
            self.card_display_panel.canvas.tag_bind(image_id, "<B1-Motion>", lambda event, img_id=image_id: ctrl.GameControl.on_drag(event, self.card_display_panel.canvas, img_id))
            self.card_display_panel.canvas.tag_bind(image_id, "<ButtonRelease-1>", lambda event, img_id=image_id, card=card: ctrl.GameControl.on_release(event, self.card_display_panel.canvas, img_id, card))
            # Bind right-click to display card information
            self.card_display_panel.canvas.tag_bind(image_id, "<Button-3>", lambda event, card=card: self.card_display_panel.display_card_info(card))

        # Setup deck cards (just an idea for deck card display)
        image_back = util.load_card_back(self.game_grid1.CARD_SIZE)
        for itr, card in enumerate(hand):
            # Load and resize the image for the card in the player's deck
            img_path = card.imgPath
            original_image = Image.open(img_path)
            resized_image = original_image.resize((size_w, size_h), Image.LANCZOS)
            card_image = ImageTk.PhotoImage(resized_image)

            # Keep a reference to the image to avoid garbage collection
            self.players[player_key]["deck_images"].append(card_image)
            self.players[player_key]["deck_images_back"].append(image_back)

            x, y = deck_positions[0]
            # Add the image to the canvas, staggered to make each visible
            x_position = x + int(itr / 3) * 0.5  # stack all cards in deck for better visual
            y_position = y - itr * 0.5
            image_id = self.card_display_panel.canvas.create_image(x_position - size_w / 2, y_position - size_h / 2, image=image_back, anchor="nw")
            self.players[player_key]["image_idx"].append(image_id)

            # Bind double-click (left button) to turn the card over
            self.card_display_panel.canvas.tag_bind(image_id, "<Double-Button-1>", lambda event, card_image=card_image, img_id=image_id: ctrl.GameControl.turn_card(event, self.card_display_panel.canvas, self.card_display_panel, card_image, img_id, card))



def show_card_list(arg):
    for itr in arg:
        itr.display()



if __name__ == "__main__":
    
    root = tk.Tk()
    app = TestMoveImg(root)
    root.mainloop()


    
    




