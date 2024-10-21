

current_player = 1

# Function to toggle the player's turn
def toggle_turn():
    global current_player
    if current_player == 1:
        current_player = 2
    else:
        current_player = 1
    return current_player

# Function to get the current player's turn
def get_current_player():
    return current_player
