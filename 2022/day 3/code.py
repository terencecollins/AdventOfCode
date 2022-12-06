import functools

class Rucksack(object):
    def __init__(self, inventory):
        midpoint = int(len(inventory)/2)
        self.inventory = inventory
        self.compartment_a, self.compartment_b = inventory[:midpoint], inventory[midpoint:]

    @classmethod
    def common_items(cls, contents):
        if len(contents) < 2:
            raise ValueError(f"common_items requires at least two items in contents, contents has length {len(contents)}")
        return functools.reduce(lambda x,y: set(x) & set(y), contents)

    @classmethod
    def item_value(cls, item):
        valuestring = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        value = valuestring.rfind(item) + 1
        return value


    @classmethod
    def common_value(cls, inventories):
        common_items = cls.common_items(inventories)
        value = 0
        for item in common_items:
            value += cls.item_value(item)
        if value == 0:
            raise RuntimeError(f"no common value in {inventories}")
        return value
    
    def compartment_share(self):
        return self.common_value([self.compartment_a, self.compartment_b])

    def __repr__(self):
        return self.inventory
    
def read_data(datafile):
    data = slurp_file(datafile)
    data_by_rucksack = data.split("\n")
    rucksacks = []
    for line in data_by_rucksack:
        if not line:
            continue
        rucksacks.append(Rucksack(line))
    return rucksacks
        
def slurp_file(filename):
    with open(filename, 'r') as f:
        contents = f.read()
    return contents

datafile = "./data/input-tst.txt"
rucksacks = read_data(datafile)
result = sum([x.compartment_share() for x in rucksacks])
print(f"shared compartment: result is {result}")
badge_cumu = 0
#CAVEAT: if rucksacks not a multiple of 3 this will be an error
for threesome_index in range(0, len(rucksacks), 3):
    threesome = rucksacks[threesome_index:threesome_index+3]
    badge_cumu += Rucksack.common_value([x.inventory for x in threesome])

print(f"badge cumulative is: {badge_cumu}")

    
        
