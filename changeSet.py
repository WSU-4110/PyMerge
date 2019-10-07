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

	def getChange(self, ilineNum, oChangeType, oData):
		change = changeList[0]
		oChangeType = change[0]
		oData = change[1]
		return pmEnums.RESULT.NOTIMPL

	def addChange(self, lineNum, changeType, data):
		self.changeList.append([changeType, data])

    
