from enum import Enum
import os

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


# test
if __name__ == "__main__":
    print('-' * 10 + ' Test ' + '-' * 10)
    str1='Blazing Will,1,4,2,1100,900.png'
    card1 = GameCard(str1)
    card1.display()

    print('-' * 10 + ' End ' + '-' * 10)
