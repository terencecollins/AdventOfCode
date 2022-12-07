from util import PuzzleObject, slurp_file
import re

class DirObject(PuzzleObject):
    def __init__(self, name, parent_dir=None):
        self.name = name
        self.parent_dir = parent_dir
        self.indent_str = "\t"
        super().__init__(name, parent_dir)

    def get_depth(self):
        depth = 0
        current_ancestor = self.parent_dir
        while current_ancestor:
            depth += 1
            current_ancestor = current_ancestor.parent_dir
        return depth
    
class DirItem(DirObject):
    def __init__(self, name, parent_dir=None, items=None):

        self.items = []
        if items:
            self.items = items
        self.update_size()
        super().__init__(name, parent_dir)

    def recursive_scan(self, item, scan_target):
        if type(item) is DirItem:
            for sus_item in item.items:
                if sus_item == self:
                    return True
                if self.recursive_scan(sus_item, self):
                    return True
        return False
    
    def add_item(self, item):
        if not item:
            raise ValueError("Non-existant (None) item added to {self}")
        
        #scan the item to prevent circular references
        if self.recursive_scan(item, self):
            raise ValueError("item {item} contains {self}")
        item.parent_dir = self
        self.items.append(item)
        self.update_size()
        has_parent = self.parent_dir
        while has_parent:
            has_parent.update_size()
            has_parent = has_parent.parent_dir

    def find_dir(self, dir_name):
        for item in self.items:
            if type(item) is DirItem:
                if item.name == dir_name:
                    return item
        return None
    
    def update_size(self):
        if self.items:
            self.size = sum(i.size for i in self.items)
        else:
            self.size = 0

    def get_subdirs(self):
        subdirs = []
        for item in self.items:
            if type(item) is DirItem:
                subdirs.append(item)
        return subdirs
    
    def str_tree(self):
        depth = self.get_depth()
        print(f"{self.indent_str*depth}- {self.name} (dir, size={self.size})")
        for item in self.items:
            item.str_tree()
            
    def __str__(self):
        return f"{self.name} (dir, size={self.size})"

    def __repr__(self):
        return f"{self.name} (dir, size={self.size})"
    
class FileItem(DirObject):
    def __init__(self, name, size, parent_dir=None):
        self.size = size
        super().__init__(name, parent_dir)

    def str_tree(self):
        depth = self.get_depth()
        print(f"{self.indent_str*depth}- {self.name} (file, size={self.size})")
        
    def __str__(self):
        return f"{self.name} (file, size={self.size})"
        
class PuzzleThing(PuzzleObject):
    def __init__(self, terminal_output):
        self.terminal_output = terminal_output
        self.root_dir = DirItem("/", parent_dir=None, items=None)
        self.current_dir = self.root_dir

        self.parse_output(self.terminal_output)
        
        super().__init__(terminal_output)

    def parse_output(self, output):
        for line in output.split("\n"):
            if line:
                self.parse_line(line)
                
    def parse_line(self, line):
        if re.match(r"^\$", line):
            self.parse_command(line)
        if re.match(r"^dir", line):
            itemtype, name = line.split(" ")
            new_dir = DirItem(name)
            self.current_dir.add_item(new_dir)
        if re.match(f"^\d+", line):
            itemsize, name = line.split(" ")
            self.current_dir.add_item(FileItem(name, int(itemsize)))
        return


    def parse_command(self, command):
        prompt,command = command.split(" ",1)
        if command.startswith("cd"):
            arg = command.split(" ", 1)[1]
            if arg == "/":
                self.current_dir = self.root_dir
            elif arg == "..":
                self.current_dir = self.current_dir.parent_dir
            else:
                self.current_dir = self.current_dir.find_dir(arg)
        if command == "ls":
            pass
        return


    def find_candidate_dirs(self, target_dir, target_size = 100000):
        candidate_dirs = []
        for subd in target_dir.get_subdirs():
            if subd.size < 100000:
                candidate_dirs.append(subd)
            candidate_dirs.extend(self.find_candidate_dirs(subd))
        return candidate_dirs

    def find_candidate_deletion_dirs(self, target_dir, target_size = 100000):
        candidate_dirs = []
        for subd in target_dir.get_subdirs():
            if subd.size > target_size:
                candidate_dirs.append(subd)
            candidate_dirs.extend(self.find_candidate_deletion_dirs(subd, target_size))
        return candidate_dirs
    
    def result_a(self):
        candidate_dirs = self.find_candidate_dirs(self.root_dir)
        return sum(smdir.size for smdir in candidate_dirs)

    def result_b(self):
        total_space = 70000000
        needed_space = 30000000
        current_unused_space = total_space - self.root_dir.size
        need_to_delete = needed_space - current_unused_space
        
        candidate_dirs = self.find_candidate_deletion_dirs(self.root_dir, target_size = need_to_delete)
        smallest_to_del = sorted(candidate_dirs, key=lambda x: x.size)[0]
        return smallest_to_del.size
        
    def str_tree(self):
        self.root_dir.str_tree()
    
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
