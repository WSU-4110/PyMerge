
from copy import deepcopy

"""
Undo function can be implemented by keeping a buffer of each row array. That is, each time a change is made, the list containing
all the row class instances is deep copied to a list containing the last n number of row copies. If undo is selected, the 
undo index is recorded and that copy of the array is used to replace the current working version. The current working version
is then copied to a redo buffer. 
"""


class Stack(object):
    def __init__(self, stack_size):
        self.max_size = stack_size
        self.stack = []

    def push(self, item):
        if len(self.stack) < self.max_size:
            self.stack.append(item)

    def pop(self):
        if len(self.stack) > 0:
            obj = self.stack.pop()
            return obj
        return None

    def _size(self):
        return len(self.stack)


class Undo(object):
    def __init__(self, buf_size):
        self.redo_buf = Stack(buf_size)
        self.undo_buf = Stack(buf_size)

        for n in range(buf_size):
            self.redo_buf.push(None)
            self.undo_buf.push(None)

    def undo(self, current_row_list):
        undo_obj = self.undo_buf.pop()

        if undo_obj is not None:
            self.redo_buf.push(deepcopy(current_row_list))
            current_row_list = deepcopy(undo_obj)
            return True
        return False

    def redo(self, current_row_list):
        undo_obj = self.redo_buf.pop()

        if undo_obj is not None:
            self.undo_buf.push(deepcopy(current_row_list))
            current_row_list = deepcopy(undo_obj)
            return True
        return False
