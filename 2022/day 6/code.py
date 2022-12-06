from util import PuzzleObject, slurp_file

class PuzzleThing(PuzzleObject):
    def __init__(self, datastream):
        self.datastream = datastream
        self.marker_size = 4
        self.message_size = 14
        super().__init__(datastream)
        
    def result_b(self):
        return self.find_pos(self.message_size)

    def result_a(self):
        return self.find_pos(self.marker_size)

    def find_pos(self, chunk_size):
        #break the stream into 4-char chunks
        position = 0
        next_pos = 0
        next_chunk = "xxxx"
        while next_chunk and not self.matches_signal(next_chunk):
            position = next_pos
            next_chunk, next_pos = self.get_next_chunk(position, chunk_size)
            #print(f"position: {position}, next_chunk: {next_chunk}, next_pos = {next_pos}")

        return position + chunk_size
        
    def get_next_chunk(self, position, chunk_size):
        return self.datastream[position:position + chunk_size], self.get_next_position(position)

    def get_next_position(self, position):
        return position + 1

    def matches_signal(self, chunk):
        els = [*chunk]
        #print(f"els: {els}, list set els: {list(set(els))}")
        if sorted(els) == sorted(list(set(els))):
            return True
        return False

def main():
    datafile = "./data/input.txt"
    device = PuzzleThing(slurp_file(datafile))
    result_a = device.result_a()
    print(f"result 1 is {result_a}")
    result_b = device.result_b()
    print(f"result 1 is {result_b}")

if __name__ == "__main__":
    main()
