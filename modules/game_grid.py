import tkinter as tk


class GameGrid:
    def __init__(self):
        # Coordinates for the card images
        self.PLAYER1, self.PLAYER2 = (180, 80), (180, 860)  # player hand starting coordinates
        self.FIELD1_DEF, self.FIELD1_ATK, self.FIELD2_ATK, self.FIELD2_DEF = (350, 235), (350, 380), (350, 560), (350, 705)
        self.CARD_SIZE = (80, 120)  # card size
        self.X_THRESHOLD = self.CARD_SIZE[0] // 2  # Distance threshold for snapping
        self.Y_THRESHOLD = self.CARD_SIZE[1] // 2  # Distance threshold for snapping
        self.DIVIDER = self.seperation_y() # y coord break players
        self.DRAGON1, self.DRAGON2 = (150, 312), (150, 627)
        self.BUTTON_TURN = (920, 470)

        # Layout of cards
        self.PLAYER1_HAND, self.PLAYER1_DECK, self.PLAYER1_ATK, self.PLAYER1_DEF = [], [], [], []
        self.PLAYER2_HAND, self.PLAYER2_DECK, self.PLAYER2_ATK, self.PLAYER2_DEF = [], [], [], []
        self.COLOR_ATK, self.COLOR_DEF = '#EB6E63', '#90EE90'

        # Run setup to initialize the grid layout
        self.layout_setup()
        # # Initialize
        self.__init_state = {
            'player1': {
                'hand': {position: None for position in self.PLAYER1_HAND},
                'deck': {self.PLAYER1_DECK[0]: []},
                'atk': {position: None for position in self.PLAYER1_ATK},
                'def': {position: None for position in self.PLAYER1_DEF}
            },
            'player2': {
                'hand': {position: None for position in self.PLAYER2_HAND},
                'deck': {self.PLAYER2_DECK[0]: []},
                'atk': {position: None for position in self.PLAYER2_ATK},
                'def': {position: None for position in self.PLAYER2_DEF}
            },
            'index': {}, 'img': {}
        } # may be move to some other class, hard to change it.
        self.setup_index()

    @property
    def info(self):
        return self.__init_state

    def setup_index(self):
        for player_key in self.__init_state:
            if player_key not in ['player1', 'player2']:
                continue  # Skip non-player keys like 'index'
            # Access player's data, i.e., hand, deck, atk, def areas
            player_data = self.__init_state[player_key]
            
            # Iterate through each area in the player's data
            for area_name, area_positions in player_data.items():
                # Add each position to the 'index' dictionary with its respective area name
                for position in area_positions.keys():
                    self.__init_state['index'][position] = area_name

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

    def canvas_reserve(self, canvas):
        coords = [self.DRAGON1, self.DRAGON2, self.BUTTON_TURN]
        for x, y in coords:
            canvas.create_rectangle(x - 10, y - 10,
                                    x + 10, y + 10,
                                    outline='black', fill='MistyRose')
    
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
        pad_x, pad_y = 40, 10    # space between cards and deck section
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

    def seperation_y(self):
        '''Let's assume upper half is player 1 and lower half is player 2'''
        return (self.FIELD1_ATK[1] + self.FIELD2_ATK[1]) / 2

    def display_area_state(self, current_state = None):
        """
        Debug function to display the current state of all areas.

        This function iterates over the state dictionary (either provided or the default __init_state)
        and prints out the status of each area (either the card present or None) for debugging purposes.

        Parameters:
        current_state (dict, optional): The state dictionary to be displayed. If None, the default __init_state is used.
        """
        if current_state == None:
            current_state = self.__init_state

        print("\n--- Current Area State ---")
        for player, areas in current_state.items():
            print(f"{player}:")
            for area_name, positions in areas.items():
                print(f"  {area_name}:")
                for position, card in positions.items():
                    if isinstance(positions, dict):  # If it is a dictionary (like hand, atk, def)
                        status = f"Occupied by {card.name}" if card else "Empty"
                        print(f"    Position {position}: {status}")
                    elif isinstance(positions, list):  # If it is a list (like deck)
                        if positions:
                            card_names = [card.name for card in positions] if positions else []
                            print(f"    Deck at position {position}: {' | '.join(card_names) if card_names else 'Empty'}")
                        else:
                            print(f"    Deck at position {position}: Empty")
        print("--- End of Area State ---\n")

    def canvas_button(self, canvas, cmd=None ,text='End Turn', offset=(0, 0), width=100, height=50):
        """
        Creates a button for end turn.
        """
        x, y = self.BUTTON_TURN
        x += offset[0]
        y += offset[1]
        
        # Create a frame to hold the button
        button_frame = tk.Frame(canvas, width=width, height=height, bg="#2C3E50", bd=0)
        button_frame.pack_propagate(False)  # Prevent frame resizing to fit contents

        # Create the button
        button = tk.Button(
            button_frame,
            text=text,
            command=cmd,
            font=("Helvetica", 12, "bold"),
            fg="white",  # Text color
            bg="#2980B9",  # Background color
            activeforeground="white",  # Text color on hover
            activebackground="#3498DB",  # Background color on hover
            relief="raised",  # Button relief style
            bd=2,  # Border width
            cursor="hand2"  # Change cursor to hand on hover
        )

        # Place the button inside the frame
        button.pack(fill=tk.BOTH, expand=True)

        # Add the frame to the canvas
        canvas.create_window(x, y, window=button_frame)


    


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
    game_grid1.canvas_reserve(canvas)

    game_grid1.display_area_state()

    #game_grid1.display_area_state()

    root.mainloop()

# For test GameGrid
if __name__ == "__main__":
    test1()

    
