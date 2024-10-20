import time
import tkinter as tk

# Global variables to store the console box and message time
console_box = None
message_time = None

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
def deck_card_click(player):
    print_to_activity_log(f"{player} - Drawn a card from deck")

def hand_card_click(player, card_num):
    print_to_activity_log(f"{player} - Card in Hand Selected: {card_num}")

def atk_card_click(player, card_num):
    print_to_activity_log(f"{player} - Attack Card Selected: {card_num}")

def def_card_click(player, card_num):
    print_to_activity_log(f"{player} - Def Card Selected: {card_num}")


def deck_card_click(player):
    print_to_activity_log(f"{player} - Drawn a card from deck")

def hand_card_click(player, card_num):
    print_to_activity_log(f"{player} - Card in Hand Selected: {card_num}")

def atk_card_click(player, card_num):
    print_to_activity_log(f"{player} - Attack Card Selected: {card_num}")

def def_card_click(player, card_num):
    print_to_activity_log(f"{player} - Def Card Selected: {card_num}")

