from random import shuffle

TRESHOLD = 8

def little_less_dumb_player(player,deck,discard,verbal = False):
    #modifie le player, mais renvoie le nouveau deck et le nouveau discard
    i = player.first_hidden_index()
    replaced_card = player.get_card_from_flat_index(i)[0]
    new_card = deck.pop()
    if new_card < TRESHOLD :
        player.replace_card(i,new_card)
        if verbal :
            print(player.tag + " remplace : "  + str(replaced_card) + " par " + str(new_card))
        discard.append(replaced_card)
    else:
        discard.append(new_card)
    return (deck,discard)

def dumb_player(player,deck,discard,verbal = False):
    #modifie le player, mais renvoie le nouveau deck et le nouveau discard
    i = player.first_hidden_index()
    replaced_card = player.get_card_from_flat_index(i)[0]
    new_card = deck.pop()
    player.replace_card(i,new_card)
    if verbal :
        print(player.tag + " remplace : "  + str(replaced_card) + " par " + str(new_card))
    discard.append(replaced_card)
    return (deck,discard)

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
        self.play_function = dumb_player
        b = all_visible
        for i in range(0,4):
            self.grid.append([(deck.pop(),all_visible) for i in range(0,3)])
        if not all_visible :
            self.flip_visible(0)
            self.flip_visible(1) 

    def first_hidden_index(self):
        n = 3 * len(self.grid)
        for i in range(0,n):
            card = self.get_card_from_flat_index(i)
            if not card[1]:
                return i
        return i

    def flip_visible(self,index):
        (col,l) = self.flat_index_to_coords(index)
        card = self.grid[col][l]
        self.grid[col][l] = (card[0],not card[1])

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

    #on applatit la grille. Les colonnes sont collées à la suite
    #[[a,b,c],[d,e,f]] devient [a,b,c,d,e,f]
    #card est un simple ENTIER. Une carte ajoutée est toujours visible
    def replace_card(self,flat_index,card):
        (col,ligne) = self.flat_index_to_coords(flat_index)
        self.grid[col][ligne] = (card,True)

    def final_score(self):
        n = 3 * len(self.grid)
        return sum([self.get_card_from_flat_index(i)[0] for i in range(0,n)])

    def check_all_visible(self):
        n = 3 * len(self.grid)
        for i in range(0,n):
            if not self.get_card_from_flat_index(i)[1]:
                return False
        return True

class Game:
    def __init__(self,test=False):
        self.grid = []
        self.deck = create_deck()
        shuffle(self.deck)
        self.discard = [self.deck.pop()]
        self.player1 = Player(self.deck,test)
        self.player1.tag = "J1"
        self.player2 = Player(self.deck)
        self.player2.tag = "J2"
        self.player2.play_function = little_less_dumb_player

    def __str__(self):
        result = ""
        result+= "[DECK : "+str(len(self.deck))+" cartes / DEF : ["+str(self.discard[-1])+"] + "+str(len(self.discard))+" cartes]\n"
        result += "\nJOUEUR 1\n"
        result += str(self.player1)
        result += "\nJOUEUR 2\n"
        result += str(self.player2)
        return result

    def play_one_round(self,player):
            player.play_function(player,self.deck,self.discard)
            return player.check_all_visible()

    def play(self):
        game_over = False
        players = [self.player1,self.player2]
        while not game_over:
            current_player = players.pop()
            game_over = self.play_one_round(current_player)
            if game_over :
                break
            else:
                players.insert(0,current_player)

def get_test_player():
    g = Game(test=True)
    return g.player1

def play_one_game(verbal=False):
    g = Game()
    if verbal :
        print(str(g))
    g.play()
    s1 = g.player1.final_score()
    s2 = g.player2.final_score()
    if verbal :
        print(str(g))
        print(g.player1.tag + " SCORE : " + str(s1))
        print(g.player2.tag + " SCORE : " + str(s2))
    return (s1,s2)

def main(n,verbal = False):
    score_total_p1 = 0
    score_total_p2 = 0
    for i in range(0,n):
        (s1,s2) = play_one_game(verbal)
        score_total_p1 += s1
        score_total_p2 += s2
    final_s1 = round(score_total_p1/i,1)
    final_s2 = round(score_total_p2/i,1)
    print("P1 : " + str(final_s1) +  " | P2 : " + str(final_s2))

if __name__ == '__main__' :
    for i in range(-1,13):
        TRESHOLD = i
        print("TRESHOLD : " + str(TRESHOLD))
        main(10000)

