import pmEnums
def ChangeHelper(ilineNum1, ilineNum2,iLine1, iLine2, oChangeType):
    if(ilineNum1 != ilineNum2): # are the lines the same line
        if(checkMove(ilineNum1, ilineNum2, iLine1, iLine2)):# if not check if they have been moved
            return #moved
        else:
            return #added
    else: 
        if(iLine1 == iLine2):
           return  # no change
        else:
            return #change