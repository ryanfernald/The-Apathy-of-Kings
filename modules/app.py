import tkinter as tk
import platform

class AoK:
    def __init__(self, master):
        self.master = master
        master.title("The Apathy of Kings")
        master.geometry("1920x1080")  # Set window size to 1920x1080

        # Player 2 Dragon Health Textbox
        self.p2_dragon_health_textbox = tk.Text(master, height=50, width=330, bd=2, relief="solid")
        self.p2_dragon_health_textbox.place(x=70, y=65)

        # Player 1 Dragon Health Textbox
        self.p1_dragon_health_textbox = tk.Text(master, height=50, width=330, bd=2, relief="solid")
        self.p1_dragon_health_textbox.place(x=70, y=970)

        # Player 2 Dragon Image Button
        self.p2_dragon_img = tk.Button(master, height=376, width=376, bg="cyan", bd=2, relief="solid")
        self.p2_dragon_img.place(x=50, y=133)

        # Player 1 Dragon Image Button
        self.p1_dragon_img = tk.Button(master, height=376, width=376, bg="maroon", bd=2, relief="solid")
        self.p1_dragon_img.place(x=50, y=576)

        # Player 2 Hand Buttons (1 row, 7 columns)
        self.p2_hand_1 = tk.Button(master, height=127, width=90, text="p2_hand_1", bg="orange", bd=2, relief="solid")
        self.p2_hand_1.place(x=493, y=10)
        self.p2_hand_2 = tk.Button(master, height=127, width=90, text="p2_hand_2", bg="orange", bd=2, relief="solid")
        self.p2_hand_2.place(x=588, y=10)
        self.p2_hand_3 = tk.Button(master, height=127, width=90, text="p2_hand_3", bg="orange", bd=2, relief="solid")
        self.p2_hand_3.place(x=683, y=10)
        self.p2_hand_4 = tk.Button(master, height=127, width=90, text="p2_hand_4", bg="orange", bd=2, relief="solid")
        self.p2_hand_4.place(x=778, y=10)
        self.p2_hand_5 = tk.Button(master, height=127, width=90, text="p2_hand_5", bg="orange", bd=2, relief="solid")
        self.p2_hand_5.place(x=873, y=10)
        self.p2_hand_6 = tk.Button(master, height=127, width=90, text="p2_hand_6", bg="orange", bd=2, relief="solid")
        self.p2_hand_6.place(x=968, y=10)
        self.p2_hand_7 = tk.Button(master, height=127, width=90, text="p2_hand_7", bg="orange", bd=2, relief="solid")
        self.p2_hand_7.place(x=1063, y=10)

        # Player 1 Hand Buttons (1 row, 7 columns)
        self.p1_hand_1 = tk.Button(master, height=127, width=90, text="p1_hand_1", bg="yellow", bd=2, relief="solid")
        self.p1_hand_1.place(x=493, y=946)
        self.p1_hand_2 = tk.Button(master, height=127, width=90, text="p1_hand_2", bg="yellow", bd=2, relief="solid")
        self.p1_hand_2.place(x=588, y=946)
        self.p1_hand_3 = tk.Button(master, height=127, width=90, text="p1_hand_3", bg="yellow", bd=2, relief="solid")
        self.p1_hand_3.place(x=683, y=946)
        self.p1_hand_4 = tk.Button(master, height=127, width=90, text="p1_hand_4", bg="yellow", bd=2, relief="solid")
        self.p1_hand_4.place(x=778, y=946)
        self.p1_hand_5 = tk.Button(master, height=127, width=90, text="p1_hand_5", bg="yellow", bd=2, relief="solid")
        self.p1_hand_5.place(x=873, y=946)
        self.p1_hand_6 = tk.Button(master, height=127, width=90, text="p1_hand_6", bg="yellow", bd=2, relief="solid")
        self.p1_hand_6.place(x=968, y=946)
        self.p1_hand_7 = tk.Button(master, height=127, width=90, text="p1_hand_7", bg="yellow", bd=2, relief="solid")
        self.p1_hand_7.place(x=1063, y=946)

        # Player 2 Defense Buttons (2 rows, 5 columns)
        self.p2_def_1 = tk.Button(master, height=187, width=132, text="p2_def_1", bg="blue", bd=2, relief="solid")
        self.p2_def_1.place(x=476, y=143)
        self.p2_def_2 = tk.Button(master, height=187, width=132, text="p2_def_2", bg="blue", bd=2, relief="solid")
        self.p2_def_2.place(x=613, y=143)
        self.p2_def_3 = tk.Button(master, height=187, width=132, text="p2_def_3", bg="blue", bd=2, relief="solid")
        self.p2_def_3.place(x=750, y=143)
        self.p2_def_4 = tk.Button(master, height=187, width=132, text="p2_def_4", bg="blue", bd=2, relief="solid")
        self.p2_def_4.place(x=887, y=143)
        self.p2_def_5 = tk.Button(master, height=187, width=132, text="p2_def_5", bg="blue", bd=2, relief="solid")
        self.p2_def_5.place(x=1024, y=143)
        
        # Player 2 Attack Buttons
        self.p2_atk_1 = tk.Button(master, height=187, width=132, text="p2_atk_1", bg="blue", bd=2, relief="solid")
        self.p2_atk_1.place(x=476, y=335)
        self.p2_atk_2 = tk.Button(master, height=187, width=132, text="p2_atk_2", bg="blue", bd=2, relief="solid")
        self.p2_atk_2.place(x=613, y=335)
        self.p2_atk_3 = tk.Button(master, height=187, width=132, text="p2_atk_3", bg="blue", bd=2, relief="solid")
        self.p2_atk_3.place(x=750, y=335)
        self.p2_atk_4 = tk.Button(master, height=187, width=132, text="p2_atk_4", bg="blue", bd=2, relief="solid")
        self.p2_atk_4.place(x=887, y=335)
        self.p2_atk_5 = tk.Button(master, height=187, width=132, text="p2_atk_5", bg="blue", bd=2, relief="solid")
        self.p2_atk_5.place(x=1024, y=335)

        # Player 1 Defense Buttons
        self.p1_def_1 = tk.Button(master, height=187, width=132, text="p1_def_1", bg="green", bd=2, relief="solid")
        self.p1_def_1.place(x=476, y=552)
        self.p1_def_2 = tk.Button(master, height=187, width=132, text="p1_def_2", bg="green", bd=2, relief="solid")
        self.p1_def_2.place(x=613, y=552)
        self.p1_def_3 = tk.Button(master, height=187, width=132, text="p1_def_3", bg="green", bd=2, relief="solid")
        self.p1_def_3.place(x=750, y=552)
        self.p1_def_4 = tk.Button(master, height=187, width=132, text="p1_def_4", bg="green", bd=2, relief="solid")
        self.p1_def_4.place(x=887, y=552)
        self.p1_def_5 = tk.Button(master, height=187, width=132, text="p1_def_5", bg="green", bd=2, relief="solid")
        self.p1_def_5.place(x=1024, y=552)


        # Player 1 Attack Buttons
        self.p1_atk_1 = tk.Button(master, height=187, width=132, text="p1_atk_1", bg="green", bd=2, relief="solid")
        self.p1_atk_1.place(x=476, y=744)
        self.p1_atk_2 = tk.Button(master, height=187, width=132, text="p1_atk_2", bg="green", bd=2, relief="solid")
        self.p1_atk_2.place(x=613, y=744)
        self.p1_atk_3 = tk.Button(master, height=187, width=132, text="p1_atk_3", bg="green", bd=2, relief="solid")
        self.p1_atk_3.place(x=750, y=744)
        self.p1_atk_4 = tk.Button(master, height=187, width=132, text="p1_atk_4", bg="green", bd=2, relief="solid")
        self.p1_atk_4.place(x=887, y=744)
        self.p1_atk_5 = tk.Button(master, height=187, width=132, text="p1_atk_5", bg="green", bd=2, relief="solid")
        self.p1_atk_5.place(x=1024, y=744)

        # Player 2 Deck Button
        self.p2_deck = tk.Button(master, height=238, width=168, text="p2_deck", bg="purple", bd=2, relief="solid")
        self.p2_deck.place(x=1229, y=274)

        # Player 1 Deck Button
        self.p1_deck = tk.Button(master, height=238, width=168, text="p1_deck", bg="purple", bd=2, relief="solid")
        self.p1_deck.place(x=1229, y=577)

        # Card Display Button
        self.card_display = tk.Button(master, height=545, width=385, text="card_display")
        self.card_display.place(x=1518, y=20)

        # Card Description Textbox
        self.card_description = tk.Text(master, height=167, width=385)
        self.card_description.place(x=1518, y=589)

        # End Turn Button
        self.end_turn = tk.Button(master, height=150, width=350, text="End Turn", bg="gray", bd=2, relief="solid")
        self.end_turn.place(x=1560, y=921)


if __name__ == "__main__":
    root = tk.Tk()
    app = AoK(root)
    root.mainloop()
