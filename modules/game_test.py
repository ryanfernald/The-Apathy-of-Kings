import tkinter as tk
import game_play as gp
import utility as util
import game_grid as ggrid
import game_control as ctrl
import game_layout as glayout


# test case 
class GameTestCase:
    def __init__(self, root):
        self.root = root
        self.root.title('Image Display Test')
        self.root.geometry("1500x960")
        
        # Create an instance of GameGrid
        self.game_grid1 = ggrid.GameGrid()
        
        # Initialize CardDisplayPanel to handle card information display
        self.card_display_panel = glayout.GameLayout(root)
        
        # Initialize GamePlay and get card information
        self.game1 = gp.GamePlay()
        # self.game1.displayGameInfo()    # message: show number of cards

        # Draw the card hands, decks, and battlefields on the canvas using the instance methods        
        self.game_grid1.canvas_layout(self.card_display_panel.canvas)
        self.game_grid1.canvas_battlefield(self.card_display_panel.canvas)
        self.game_grid1.canvas_reserve(self.card_display_panel.canvas)
        

        # Create a dictionary to hold player data
        self.gamestate = self.game_grid1.info


        self.img_list = {} # usage: avoid garbage collection
        self.image_back = util.load_card_back(self.game_grid1.CARD_SIZE)

        self.setup_player_hand('player1')
        self.setup_player_hand('player2')
        self.setup_player_deck('player1')
        self.setup_player_deck('player2')

        # debug message
        self.display_area_state()








    

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
            card_image = util.resize_image(imgPath=card.imgPath, argW=size_w, argH=size_h)

            # Add the image to the canvas and get the image_id
            x_position, y_position = position
            image_id = self.card_display_panel.canvas.create_image(
                x_position - size_w / 2, y_position - size_h / 2, image=card_image, anchor="nw"
            )
            # example of overwriting the image: 
            # self.card_display_panel.canvas.itemconfig(image_id, image=new_image)

            # Store the (GameCard, image_id) tuple in the gamestate
            self.gamestate[player_key]['hand'][position] = (card, image_id)
            self.img_list[image_id] = card_image
            # Optionally bind mouse events to the image on the canvas using image_id
            self.card_display_panel.canvas.tag_bind(
                image_id, "<Button-1>", lambda event, img_id=image_id: ctrl.GameControl.start_drag(
                    event, self.card_display_panel.canvas, img_id
                )
            )
            self.card_display_panel.canvas.tag_bind(
                image_id, "<B1-Motion>", lambda event, img_id=image_id: ctrl.GameControl.on_drag(
                    event, self.card_display_panel.canvas, img_id
                )
            )
            self.card_display_panel.canvas.tag_bind(
                image_id, "<ButtonRelease-1>", lambda event, img_id=image_id, card=card: ctrl.GameControl.on_release(
                    event, self.card_display_panel.canvas, img_id, card
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

        for itr, card in enumerate(cards):
            card_image = self.image_back
            # Add the image to the canvas, staggered to make each visible
            x_position = deck_x + int(itr / 3) * 0.5  # stack all cards in deck for better visual
            y_position = deck_y - itr * 0.5
            image_id = self.card_display_panel.canvas.create_image(
                x_position - size_w / 2, y_position - size_h / 2, image=self.image_back, anchor="nw"
                )
            # self.state[player_key]["image_idx"].append(image_id)
            self.gamestate[player_key]['deck'][deck_position].append((card, image_id))

            # Bind double-click (left button) to turn the card over
            self.card_display_panel.canvas.tag_bind(
                image_id, "<Double-Button-1>", 
                lambda event, card_image=self.image_back, img_id=image_id: ctrl.GameControl.turn_card(
                    event, self.card_display_panel.canvas, self.card_display_panel, card_image, img_id, card, self.gamestate
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




if __name__ == "__main__":
    
    root = tk.Tk()
    app = GameTestCase(root)
    root.mainloop()


    
    




