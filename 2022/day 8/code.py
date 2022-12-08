from util import PuzzleObject, slurp_file

class Tree(PuzzleObject):
    def __init__(self, value, row, column):
        self.value = value
        self.row = row
        self.column = column
        self.visible = None
        self.scenic_score = 0
        super().__init__(value, row, column)
        
    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __eq__(self, other):
        return self.value == other.value
    
class PuzzleThing(PuzzleObject):
    def __init__(self, tree_data):
        self.trees = []
        self.terminal_matrix = self.parse_data(tree_data)
        super().__init__(tree_data)

    def parse_data(self, data):
        for row, line in enumerate(data.split("\n")):
            if line:
                self.trees.append([Tree(value, row, column) for column, value in enumerate(list(line))])

        for row in self.trees:
            for this_tree in row:
                self.set_tree_visible_and_score(this_tree)
                
    def set_tree_visible_and_score(self, tree):
        row = tree.row
        column = tree.column
        #edges always visible
        if row == 0 or column == 0 or row == len(self.trees[0]) - 1 or column == len(self.trees) - 1:
            tree.visible = True
            tree.scenic_score = 0
                                
        tree.visible = self.interior_tree_visible(row,column)
        tree.scenic_score = self.interior_tree_score(row,column)
        
    def interior_tree_visible(self, row, column):
        if self.interior_tree_visible_up(row, column) or self.interior_tree_visible_down(row, column) or self.interior_tree_visible_left(row, column) or self.interior_tree_visible_right(row, column):
            return True
        return False

    def interior_tree_score(self, row, column):
        return(self.interior_tree_score_up(row, column) * self.interior_tree_score_down(row, column) * self.interior_tree_score_left(row, column) * self.interior_tree_score_right(row, column))

    def tallest_in_line(self, tree, line_trees):
        for line_tree in line_trees:
            if not tree > line_tree:
                return False
        return True

    def interior_tree_count(self, tree, line_trees):
        tree_count = 0
        for line_tree in line_trees:
            tree_count += 1
            if not tree > line_tree:
                return tree_count
        return tree_count

    def get_trees_up(self, row, column):
        return reversed([trow[column] for trow in self.trees[:row]])

    def get_trees_down(self, row, column):
        return [trow[column] for trow in self.trees[row+1:]]

    def get_trees_left(self, row, column):
        return reversed([tree for tree in self.trees[row][:column]])

    def get_trees_right(self, row, column):
        return [tree for tree in self.trees[row][column+1:]]
        
    def interior_tree_visible_up(self, row, column):
        line_trees = self.get_trees_up(row, column)
        return self.tallest_in_line(self.trees[row][column], line_trees)
    
    def interior_tree_visible_down(self, row, column):
        line_trees = self.get_trees_down(row, column)
        return self.tallest_in_line(self.trees[row][column], line_trees)
    
    def interior_tree_visible_left(self, row, column):
        line_trees = self.get_trees_left(row, column)
        return self.tallest_in_line(self.trees[row][column], line_trees)

    def interior_tree_visible_right(self, row, column):
        line_trees = self.get_trees_right(row, column)
        return self.tallest_in_line(self.trees[row][column], line_trees)

    def interior_tree_score_up(self, row, column):
        line_trees = self.get_trees_up(row, column)
        return self.interior_tree_count(self.trees[row][column], line_trees)
    
    def interior_tree_score_down(self, row, column):
        line_trees = self.get_trees_down(row, column)
        return self.interior_tree_count(self.trees[row][column], line_trees)
    
    def interior_tree_score_left(self, row, column):
        line_trees = self.get_trees_left(row, column)
        return self.interior_tree_count(self.trees[row][column], line_trees)

    def interior_tree_score_right(self, row, column):
        line_trees = self.get_trees_right(row, column)
        return self.interior_tree_count(self.trees[row][column], line_trees)
    
    def result_a(self):
        visible_trees = [tree for row in self.trees for tree in row if tree.visible]
        return(len(visible_trees)) 

    def result_b(self):
        highest_score = max([tree.scenic_score for row in self.trees for tree in row])
        return highest_score
    
def main():
    datafile = "./data/input.txt"
    device = PuzzleThing(slurp_file(datafile))
    result_a = device.result_a()
    #device.str_tree()
    print(f"result 1 is {result_a}")
    result_b = device.result_b()
    print(f"result 2 is {result_b}")

if __name__ == "__main__":
    main()
