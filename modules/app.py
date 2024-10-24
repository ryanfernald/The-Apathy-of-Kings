import tkinter as tk
import time
from modules.button_clicks import deck_card_click, hand_card_click, atk_card_click, def_card_click, set_console, remove_message, end_turn_click
from modules.card_mgmt import CardManager


class AoK:
    def __init__(self, master):
        master.title("The Apathy of Kings")
        master.configure(bg="dark grey")
        master.geometry("1600x1100")

        canvas = tk.Canvas(master)
        scrollbar_y = tk.Scrollbar(master, orient="vertical", command=canvas.yview)
        scrollbar_x = tk.Scrollbar(master, orient="horizontal", command=canvas.xview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # Pack the scrollbars and the canvas
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

        self.card_manager = CardManager()

        # Enable touchpad scrolling on canvas
        canvas.unbind_all("<MouseWheel>")
        canvas.unbind_all("<Shift-MouseWheel>")
        
        # Enable touchpad scrolling on canvas (cross-platform)
        canvas.bind("<Enter>", lambda e: canvas.focus_set())
        canvas.bind("<MouseWheel>", lambda event: canvas.yview_scroll(-1 * int(event.delta / 120), "units"))
        canvas.bind("<Shift-MouseWheel>", lambda event: canvas.xview_scroll(-1 * int(event.delta / 120), "units"))

        # Hand buttons for Player 1 and Player 2
        self.p1_hand_buttons = []
        self.p2_hand_buttons = []

        # For Player 1 hand buttons
        for i in range(7):
            p1_button = tk.Button(scrollable_frame, height=8, width=12, bg="blue", bd=4,
                                command=lambda i=i: hand_card_click("P1", i+1, self.p1_atk_buttons, self.p1_def_buttons))
            p1_button.grid(row=6, column=i+2, padx=2, pady=2)
            self.p1_hand_buttons.append(p1_button)
        # For Player 2 hand buttons
        for i in range(7):
            p2_button = tk.Button(scrollable_frame, height=8, width=12, bg="blue", bd=4,
                                command=lambda i=i: hand_card_click("P2", i+1, self.p2_atk_buttons, self.p2_def_buttons))
            p2_button.grid(row=0, column=i+2, padx=2, pady=2)
            self.p2_hand_buttons.append(p2_button)

        # Player 2 Dragon Health Textbox (Row 1, Col 0-1)
        self.p2_drgn_health = tk.Text(scrollable_frame, height=8, width=24, bd=4, relief="solid")
        self.p2_drgn_health.grid(row=1, column=0, columnspan=2, padx=2, pady=2)


        # Attack and defense buttons for Player 1 (Row 4 and Row 5)
        self.p1_atk_buttons = []
        self.p1_def_buttons = []

        # Attack and defense buttons for Player 1 (Row 4 and Row 5)
        for i in range(5):
            atk_button = tk.Button(scrollable_frame, height=12, width=16, bg="green", bd=4, relief="solid",
                                command=lambda i=i: atk_card_click("P1", i+1, self.p1_atk_buttons))
            atk_button.grid(row=4, column=i+3, padx=2, pady=2)
            atk_button.image = None  # Initialize image attribute to None
            self.p1_atk_buttons.append(atk_button)

            def_button = tk.Button(scrollable_frame, height=12, width=16, bg="yellow", bd=4, relief="solid",
                                command=lambda i=i: def_card_click("P1", i+1, self.p1_def_buttons))
            def_button.grid(row=5, column=i+3, padx=2, pady=2)
            def_button.image = None  # Initialize image attribute to None
            self.p1_def_buttons.append(def_button)

        # Attack and defense buttons for Player 2 (Row 1 and Row 2)
        self.p2_atk_buttons = []
        self.p2_def_buttons = []

        # Attack and defense buttons for Player 2 (Row 1 and Row 2)
        for i in range(5):
            atk_button = tk.Button(scrollable_frame, height=12, width=16, bg="red", bd=4, relief="solid",
                                command=lambda i=i: atk_card_click("P2", i+1, self.p2_atk_buttons))
            atk_button.grid(row=2, column=i+3, padx=2, pady=2)
            atk_button.image = None  # Initialize image attribute to None
            self.p2_atk_buttons.append(atk_button)

            def_button = tk.Button(scrollable_frame, height=12, width=16, bg="orange", bd=4, relief="solid",
                                command=lambda i=i: def_card_click("P2", i+1, self.p2_def_buttons))
            def_button.grid(row=1, column=i+3, padx=2, pady=2)
            def_button.image = None  # Initialize image attribute to None
            self.p2_def_buttons.append(def_button)

        # Player 1 Dragon Health Textbox (Row 5, Col 0-1)
        self.p1_drgn_health = tk.Text(scrollable_frame, height=8, width=24, bd=4, relief="solid")
        self.p1_drgn_health.grid(row=5, column=0, columnspan=2, padx=2, pady=2)

        # Player 2 Dragon Button (Row 2, Col 0-1)
        self.p2_drgn = tk.Button(scrollable_frame, height=12, width=24, text="p2_drgn", bg="grey", bd=4, relief="solid")
        self.p2_drgn.grid(row=2, column=0, columnspan=2, padx=2, pady=2)

        # Player 1 Dragon Button (Row 4, Col 0-1)
        self.p1_drgn = tk.Button(scrollable_frame, height=12, width=24, text="p1_drgn", bg="grey", bd=4, relief="solid")
        self.p1_drgn.grid(row=4, column=0, columnspan=2, padx=2, pady=2)

        # Deck button for Player 2 (Row 2, Col 9)
        self.p2_deck = tk.Button(scrollable_frame, height=12, width=16, text="Deck", bg="maroon", bd=4,
                                 command=lambda: deck_card_click("P2", self.p2_hand_buttons), relief="solid")
        self.p2_deck.grid(row=2, column=9, padx=2, pady=2)

        # Deck button for Player 1 (Row 4, Col 9)
        self.p1_deck = tk.Button(scrollable_frame, height=12, width=16, text="Deck", bg="maroon", bd=4,
                                 command=lambda: deck_card_click("P1", self.p1_hand_buttons), relief="solid")
        self.p1_deck.grid(row=4, column=9, padx=2, pady=2)

        # Card Display Button (Row 0, Col 11-12, rowspan=3)
        self.card_disp = tk.Button(scrollable_frame, height=30, width=45, text="card_disp", bg="cyan", bd=4, relief="solid")
        self.card_disp.grid(row=0, column=11, rowspan=3, columnspan=2, padx=2, pady=2)

        # Activity Log Textbox (Row 4, Col 11-12)
        self.activity_log = tk.Text(scrollable_frame, height=12, width=50, bd=4, relief="solid", font=("Ubuntu Light", 10), borderwidth=5)
        self.activity_log.grid(row=4, column=11, columnspan=2, padx=6, pady=2)
        # Set the console box in button_clicks.py
        set_console(self.activity_log)

        # Start the message removal timer
        remove_message()

        # End Turn Button (Row 6, Col 12)
        self.end_turn = tk.Button(scrollable_frame, height=8, width=24, text="End Turn", bg="blue", bd=4,
                                  command=end_turn_click, relief="solid")
        self.end_turn.grid(row=6, column=12, padx=2, pady=2)


if __name__ == "__main__":
    root = tk.Tk()
    app = AoK(root)
    root.mainloop()
