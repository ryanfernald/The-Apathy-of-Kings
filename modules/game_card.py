from enum import Enum

'''
class GameCard:
    def __init__(self, argString):
        temp = self.stateParsing(argString)
        self.__name = temp[0]   # card name
        self.__type = CardType(int(temp[1]))   # card type: attack card/ defense card/ support card
        self.__star = int(temp[2])
        self.__element = CardElement(int(temp[3]))
        self.__atk = int(temp[4])
        self.__def = int(temp[5])

    def stateParsing(self, argString):
        res = argString.split('.')[0].split(',')
        return res
    @property
    def name(self):
        return self.__name
    @property
    def type(self):
        return self.__type
    @property
    def star(self):
        return self.__star
    @property
    def element(self):
        return self.__element
    @property
    def attack(self):
        return self.__atk
    @property
    def defense(self):
        return self.__def

    def display(self):
        print('-' * 8 + ' Card Status ' + '-' * 8)
        print(f'Name: {self.__name}')
        print(f'Type: {self.__type}')
        print(f'Star: {self.__star}')
        print(f'Element: {self.__element}')
        print(f'Attack: {self.__atk}')
        print(f'Defense: {self.__def}')
    '''

class GameCard:
    def __init__(self, argName: str, argType: int, argPath):
        self.__name = argName   # card name
        self.__type = CardType(argType)   # card type: attack card/ defense card/ support card
        self.__imgPath = argPath
        self.__view = CardView(0)
    
    @property
    def name(self):
        return self.__name
    @property
    def type(self):
        return self.__type
    @property
    def imgPath(self):
        return self.__imgPath
    @property
    def view(self):
        return self.__view
    @name.setter
    def name(self, argName: str):
        self.__name = argName
    @type.setter    
    def type(self, argType: int):
        self.__type = argType
    @imgPath.setter
    def imgPath(self, argPath):
        self.__imgPath = argPath
    @view.setter
    def view(self, argView):
        self.__view = argView

    def stateParsing(self, argString: str):
        res = argString.split('.')[0].split(',')
        return res

    def display(self):
        print('-' * 8 + ' Card Status ' + '-' * 8)
        print(f'Name: {self.__name}')
        print(f'Type: {self.__type}')

    def info(self):
        res = []
        res.append(f'Name: {self.__name}')
        res.append(f'Type: {self.__type}')
        return res

class GameCardAtk(GameCard):
    def __init__(self, argString: str, argPath):
        temp = super().stateParsing(argString)
        super().__init__(temp[0], int(temp[1]), argPath)
        self.__star = int(temp[2])
        self.__element = CardElement(int(temp[3]))
        self.__atk = int(temp[4])
        self.__def = int(temp[5])
        self.__hp = self.__def
    
    @property
    def star(self):
        return self.__star
    @property
    def element(self):
        return self.__element
    @property
    def attack(self):
        return self.__atk
    @property
    def defense(self):
        return self.__def
    @property
    def hp(self):
        return self.__hp
    @hp.setter
    def hp(self, update: int):
        self.__hp = update

    def display(self):
        super().display()
        print(f'Star: {self.__star}')
        print(f'Element: {self.__element}')
        print(f'Attack: {self.__atk}')
        print(f'Defense: {self.__def}')
        print(f'HP: {self.__hp}')
    
    def info(self):
        res = []
        res.extend(super().info())
        res.append(f'Star: {self.__star}')
        res.append(f'Element: {self.__element}')
        res.append(f'Attack: {self.__atk}')
        res.append(f'Defense: {self.__def}')
        res.append(f'HP: {self.__hp}')
        return res
    
    def __repr__(self):
        """
        show a string when print an object # not useful currently, could be delete
        """
        return (
            f"{self.__class__.__name__}("
            f"name='{self.name}', "
            f"card_type={self.type.value}, "
            f"img_path='{self.imgPath}', "
            f"star={self.__star}, "
            f"element=CardElement({self.__element.value}), "
            f"attack={self.__atk}, "
            f"defense={self.__def})"
        )

class GameCardSup(GameCard):
    def __init__(self, argString: str, argPath):
        temp = super().stateParsing(argString)
        super().__init__(temp[0], int(temp[1]), argPath)
    
class GameCardDef(GameCard):
    def __init__(self, argString: str, argPath):
        temp = super().stateParsing(argString)
        super().__init__(temp[0], int(temp[1]), argPath)
        self.__def = int(temp[2])
        self.__hp = self.__def
    
    @property
    def defense(self):
        return self.__def
    @property
    def hp(self):
        return self.__hp
    @hp.setter
    def hp(self, update: int):
        self.__hp = update

    def display(self):
        super().display()
        print(f'Defense: {self.__def}')
        print(f'HP: {self.__hp}')
    
    def info(self):
        res = []
        res.extend(super().info())
        res.append(f'Defense: {self.__def}')
        res.append(f'HP: {self.__hp}')
        return res

# not sure use CardType or not for now
class CardType(Enum):
    ATTACK =1
    SUPPORT = 2
    DEFENSE = 3

# not sure use CardElement or not for now
class CardElement(Enum):    
    WIND = 1
    FIRE = 2
    EARTH = 3
    WATER = 4
    ELECTRO = 5

# tracking Card front image or back image
class CardView(Enum):
    FRONT = 1
    BACK = 0

# test
if __name__ == "__main__":
    print('-' * 10 + ' Test ' + '-' * 10)
    path1 = 'd:\\Documents\\Code\\2024Fall\\CS122_Project\\The-Apathy-of-Kings-main\\modules\\assets\\cards\\Fire Attack Cards\\Emberbloom,1,4,2,900,700.png'
    game_str = path1.split('\\')[-1]
    card1 = GameCardAtk(game_str, path1)
    print(card1.type)
    print(card1.view)

    print('-' * 10 + ' End ' + '-' * 10)
