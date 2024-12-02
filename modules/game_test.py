import tkinter as tk
from . import game_play as gp
from . import utility as util
from . import game_grid as ggrid
from . import game_control as ctrl
from . import game_layout as glayout
from . import game_card as gc

# test case 
class TheApathyofKings:
    def __init__(self, root):
        self.top, self.bottom = 0, 960
        self.root = root
        self.root.title('The Apathy of Kings')
        self.root.geometry(f"1500x{self.bottom}")
        
        # Create an instance of GameGrid
        self.game_grid1 = ggrid.GameGrid()
        
        # Initialize CardDisplayPanel to handle card information display
        self.card_display_panel = glayout.GameLayout(root, self.game_grid1)
        
        # Initialize GamePlay and get card information
        self.game1 = gp.GamePlay()
        # self.game1.displayGameInfo()    # message: show number of cards

        # Create a dictionary to hold player data
        self.gamestate = self.game_grid1.info
        # self.player_img_id = {'player1': [], 'player2': []}

        self.current_turn = 'player1'

        # Draw the card hands, decks, and battlefields on the canvas using the instance methods        
        # self.game_grid1.canvas_layout(self.card_display_panel.canvas)
        # self.game_grid1.canvas_battlefield(self.card_display_panel.canvas)
        # self.game_grid1.canvas_reserve(self.card_display_panel.canvas)

        # Assign dragons to the gamestate
        self.gamestate['player1']['dragon'] = self.game1.info['player1']['dragon']
        self.gamestate['player2']['dragon'] = self.game1.info['player2']['dragon']

        # Add dragon coordinates to the gamestate index for lookups
        self.gamestate['index'][self.game_grid1.DRAGON1] = 'dragon1'
        self.gamestate['index'][self.game_grid1.DRAGON2] = 'dragon2'


        # Display and bind interactions for Player 1's dragon
        if self.gamestate['player1']['dragon']:
            # print(f"Adding Player 1's dragon {self.gamestate['player1']['dragon'].name} to canvas and binding interactions.")
            self.game_grid1.display_dragons(self.card_display_panel.canvas, self.gamestate)
            ctrl.GameControl.bind_dragon_interactions(
                self.card_display_panel.canvas, self.gamestate['player1']['dragon'], self.card_display_panel
            )

        # Display and bind interactions for Player 2's dragon
        if self.gamestate['player2']['dragon']:
            # print(f"Adding Player 2's dragon {self.gamestate['player2']['dragon'].name} to canvas and binding interactions.")
            self.game_grid1.display_dragons(self.card_display_panel.canvas, self.gamestate)
            ctrl.GameControl.bind_dragon_interactions(
                self.card_display_panel.canvas, self.gamestate['player2']['dragon'], self.card_display_panel
            )
            
        # Assign dragons to the gamestate
        self.gamestate['player1']['dragon'] = self.game1.info['player1']['dragon']
        self.gamestate['player2']['dragon'] = self.game1.info['player2']['dragon']

        # Add dragon coordinates to the gamestate index for lookups
        self.gamestate['index'][self.game_grid1.DRAGON1] = 'dragon1'
        self.gamestate['index'][self.game_grid1.DRAGON2] = 'dragon2'


        # Display and bind interactions for Player 1's dragon
        if self.gamestate['player1']['dragon']:
            # print(f"Adding Player 1's dragon {self.gamestate['player1']['dragon'].name} to canvas and binding interactions.")
            self.game_grid1.display_dragons(self.card_display_panel.canvas, self.gamestate)
            ctrl.GameControl.bind_dragon_interactions(
                self.card_display_panel.canvas, self.gamestate['player1']['dragon'], self.card_display_panel
            )

        # Display and bind interactions for Player 2's dragon
        if self.gamestate['player2']['dragon']:
            # print(f"Adding Player 2's dragon {self.gamestate['player2']['dragon'].name} to canvas and binding interactions.")
            self.game_grid1.display_dragons(self.card_display_panel.canvas, self.gamestate)
            ctrl.GameControl.bind_dragon_interactions(
                self.card_display_panel.canvas, self.gamestate['player2']['dragon'], self.card_display_panel
            )



        self.game_grid1.canvas_button(self.card_display_panel.canvas, cmd=lambda: self.toggle_color)

        
        # self.game_grid1.canvas_button(
        #     self.card_display_panel.canvas, 
        #     cmd=lambda: ctrl.GameControl.display_gamestate_layout(self.gamestate),
        #     text='GameState',
        #     offset=(0, -80)
        #     )

        # end turn button
        self.button_end_turn = self.game_grid1.canvas_button(self.card_display_panel.canvas, cmd=self.end_turn, color='#140AB4')
        
        # debug button
        # self.game_grid1.canvas_button(
        #     self.card_display_panel.canvas, 
        #     cmd=self.debug_info,
        #     text='Debug',
        #     offset=(0, 80)
        #     )

        self.image_back = util.load_card_back(self.game_grid1.CARD_SIZE)

        # Render dragons on the canvas
        self.game_grid1.display_dragons(self.card_display_panel.canvas, self.game1.info)

        self.setup_player_hand('player1')
        self.setup_player_deck('player1')
        self.setup_player_hand('player2')
        self.setup_player_deck('player2')

        # self.reassign_action_by_location()
        self.reassign_action()
        # debug message
        # self.display_area_state()







    def end_turn(self):
        """
        End turn mechanism
        """
        # Switch to the other player
        self.current_turn = 'player1' if self.current_turn == 'player2' else 'player2'
        print('current turn: ', self.current_turn)
        # Update the canvas to reflect the new turn
        colors = {'player1': '#382df3', 'player2': '#f32d38'}
        self.button_end_turn.config(
            bg=colors[self.current_turn],
            text=f"End {self.current_turn.capitalize()}'s Turn"  # Dynamically update text
        )

        ## big step for this game
        # self.reassign_action_by_location()
        self.reassign_action()

    def reassign_action(self):
        opponent = 'player1' if self.current_turn == 'player2' else 'player2'
        # set proper action for current player
        for img_id in self.gamestate['img_id'][self.current_turn]:
            ctrl.GameControl.action_by_card_view(self.gamestate, self.card_display_panel, img_id)
        # disable opponent action
        for img_id in self.gamestate['img_id'][opponent]:
            ctrl.GameControl.action_card_disable(self.gamestate, self.card_display_panel, img_id)
    
    ## helper function for debug
    def reassign_action_by_location(self):
        '''reassign card action based on the card location'''
        opponent = 'player1' if self.current_turn == 'player2' else 'player2'
        for area_itr in self.gamestate[self.current_turn]:
            if area_itr == 'deck':
                for coord in self.gamestate[self.current_turn][area_itr]:
                    for card_info in self.gamestate[self.current_turn][area_itr][coord]:
                        # print(card_info[0].view, card_info[1])
                        ctrl.GameControl.action_card_disable(self.gamestate, self.card_display_panel, card_info[1])
                        ctrl.GameControl.action_card_back(self.gamestate, self.card_display_panel, card_info[1])
            else:
                for coord in self.gamestate[self.current_turn][area_itr]:
                    if self.gamestate[self.current_turn][area_itr][coord]:
                        # print(self.gamestate[self.current_turn][area_itr][coord][0].view, self.gamestate[self.current_turn][area_itr][coord][1])
                        ctrl.GameControl.action_card_disable(self.gamestate, self.card_display_panel, self.gamestate[self.current_turn][area_itr][coord][1])
                        ctrl.GameControl.action_card_front(self.gamestate, self.card_display_panel, self.gamestate[self.current_turn][area_itr][coord][1])
        
        print(opponent)
        for area_itr in self.gamestate[opponent]:
            print(area_itr)
            if area_itr == 'deck':
                for coord in self.gamestate[opponent][area_itr]:
                    for card_info in self.gamestate[opponent][area_itr][coord]:
                        # print(card_info[0].view, card_info[1])
                        ctrl.GameControl.action_card_disable(self.gamestate, self.card_display_panel, card_info[1])
                        ctrl.GameControl.action_card_back(self.gamestate, self.card_display_panel, card_info[1])
            else:
                for coord in self.gamestate[opponent][area_itr]:
                    if self.gamestate[opponent][area_itr][coord]:
                        # print(self.gamestate[opponent][area_itr][coord][0].view, self.gamestate[opponent][area_itr][coord][1])
                        ctrl.GameControl.action_card_disable(self.gamestate, self.card_display_panel, self.gamestate[opponent][area_itr][coord][1])
                        ctrl.GameControl.action_card_front(self.gamestate, self.card_display_panel, self.gamestate[opponent][area_itr][coord][1])
    
    ## helper function for debug
    def card_view_correction(self):
        opponent = 'player1' if self.current_turn == 'player2' else 'player2'
        for area_itr in self.gamestate[self.current_turn]:
            if area_itr == 'deck':
                for coord in self.gamestate[self.current_turn][area_itr]:
                    for card_info in self.gamestate[self.current_turn][area_itr][coord]:
                        # print(card_info[0].view, card_info[1])
                        card_info[0].view = gc.CardView.BACK

            else:
                for coord in self.gamestate[self.current_turn][area_itr]:
                    if self.gamestate[self.current_turn][area_itr][coord]:
                        # print(self.gamestate[self.current_turn][area_itr][coord][0].view, self.gamestate[self.current_turn][area_itr][coord][1])
                        self.gamestate[self.current_turn][area_itr][coord][0].view = gc.CardView.FRONT
        
        for area_itr in self.gamestate[opponent]:
            if area_itr == 'deck':
                for coord in self.gamestate[opponent][area_itr]:
                    for card_info in self.gamestate[opponent][area_itr][coord]:
                        # print(card_info[0].view, card_info[1])
                        card_info[0].view = gc.CardView.BACK
            else:
                for coord in self.gamestate[opponent][area_itr]:
                    if self.gamestate[opponent][area_itr][coord]:
                        # print(self.gamestate[opponent][area_itr][coord][0].view, self.gamestate[opponent][area_itr][coord][1])
                        self.gamestate[opponent][area_itr][coord][0].view = gc.CardView.FRONT

    ## helper function for debug
    def debug_display_card_info(self):
        opponent = 'player1' if self.current_turn == 'player2' else 'player2'
        print(self.current_turn)
        for area_itr in self.gamestate[self.current_turn]:
            print(area_itr)
            if area_itr == 'deck':
                for coord in self.gamestate[self.current_turn][area_itr]:
                    print(type(self.gamestate[self.current_turn][area_itr][coord]))
                    for card_info in self.gamestate[self.current_turn][area_itr][coord]:
                        print(card_info[0].view, card_info[1])
            else:
                for coord in self.gamestate[self.current_turn][area_itr]:
                    if self.gamestate[self.current_turn][area_itr][coord]:
                        print(self.gamestate[self.current_turn][area_itr][coord][0].view, self.gamestate[self.current_turn][area_itr][coord][1])
        
        print(opponent)
        for area_itr in self.gamestate[opponent]:
            print(area_itr)
            if area_itr == 'deck':
                for coord in self.gamestate[opponent][area_itr]:
                    for card_info in self.gamestate[opponent][area_itr][coord]:
                        print(card_info[0].view, card_info[1])
            else:
                for coord in self.gamestate[opponent][area_itr]:
                    if self.gamestate[opponent][area_itr][coord]:
                        print(self.gamestate[opponent][area_itr][coord][0].view, self.gamestate[opponent][area_itr][coord][1])
        

    def debug_info(self):
        print('current: ', self.current_turn)
        # print('player_img_id: ', self.gamestate['img_id'])
        self.debug_display_card_info()



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
            card.view = gc.CardView.FRONT
            # print('setup card in hand: ', card.view)
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
            self.gamestate['img_id'][player_key].append(image_id)
            # print(player_key, ' hand: ', self.gamestate[player_key]['hand'][position][0].view)
            # ctrl.GameControl.action_by_card_view(self.gamestate, self.card_display_panel, image_id)
            
            # Optionally bind mouse events to the image on the canvas using image_id
            # self.card_display_panel.canvas.tag_bind(
            #     image_id, "<Button-1>", lambda event, img_id=image_id: ctrl.GameControl.start_drag(
            #         event, self.card_display_panel.canvas, img_id, self.gamestate
            #     )
            # )
            # self.card_display_panel.canvas.tag_bind(
            #     image_id, "<B1-Motion>", lambda event, img_id=image_id: ctrl.GameControl.on_drag(
            #         event, self.card_display_panel.canvas, img_id, self.gamestate
            #     )
            # )
            # self.card_display_panel.canvas.tag_bind(
            #     image_id, "<ButtonRelease-1>", lambda event, img_id=image_id: ctrl.GameControl.on_release(
            #         event, self.card_display_panel.canvas, img_id, self.gamestate
            #     )
            # )
            self.card_display_panel.canvas.tag_bind(
                image_id, "<Button-3>", lambda event, card=card: self.card_display_panel.display_card_info(card)
            )
            self.card_display_panel.canvas.tag_bind(
                image_id, "<Button-2>", lambda event, card=card: self.card_display_panel.display_card_info(card)
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
            card.view = gc.CardView.BACK
            # Add the image to the canvas, staggered to make each visible
            x_position = deck_x + int(itr / 3) * 0.5  # stack all cards in deck for better visual
            y_position = deck_y - itr * 0.5
            image_id = self.card_display_panel.canvas.create_image(
                x_position - size_w / 2, y_position - size_h / 2, image=card_image, anchor="nw"
                )
            
            self.gamestate[player_key]['deck'][deck_position].append((card, image_id))
            self.gamestate['img'][image_id] = card_image
            self.gamestate['img_id'][player_key].append(image_id)
            
            ctrl.GameControl.action_by_card_view(self.gamestate, self.card_display_panel, image_id)
            
            # # Bind left-click to check card debug info
            # self.card_display_panel.canvas.tag_bind(
            #     image_id, "<Button-1>", lambda event, img_id=image_id: ctrl.GameControl.start_drag(
            #         event, self.card_display_panel.canvas, img_id, self.gamestate
            #     )
            # ) # does not work.......why??
            # Bind double-click (left button) to turn the card over
            # self.card_display_panel.canvas.tag_bind(
            #     image_id, "<Double-Button-1>", 
            #     lambda event, img_id=image_id: ctrl.GameControl.turn_card(
            #         event, self.card_display_panel, img_id, self.gamestate
            #         )
            #     )
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

    def debug_gamestate(self):
        """
        Displays the count of cards for each player in each area of the gamestate.

        Args:
            gamestate (dict): The gamestate dictionary.
        """
        for player in ['player1', 'player2']:
            print(f"Card counts for {player}:")
            player_data = self.gamestate.get(player, {})
            for area in ['hand', 'deck', 'atk', 'def']:
                area_data = player_data.get(area, {})
                if area == 'deck':
                    # Deck contains a list of (card, img_id) tuples
                    count = len(area_data)
                else:
                    # Other areas contain a single (card, img_id) tuple per coordinate
                    count = len(area_data)
                print(f"  {area.capitalize()}: {count} cards")
            print()    

if __name__ == "__main__":
    
    root = tk.Tk()
    app = TheApathyofKings(root)
    root.mainloop()


    
    




