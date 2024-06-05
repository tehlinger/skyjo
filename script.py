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
    def __init__(self,deck,all_visible=False):
        self.grid = []
        b = all_visible
        for i in range(0,4):
            self.grid.append([(deck.pop(),all_visible) for i in range(0,3)])
        self.grid[0][1] = (self.grid[0][1][0],True)
        self.grid[0][0] = (self.grid[0][0][0],True)

    def display_card_column(self,column):
        result = ""
        for i in column:
            if i[1] is False:
                result = result + "XX"
            else:
                n = i[0]
                result = result + str(n).rjust(2,'0')
            result = result + "|"
        result = result[:-1]
        return result

    def __str__(self):
        result = ""
        for i in range(0,4):
            #padded_string = "|".join([str(j[0]).rjust(2,'0') for j in self.grid[i]])
            col = self.grid[i]
            padded_string = self.display_card_column(col)
            result = result +  padded_string + "\n"
        return result

    def flat_index_to_coords(self,i):
        col = i // 3
        l = i % 3
        return (col,l)

    def coords_to_flat_index(self,col,l):
        return col * 3 + l 

    def get_card_from_flat_index(self,flat_index):
        (col,l) = self.flat_index_to_coords(flat_index)
        return self.grid[col][l]

    def replace_card(self,flat_index):
        #on applatit la grille. Les colonnes sont collées à la suite
        #[[a,b,c],[d,e,f]] devient [a,b,c,d,e,f]
        return

class Game:
    def __init__(self,test=False):
        self.grid = []
        self.deck = create_deck()
        shuffle(self.deck)
        self.discard = [self.deck.pop()]
        self.player1 = Player(self.deck,test)
        self.player2 = Player(self.deck)

    def __str__(self):
        result = ""
        result+= "[DECK : "+str(len(self.deck))+" cartes / DEF : "+str(self.discard[-1])+"]\n"
        result += "\nJOUEUR 1\n"
        result += str(self.player1)
        result += "\nJOUEUR 2\n"
        result += str(self.player2)
        return result

def get_test_player():
    g = Game(test=True)
    return g.player1

def main():
    g = Game()
    print(str(g))

#if __name__ == '__main__' :
#    main()
