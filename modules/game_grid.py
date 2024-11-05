import tkinter as tk
import random
from PIL import Image, ImageTk
import game_card as gc
import utility as util


class GameGrid:
    def __init__(self):
        # Coordinates for the card images
        self.PLAYER1, self.PLAYER2 = (100, 80), (100, 860)  # player hand starting coordinates
        self.FIELD1_DEF, self.FIELD1_ATK, self.FIELD2_ATK, self.FIELD2_DEF = (150, 235), (150, 390), (150, 550), (150, 705)
        self.CARD_SIZE = (100, 150)  # card size
        self.X_THRESHOLD = 50  # Distance threshold for snapping
        self.Y_THRESHOLD = 75  # Distance threshold for snapping
        self.DIVIDER = self.seperation_y() # y coord break players

        # Layout of cards
        self.PLAYER1_HAND, self.PLAYER1_DECK, self.PLAYER1_ATK, self.PLAYER1_DEF = [], [], [], []
        self.PLAYER2_HAND, self.PLAYER2_DECK, self.PLAYER2_ATK, self.PLAYER2_DEF = [], [], [], []
        self.COLOR_ATK, self.COLOR_DEF = '#EB6E63', '#90EE90'

        # Occupancy tracking
        self.area_state = {
            "player1_hand": {},
            "player2_hand": {},
            "player1_deck": {},
            "player2_deck": {},
            "player1_atk": {},
            "player1_def": {},
            "player2_atk": {},
            "player2_def": {}
        }

        # Run setup to initialize the grid layout
        self.layout_setup()


    def canvas_draw(self, canvas, x=None, y=None, fill_color='#ADD8E6'):
        if x is None and y is None:
            pass
        else:
            canvas.create_rectangle(x - self.X_THRESHOLD, y - self.Y_THRESHOLD,
                                    x + self.X_THRESHOLD, y + self.Y_THRESHOLD,
                                    outline='black', fill=fill_color)
            
    def canvas_layout(self, canvas):
        hand_x, hand_y = self.layout_player_section()
        for x, y in zip(hand_x, hand_y):
            self.canvas_draw(canvas, x, y)

    def canvas_battlefield(self, canvas):
        all = self.PLAYER1_ATK + self.PLAYER2_ATK
        hand_x = [x1 for x1, _ in all]
        hand_y = [y1 for _, y1 in all]
        for x, y in zip(hand_x, hand_y):
            self.canvas_draw(canvas, x, y, self.COLOR_ATK)

        all = self.PLAYER1_DEF + self.PLAYER2_DEF
        hand_x = [x1 for x1, _ in all]
        hand_y = [y1 for _, y1 in all]
        for x, y in zip(hand_x, hand_y):
            self.canvas_draw(canvas, x, y, self.COLOR_DEF)
    
    # get all spot into 2 list, make sure to add all spot list
    def layout_player_section(self):
        all = self.PLAYER1_HAND + self.PLAYER2_HAND + self.PLAYER1_DECK + self.PLAYER2_DECK
        x = [x1 for x1, _ in all]
        y = [y1 for _, y1 in all]
        return x, y
    def layout_player_section_no_deck(self):
        all = self.PLAYER1_HAND + self.PLAYER2_HAND
        x = [x1 for x1, _ in all]
        y = [y1 for _, y1 in all]
        return x, y
    def layout_player_def(self):
        all = self.PLAYER1_DEF + self.PLAYER2_DEF
        x = [x1 for x1, _ in all]
        y = [y1 for _, y1 in all]
        return x, y
    def layout_player_atk(self):
        all = self.PLAYER1_ATK + self.PLAYER2_ATK
        x = [x1 for x1, _ in all]
        y = [y1 for _, y1 in all]
        return x, y
    
    # must run to setup grid
    def layout_setup(self):
        # Initialize the layouts
        self.layout_setup_hand()
        self.layout_setup_deck()
        self.layout_setup_battlefield()

        # Initialize occupied spaces as False for each position in the respective areas
        self.area_state = {
            "player1_hand": {position: False for position in self.PLAYER1_HAND},
            "player2_hand": {position: False for position in self.PLAYER2_HAND},
            "player1_deck": {position: False for position in self.PLAYER1_DECK},
            "player2_deck": {position: False for position in self.PLAYER2_DECK},
            "player1_atk": {position: False for position in self.PLAYER1_ATK},
            "player1_def": {position: False for position in self.PLAYER1_DEF},
            "player2_atk": {position: False for position in self.PLAYER2_ATK},
            "player2_def": {position: False for position in self.PLAYER2_DEF},
        }

    def layout_setup_hand(self):
        size_w, size_h = self.CARD_SIZE   # card size, should change upon resize window
        pad_x, pad_y = 15, 0    # space between cards
        num = 7 # number of card in hand

        self.PLAYER1_HAND = []
        x, y = self.PLAYER1
        for itr in range(num):
            temp = ((x + (size_w + pad_x) * itr), (y + pad_y * itr))
            self.PLAYER1_HAND.append(temp)

        self.PLAYER2_HAND = []
        x, y = self.PLAYER2
        for itr in range(num):
            temp = ((x + (size_w + pad_x) * itr), (y + pad_y * itr))
            self.PLAYER2_HAND.append(temp)

    # relative to player hand corrodinate
    def layout_setup_deck(self):
        size_w, size_h = self.CARD_SIZE   # card size, should change upon resize window
        pad_x, pad_y = 40, 20    # space between cards and deck section
        temp = ((self.PLAYER1_HAND[-1][0] + (size_w + pad_x)), (self.PLAYER1_HAND[-1][1] + pad_y))
        self.PLAYER1_DECK.append(temp)
        temp = ((self.PLAYER2_HAND[-1][0] + (size_w + pad_x)), (self.PLAYER2_HAND[-1][1] - pad_y))
        self.PLAYER2_DECK.append(temp)

    def layout_setup_battlefield(self):
        size_w, size_h = self.CARD_SIZE   # card size, should change upon resize window
        pad_x, pad_y = 20, 0    # space between cards
        num = 5 # number of card in hand
        self.PLAYER1_ATK = []
        x, y = self.FIELD1_ATK
        for itr in range(num):
            temp = ((x + (size_w + pad_x) * itr), (y + pad_y * itr))
            self.PLAYER1_ATK.append(temp)
        self.PLAYER1_DEF = []
        x, y = self.FIELD1_DEF
        for itr in range(num):
            temp = ((x + (size_w + pad_x) * itr), (y + pad_y * itr))
            self.PLAYER1_DEF.append(temp)
        self.PLAYER2_ATK = []
        x, y = self.FIELD2_ATK
        for itr in range(num):
            temp = ((x + (size_w + pad_x) * itr), (y + pad_y * itr))
            self.PLAYER2_ATK.append(temp)
        self.PLAYER2_DEF = []
        x, y = self.FIELD2_DEF
        for itr in range(num):
            temp = ((x + (size_w + pad_x) * itr), (y + pad_y * itr))
            self.PLAYER2_DEF.append(temp)

    def display_area_state(self):
        """Display the current state of all areas."""
        for area, positions in self.area_state.items():
            print(f"{area}:")
            for position, occupied in positions.items():
                status = "Occupied" if occupied else "Empty"
                print(f"  Position {position}: {status}")

    def seperation_y(self):
        '''Let's assume upper half is player 1 and lower half is player 2'''
        return (self.FIELD1_ATK[1] + self.FIELD2_ATK[1]) / 2

def test1():
    root = tk.Tk()
    root.title('GameGrid Layout Test')
    root.geometry("1600x960")

    # Create a canvas to draw the grid
    canvas = tk.Canvas(root, width=1000, height=960, bg="#f2f6fc")
    canvas.pack(padx=10, pady=10)

    # Create an instance of GameGrid
    game_grid1 = GameGrid()
    #print(game_grid1.OCCUPIED_SPACES)
    #print(len(game_grid1.OCCUPIED_SPACES))

    # Draw the card hands, decks, and battlefields on the canvas
    game_grid1.canvas_layout(canvas)
    game_grid1.canvas_battlefield(canvas)

    #game_grid1.display_area_state()

    root.mainloop()

# For test GameGrid
if __name__ == "__main__":
    test1()

    
