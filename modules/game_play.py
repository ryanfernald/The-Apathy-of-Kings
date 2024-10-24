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
        GameGrid.layout_setup()

        self.root = root
        self.root.title('Image Display Test')
        self.root.geometry("1500x960")
        
        # Create a canvas 
        self.canvas = tk.Canvas(root, width=1000, height=960)
        self.canvas.grid(row=0, column=0, rowspan=2, padx=10, pady=10)
        #self.canvas.create_rectangle(GameGrid.TARGET_X - GameGrid.X_THRESHOLD, GameGrid.TARGET_Y - GameGrid.Y_THRESHOLD, GameGrid.TARGET_X + GameGrid.X_THRESHOLD, GameGrid.TARGET_Y + GameGrid.Y_THRESHOLD, outline='black', fill='#ADD8E6')
        GameGrid.canvas_layout(self.canvas)
        GameGrid.canvas_battlefield(self.canvas)

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
        #game1.displayGameInfo()    # message: show number of cards

        # Store the image references in separate lists
        self.hand_images = []  # For player1_hand images

        self.image_idx = []
        for itr, card in enumerate(game1.player1_hand):
            size_w, size_h = GameGrid.CARD_SIZE
            # Load and resize the image for the card in player 1's hand
            img_path = card.imgPath # game1.player1_hand[0].imgPath # single card demo change to multiple
            original_image = Image.open(img_path)
            resized_image = original_image.resize((size_w, size_h), Image.LANCZOS)
            image = ImageTk.PhotoImage(resized_image)

            # Keep a reference to the image to avoid garbage collection
            self.hand_images.append(image)

            # Add the image to the canvas, staggered to make each visible
            # x_position = 50 + itr * (size_w + 15)  # Stagger the cards horizontally
            # y_position = 100
            x_position, y_position = GameGrid.PLAYER1_HAND[itr]
            

            image_id = self.canvas.create_image(x_position - size_w/2, y_position - size_h/2, image=image, anchor="nw")
            self.image_idx.append(image_id)

            # Bind mouse events for dragging using Helper class
            self.canvas.tag_bind(image_id, "<Button-1>", lambda event: Helper.start_drag(event))
            self.canvas.tag_bind(image_id, "<B1-Motion>", lambda event, img_id=image_id: Helper.on_drag(event, self.canvas, img_id))
            self.canvas.tag_bind(image_id, "<ButtonRelease-1>", lambda event, img_id=image_id, card=card: Helper.on_release(event, self.canvas, img_id, card))
            # Bind right-click to display card information
            self.canvas.tag_bind(
                image_id,
                "<Button-3>",
                lambda event, card=card: Helper.display_card_info(self.card_info_text, self.card_image_canvas, card)
            )   # Q: I try to take out event, but it will have issue without it. why?

        self.image_back = util.load_card_back()
        self.deck_images = []  # For player1_deck images
        self.deck_images_back = []
        # just an idea for deck card display
        self.deck1_idx = []
        for itr, card in enumerate(game1.player1_deck):
            size_w, size_h = GameGrid.CARD_SIZE
            # Load and resize the image for the card in player 1's hand
            img_path = card.imgPath # game1.player1_hand[0].imgPath # single card demo change to multiple
            original_image = Image.open(img_path)
            resized_image = original_image.resize((size_w, size_h), Image.LANCZOS)
            card_image = ImageTk.PhotoImage(resized_image)

            # Keep a reference to the image to avoid garbage collection
            self.deck_images.append(card_image)

            self.deck_images_back.append(self.image_back)

            x, y = GameGrid.PLAYER1_DECK[0]
            # Add the image to the canvas, staggered to make each visible
            x_position = x + int(itr/3) * (0.5)  # stack all cards in deck for better visual
            y_position = y - itr * (0.5)    # replace the image with card_back image
            image_id = self.canvas.create_image(x_position - size_w/2, y_position - size_h/2, image=self.image_back, anchor="nw")
            self.deck1_idx.append(image_id)

            # # Bind mouse events for dragging using Helper class
            # self.canvas.tag_bind(image_id, "<Button-1>", lambda event: Helper.start_drag(event))
            # self.canvas.tag_bind(image_id, "<B1-Motion>", lambda event, img_id=image_id: Helper.on_drag(event, self.canvas, img_id))
            # self.canvas.tag_bind(image_id, "<ButtonRelease-1>", lambda event, img_id=image_id: Helper.on_release(event, self.canvas, img_id))
            # # Bind right-click to display card information
            # self.canvas.tag_bind(
            #     image_id,
            #     "<Button-3>",
            #     lambda event, card=card: Helper.display_card_info(self.card_info_text, self.card_image_canvas, card)
            # )
            # Bind double-click (left button) to turn the card over
            self.canvas.tag_bind(image_id, "<Double-Button-1>", lambda event, card_image=card_image, img_id=image_id: Helper.turn_card(event, self.canvas, card_image, img_id, card))

class GameGrid:
    TARGET_X = 500  # Example target x-coordinate
    TARGET_Y = 500  # Example target y-coordinate
    # Coordinates to the card image 
    PLAYER1, PLAYER2 = (100, 80), (100, 860)   # player hand starting corrodinate
    FIELD1_DEF, FIELD1_ATK, FIELD2_ATK, FIELD2_DEF = (150, 235), (150, 390), (150, 550), (150, 705)
    CARD_SIZE = (100, 150)  # card size
    X_THRESHOLD = 50  # Distance threshold for snapping
    Y_THRESHOLD = 75  # Distance threshold for snapping
    PLAYER1_HAND, PLAYER1_DECK, PLAYER1_ATK, PLAYER1_DEF = [], [], [], []
    PLAYER2_HAND, PLAYER2_DECK, PLAYER2_ATK, PLAYER2_DEF = [], [], [], []
    COLOR_ATK, COLOR_DEF = '#EB6E63', '#90EE90'

    @staticmethod
    def canvas_draw(canvas):
        canvas.create_rectangle(GameGrid.TARGET_X - GameGrid.X_THRESHOLD, GameGrid.TARGET_Y - GameGrid.Y_THRESHOLD, GameGrid.TARGET_X + GameGrid.X_THRESHOLD, GameGrid.TARGET_Y + GameGrid.Y_THRESHOLD, outline='black', fill='#ADD8E6')
    @staticmethod
    def canvas_draw(canvas, x, y, fill_color = '#ADD8E6'):
        canvas.create_rectangle(x - GameGrid.X_THRESHOLD, y - GameGrid.Y_THRESHOLD, x + GameGrid.X_THRESHOLD, y + GameGrid.Y_THRESHOLD, outline='black', fill=fill_color)
    @staticmethod
    def canvas_layout(canvas):
        hand_x, hand_y = GameGrid.layout_player_section()
        for x, y in zip(hand_x, hand_y):
            GameGrid.canvas_draw(canvas, x, y)

    @staticmethod
    def canvas_battlefield(canvas):
        all = GameGrid.PLAYER1_ATK + GameGrid.PLAYER2_ATK
        hand_x = [x1 for x1, y1 in all]
        hand_y = [y1 for x1, y1 in all]
        for x, y in zip(hand_x, hand_y):
            GameGrid.canvas_draw(canvas, x, y, GameGrid.COLOR_ATK)

        all = GameGrid.PLAYER1_DEF + GameGrid.PLAYER2_DEF
        hand_x = [x1 for x1, y1 in all]
        hand_y = [y1 for x1, y1 in all]
        for x, y in zip(hand_x, hand_y):
            GameGrid.canvas_draw(canvas, x, y, GameGrid.COLOR_DEF)
    
    # get all spot into 2 list, make sure to add all spot list
    @staticmethod
    def layout_player_section():
        all = GameGrid.PLAYER1_HAND + GameGrid.PLAYER2_HAND + GameGrid.PLAYER1_DECK + GameGrid.PLAYER2_DECK
        x = [x1 for x1, y1 in all]
        y = [y1 for x1, y1 in all]
        return x, y
    @staticmethod
    def layout_player_section_no_deck():
        all = GameGrid.PLAYER1_HAND + GameGrid.PLAYER2_HAND
        x = [x1 for x1, y1 in all]
        y = [y1 for x1, y1 in all]
        return x, y
    @staticmethod
    def layout_player_def():
        all = GameGrid.PLAYER1_DEF + GameGrid.PLAYER2_DEF
        x = [x1 for x1, y1 in all]
        y = [y1 for x1, y1 in all]
        return x, y
    @staticmethod
    def layout_player_atk():
        all = GameGrid.PLAYER1_ATK + GameGrid.PLAYER2_ATK
        x = [x1 for x1, y1 in all]
        y = [y1 for x1, y1 in all]
        return x, y
    
    # must run to setup grid
    @staticmethod
    def layout_setup():
        GameGrid.layout_setup_hand()
        GameGrid.layout_setup_deck()
        GameGrid.layout_setup_battlefield()

    @staticmethod
    def layout_setup_hand():
        size_w, size_h = GameGrid.CARD_SIZE   # card size, should change upon resize window
        pad_x, pad_y = 15, 0    # space between cards
        num = 7 # number of card in hand
        GameGrid.PLAYER1_HAND = []
        x, y = GameGrid.PLAYER1
        for itr in range(num):
            temp = ((x + (size_w + pad_x) * itr), (y + pad_y * itr))
            GameGrid.PLAYER1_HAND.append(temp)
        GameGrid.PLAYER2_HAND = []
        x, y = GameGrid.PLAYER2
        for itr in range(num):
            temp = ((x + (size_w + pad_x) * itr), (y + pad_y * itr))
            GameGrid.PLAYER2_HAND.append(temp)

    # relative to player hand corrodinate
    @staticmethod
    def layout_setup_deck():
        size_w, size_h = GameGrid.CARD_SIZE   # card size, should change upon resize window
        pad_x, pad_y = 40, 20    # space between cards and deck section
        temp = ((GameGrid.PLAYER1_HAND[-1][0] + (size_w + pad_x)), (GameGrid.PLAYER1_HAND[-1][1] + pad_y))
        GameGrid.PLAYER1_DECK.append(temp)
        temp = ((GameGrid.PLAYER2_HAND[-1][0] + (size_w + pad_x)), (GameGrid.PLAYER2_HAND[-1][1] - pad_y))
        GameGrid.PLAYER2_DECK.append(temp)

    @staticmethod
    def layout_setup_battlefield():
        size_w, size_h = GameGrid.CARD_SIZE   # card size, should change upon resize window
        pad_x, pad_y = 20, 0    # space between cards
        num = 5 # number of card in hand
        GameGrid.PLAYER1_ATK = []
        x, y = GameGrid.FIELD1_ATK
        for itr in range(num):
            temp = ((x + (size_w + pad_x) * itr), (y + pad_y * itr))
            GameGrid.PLAYER1_ATK.append(temp)
        GameGrid.PLAYER1_DEF = []
        x, y = GameGrid.FIELD1_DEF
        for itr in range(num):
            temp = ((x + (size_w + pad_x) * itr), (y + pad_y * itr))
            GameGrid.PLAYER1_DEF.append(temp)
        GameGrid.PLAYER2_ATK = []
        x, y = GameGrid.FIELD2_ATK
        for itr in range(num):
            temp = ((x + (size_w + pad_x) * itr), (y + pad_y * itr))
            GameGrid.PLAYER2_ATK.append(temp)
        GameGrid.PLAYER2_DEF = []
        x, y = GameGrid.FIELD2_DEF
        for itr in range(num):
            temp = ((x + (size_w + pad_x) * itr), (y + pad_y * itr))
            GameGrid.PLAYER2_DEF.append(temp)

class Helper:
    # Add a dictionary to track whether an image is locked or not
    snapped_images = {}

    # Static method to start the drag operation
    @staticmethod
    def start_drag(event):
        # Record the starting point of the drag
        event.widget.start_x = event.x
        event.widget.start_y = event.y

    # Static method to handle the dragging operation
    @staticmethod
    def on_drag(event, canvas, image_id):
        # Bring the card being dragged to the top of the stack
        canvas.tag_raise(image_id)

        # Calculate the change in position
        dx = event.x - event.widget.start_x
        dy = event.y - event.widget.start_y

        # Move the image by the delta
        canvas.move(image_id, dx, dy)
        #print(f'({event.widget.start_x}, {event.widget.start_y})')
        # Update the starting point to the new position
        event.widget.start_x = event.x
        event.widget.start_y = event.y

    @staticmethod
    def on_release(event, canvas, image_id, card):
        # After releasing the card, check if it needs to snap to a specific position
        area = GameGrid.PLAYER1_HAND + GameGrid.PLAYER2_HAND
        if card.type == gc.CardType.ATTACK:
            area.extend(GameGrid.PLAYER1_ATK + GameGrid.PLAYER2_ATK)
        if card.type == gc.CardType.DEFENSE:
            area.extend(GameGrid.PLAYER1_DEF + GameGrid.PLAYER2_DEF)
        Helper.location_auto_lockin(canvas, image_id, area)


    @staticmethod
    def location_auto_lockin(canvas, image_id, area):
        # Get the current position of the card
        x1, y1, x2, y2 = canvas.bbox(image_id)
        card_center_x = (x1 + x2) / 2
        card_center_y = (y1 + y2) / 2

        # Find the closest area to the card's center
        closest_area = None
        min_distance = float('inf')

        for (area_x, area_y) in area:
            # Calculate the Euclidean distance from card center to each area's center
            distance = (card_center_x - area_x) ** 2 + (card_center_y - area_y) ** 2
            if distance < min_distance:
                min_distance = distance
                closest_area = (area_x, area_y)
        #if closest_area:
        if (abs(card_center_x - closest_area[0]) <= GameGrid.X_THRESHOLD * 2 and
            abs(card_center_y - closest_area[1]) <= GameGrid.Y_THRESHOLD * 2):
            # Snap the card image to the target coordinate by aligning its center
            canvas.coords(image_id, closest_area[0] - (x2 - x1)/2, closest_area[1] - (y2 - y1)/2) 


    @staticmethod
    def distance(x1, y1, x2, y2):
        return (x1 - x2) ** 2 + (y1 - y2) ** 2

    @staticmethod
    def turn_card(event, canvas, card_image, img_id, card):
        """Method to turn over the card and display the real image."""
        # Change the image of the card to the actual card image
        canvas.itemconfig(img_id, image=card_image)

        # Keep a reference to avoid garbage collection
        canvas.image = card_image

        # Bind mouse events for dragging using Helper class
        canvas.tag_bind(img_id, "<Button-1>", lambda event: Helper.start_drag(event))
        canvas.tag_bind(img_id, "<B1-Motion>", lambda event, img_id=img_id: Helper.on_drag(event, canvas, img_id))
        #canvas.tag_bind(img_id, "<ButtonRelease-1>", lambda event, img_id=img_id: Helper.on_release(event, canvas, img_id))
        canvas.tag_bind(img_id, "<ButtonRelease-1>", lambda event, img_id=img_id, card=card: Helper.on_release(event, canvas, img_id, card))
        # Bind right-click to display card information
        # canvas.tag_bind(
        #     img_id,
        #         "<Button-3>",
        #         lambda event, card=card: Helper.display_card_info(self.card_info_text, self.card_image_canvas, card)
        #     )

    # Static method to display card information # did not work as expected
    @staticmethod
    def display_card_info(card_info_text, card_image_canvas, game_card):
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
        resized_image = original_image.resize((440, 660), Image.LANCZOS)
        card_image = ImageTk.PhotoImage(resized_image)

        # Display the image on the canvas
        card_image_canvas.create_image(240, 360, anchor="center", image=card_image)

        # Keep a reference to avoid garbage collection
        card_image_canvas.image = card_image 

    # Static method to check if two card images overlap # to be test later
    @staticmethod
    def is_overlap(canvas, image_id_1, image_id_2):
        # Get the bounding box for both images
        x1, y1, x2, y2 = canvas.bbox(image_id_1)
        x3, y3, x4, y4 = canvas.bbox(image_id_2)

        # Check if the bounding boxes overlap
        if (x1 < x4 and x2 > x3 and y1 < y4 and y2 > y3):
            return True
        else:
            return False

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


    
    




