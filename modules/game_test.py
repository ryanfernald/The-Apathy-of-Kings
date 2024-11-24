import tkinter as tk
from . import game_play as gp
from . import utility as util
from . import game_grid as ggrid
from . import game_control as ctrl
from . import game_layout as glayout


# test case 
class GameTestCase:
    def __init__(self, root):
        self.top, self.bottom = 0, 960
        self.root = root
        self.root.title('Image Display Test')
        self.root.geometry(f"1500x{self.bottom}")
        
        # Create an instance of GameGrid
        self.game_grid1 = ggrid.GameGrid()
        
        # Initialize CardDisplayPanel to handle card information display
        self.card_display_panel = glayout.GameLayout(root)
        
        # Initialize GamePlay and get card information
        self.game1 = gp.GamePlay()
        # self.game1.displayGameInfo()    # message: show number of cards

        # Create a dictionary to hold player data
        self.gamestate = self.game_grid1.info
        # Declare player region
        self.player_areas = {'player1': (self.top, self.game_grid1.DIVIDER), 
                             'player2': (self.game_grid1.DIVIDER, self.bottom)}
        self.current_turn = 'player1'

        # Draw the card hands, decks, and battlefields on the canvas using the instance methods        
        self.game_grid1.canvas_layout(self.card_display_panel.canvas)
        self.game_grid1.canvas_battlefield(self.card_display_panel.canvas)
        self.game_grid1.canvas_reserve(self.card_display_panel.canvas)
        self.game_grid1.canvas_button(self.card_display_panel.canvas, cmd=lambda: print('End Turn'))
        self.game_grid1.canvas_button(
            self.card_display_panel.canvas, 
            cmd=lambda: ctrl.GameControl.display_gamestate_layout(self.gamestate),
            text='GameState',
            offset=(0, -80)
            )

        self.image_back = util.load_card_back(self.game_grid1.CARD_SIZE)

        self.setup_player_hand('player1')
        self.setup_player_hand('player2')
        self.setup_player_deck('player1')
        self.setup_player_deck('player2')

        # debug message
        # self.display_area_state()






    def set_area_access(self):
        """
        Updates the canvas to enable access to the current player's area
        and disable access to the other player's area.
        """
        for player_key, (start_y, end_y) in self.player_areas.items():
            if player_key == self.current_turn:
                # Allow access: Highlight area (example visual cue)
                self.card_display_panel.canvas.create_rectangle(0, start_y, 980, end_y, tags=f"{player_key}_area")
            else:
                # Restrict access: Disable or hide area (example visual cue)
                self.card_display_panel.canvas.create_rectangle(0, start_y, 980, end_y, tags=f"{player_key}_area")

    def end_turn(self):
        """
        Toggles the turn and updates canvas accessibility.
        """
        # Switch to the other player
        self.current_turn = 'player2' if self.current_turn == 'player1' else 'player1'
        print('current turn: ', self.current_turn)
        # Update the canvas to reflect the new turn
        self.card_display_panel.canvas.delete("player1_area")
        self.card_display_panel.canvas.delete("player2_area")
        self.set_area_access()


    def setup_player_hand(self, player_key):
        """
        Setup player hand cards with GameCard instances and store them in __init_state.

        Parameters:
        player_key (str): The player identifier ('player1' or 'player2').
        """
        
        cards = self.game1.info[player_key]['hand']

        # Get the positions for the player's hand
        hand_positions = self.game_grid1.PLAYER1_HAND if player_key == 'player1' else self.game_grid1.PLAYER2_HAND
        # Load and resize the card image
        size_w, size_h = self.game_grid1.CARD_SIZE

        for position, card in zip(hand_positions, cards):
            card.flip()
            card_image = util.resize_image_w_bg(imgPath=card.imgPath, coord=(size_w, size_h), player=player_key)

            # Add the image to the canvas and get the image_id
            x_position, y_position = position
            image_id = self.card_display_panel.canvas.create_image(
                x_position - size_w / 2, y_position - size_h / 2, image=card_image, anchor="nw"
            )
            # example of overwriting the image: 
            # self.card_display_panel.canvas.itemconfig(image_id, image=new_image)

            # Store the (GameCard, image_id) tuple in the gamestate
            self.gamestate[player_key]['hand'][position] = (card, image_id)
            self.gamestate['img'][image_id] = card_image
            # Optionally bind mouse events to the image on the canvas using image_id
            self.card_display_panel.canvas.tag_bind(
                image_id, "<Button-1>", lambda event, img_id=image_id: ctrl.GameControl.start_drag(
                    event, self.card_display_panel.canvas, img_id, self.gamestate
                )
            )
            self.card_display_panel.canvas.tag_bind(
                image_id, "<B1-Motion>", lambda event, img_id=image_id: ctrl.GameControl.on_drag(
                    event, self.card_display_panel.canvas, img_id, self.gamestate
                )
            )
            self.card_display_panel.canvas.tag_bind(
                image_id, "<ButtonRelease-1>", lambda event, img_id=image_id: ctrl.GameControl.on_release(
                    event, self.card_display_panel.canvas, img_id, self.gamestate
                )
            )
            self.card_display_panel.canvas.tag_bind(
                image_id, "<Button-3>", lambda event, card=card: self.card_display_panel.display_card_info(card)
            )

    def setup_player_deck(self, player_key):
        """
        Setup player hand cards with GameCard instances and store them in __init_state.

        Parameters:
        player_key (str): The player identifier ('player1' or 'player2').
        """
        
        cards = self.game1.info[player_key]['deck']

        # Get the positions for the player's hand
        deck_position = self.game_grid1.PLAYER1_DECK[0] if player_key == 'player1' else self.game_grid1.PLAYER2_DECK[0]
        deck_x, deck_y = deck_position
        # Load and resize the card image
        size_w, size_h = self.game_grid1.CARD_SIZE
        card_image = self.image_back

        for itr, card in enumerate(cards):
            # Add the image to the canvas, staggered to make each visible
            x_position = deck_x + int(itr / 3) * 0.5  # stack all cards in deck for better visual
            y_position = deck_y - itr * 0.5
            image_id = self.card_display_panel.canvas.create_image(
                x_position - size_w / 2, y_position - size_h / 2, image=card_image, anchor="nw"
                )
            
            self.gamestate[player_key]['deck'][deck_position].append((card, image_id))
            self.gamestate['img'][image_id] = card_image

            # # Bind left-click to check card debug info
            # self.card_display_panel.canvas.tag_bind(
            #     image_id, "<Button-1>", lambda event, img_id=image_id: ctrl.GameControl.start_drag(
            #         event, self.card_display_panel.canvas, img_id, self.gamestate
            #     )
            # ) # does not work.......why??
            # Bind double-click (left button) to turn the card over
            self.card_display_panel.canvas.tag_bind(
                image_id, "<Double-Button-1>", 
                lambda event, img_id=image_id: ctrl.GameControl.turn_card(
                    event, self.card_display_panel, img_id, self.gamestate
                    )
                )
        # print(f'{player_key} deck: {len(self.state[player_key]["deck_images"])}')

    def display_area_state(self):
        """
        Debug function to display the current state of all areas.

        This function iterates over the state dictionary and prints out the status of each area (either the card present or None) for debugging purposes.

        Parameters:
        current_state (dict, optional): The state dictionary to be displayed. If None, the default __init_state is used.
        """
        
        current_state = self.gamestate

        print("\n--- Current Area State ---")
        for player, areas in current_state.items():
            if player == 'index':
                # print(f'index: {len(self.gamestate['index'])}')
                continue
            if player == 'img':
                continue
            print(f"\nPlayer: {player}")
            for area_name, positions in areas.items():
                print(f"  Area: {area_name}")
                if isinstance(positions, dict):
                    # For areas like hand, atk, def
                    for position, card_tuple in positions.items():
                        if isinstance(card_tuple, list):
                            # For deck areas (decks are represented as a list of cards)
                            # card_descriptions = [
                            #     f"Name: {card.name}, HP: {card.hp}" if hasattr(card, 'hp') else f"Name: {card.name}"
                            #     for card, _ in card_tuple
                            # ]
                            # print(f"    Deck at position {position}: {' | '.join(card_descriptions)}")
                            print(f"    Deck at position {position}: {len(card_tuple)} cards")
                        else:
                            # For areas like hand, atk, def
                            if card_tuple:
                                card, image_id = card_tuple
                                card_description = f"Name: {card.name}, HP: {card.hp}" if hasattr(card, 'hp') else f"Name: {card.name}"
                                print(f"    Position {position}: Occupied by {card_description} (Canvas ID: {image_id})")
                            else:
                                print(f"    Position {position}: Empty")
                else:
                    print(f"  Area {area_name}: Empty")
        print("\n--- End of Area State ---\n")

    def display_gamestate_layout(self):
        """
        Debug function to display the current layout of the game state in a compact grid format.
        
        Displays an 'O' if a position is occupied by a card and 'X' if it is empty.

        Parameters:
        gamestate (dict): The game state dictionary to be displayed.
        """
        gamestate = self.gamestate
        print("\n--- Game State Layout ---")

        for player_key in ['player1', 'player2']:
            print(f"\nPlayer: {player_key}")

            # Creating a list for each area to display positions in a grid-like format
            areas_to_display = ['hand', 'atk', 'def', 'deck']
            layout = []

            # Iterate over the areas for each player to get the status ('O' or 'X')
            for area_name in areas_to_display:
                area_positions = gamestate[player_key][area_name]
                area_line = []
                area_line.append(area_name)
                if area_name == 'deck':
                    for position, card_list in area_positions.items():
                        if card_list:
                            area_line.append('O')
                        else:
                            area_line.append('X')
                else:
                    for position, card_tuple in area_positions.items():
                        if card_tuple:
                            area_line.append('O')
                        else:
                            area_line.append('X')

                layout.append(area_line)

            # Print the layout for the player
            # Assuming the layout for each area should be displayed one after the other
            for line in layout:
                print('  ' + ' '.join(line))

        print("\n--- End of Game State Layout ---\n")


if __name__ == "__main__":
    
    root = tk.Tk()
    app = GameTestCase(root)
    root.mainloop()


    
    




