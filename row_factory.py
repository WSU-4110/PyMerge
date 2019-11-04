import pmEnums
import table_row
import undo_redo
import hashlib
import gui_config as gui_cfg

class RowFactory():
    def __init__(self):
        """
        Factory to either instantiate a row instance, or find the reference to an already
        instantiated one via hash.
        """
        super().__init__()
        self.table: QTableWidget
        self.hashTable: list = []
        self.rows: list = []

    def getRow(self, line_numR, table, right_text,
               left_text, line_numL, change_flags):

        stringIn = right_text + left_text        
        n = 0
        line_hash = 0
        while n < len(stringIn):            
            line_hash += ord(stringIn[n])
            n += 1
            
        print("\n\n\nhash: " + str(line_hash) )
        print( "right "+ right_text + "\n" +"left " + left_text)
        
        n = 0
        if change_flags[1] == pmEnums.CHANGEDENUM.SAME and change_flags[0] == pmEnums.CHANGEDENUM.SAME:
            while n < len( self.hashTable ):            
                if line_hash == self.hashTable[n]:                
                    print("row replicated at line" + str(line_numR))
                    print("left:   " + self.rows[n].left_text + "\nright:   " + self.rows[n].right_text + "\nchangedType:   " + str(self.rows[n].change_state_flags[1])  )
                    self.table = table
                    self.table.item(line_numR, gui_cfg.RIGHT_TXT_COL_IDX).setBackground(gui_cfg.COLORS["ROW_DEFAULT"])
                    self.table.item(line_numL, gui_cfg.LEFT_TXT_COL_IDX).setBackground(gui_cfg.COLORS["ROW_DEFAULT"])
                    
                    return self.rows[n]
                n += 1

        print("row instantiated")
        row_instance = table_row.Row(
            line_numR, table, right_text, left_text, line_numL, change_flags
            )
        self.hashTable.append(line_hash)
        row_instance.actual_indices[0] = line_numL
        row_instance.actual_indices[1] = line_numR
        self.rows.append(row_instance)
                
        return row_instance
        
            
        
