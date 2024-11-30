class Dragon:
    def __init__(self, name, element, defense, hp, img_path):
        self.name = name
        self.element = element
        self.defense = defense
        self.hp = hp
        self.img_path = img_path

    def info(self):
        return [
            f"Name: {self.name}",
            f"Element: {self.element}",
            f"Defense: {self.defense}",
            f"HP: {self.hp}",
        ]
