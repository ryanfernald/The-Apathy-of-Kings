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

# test case 
class TestMoveImg:
    def __init__(self, root):
        self.root = root
        self.root.title('Image Display Test')
        self.root.geometry("1280x960")
        
        # Create a canvas 
        self.canvas = tk.Canvas(root, width=780, height=960)
        self.canvas.grid(row=0, column=0, rowspan=2, padx=10, pady=10)
        
        # **Info panel to display selected card details (Card Image and Info)**
        self.card_display_frame = tk.Frame(root, bg="lightgrey", width=480, height=720)
        self.card_display_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # **Add a label and canvas to display the card image**
        self.card_image_label = tk.Label(self.card_display_frame, text="Card Image", bg="lightgrey")
        self.card_image_label.pack()
        self.card_image_canvas = tk.Canvas(self.card_display_frame, width=480, height=720, bg="white")
        self.card_image_canvas.pack()

        # **Add text widget to display card information**
        self.card_info_text = tk.Text(self.card_display_frame, height=10, width=60)
        self.card_info_text.pack()

        # Initialize GamePlay and get card information
        game1 = GamePlay()
        game1.displayGameInfo()

        # Store the image references in separate lists
        self.hand_images = []  # For player1_hand images

        self.image_idx = []
        for itr, card in enumerate(game1.player1_hand):
            size_w, size_h = 100, 150
            # Load and resize the image for the card in player 1's hand
            img_path = card.imgPath # game1.player1_hand[0].imgPath # single card demo change to multiple
            original_image = Image.open(img_path)
            resized_image = original_image.resize((size_w, size_h), Image.LANCZOS)
            image = ImageTk.PhotoImage(resized_image)

            # Keep a reference to the image to avoid garbage collection
            self.hand_images.append(image)

            # Add the image to the canvas, staggered to make each visible
            x_position = 50 + itr * (size_w + 10)  # Stagger the cards horizontally
            y_position = 100
            image_id = self.canvas.create_image(x_position, y_position, image=image, anchor="nw")
            self.image_idx.append(image_id)

            # Bind mouse events for dragging using Helper class
            self.canvas.tag_bind(image_id, "<Button-1>", lambda event: Helper.start_drag(event))
            self.canvas.tag_bind(image_id, "<B1-Motion>", lambda event, img_id=image_id: Helper.on_drag(event, self.canvas, img_id))
            # Bind right-click to display card information
            self.canvas.tag_bind(image_id, "<Button-3>", lambda event, card=card: self.display_card_info(card))

        self.deck_images = []  # For player1_deck images
        # just an idea for deck card display
        self.deck1_idx = []
        for itr, card in enumerate(game1.player1_deck):
            size_w, size_h = 100, 150
            # Load and resize the image for the card in player 1's hand
            img_path = card.imgPath # game1.player1_hand[0].imgPath # single card demo change to multiple
            original_image = Image.open(img_path)
            resized_image = original_image.resize((size_w, size_h), Image.LANCZOS)
            image = ImageTk.PhotoImage(resized_image)

            # Keep a reference to the image to avoid garbage collection
            self.deck_images.append(image)

            # Add the image to the canvas, staggered to make each visible
            x_position = 50 + int(itr/2) * (1)  # stack all cards in deck for better visual
            y_position = 400 - itr * (1)    # replace the image with card_back image
            image_id = self.canvas.create_image(x_position, y_position, image=image, anchor="nw")
            self.deck1_idx.append(image_id)

            # Bind mouse events for dragging using Helper class
            self.canvas.tag_bind(image_id, "<Button-1>", lambda event: Helper.start_drag(event))
            self.canvas.tag_bind(image_id, "<B1-Motion>", lambda event, img_id=image_id: Helper.on_drag(event, self.canvas, img_id))
            # Bind right-click to display card information
            self.canvas.tag_bind(image_id, "<Button-3>", lambda event, card=card: self.display_card_info(card))

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
        self.card_image = ImageTk.PhotoImage(resized_image)

        # Display the image on the canvas
        self.card_image_canvas.create_image(240, 360, anchor="center", image=self.card_image)

        # Keep a reference to avoid garbage collection
        self.card_image_canvas.image = self.card_image

class Helper:
    # Static method to start the drag operation
    @staticmethod
    def start_drag(event):
        # Record the starting point of the drag
        event.widget.start_x = event.x
        event.widget.start_y = event.y

    # Static method to handle the dragging operation
    @staticmethod
    def on_drag(event, canvas, image_id):
        # Calculate the change in position
        dx = event.x - event.widget.start_x
        dy = event.y - event.widget.start_y

        # Move the image by the delta
        canvas.move(image_id, dx, dy)

        # Update the starting point to the new position
        event.widget.start_x = event.x
        event.widget.start_y = event.y

    # Static method to display card information # did not work as expected
    @staticmethod
    def display_card_info(card_image_canvas, card_info_text, game_card):
        # Clear previous information
        card_info_text.delete(1.0, tk.END)
        card_image_canvas.delete("all")

        # Display card information
        card_info = game_card.info()
        for itr in card_info:
            card_info_text.insert(tk.END, itr + '\n')

        # Load and display the card image
        img_path = game_card.imgPath
        original_image = Image.open(img_path)
        resized_image = original_image.resize((500, 750), Image.LANCZOS)
        card_image = ImageTk.PhotoImage(resized_image)

        # Display the image on the canvas
        card_image_canvas.create_image(250, 375, anchor="center", image=card_image)

        # Keep a reference to avoid garbage collection
        card_image_canvas.image = card_image 


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

'''# test case to demonstrate dragging image around
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

    root.mainloop()'''

if __name__ == "__main__":
    root = tk.Tk()
    app = TestMoveImg(root)
    root.mainloop()

    '''print('\n\n' +'-'*30 + '\n')
    show_card_list(game1.player1_hand)
    print('\n\n' +'-'*30 + '\n')
    show_card_list(game1.player2_hand)'''