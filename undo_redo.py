from copy import deepcopy
import threading

"""
Undo function can be implemented by keeping a buffer of each state change. That is, each time a change is made, 
the row state is  copied to a list containing the last n number of row copies. If undo is selected, the 
undo index is recorded and that copy of the row state is used to replace the current working version. The current working version
is then copied to a redo buffer. 
"""


class Stack(object):
    def __init__(self, stack_size: int):
        self.max_size: int = stack_size
        self.stack = []

    def stack_push(self, item):
        # Check if stack is full, then append the object onto the end
        if len(self.stack) < self.max_size or self.max_size == -1:
            self.stack.append(item)
        else:
            self.__rotate()
            self.stack[-1] = item

    def __rotate(self):
        # Move the stack up, "forgetting" the oldest undo or redo move
        for n in range(1, len(self.stack)):
            self.stack[n - 1] = self.stack[n]

    def stack_pop(self):
        # Check if stack is empty, then pop the top object
        return self.stack.pop()
        # if len(self.stack) > 0:
        #     return self.stack.pop()
        # return None

    def _size(self):
        return len(self.stack)


class UndoRedoAction(object):
    __slots__ = [
        "obj_copy",
        "obj_ref",
        "row_obj",
        "row_num",
        "table",
        "left_text",
        "right_text",
        "line_num",
        "right_background_color",
        "left_background_color",
    ]

    def __init__(self, row_obj):
        self.obj_copy = deepcopy(row_obj)
        self.obj_ref = row_obj
        # self.row_obj = row_obj
        # self.row_num = row_obj.row_num
        # self.table = row_obj.table
        # self.right_text = row_obj.right_text
        # self.left_text = row_obj.left_text
        # self.right_background_color = row_obj.right_background_color
        # self.left_background_color = row_obj.left_background_color

    def set_state(self):
        """
        Set the current state of the row object to what was recorded in the instance variables
        :return: No return value
        """
        # self.table.item(self.row_num, 1).setBackground(self.right_background_color)
        # self.table.item(self.row_num, 4).setBackground(self.left_background_color)
        # self.table.item(self.row_num, 1).setText(self.right_text)
        # self.table.item(self.row_num, 4).setText(self.left_text)

        self.obj_ref = self.obj_copy


class UndoRedo(object):
    __instance = None

    @staticmethod
    def get_instance(buf_size=15):
        if UndoRedo.__instance is None:
            UndoRedo(buf_size)
        return UndoRedo.__instance

    def __init__(self, buf_size):
        if UndoRedo.__instance is not None:
            raise Exception("Only a single instance of UndoRedo is allowed!")
        else:
            self.redo_buf = Stack(buf_size)
            self.undo_buf = Stack(buf_size)
            UndoRedo.__instance = self

    def set_buf_size(self, buf_size: int):
        self.undo_buf.max_size = buf_size
        self.redo_buf.max_size = buf_size

    def record_action(self, row_obj):
        record_obj = UndoRedoAction(row_obj)
        self.undo_buf.stack_push(deepcopy(record_obj))
        #print(self.undo_buf.stack)

    def undo(self):
        undo_obj = self.undo_buf.stack_pop()  # Get the state we want to set
        #redo_obj = UndoRedoAction(undo_obj.obj_)  # Record the current state

        # Check if object is None, then push the recorded current state.
        if undo_obj is not None:
            self.redo_buf.stack_push(deepcopy(undo_obj))

        # Restore the state to what was popped
            undo_obj.set_state()
            return True
        return False

    def redo(self):
        redo_obj = self.undo_buf.stack_pop()
        #undo_obj = UndoRedoAction(redo_obj.row_obj)

        # Check if object is None, then push the recorded current state.
        if redo_obj is not None:
            self.undo_buf.stack_push(deepcopy(redo_obj))

            # Restore the state to what was popped
            redo_obj.set_state()
            return True
        return False

"""
        self.row_obj = row_obj
        self.row_num = row_obj.row_num
        self.table = row_obj.table
        self.right_text = row_obj.right_text
        self.left_text = row_obj.left_text
        self.right_background_color = row_obj.right_background_color
        self.left_background_color = row_obj.left_background_color
"""


class Test(object):
    def __init__(self, num):
        self.num = num

    def set_num(self, num):
        self.num = num


# a, b, c, d, e, f, g = Test(1), Test(2), Test(3), Test(4), Test(5), Test(6), Test(7)
#
# undo_redo_ctrlr = UndoRedo(4)
#
# undo_redo_ctrlr.record_action(a)
# a.set_num(2)
# print("a = ", a.num)
#
# undo_redo_ctrlr.record_action(a)
# b.set_num(2)
# print("b = ", b.num)
#
# undo_redo_ctrlr.record_action(a)
# a.set_num(4)
# print("a = ", a.num)
#
# undo_redo_ctrlr.undo()
# print("a = ", a.num)
#
# undo_redo_ctrlr.record_action(a)
# c.set_num(2)
# print("c = ", c.num)
#
# undo_redo_ctrlr.undo()
# print("a = ", a.num)
#
# print(f"Undo Stack")
# for n in range(len(undo_redo_ctrlr.undo_buf.stack)):
#     print(undo_redo_ctrlr.undo_buf.stack[n], "\t", undo_redo_ctrlr.undo_buf.stack[n].obj_ref.num)
#
# print(f"\nRedo Stack")
# for n in range(len(undo_redo_ctrlr.redo_buf.stack)):
#     print(undo_redo_ctrlr.redo_buf.stack[n], "\t", undo_redo_ctrlr.redo_buf.stack[n].obj_ref.num)

# undo_redo_ctrlr.undo()