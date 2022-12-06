class PuzzleObject(object):
    def __init__(self, *args, **kwargs):
        super().__init__()

    def set_is_contained(self, a, b):
        return ((a <= b) or (b <= a))

    def sets_overlap(self, a, b):
        if a & b:
            return True
        return False

    def result_a(self):
        pass

    def result_b(self):
        pass

    def expand_range(self, range_string, range_separator="-"):
        #returns a set  based on the range string
        start, end = range_string.split(range_separator)
        expansion = set(range(int(start), int(end)+1))
        return expansion
    
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

def slurp_file(filename):
    with open(filename, 'r') as f:
        contents = f.read()
    return contents

