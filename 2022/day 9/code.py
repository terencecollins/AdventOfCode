from util import PuzzleObject, slurp_file

class Knot(PuzzleObject):
    def __init__(self, pos_x, pos_y):
        self.pos_x = 0
        self.pos_y = 0
        self.history = [(self.pos_x, self.pos_y)]
        self.dv = {
            "U": (self.mod_y, 1),
            "D": (self.mod_y, -1),            
            "R": (self.mod_x, 1),
            "L": (self.mod_x, -1),}
        super().__init__(pos_x, pos_y)

        
    def move(self, direction, amount):
        for i in range(0, amount):
            self.dv[direction][0](amount * self.dv[direction][1])
            self.update_pos_history()
            
    def set_pos(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.update_pos_history()
        
    def mod_y(self, amount):
        self.pos_y += amount
        
    def mod_x(self, amount):
        self.pos_x += amount

    def update_pos_history(self):
        self.history.append((self.pos_x, self.pos_y))
        
class PuzzleThing(PuzzleObject):
    def __init__(self, num_knots, movements):
        self.num_knots = num_knots
        self.knots = []
        for knot in range(self.num_knots):
            self.knots.append(Knot(0,0))

        self.head = self.knots[0]
        self.tail = self.knots[self.num_knots - 1]
        self.execute_movements([x for x in movements.split("\n") if x])

    def execute_movements(self, movements):
        for movement in movements:
            if not movement:
                next
            direction, amount = movement.split(" ")

            #print(f"\n\n== {direction} {amount} ==\n")
            for i in range(0, int(amount)):
                self.move_head(direction, 1)
                for knotnum in range(1, self.num_knots):
                    self.move_tailknot(self.knots[knotnum], self.knots[knotnum - 1])
                #self.display_rope_grid()
            
    def move_head(self, direction, amount):
        self.head.move(direction, amount)

    def move_tailknot(self, tail, head):
        head_x = head.pos_x
        head_y = head.pos_y
        tail_x = tail.pos_x
        tail_y = tail.pos_y

        if abs(head_x - tail_x) > 1 and abs(head_y - tail_y) > 1:
            tail_x = self.calc_diff(head_x, tail_x)
            tail_y = self.calc_diff(head_y, tail_y)
        else:
            if abs(head_x - tail_x) > 1:
                tail_x = self.calc_diff(head_x, tail_x)
                if tail_x != tail.pos_x:
                    #if only x has moved, then Y should match head
                    tail_y = head_y
            if abs(head_y - tail_y) > 1:            
                tail_y = self.calc_diff(head_y, tail_y)
                if tail_y != tail.pos_y:
                    #if only Y has moved, then X should match head
                    tail_x = head_x
        tail.set_pos(tail_x, tail_y)
        
    def calc_diff(self, head_val, tail_val):
        if tail_val < head_val:
            return head_val - 1
        if tail_val > head_val:
            return head_val + 1

    def display_rope_grid(self):
        print("\n\n")
        for y in range(5, -1, -1):
            for x in range(0, 6):
                occupied = False
                for knotnum in range(0, self.num_knots):
                    if self.knots[knotnum].pos_y == y and self.knots[knotnum].pos_x == x:
                        if knotnum == 0:
                            knotnum = "H"
                        print(f"{knotnum}", end="")
                        occupied = True
                        break
                if not occupied:
                    print(f".", end="")
            print("\n", end="")
            
    def result(self):
        unique_tail_positions = set(self.tail.history)
        return len(unique_tail_positions)
    
def main():
    datafile = "./data/input.txt"
    puzzle_a = PuzzleThing(2, slurp_file(datafile))
    result_a = puzzle_a.result()
    print(f"result 1 is {result_a}")
    puzzle_b = PuzzleThing(10, slurp_file(datafile))
    result_b = puzzle_b.result()
    print(f"result 2 is {result_b}")

if __name__ == "__main__":
    main()
