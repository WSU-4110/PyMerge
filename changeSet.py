"""
changeSet class, provides a data structure to make working with file differences (change sets)
easier by abstracting the data storage, and providing a single accessor function.
"""
import pmEnums

# class Change:
# 	def __init__(self, lineNum, changeType, data):
# 		self.lineNum = lineNum
# 		self.changeType = changeType
# 		self.data = data	
    
class ChangeSet:

	changeList = []

	def __init__(self):
		pass
    
	def getChange( self, ilineNum, oChangeType, oData ):
		oreturnObj[0] = pmEnums.CHANGEDENUM.CHANGED
		return pmEnums.RESULT.NOTIMPL

	def setChange(self, lineNum, changeType, data):
		self.changeList.append((lineNum, changeType, data))

    #some private list to store all the strings at easy line numbers
    

    
