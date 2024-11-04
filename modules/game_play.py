import tkinter as tk
import random
from PIL import Image, ImageTk
import game_card as gc
import utility as util
import game_grid as ggrid

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
        # Create an instance of GameGrid
        self.game_grid1 = ggrid.GameGrid()

        self.root = root
        self.root.title('Image Display Test')
        self.root.geometry("1500x960")
        
        # Create a canvas 
        self.canvas = tk.Canvas(root, width=1000, height=960)
        self.canvas.grid(row=0, column=0, rowspan=2, padx=10, pady=10)
        #self.canvas.create_rectangle(GameGrid.TARGET_X - GameGrid.X_THRESHOLD, GameGrid.TARGET_Y - GameGrid.Y_THRESHOLD, GameGrid.TARGET_X + GameGrid.X_THRESHOLD, GameGrid.TARGET_Y + GameGrid.Y_THRESHOLD, outline='black', fill='#ADD8E6')
        self.game_grid1.canvas_layout(self.canvas)
        self.game_grid1.canvas_battlefield(self.canvas)

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
            size_w, size_h = self.game_grid1.CARD_SIZE
            # Load and resize the image for the card in player 1's hand
            img_path = card.imgPath # game1.player1_hand[0].imgPath # single card demo change to multiple
            original_image = Image.open(img_path)
            resized_image = original_image.resize((size_w, size_h), Image.LANCZOS)
            image = ImageTk.PhotoImage(resized_image)

            # Keep a reference to the image to avoid garbage collection
            self.hand_images.append(image)

            # Add the image to the canvas
            x_position, y_position = self.game_grid1.PLAYER1_HAND[itr]
            

            image_id = self.canvas.create_image(x_position - size_w/2, y_position - size_h/2, image=image, anchor="nw")
            self.image_idx.append(image_id)

            # Bind mouse events for dragging using Helper class
            self.canvas.tag_bind(image_id, "<Button-1>", lambda event, img_id=image_id: GameControl.start_drag(event, self.canvas, img_id))
            self.canvas.tag_bind(image_id, "<B1-Motion>", lambda event, img_id=image_id: GameControl.on_drag(event, self.canvas, img_id))
            self.canvas.tag_bind(image_id, "<ButtonRelease-1>", lambda event, img_id=image_id, card=card: GameControl.on_release(event, self.canvas, img_id, card))
            # Bind right-click to display card information
            self.canvas.tag_bind(
                image_id,
                "<Button-3>",
                lambda event, card=card: GameControl.display_card_info(self.card_info_text, self.card_image_canvas, card)
            )   # Q: I try to take out event, but it will have issue without it. why?

        self.image_back = util.load_card_back(self.game_grid1.CARD_SIZE)
        self.deck_images = []  # For player1_deck images
        self.deck_images_back = []
        # just an idea for deck card display
        self.deck1_idx = []
        for itr, card in enumerate(game1.player1_deck):
            size_w, size_h = self.game_grid1.CARD_SIZE
            # Load and resize the image for the card in player 1's hand
            img_path = card.imgPath # game1.player1_hand[0].imgPath # single card demo change to multiple
            original_image = Image.open(img_path)
            resized_image = original_image.resize((size_w, size_h), Image.LANCZOS)
            card_image = ImageTk.PhotoImage(resized_image)

            # Keep a reference to the image to avoid garbage collection
            self.deck_images.append(card_image)

            self.deck_images_back.append(self.image_back)

            x, y = self.game_grid1.PLAYER1_DECK[0]
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
            self.canvas.tag_bind(image_id, "<Double-Button-1>", lambda event, card_image=card_image, img_id=image_id: GameControl.turn_card(event, self.canvas, card_image, img_id, card))


class GameControl:
    
    ORIGINAL_LOC = (0, 0)

    # Static method to start the drag operation
    @staticmethod
    def start_drag(event, canvas, image_id):
        # Record the starting point of the drag
        GameControl.ORIGINAL_LOC = canvas.coords(image_id)
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
        area = ggrid.GameGrid().PLAYER1_HAND + ggrid.GameGrid().PLAYER2_HAND
        if card.type == gc.CardType.ATTACK:
            area.extend(ggrid.GameGrid().PLAYER1_ATK + ggrid.GameGrid().PLAYER2_ATK)
        if card.type == gc.CardType.DEFENSE:
            area.extend(ggrid.GameGrid().PLAYER1_DEF + ggrid.GameGrid().PLAYER2_DEF)
        if not GameControl.location_auto_lockin(canvas, image_id, area):
            original_x, original_y = GameControl.ORIGINAL_LOC
            canvas.coords(image_id, original_x, original_y)


    @staticmethod
    def location_auto_lockin(canvas, image_id, area):
        # Get the current position of the card
        card_center_x, card_center_y, width, height = GameControl.get_card_center(canvas, image_id)

        # Find the closest area to the card's center
        closest_area = GameControl.find_closest_area(card_center_x, card_center_y, area)

        # If the card should snap to the closest area, align it
        return GameControl.snap_to_closest_area(canvas, image_id, card_center_x, card_center_y, closest_area, width, height)


    @staticmethod
    def get_card_center(canvas, image_id):
        """Get the current position and size of the card."""
        x1, y1, x2, y2 = canvas.bbox(image_id)
        card_center_x = (x1 + x2) / 2
        card_center_y = (y1 + y2) / 2
        width = x2 - x1
        height = y2 - y1
        return card_center_x, card_center_y, width, height


    @staticmethod
    def find_closest_area(card_center_x, card_center_y, area):
        """Find the closest area to the card's current center."""
        closest_area = None
        min_distance = float('inf')

        for (area_x, area_y) in area:
            # Calculate the Euclidean distance from card center to each area's center
            distance = (card_center_x - area_x) ** 2 + (card_center_y - area_y) ** 2
            if distance < min_distance:
                min_distance = distance
                closest_area = (area_x, area_y)
        
        return closest_area


    @staticmethod
    def snap_to_closest_area(canvas, image_id, card_center_x, card_center_y, closest_area, width, height):
        """Snap the card to the closest area if within the threshold distance."""
        if (closest_area and
                abs(card_center_x - closest_area[0]) <= ggrid.GameGrid().X_THRESHOLD * 2 and
                abs(card_center_y - closest_area[1]) <= ggrid.GameGrid().Y_THRESHOLD * 2):
            # Snap the card image to the target coordinate by aligning its center
            canvas.coords(image_id, closest_area[0] - width / 2, closest_area[1] - height / 2)
            return True
        return False

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
        canvas.tag_bind(img_id, "<Button-1>", lambda event, img_id=img_id: GameControl.start_drag(event, canvas, img_id))
        canvas.tag_bind(img_id, "<B1-Motion>", lambda event, img_id=img_id: GameControl.on_drag(event, canvas, img_id))
        #canvas.tag_bind(img_id, "<ButtonRelease-1>", lambda event, img_id=img_id: Helper.on_release(event, canvas, img_id))
        canvas.tag_bind(img_id, "<ButtonRelease-1>", lambda event, img_id=img_id, card=card: GameControl.on_release(event, canvas, img_id, card))
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



if __name__ == "__main__":
    
    root = tk.Tk()
    app = TestMoveImg(root)
    root.mainloop()


    
    




