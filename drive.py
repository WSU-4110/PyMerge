import pmEnums
import changeSet

cs = changeSet.changeSet
obj = [pmEnums.CHANGEDENUM.SAME]
cs.access( 1, pmEnums.ATTRIB.DATA, obj )

print ( obj[0] )
