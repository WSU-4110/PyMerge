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

class ChangeSet(object):

	def __init__(self):
		self.changeList: list = []
		self.change_set_ready: bool = False
		pass

	def getChange(self, ilineNum, oChangeType, oData ):
		change = self.changeList[ilineNum]
		oChangeType[0] = change[1]
		oData[0] = change[2]
		return pmEnums.RESULT.NOTIMPL

	def addChange(self, lineNum, changeType, data):
		self.changeList.append((lineNum, changeType, data))


# change_set = ChangeSet()