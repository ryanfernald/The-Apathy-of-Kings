import time
import tkinter as tk
from PIL import Image, ImageTk
from modules.gameboard_management import toggle_turn, get_current_player
from modules.card_mgmt import CardManager
from modules.resize_img import resize_image

# Global variables to store the console box and message time
console_box = None
message_time = None
selected_card_img = None 

def set_console(console):
    global console_box
    console_box = console

def print_to_activity_log(message):
    global message_time
    if console_box:
        console_box.insert(tk.END, message + "\n")
        console_box.see(tk.END)
    print(message)
    message_time = time.time()

def remove_message():
    global message_time
    if message_time and time.time() - message_time >= 4:  
        console_box.delete("1.0", tk.END)
    console_box.after(1000, remove_message)

# Button click functions
def atk_card_click(player, index, atk_buttons):
    print_to_activity_log(f"{player} - Attack Card Selected: {index}")
    global selected_card_img
    if selected_card_img:
        move_card_to_field(selected_card_img, atk_buttons[index - 1])
        selected_card_img = None  # Clear the selection after move

def def_card_click(player, index, def_buttons):
    print_to_activity_log(f"{player} - Defense Card Selected: {index}")
    global selected_card_img
    if selected_card_img:
        move_card_to_field(selected_card_img, def_buttons[index - 1])
        selected_card_img = None  # Clear the selection after move

# End Turn button click function
def end_turn_click():
    # Get the current player before toggling
    current_player = get_current_player()
    next_player = toggle_turn()

    # Print messages for turn ending and starting
    print_to_activity_log(f"Player {current_player} turn ended, Player {next_player} turn now.")

card_manager = CardManager()
hand_cards_p1 = [None] * 7  # Player 1 hand slots
hand_cards_p2 = [None] * 7  # Player 2 hand slots

def deck_card_click(player, hand_buttons):
    card_img = card_manager.draw_card()  # Draw a card from the deck
    if card_img:
        for i in range(len(hand_buttons)):
            if player == "P1" and not hand_cards_p1[i]:
                hand_cards_p1[i] = card_img
                update_button_image(hand_buttons[i], card_img)
                print_to_activity_log(f"{player} - Drawn a card from deck")
                break
            elif player == "P2" and not hand_cards_p2[i]:
                hand_cards_p2[i] = card_img
                update_button_image(hand_buttons[i], card_img)
                print_to_activity_log(f"{player} - Drawn a card from deck")
                break

def update_button_image(button, card_img):
    resized_card = resize_image(card_img, button.winfo_width(), button.winfo_height())
    button.config(image=resized_card)
    button.image = resized_card  # Store the image reference to avoid garbage collection

    # Prompt player to select a field slot (atk or def)
def on_field_button_click(index, field_buttons, card_img):
    print(f"Moving card {card_img} to field button {index}")  # Debug statement
    move_card_to_field(card_img, field_buttons[index])

def load_image(image_path):
    try:
        img = Image.open(image_path)
        img = img.resize((100, 140), Image.Resampling.LANCZOS) #FIX RESIZE LATER
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return None
    
def move_card_to_field(card_image_path, field_button):
    card_image = load_image(card_image_path)  # Load the image
    if card_image and getattr(field_button, 'image', None) is None:  # Check if image is valid
        field_button.config(image=card_image)  # Set the card image on the button
        field_button.image = card_image  # Store the image reference to avoid garbage collection
        print_to_activity_log(f"Card moved to field: {field_button}")
    else:
        print_to_activity_log("This field is already occupied or image is invalid!")

# Enable the field buttons (atk + def) for the player to select
def on_field_button_click(index, field_buttons, card_img):
    print(f"Moving card {card_img} to field button {index}")  # Debug statement
    move_card_to_field(card_img, field_buttons[index])

    # Enable the field buttons for the player to select
    for i, button in enumerate(field_buttons):
        button.config(state=tk.NORMAL, command=lambda i=i: on_field_button_click(i))

def enable_field_buttons(field_buttons, card_img):
    # Enable the field buttons for the player to select
    for i, button in enumerate(field_buttons):
        button.config(state=tk.NORMAL, command=lambda i=i: on_field_button_click(i, field_buttons, card_img))
    
    # Temporarily disable all field buttons after the card is placed
    for i, button in enumerate(field_buttons):
        button.config(state=tk.DISABLED)

# New functions to handle field selection
def move_to_attack(card_img, atk_buttons):
    enable_field_buttons(atk_buttons, card_img)

def move_to_defense(card_img, def_buttons):
    enable_field_buttons(def_buttons, card_img)

def enable_field_buttons(field_buttons, card_img):
    # Enable the field buttons for the player to select
    for i, button in enumerate(field_buttons):
        button.config(state=tk.NORMAL, command=lambda i=i: on_field_button_click(i, field_buttons, card_img))

def hand_card_click(player, card_num, atk_buttons, def_buttons):
    global selected_card_img
    if player == "P1" and hand_cards_p1[card_num - 1]:
        selected_card_img = hand_cards_p1[card_num - 1]
        print_to_activity_log(f"P1 selected card {selected_card_img}")
        hand_cards_p1[card_num - 1] = None  # Remove from hand
    elif player == "P2" and hand_cards_p2[card_num - 1]:
        selected_card_img = hand_cards_p2[card_num - 1]
        print_to_activity_log(f"P2 selected card {selected_card_img}")
        hand_cards_p2[card_num - 1] = None  # Remove from hand
