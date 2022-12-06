from util import PuzzleObject, slurp_file
import re

class PuzzleThing(PuzzleObject):
    def __init__(self, stack_input, instructions):
        self.stacks = self.stacks_as_lists(stack_input)
        self.instructions = [i for i in instructions.split("\n") if i]
        super().__init__()


    def stacks_as_lists(self, stack_input):
        column_length = 4
        rows = []
        stacks = []
        stack_input_lines = stack_input.split("\n")
        #init stacks as a bunch of empty lists
        for i in range(int((len(stack_input_lines[0]) + 1) / column_length)):
                       stacks.append(list())
                       
        for position, line in enumerate(stack_input_lines[0:-1]):
            rows.append([line[i:i+column_length] for i in range(0, len(line), column_length)])

            #now turn into columns
            for col_num, crate in enumerate(rows[-1]):
                crate_value = crate.replace("[","").replace("]","").replace(" ","")
                if crate_value:
                    stacks[col_num].append(crate_value)

        for stack in stacks:
            stack.reverse()

        return stacks

    def exec_instructions(self, exec_routine):
        inst_pattern = re.compile(r"move (?P<amount>\d+) from (?P<source>\d+) to (?P<destination>\d+)$")
        for num, instruction in enumerate(self.instructions, 1):
            m = inst_pattern.search(instruction)
            if not m:
                raise ValueError(f"Bad instruction on line {num}")
            else:
                try:
                    amount = int(m.group("amount"))
                    source = int(m.group("source"))
                    destination = int(m.group("destination"))
                except IndexError as e:                    
                    raise ValueError(f"Bad instruction on line {num}")
            exec_routine(amount, source, destination)
        
    def exec_instructions_a(self):
        self.exec_instructions(self.exec_instruction_a)

    def exec_instructions_b(self):
        self.exec_instructions(self.exec_instruction_b)
        
    def exec_instruction_a(self, amount, source, destination):
        amount = (-1 * amount)
        self.stacks[destination-1].extend(reversed(self.stacks[source-1][amount:]))
        self.stacks[source-1][amount:] = []


    def exec_instruction_b(self, amount, source, destination):
        amount = (-1 * amount)
        self.stacks[destination-1].extend(self.stacks[source-1][amount:])
        self.stacks[source-1][amount:] = []
        
    def result_a(self):
        self.exec_instructions_a()
        result = "".join(stack[-1] for stack in self.stacks)
        return result
    
    def result_b(self):
        self.exec_instructions_b()
        result = "".join(stack[-1] for stack in self.stacks if stack)
        return result


def read_data(datafile, ThingieClass, split_string="\n", additional_func=None):
    data = slurp_file(datafile)
    data_by_thingie = data.split("\n")
    thingies = []
    for line in data_by_thingie:
        if not line:
            continue
        if additional_func:
            thingies.append(ThingieClass(additional_func(line)))
        else:
            thingies.append(ThingieClass(line))
    return thingies
    
def main():
    datafile = "./data/input.txt"
    data = slurp_file(datafile)
    stack_input, instructions = data.split("\n\n")
    pz = PuzzleThing(stack_input, instructions)
    result_a = pz.result_a()
    print(f"result 1 is {result_a}")
    pz = PuzzleThing(stack_input, instructions)
    result_b = pz.result_b()
    print(f"result 2 is {result_b}")

if __name__ == "__main__":
    main()
