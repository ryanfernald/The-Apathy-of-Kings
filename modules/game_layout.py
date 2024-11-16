import tkinter as tk
import utility as util


class GameLayout:
    def __init__(self, root):
        # Create a canvas 
        self.canvas = tk.Canvas(root, width=1000, height=960)
        self.canvas.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

        # Info panel to display selected card details (Card Image and Info)
        self.card_display_frame = tk.Frame(root, bg="lightgrey", width=480, height=720)
        self.card_display_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Add a label and canvas to display the card image
        self.card_image_label = tk.Label(self.card_display_frame, text="Card Image", bg="lightgrey")
        self.card_image_label.pack()
        self.card_image_canvas = tk.Canvas(self.card_display_frame, width=480, height=720, bg="white")
        self.card_image_canvas.pack()

        # Add text widget to display card information
        self.card_info_text = tk.Text(self.card_display_frame, height=10, width=60)
        self.card_info_text.pack()

        # Keep a reference for the displayed image
        self.card_image_ref = None

    def display_card_info(self, game_card):
        # Clear previous information
        self.card_info_text.delete(1.0, tk.END)
        self.card_image_canvas.delete("all")

        # Display card information
        card_info = game_card.info()
        for itr in card_info:
            self.card_info_text.insert(tk.END, itr + '\n')

        # Load and display the card image
        card_image = util.resize_image(game_card.imgPath)

        # Display the image on the canvas
        self.card_image_canvas.create_image(240, 360, anchor="center", image=card_image)

        # Keep a reference to avoid garbage collection
        # self.card_image_ref = card_image
        # self.card_image_canvas.image = card_image


