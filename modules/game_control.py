import time
from . import game_grid as ggrid
from . import game_card as gc
from . import utility as util


class GameControl:
    
    card_original_coords = (0, 0)

    
    # Static method to start the drag operation
    @staticmethod
    def start_drag(event, canvas, image_id, gamestate):
        # Record the starting point of the drag
        GameControl.card_original_coords = canvas.coords(image_id)
        event.widget.start_x = event.x
        event.widget.start_y = event.y
        ### following are debug messages, delete after completion
        result = GameControl.find_card_by_image_id(gamestate, image_id)
        print(f"{result['player']}'s {result['card'].name} {result['card'].view} at {result['area']} coord: {result['coord']}")
        cur_card = GameControl.find_card_by_coord(gamestate, result['coord'])
        print(cur_card) # debug function find_card_by_coord()
        # print(f"({GameControl.card_original_coords[0]}, {GameControl.card_original_coords[1]})")
        
        # print('index\n', gamestate['index'])
        # print('img\n', gamestate['img'])
        # print('gamestate\n', gamestate)
        # debug message for game layout !!! THis debug message is now show layout upon click, not after movement
        # GameControl.display_gamestate_layout(gamestate)
        print('movable area: ' , GameControl.get_allowed_move_area(gamestate, canvas, image_id))
        print('attackable area: ', GameControl.get_allowed_attack_area(gamestate, canvas, image_id))

    # Static method to handle the dragging operation
    @staticmethod
    def on_drag(event, canvas, image_id, gamestate):
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
    def on_release(event, canvas, image_id, gamestate):
        result = GameControl.find_card_by_image_id(gamestate, image_id)
        card = result['card']
        # determin the allowed area based on the card type or player
        area = GameControl.get_allowed_move_area(gamestate, canvas, image_id)
        if not GameControl.location_auto_lockin(canvas, image_id, area, gamestate):
            # only GameCardAtk allow to attack
            if isinstance(card, gc.GameCardAtk) & GameControl.is_attack(canvas.coords(image_id)):
                # to do: add method to determin which space is attack
                # print(canvas.coords(image_id), 'being attack in function on_release')
                # print('attack') # debug message
                GameControl.attack_animation(canvas, image_id, card, gamestate)
            GameControl.animate_move_back(canvas, image_id, GameControl.card_original_coords)
        # debug message for game layout 
        # GameControl.display_gamestate_layout(gamestate)    

    @staticmethod ### delete if get_allowed_move_area() fully functional
    def get_allowed_area(canvas, image_id, card, gamestate):
        card_info = GameControl.find_card_by_image_id(gamestate, image_id)
        if not card_info:
            return []  # If card information cannot be found, return an empty list

        player_key = card_info['player']
        allowed_area = []

        # Determine the allowed area based on the player and card type
        if player_key == 'player1':
            if isinstance(card, gc.GameCardAtk):
                allowed_area = list(gamestate['player1']['atk'].keys())
            elif isinstance(card, gc.GameCardDef):
                allowed_area = list(gamestate['player1']['def'].keys())
            else:
                allowed_area = list(gamestate['player1']['hand'].keys())
        elif player_key == 'player2':
            if isinstance(card, gc.GameCardAtk):
                allowed_area = list(gamestate['player2']['atk'].keys())
            elif isinstance(card, gc.GameCardDef):
                allowed_area = list(gamestate['player2']['def'].keys())
            else:
                allowed_area = list(gamestate['player2']['hand'].keys())

        return allowed_area

    @staticmethod
    def get_allowed_move_area(gamestate, canvas, image_id):
        card_info = GameControl.find_card_by_image_id(gamestate, image_id)
        if not card_info:
            # if card_info is None, that means that program have logic error
            return []  # If card information cannot be found, return an empty list

        player_key = card_info['player']
        cur_area = card_info['area']
        allowed_area = []
        
        # Determine the allowed area based on the player and card type
        player_data = gamestate.get(player_key, {})
        if isinstance(card_info['card'], gc.GameCardAtk):
            # Get the 'atk' area and exclude occupied spaces
            atk_area = player_data.get('atk', {})
            allowed_area = [pos for pos, occupied in atk_area.items() if occupied is None]
        elif isinstance(card_info['card'], gc.GameCardDef):
            # Get the 'def' area and exclude occupied spaces
            def_area = player_data.get('def', {})
            allowed_area = [pos for pos, occupied in def_area.items() if occupied is None]
        
        if cur_area == 'hand':
            hand_empty = GameControl.hand_empty_area(gamestate, player_key)
            allowed_area.extend(hand_empty)    

        return allowed_area

    @staticmethod
    def get_allowed_attack_area(gamestate, canvas, image_id):
        card_info = GameControl.find_card_by_image_id(gamestate, image_id)
        if not card_info:
            # if card_info is None, that means that program have logic error
            return [] # If card_info is None, return an empty list
        if card_info['area'] == 'hand':
            return [] # card can not attack if it is in hand area

        # Determine the current player key and opponent player key
        player_key = card_info['player']
        opponent_key = 'player2' if player_key == 'player1' else 'player1'

        # Get the opponent's areas
        atk_area = gamestate[opponent_key]['atk']
        def_area = gamestate[opponent_key]['def']

        # Collect occupied spaces from atk and def areas
        attackable_area = [
            coord for coord, card_list in atk_area.items() if card_list is not None
        ] + [
            coord for coord, card_list in def_area.items() if card_list is not None
        ]

        return attackable_area

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
        # print(f'{who} card in {cur}\'s area')   # debug message
        return not (who == cur)

    @staticmethod
    def animate_move_back(canvas, image_id, coord, coord_offset=(0, 0)):
        """Animate the card moving back to its original location."""
        current_x, current_y = canvas.coords(image_id)
        target_x, target_y = coord
        target_x = target_x + coord_offset[0]
        target_y = target_y + coord_offset[1]

        steps = 20  # Number of animation steps
        dx = (target_x - current_x) / steps
        dy = (target_y - current_y) / steps

        for _ in range(steps):
            canvas.move(image_id, dx, dy)
            canvas.update()
            time.sleep(0.01)

    @staticmethod
    def location_auto_lockin(canvas, image_id, area, gamestate):
        '''function return True or False'''
        # Get the current position of the card
        card_center_x, card_center_y, width, height = GameControl.get_card_center(canvas, image_id)

        # Find the closest area to the card's center
        closest_area = GameControl.find_closest_area(card_center_x, card_center_y, area)
        #print(f"closest: {closest_area}")
        # If the card should snap to the closest area, align it
        return GameControl.snap_to_closest_area(canvas, image_id, card_center_x, card_center_y, closest_area, width, height, gamestate)


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
    def snap_to_closest_area(canvas, image_id, card_center_x, card_center_y, closest_area, width, height, gamestate):
        """Snap the card to the closest area if within the threshold distance."""
        if (closest_area and
                abs(card_center_x - closest_area[0]) <= ggrid.GameGrid().X_THRESHOLD * 2 and
                abs(card_center_y - closest_area[1]) <= ggrid.GameGrid().Y_THRESHOLD * 2):
            # Snap the card image to the target coordinate by aligning its center
            canvas.coords(image_id, closest_area[0] - width / 2, closest_area[1] - height / 2)
            # update gamestate
            GameControl.gamestate_update_move(gamestate, image_id, closest_area)
            # print(gamestate) # really long debug message, almost blind myself
            
            return True
        return False
    
    @staticmethod
    def gamestate_update_move(gamestate, image_id, new_coord):
        #print('method: gamestate_update_move()') # debug message
        card_info = GameControl.find_card_by_image_id(gamestate, image_id)
        # Extract information from card_info
        player_key = card_info['player']
        area_name = card_info['area']
        old_position = card_info['coord']
        card_tuple = (card_info['card'], image_id)
        # set old to None
        if area_name == 'deck':
            gamestate[player_key][area_name][old_position]
        else:
            gamestate[player_key][area_name][old_position] = None
        # find area by new coord
        new_area = gamestate['index'][new_coord]
        # add to new coord
        gamestate[player_key][new_area][new_coord] = card_tuple


    @staticmethod
    def turn_card(event, card_display_panel, img_id, gamestate):
        """Method to turn over the card and display the real image."""
        card_info = GameControl.find_card_by_image_id(gamestate, img_id)
        ## TO-DO: structure problem deck is a list. # find_card_by_image_id() cause issue because loop check for dict, sovle by using area_name directly
        # print('method: turn_card()\nDebug:', card_info) # debug message
        player_key = card_info['player']
        area_name = card_info['area']
        old_position = card_info['coord']
        card_tuple = (card_info['card'], img_id)

        coord = GameControl.hand_state(gamestate, player_key)
        print(f"Try to turn card and move to ({coord})")
        if coord == None:
            return

        # class GameCard method to identify card is currently front or back 
        card_tuple[0].flip()

        # overwrite with front image
        card_image = util.resize_image_w_bg(card_tuple[0].imgPath, ggrid.GameGrid().CARD_SIZE, player_key)
        # Change the image of the card to the actual card image
        card_display_panel.canvas.itemconfig(img_id, image=card_image)
        
        # Keep a reference to avoid garbage collection
        gamestate['img'][img_id] = card_image
        
        # to-do: add code to make sure deck card move to hand area if there is empty spot ## solve, but final location have error
        # bug: move card to hand area not last touched card spot ## solve
        # auto move card to empty hand area. ## solve, add offset to coord for this issue
        coord_offset = ((0 - ggrid.GameGrid().CARD_SIZE[0] / 2), (0 - ggrid.GameGrid().CARD_SIZE[1] / 2))
        GameControl.animate_move_back(card_display_panel.canvas, img_id, coord, coord_offset)
        # update gamestate
        GameControl.gamestate_update_move(gamestate, img_id, coord)

        # Bind mouse events for dragging using GameControl class
        card_display_panel.canvas.tag_bind(
            img_id, "<Button-1>", lambda event, img_id=img_id: GameControl.start_drag(
                event, card_display_panel.canvas, img_id, gamestate)
                )
        card_display_panel.canvas.tag_bind(
            img_id, "<B1-Motion>", lambda event, img_id=img_id: GameControl.on_drag(
                event, card_display_panel.canvas, img_id, gamestate)
                )
        card_display_panel.canvas.tag_bind(
            img_id, "<ButtonRelease-1>", lambda event, img_id=img_id: GameControl.on_release(
                event, card_display_panel.canvas, img_id, gamestate)
                )
        # display card info on right pane
        card_display_panel.canvas.tag_bind(
            img_id, "<Button-3>", lambda event: card_display_panel.display_card_info(card_tuple[0]))

    # Static method to test if the clicked card belongs to Player 1 or Player 2
    @staticmethod
    def whose_card():
        """Determine if the card belongs to Player 1 or Player 2 based on its coordinates."""
        # this simple way does not work correctly as more method implemented
        # anything place could use find_card_by_image_id(), don't use this method
        if GameControl.card_original_coords[1] < ggrid.GameGrid().DIVIDER:
            return 'player1'
        elif GameControl.card_original_coords[1] > ggrid.GameGrid().DIVIDER:
            return 'player2'
        else:
            return None 

    # @staticmethod
    # def whose_card_by_img_id(gamestate, image_id):
    #     """
    #     Determine if the card belongs to Player 1 or Player 2 based on image_id.

    #     Args:
    #         gamestate (dict): The game state containing player data and cards.
    #         image_id (int): The unique identifier for the card image.

    #     Returns:
    #         str: 'player1' or 'player2', None if not found just in case.
    #     """
    #     # Iterate through both players in the game state
    #     for player_key in ['player1', 'player2']:
    #         player_data = gamestate.get(player_key, {})

    #         # Check 'hand', 'atk', and 'def' areas for the image_id
    #         for area in ['hand', 'atk', 'def']:
    #             area_data = player_data.get(area, {})
    #             for position, card_info in area_data.items():
    #                 # card_info is expected to be a tuple: (card_object, img_id)
    #                 if card_info and len(card_info) > 1 and card_info[1] == image_id:
    #                     return player_key  # Return the player's key

    #     # If no match is found, return None
    #     return None




    # # Static method to determin if the card movement is attack other player. ### delete, unused
    # @staticmethod
    # def validate_card_movement(card_coords, target_area):
    #     player_area = GameControl.whose_card(card_coords, ggrid.GameGrid())
    #     if player_area == 'player1':
    #         return None
    #     elif player_area == 'player2':
    #         return None
    #     return None
        
    @staticmethod
    def attack_animation(canvas, image_id, card, gamestate):
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
        GameControl.animation_damage(canvas, image_id, card.attack, gamestate)

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
    def animation_damage(canvas, image_id, attack_value, gamestate):
        """Display the card's attack value on the canvas for 1.5 seconds."""
        area = GameControl.area_underattack()
        card_center_x, card_center_y, _, _ = GameControl.get_card_center(canvas, image_id)
        closest_area = GameControl.find_closest_area(card_center_x, card_center_y, area)
        atk_x, atk_y = closest_area
        # print(f'{closest_area} being attacked') # debug message
        text_id = canvas.create_text(atk_x, atk_y, text=str(0 - attack_value), font=('Helvetica', 16, 'bold'), fill='red')
        canvas.update()
        ### core method for game rule ###
        if GameControl.card_reduce_hp(gamestate, closest_area, attack_value):
            GameControl.remove_card_by_coord(gamestate, closest_area)

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
    def card_reduce_hp(gamestate, coord, attack_value):
        # to-do: will get error if attack empty space
        card = GameControl.find_card_by_coord(gamestate, coord)
        #print(card)
        card.hp = card.hp - attack_value
        return True if card.hp <= 0 else False
        
    @staticmethod
    def find_card_by_coord(gamestate, coord):
        area_name = gamestate['index'][coord]
        for player_key in ['player1', 'player2']:
            if area_name in gamestate[player_key]:
                positions = gamestate[player_key][area_name]
                if coord in positions:
                    return positions[coord][0]

    @staticmethod
    def remove_card_by_coord(gamestate, coord):
        # gamestate['index'] = {coord: 'area_name'} # area_name is hand, atk, def, or deck.
        area_name = gamestate['index'][coord]
        for player_key in ['player1', 'player2']:
            if coord in gamestate[player_key][area_name]:
                # card, image_id = gamestate[player_key][area_name][coord] # {coord: (card, image_id)}
                gamestate['img'].pop(gamestate[player_key][area_name][coord][1])
                gamestate[player_key][area_name][coord] = None
                
    @staticmethod
    def defense_empty(gamestate, player_key):
        """
        Purpose: Checks if all defense positions for a specified player are empty.
        Game rule: only defense position empty could attack Dragon.
        This function iterates through the defense positions (`'def'` area) of a given player
        in the `gamestate` and determines if all positions are empty (i.e., contain `None`).

        Args:
            gamestate (dict): A dictionary representing the current state of the game.
                            The `gamestate` includes player-specific areas, such as `'def'` 
                            for defense positions, `'atk'` for attack positions, etc.
            player_key (str): The key representing the player whose defense positions
                            are to be checked. Valid values are `'player1'` and `'player2'`.

        Returns:
            bool: `True` if all defense positions for the specified player are empty, 
                `False` otherwise.

        Example:
            gamestate = {
                'player1': {
                    'def': {
                        (350, 235): None,
                        (450, 235): None,
                        (550, 235): None,
                        (650, 235): None,
                        (750, 235): None
                    }
                },
                'player2': {
                    'def': {
                        (350, 705): None,
                        (450, 705): (GameCardDef(name='Fortified Walls', card_type=3, defense=800, HP=800), 101),
                        (550, 705): None,
                        (650, 705): None,
                        (750, 705): None
                    }
                }
            }

            # Check if player1's defense positions are empty
            defense_empty(gamestate, 'player1')  # Output: True

            # Check if player2's defense positions are empty
            defense_empty(gamestate, 'player2')  # Output: False
        """
        for position, info in gamestate[player_key]['def'].items():
            if info != None:
                return False
        return True

    @staticmethod
    def hand_state(gamestate, player_key):
        """
        Determines if the player's hand is full.

        Parameters:
        player_key (str): The player identifier ('player1' or 'player2').

        Returns:
        bool: None if the hand is full, Coord otherwise.
        """
        # Access the hand area from the gamestate for the given player
        hand_area = gamestate[player_key]['hand']
        #print(len(hand_area))
        # Check if all positions in the hand have a card (i.e., not None)
        for coord, card in hand_area.items():
            # print(f"{coord} => {card[0].name}")
            if card is None:
                return coord  # If any position is empty, return a coord
            
    @staticmethod
    def hand_empty_area(gamestate, player_key):
        hand_area = gamestate[player_key]['hand']
        return [coord for coord, card in hand_area.items() if card is None]

    @staticmethod
    def find_card_by_image_id(gamestate, image_id):
        """
        Search for the card associated with a given image ID in the gamestate.

        Parameters:
        ----------
        gamestate : dict
            The current state of the game, containing information about all player areas (hand, deck, atk, def).
        image_id : int
            The image ID to search for in the game state.

        Returns:
        -------
        dict or None
            If a card matching the image ID is found, a dictionary containing:
                - "player": str, the player key ('player1' or 'player2')
                - "area": str, the area name ('hand', 'deck', 'atk', or 'def')
                - "position": tuple, the coordinates of the card in the respective area
                - "card": GameCard, the GameCard instance associated with the image ID
            If no card is found, returns None.
        """
        #print("method: find_card_by_image_id()") # debug message
        for player_key, areas in gamestate.items():
            for area_name, positions in areas.items():
                if area_name in ['hand', 'atk', 'def']:
                    # print(player_key, 'find_card_by_image_id: ', image_id, ' at hand, atk, def') # debug message
                    # For areas like hand, atk, def
                    for position, card_tuple in positions.items():
                        if card_tuple and len(card_tuple) == 2:
                            card, stored_image_id = card_tuple
                            if stored_image_id == image_id:
                                #print(image_id, ' at ' , area_name, position) # debug message
                                return {
                                    "player": player_key,
                                    "area": area_name,
                                    "coord": position,
                                    "card": card
                                }
                elif area_name == 'deck':
                    # print('find_card_by_image_id: ', image_id, ' at deck') # debug message
                    # deck value is list
                    for deck_position, deck_cards in positions.items():
                        for card, stored_image_id in deck_cards:
                            if stored_image_id == image_id:
                                #print(image_id, ' at ' , area_name, position, 'idx in deck list: ', deck_cards.index((card, stored_image_id)), ' out of ', len(deck_cards)) # debug message
                                return {
                                    "player": player_key,
                                    "area": "deck",
                                    "coord": deck_position,
                                    "card": card
                                }
        return None

    
    def display_gamestate_layout(gamestate):
        """
        Debug function to display the current layout of the game state in a compact grid format.
        
        Displays an 'O' if a position is occupied by a card and 'X' if it is empty.

        Parameters:
        gamestate (dict): The game state dictionary to be displayed.
        """
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


