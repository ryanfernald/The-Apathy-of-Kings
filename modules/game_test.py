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

        # Create a dictionary to hold player data
        self.state = {
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
        self.setup_player_cards(self.game1.info, "player1", self.game_grid1.PLAYER1_HAND, self.game_grid1.PLAYER1_DECK)

        # Setup player 2 cards (repeat similar setup for player 2)
        self.setup_player_cards(self.game1.info, "player2", self.game_grid1.PLAYER2_HAND, self.game_grid1.PLAYER2_DECK)
        # print(f'player1 image_idx: {len(self.state['player1']['image_idx'])}')
        # print(self.state['player1']['image_idx'])

    def setup_player_cards(self, game, player_key, hand_positions, deck_positions):
        size_w, size_h = self.game_grid1.CARD_SIZE
        
        # Setup hand cards
        for itr, card in enumerate(game[player_key]['hand']):
            # Load and resize the image for the card in the player's hand
            image = util.resize_image(imgPath = card.imgPath, argW = size_w, argH = size_h)

            # Keep a reference to the image to avoid garbage collection
            self.state[player_key]["hand_images"].append(image)

            # Add the image to the canvas
            x_position, y_position = hand_positions[itr]
            image_id = self.card_display_panel.canvas.create_image(x_position - size_w / 2, y_position - size_h / 2, image=image, anchor="nw")
            self.state[player_key]["image_idx"].append(image_id)

            # Bind mouse events for dragging using GameControl class
            self.card_display_panel.canvas.tag_bind(image_id, "<Button-1>", lambda event, img_id=image_id: ctrl.GameControl.start_drag(event, self.card_display_panel.canvas, img_id))
            self.card_display_panel.canvas.tag_bind(image_id, "<B1-Motion>", lambda event, img_id=image_id: ctrl.GameControl.on_drag(event, self.card_display_panel.canvas, img_id))
            self.card_display_panel.canvas.tag_bind(image_id, "<ButtonRelease-1>", lambda event, img_id=image_id, card=card: ctrl.GameControl.on_release(event, self.card_display_panel.canvas, img_id, card))
            # Bind right-click to display card information
            self.card_display_panel.canvas.tag_bind(image_id, "<Button-3>", lambda event, card=card: self.card_display_panel.display_card_info(card))
        # print(f'{player_key}: {len(self.state[player_key]['hand_images'])}')
        # Setup deck cards (just an idea for deck card display)
        image_back = util.load_card_back(self.game_grid1.CARD_SIZE)
        for itr, card in enumerate(game[player_key]['deck']):
            # Load and resize the image for the card in the player's deck
            # img_path = card.imgPath
            # original_image = Image.open(img_path)
            # resized_image = original_image.resize((size_w, size_h), Image.LANCZOS)
            # card_image = ImageTk.PhotoImage(resized_image)
            card_image = util.resize_image(imgPath = card.imgPath, argW = size_w, argH = size_h)

            # Keep a reference to the image to avoid garbage collection
            self.state[player_key]["deck_images"].append(card_image)
            self.state[player_key]["deck_images_back"].append(image_back)

            x, y = deck_positions[0]
            # Add the image to the canvas, staggered to make each visible
            x_position = x + int(itr / 3) * 0.5  # stack all cards in deck for better visual
            y_position = y - itr * 0.5
            image_id = self.card_display_panel.canvas.create_image(x_position - size_w / 2, y_position - size_h / 2, image=image_back, anchor="nw")
            self.state[player_key]["image_idx"].append(image_id)

            # Bind double-click (left button) to turn the card over
            self.card_display_panel.canvas.tag_bind(image_id, "<Double-Button-1>", lambda event, card_image=card_image, img_id=image_id: ctrl.GameControl.turn_card(event, self.card_display_panel.canvas, self.card_display_panel, card_image, img_id, card))
        # print(f'{player_key} deck: {len(self.state[player_key]["deck_images"])}')




if __name__ == "__main__":
    
    root = tk.Tk()
    app = GameTestCase(root)
    root.mainloop()


    
    




