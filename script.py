from random import shuffle

def create_deck():
    result = []
    composition = [(-2, 5),(-1,10),(0,15)]
    for (number,quantity) in composition :
        for i in range(0,quantity):
            result.append(number)
    for i in range(1,13):
        for j in range(0,10):
            result.append(i)
    return result

class Player:
    #Les cartes sont des tuples (n, Bool) où n est la valeur et Bool est vrai si la carte est visible
    def __init__(self,deck):
        self.grid = []
        for i in range(0,4):
            self.grid.append([(deck.pop(),False) for i in range(0,3)])
        self.grid[0][1] = (self.grid[0][1],True)
        self.grid[0][0] = (self.grid[0][0],True)

    def display_card_column(self,column):
        result = ""
        for i in column:
            if i[1] is False:
                result = result + "XX"
            else:
                n = i[0][0]
                result = result + str(n).rjust(2,'0')
            result = result + "|"
        result = result[:-1]
        return result

    def __str__(self):
        result = ""
        for i in range(0,4):
            #padded_string = "|".join([str(j[0]).rjust(2,'0') for j in self.grid[i]])
            padded_string = self.display_card_column(self.grid[i])
            result = result +  padded_string + "\n"
        return result

class Game:
    def __init__(self):
        self.grid = []
        self.deck = create_deck()
        shuffle(self.deck)
        self.player1 = Player(self.deck)
        self.player2 = Player(self.deck)

    def __str__(self):
        result = ""
        result+= "[DECK : "+str(len(self.deck))+" cartes]\n"
        result += "\nJOUEUR 1\n"
        result += str(self.player1)
        result += "\nJOUEUR 2\n"
        result += str(self.player2)
        return result

def main():
    g = Game()
    print(str(g))

if __name__ == '__main__' :
    main()
