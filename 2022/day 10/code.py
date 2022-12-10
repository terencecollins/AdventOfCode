from util import PuzzleObject, slurp_file

        
class PuzzleThing(PuzzleObject):
    def __init__(self, instructions):
        self.cycle = 0
        self.register = 1
        self.cycle_history = []
        self.pixels = []
        self.execute_instructions([x for x in instructions.split("\n") if x])

    def get_value_at_cycle(self, cycle):
        return self.cycle_history[cycle]

    def set_next_cycle_value(self, value):
        self.cycle += 1
        self.cycle_history.append(value)
        #set an unknown state " "
        self.pixels.append(" ")
        self.set_pixel(self.cycle, value)

    def set_pixel(self, cycle, value):
        row_position = (self.cycle - 1) % 40
        if row_position >= (value - 1) and row_position <= (value + 1):
            self.pixels[cycle-1] = "#"
        else:
            self.pixels[cycle-1] = "."
            
    def noop(self):
        self.set_next_cycle_value(self.register)
        
    def addx(self, x):
        cycle_length = 2
        for cyc_val in range(0, cycle_length):
            self.set_next_cycle_value(self.register)
        self.register += x

    def signal_strength(self, cycle, value):
        return (cycle+1) * value
    
    def execute_instructions(self, instructions):
        for instruction in instructions:
            if not instruction:
                next
            if instruction == "noop":
                self.noop()
            else:
                function, value = instruction.split(" ")
                #right now only function is addx
                self.addx(int(value))
        return
            
    def result(self):
        sssum = 0
        for cnum in range(19, 259, 40):
            sssum += self.signal_strength(cnum, self.cycle_history[cnum])

        return sssum

    def draw_crt(self):
        for pixnum, pixel in enumerate(self.pixels, 1):
            if not ((pixnum-1) % 40):
                print(f"\n", end="")
            print(f"{pixel}", end="")
        print("\n")
        
def main():
    datafile = "./data/input.txt"
    puzzle_a = PuzzleThing(slurp_file(datafile))
    result_a = puzzle_a.result()
    print(f"result 1 is {result_a}")
    print(f"result 2:\n")
    puzzle_a.draw_crt()

if __name__ == "__main__":
    main()
