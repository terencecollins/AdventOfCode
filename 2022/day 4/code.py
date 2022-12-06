from util import PuzzleObject, read_data

class PuzzleThing(PuzzleObject):
    def __init__(self, range_strings):
        self.a1, self.a2 = range_strings.split(",")
        self.assign1 = self.expand_range(self.a1)
        self.assign2 = self.expand_range(self.a2)
        super().__init__(range_strings)
        
    def result_b(self):
        if self.sets_overlap(self.assign1, self.assign2):
            return 1
        return 0

    def result_a(self):
        if self.set_is_contained(self.assign1, self.assign2):
            return 1
        return 0

def main():
    datafile = "./data/input.txt"
    inputs = read_data(datafile, PuzzleThing)
    result_a = sum([x.result_a() for x in inputs])
    print(f"result 1 is {result_a}")
    result_b = sum([x.result_b() for x in inputs])
    print(f"result 2 is {result_b}")

if __name__ == "__main__":
    main()
