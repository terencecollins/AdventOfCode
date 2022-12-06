ROCK = 0
PAPER = 1
SCISSORS = 2

DRAW = 3
WIN = 6
LOSS = 0

class RPSGame(object):
    def __init__(self, opponent_move, personal_move, naive=True):
        self.opponent_move = self.translate_column_a(opponent_move)
        if naive:
            self.personal_move = self.translate_column_b_naive(personal_move)
        else:
            self.personal_move = self.translate_column_b(personal_move)            

    def translate_column_a(self, move):
        moves = { "A": ROCK,
                  "B": PAPER,
                  "C": SCISSORS}

        return self.translate_column(moves, move)

    def translate_column_b_naive(self, move):
        moves = { "X": ROCK,
                  "Y": PAPER,
                  "Z": SCISSORS}

        return self.translate_column(moves, move)
    
    def translate_column_b(self, move):
        moves = { "X": LOSS,
                  "Y": DRAW,
                  "Z": WIN}

        if moves[move] == DRAW:
            return self.opponent_move
        if moves[move] == WIN:
            return ((self.opponent_move % 3) +1) %3
            
        return ((self.opponent_move % 3) - 1)  %3
    
    def translate_column(self, moves, move):
        return moves[move]
                  

    def result(self):
        if self.opponent_move == self.personal_move:
            return DRAW
        if ((self.opponent_move+1) % 3)  == self.personal_move % 3:
            return WIN
        return LOSS

    def value(self):
        return (self.personal_move + 1) + self.result()


        
def read_data(datafile, naive=True):
    data = slurp_file(datafile)
    data_by_game = data.split("\n")
    games = []
    for line in data_by_game:
        if not line:
            continue
        opp_move, pers_move = line.split(" ")
        games.append(RPSGame(opp_move, pers_move, naive))
    return games

def slurp_file(filename):
    with open(filename, 'r') as f:
        contents = f.read()
    return contents

#naive: in the first part, code is not explained but assumed to be a RPS move
#in second parst (naive=False) code is desired outcome of the RPS game

naive = False
datafile = "./data/input.txt"
games = read_data(datafile, naive)
result = sum([x.value() for x in games])
print(f"total result is {result}")

                     
