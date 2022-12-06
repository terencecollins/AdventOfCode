#from operator import attrgetter

class Elf(object):
    def __init__(self, position, caloric_list):
        self.position = position
        self.caloric_list = caloric_list
        self.caloric_sum = sum(caloric_list)
        
    def __str__(self):
        return f"Elf #{self.position}: {self.caloric_sum}"
    
def read_data(datafile):
    data = slurp_file(datafile)
    data_by_elf = data.split("\n\n")
    elves = []
    for position, data in enumerate(data_by_elf,1):
        elves.append(Elf(position,[int(x) for x in data.split("\n") if x]))
    return elves
        
def slurp_file(filename):
    with open(filename, 'r') as f:
        contents = f.read()
    return contents

datafile = "./data/input.txt"        
elves = read_data(datafile)
elves.sort(key=lambda x: x.caloric_sum, reverse=True)
top_n = 3
top_n_sum = 0
top_n_elves = elves[:top_n]
#max_calorie_elf = max(elves, key=attrgetter("caloric_sum"))
max_calorie_elf = elves[0]
for elf in top_n_elves:
    top_n_sum += elf.caloric_sum
    print(elf)

    

print(f"top_n_sum: {top_n_sum}")

