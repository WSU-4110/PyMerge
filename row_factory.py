import pmEnums
import table_row
import undo_redo
import hashlib

class RowFactory():
    def __init__(self):
        """
        Factory to either instantiate a row instance, or find the reference to an already
        instantiated one via hash.
        """
        
        self.hashTable: list = []
        self.rows: list = []

    def getRow(self, line_numR, table, right_text,
               left_text, line_numL, change_flags):
        
        line_hash = hashlib.md5((right_text + left_text).encode('utf-8'))

        if change_flags[0] == pmEnums.CHANGEDENUM.SAME and change_flags[1] == pmEnums.CHANGEDENUM.SAME:
            for n in self.hashTable:
                if line_hash == self.hashTable[n]:
                    return rows[n]

        
        row_instance = table_row.Row(
            line_numR, table, right_text, left_text, line_numL, change_flags
            )
        return row_instance
        
            
        
