import os
import random
from PIL import Image, ImageTk

class CardManager:
    def __init__(self):
        self.deck = []
        self.load_deck()
    
    def get_card_image_path(self, subfolder, filename):
        # Normalize the path to be cross-platform
        return os.path.join('modules', 'assets', 'cards', subfolder, filename).replace('\\', '/')

    def load_card_image(self, subfolder, filename, size=(80, 100)):
        image_path = self.get_card_image_path(subfolder, filename)
        if not os.path.exists(image_path):
            print(f"Image path does not exist: {image_path}")
            return None

        try:
            img = Image.open(image_path)
            img = img.resize(size, Image.ANTIALIAS)
            card_img = ImageTk.PhotoImage(img)
            return card_img
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            return None

    def load_deck(self):
        # Collect card images from subfolders
        base_dir = "modules/assets/cards"
        categories = ['Defense Cards', 'Earth Attack Cards', 'Electric Attack Cards', 
                      'Fire Attack Cards', 'Water Attack Cards', 'Wind Attack Cards', 'Support Cards']

        for category in categories:
            folder = os.path.join(base_dir, category)
            for card_img in os.listdir(folder):
                if card_img.endswith(".png"):
                    # You might want to load card images here if necessary, otherwise store the path
                    self.deck.append(os.path.join(folder, card_img))

        random.shuffle(self.deck)  # Shuffle the deck at the start

    def draw_card(self):
        if self.deck:
            return self.deck.pop()  # Remove and return the top card
        return None  # Return None if deck is empty

    def reset_deck(self):
        self.deck = []
        self.load_deck()
