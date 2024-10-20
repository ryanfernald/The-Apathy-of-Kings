import tkinter as tk
import time
from modules.button_clicks import deck_card_click, hand_card_click, atk_card_click, def_card_click, set_console, remove_message


class AoK:
    def __init__(self, master):
        self.master = master
        master.title("The Apathy of Kings")
        #master.geometry("1920x1080")
        master.configure(bg="dark grey")


        # Player 2 Hand Buttons (Row 0, Col 2-8)
        for i in range(7):
            button = tk.Button(master, height=8, width=12, text=f"p2_hand_{i+1}", bg="blue", bd=4, 
                               command=lambda i=i: hand_card_click("P2", i+1), relief="solid")
            button.grid(row=0, column=i+2, padx=2, pady=2)

        # Player 1 Hand Buttons (Row 6, Col 2-8)
        for i in range(7):
            button = tk.Button(master, height=8, width=12, text=f"p1_hand_{i+1}", bg="blue", bd=4, 
                               command=lambda i=i: hand_card_click("P1", i+1), relief="solid")
            button.grid(row=6, column=i+2, padx=2, pady=2)

        # Player 2 Dragon Health Textbox (Row 1, Col 0-1)
        self.p2_drgn_health = tk.Text(master, height=8, width=24, bd=4, relief="solid")
        self.p2_drgn_health.grid(row=1, column=0, columnspan=2, padx=2, pady=2)

        # Player 2 Defense Buttons (Row 1, Col 3-7)
        for i in range(5):
            button = tk.Button(master, height=12, width=16, text=f"p2_def_{i+1}", bg="orange", bd=4,
                               command=lambda i=i: def_card_click("P2", i+1), relief="solid")
            button.grid(row=1, column=i+3, padx=2, pady=2)

        # Player 2 Attack Buttons (Row 2, Col 3-7)
        for i in range(5):
            button = tk.Button(master, height=12, width=16, text=f"p2_atk_{i+1}", bg="red", bd=4,
                               command=lambda i=i: atk_card_click("P2", i+1), relief="solid")
            button.grid(row=2, column=i+3, padx=2, pady=2)

        # Player 1 Attack Buttons (Row 4, Col 3-7)
        for i in range(5):
            button = tk.Button(master, height=12, width=16, text=f"p1_atk_{i+1}", bg="green", bd=4,
                               command=lambda i=i: atk_card_click("P1", i+1), relief="solid")
            button.grid(row=4, column=i+3, padx=2, pady=2)

        # Player 1 Defense Buttons (Row 5, Col 3-7)
        for i in range(5):
            button = tk.Button(master, height=12, width=16, text=f"p1_def_{i+1}", bg="yellow", bd=4,
                               command=lambda i=i: def_card_click("P1", i+1), relief="solid")
            button.grid(row=5, column=i+3, padx=2, pady=2)

        # Player 1 Dragon Health Textbox (Row 5, Col 0-1)
        self.p1_drgn_health = tk.Text(master, height=8, width=24, bd=4, relief="solid")
        self.p1_drgn_health.grid(row=5, column=0, columnspan=2, padx=2, pady=2)

        # Player 2 Dragon Button (Row 2, Col 0-1)
        self.p2_drgn = tk.Button(master, height=12, width=24, text="p2_drgn", bg="grey", bd=4, relief="solid")
        self.p2_drgn.grid(row=2, column=0, columnspan=2, padx=2, pady=2)

        # Player 1 Dragon Button (Row 4, Col 0-1)
        self.p1_drgn = tk.Button(master, height=12, width=24, text="p1_drgn", bg="grey", bd=4, relief="solid")
        self.p1_drgn.grid(row=4, column=0, columnspan=2, padx=2, pady=2)

        # Player 2 Deck Button (Row 2, Col 9)
        self.p2_deck = tk.Button(master, height=12, width=16, text="p2_deck", bg="maroon", bd=4,
                                 command=lambda: deck_card_click("P2"), relief="solid")
        self.p2_deck.grid(row=2, column=9, padx=2, pady=2)

        # Player 1 Deck Button (Row 4, Col 9)
        self.p1_deck = tk.Button(master, height=12, width=16, text="p1_deck", bg="maroon", bd=4,
                                 command=lambda: deck_card_click("P1"), relief="solid")
        self.p1_deck.grid(row=4, column=9, padx=2, pady=2)

        # Card Display Button (Row 0, Col 11-12, rowspan=3)
        self.card_disp = tk.Button(master, height=30, width=45, text="card_disp", bg="cyan", bd=4, relief="solid")
        self.card_disp.grid(row=0, column=11, rowspan=3, columnspan=2, padx=2, pady=2)

        # Activity Log Textbox (Row 4, Col 11-12)
        self.activity_log = tk.Text(master, height=12, width=50, bd=4, relief="solid", font=("Ubuntu Light", 10), borderwidth=5)
        self.activity_log.grid(row=4, column=11, columnspan=2, padx=6, pady=2)
        # Set the console box in button_clicks.py
        set_console(self.activity_log)

        # Start the message removal timer
        remove_message()

        # End Turn Button (Row 6, Col 12)
        self.end_turn = tk.Button(master, height=8, width=24, text="End Turn", bg="blue", bd=4, relief="solid")
        self.end_turn.grid(row=6, column=12, padx=2, pady=2)


if __name__ == "__main__":
    root = tk.Tk()
    app = AoK(root)
    root.mainloop()
