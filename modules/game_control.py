import time
import game_grid as ggrid
import game_card as gc


class GameControl:
    
    card_original_coords = (0, 0)

    # Static method to start the drag operation
    @staticmethod
    def start_drag(event, canvas, image_id):
        # Record the starting point of the drag
        GameControl.card_original_coords = canvas.coords(image_id)
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
        # determin the allowed area based on the card type or player
        area = GameControl.get_allowed_area(canvas, image_id, card)
        if not GameControl.location_auto_lockin(canvas, image_id, area):
            if isinstance(card, gc.GameCardAtk) & GameControl.is_attack(canvas.coords(image_id)):
                # to do: add method to determin which space is attack
                print('attack') # debug message
                GameControl.attack_animation(canvas, image_id, card)
            GameControl.animate_move_back(canvas, image_id, GameControl.card_original_coords)

    @staticmethod
    def get_allowed_area(canvas, image_id, card):
        who = GameControl.whose_card()
        allowed_area = []
        # print(who)
        if who == 'player1':
            if card.type == gc.CardType.ATTACK:
                allowed_area = ggrid.GameGrid().PLAYER1_ATK
            elif card.type == gc.CardType.DEFENSE:
                allowed_area = ggrid.GameGrid().PLAYER1_DEF
            else:
                allowed_area = ggrid.GameGrid().PLAYER1_HAND
        elif who == 'player2':
            if card.type == gc.CardType.ATTACK:
                allowed_area = ggrid.GameGrid().PLAYER2_ATK
            elif card.type == gc.CardType.DEFENSE:
                allowed_area = ggrid.GameGrid().PLAYER2_DEF
            else:
                allowed_area = ggrid.GameGrid().PLAYER2_HAND
        return allowed_area

    @staticmethod
    def card_current_area(card_coords):
        '''Determine the current area of a card based on its current coords.'''
        if card_coords[1] < ggrid.GameGrid().DIVIDER:
            return 'player1'
        else:
            return 'player2'
        
    def is_attack(card_coords):
        who = GameControl.whose_card()
        cur = GameControl.card_current_area(card_coords)
        print(f'{who} card in {cur}\'s area')   # debug message
        return not (who == cur)

    @staticmethod
    def animate_move_back(canvas, image_id, original_loc):
        """Animate the card moving back to its original location."""
        current_x, current_y = canvas.coords(image_id)
        target_x, target_y = original_loc

        steps = 20  # Number of animation steps
        dx = (target_x - current_x) / steps
        dy = (target_y - current_y) / steps

        for _ in range(steps):
            canvas.move(image_id, dx, dy)
            canvas.update()
            time.sleep(0.01)

    @staticmethod
    def location_auto_lockin(canvas, image_id, area):
        '''function return True or False'''
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
    def turn_card(event, canvas, card_display_panel, card_image, img_id, card, gamestate):
        """Method to turn over the card and display the real image."""
        if GameControl.is_hand_full(GameControl.whose_card(), gamestate):
            return
        # Change the image of the card to the actual card image
        canvas.itemconfig(img_id, image=card_image)

        # Keep a reference to avoid garbage collection
        canvas.image = card_image
        # to-do: add code to make sure deck card move to hand area if there is empty spot
        # bug: move card to hand area not last touched card spot

        # Bind mouse events for dragging using GameControl class
        canvas.tag_bind(img_id, "<Button-1>", lambda event, img_id=img_id: GameControl.start_drag(event, canvas, img_id))
        canvas.tag_bind(img_id, "<B1-Motion>", lambda event, img_id=img_id: GameControl.on_drag(event, canvas, img_id))
        canvas.tag_bind(img_id, "<ButtonRelease-1>", lambda event, img_id=img_id, card=card: GameControl.on_release(event, canvas, img_id, card))
        # Bind right-click to display card information
        # canvas.tag_bind(
        #     img_id,
        #         "<Button-3>",
        #         lambda event, card=card: card_display_panel.display_card_info(card)
        #     )   # bug: only show first turned card info. why??
        card_display_panel.canvas.tag_bind(img_id, "<Button-3>", lambda event, card=card: card_display_panel.display_card_info(card))

    # Static method to test if the clicked card belongs to Player 1 or Player 2
    @staticmethod
    def whose_card():
        """Determine if the card belongs to Player 1 or Player 2 based on its coordinates."""
        if GameControl.card_original_coords[1] < ggrid.GameGrid().DIVIDER:
            return 'player1'
        elif GameControl.card_original_coords[1] > ggrid.GameGrid().DIVIDER:
            return 'player2'
        else:
            return None

    # Static method to determin if the card movement is attack other player. ### delete, unused
    @staticmethod
    def validate_card_movement(card_coords, target_area):
        player_area = GameControl.whose_card(card_coords, ggrid.GameGrid())
        if player_area == 'player1':
            return None
        elif player_area == 'player2':
            return None
        return None

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
        
    @staticmethod
    def attack_animation(canvas, image_id, card):
        """Show an animation on the canvas to represent an attack."""
        current_x, current_y = canvas.coords(image_id)
        target_y = current_y - 30  # Move up to represent an attack

        steps = 10  # Number of animation steps
        dy = (target_y - current_y) / steps

        # Move the card up to simulate an attack
        for _ in range(steps):
            canvas.move(image_id, 0, dy)
            canvas.update()
            time.sleep(0.02)

        # Move the card back to its original position
        for _ in range(steps):
            canvas.move(image_id, 0, -dy)
            canvas.update()
            time.sleep(0.02)
        GameControl.animation_damage(canvas, image_id, card.attack)

    ## to do: make attack effect
    @staticmethod
    def attack_line_animation(canvas, image_id):
        """Draw a red bolded line to represent an attack, and make it disappear after 2 seconds."""
        area = GameControl.area_underattack()
        card_center_x, card_center_y, _, _ = GameControl.get_card_center(canvas, image_id)
        closest_area = GameControl.find_closest_area(card_center_x, card_center_y, area)
        
        # Get the current position of the card
        atk_x, atk_y = closest_area
        line_id = canvas.create_line(atk_x, atk_y, atk_x, atk_y - 100, width=20, fill='red')
        canvas.update()

        # Pause for 2 seconds to display the attack line
        time.sleep(1.5)

        # Remove the attack line
        canvas.delete(line_id)
        canvas.update()

    @staticmethod
    def animation_damage(canvas, image_id, attack_value):
        """Display the card's attack value on the canvas for 1.5 seconds."""
        area = GameControl.area_underattack()
        card_center_x, card_center_y, _, _ = GameControl.get_card_center(canvas, image_id)
        closest_area = GameControl.find_closest_area(card_center_x, card_center_y, area)
        atk_x, atk_y = closest_area
        text_id = canvas.create_text(atk_x, atk_y, text=str(0 - attack_value), font=('Helvetica', 16, 'bold'), fill='red')
        canvas.update()

        # Pause for 1.5 seconds to display the attack value
        time.sleep(1.5)

        # Remove the displayed attack value
        canvas.delete(text_id)
        canvas.update()

    @staticmethod
    def area_underattack():
        who = GameControl.whose_card()
        if who == 'player1':
            return ggrid.GameGrid().PLAYER2_ATK + ggrid.GameGrid().PLAYER2_DEF
        elif who == 'player2':
            return ggrid.GameGrid().PLAYER1_ATK + ggrid.GameGrid().PLAYER1_DEF

    @staticmethod
    def is_hand_full(player_key, gamestate):
        """
        Determines if the player's hand is full.

        Parameters:
        player_key (str): The player identifier ('player1' or 'player2').

        Returns:
        bool: True if the hand is full, False otherwise.
        """
        # Access the hand area from the gamestate for the given player
        hand_area = gamestate[player_key]['hand']

        # Check if all positions in the hand have a card (i.e., not None)
        for position, card in hand_area.items():
            if card is None:
                return False  # If any position is empty, the hand is not full

        return True  # If all positions are filled, the hand is full
