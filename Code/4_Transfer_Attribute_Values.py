"""
Transfers attribues between two unjoined tabes based on key values. 
Created to optimize performance, transfer values without a database join.
Greg Whitaker, GIS Analyst II
Lakewood, CO
2017
______________________________________________________________________________________
"""

# import module(s)
import arcpy 

# get parameters
sourceFC = arcpy.GetParameterAsText(0)
sourceKeyField = arcpy.GetParameterAsText(1)
sourceField = arcpy.GetParameterAsText(2)

updateFC = arcpy.GetParameterAsText(3)
updateKeyField = arcpy.GetParameterAsText(4)
updateField = arcpy.GetParameterAsText(5)

sourceFieldsList = [sourceKeyField, sourceField]
# use comprehension to build a dictionary from a da.SearchCursor
valueDict = {(r[0]):(r[1]) for r in arcpy.da.SearchCursor(sourceFC, sourceFieldsList)}

updateFieldsList = [updateKeyField, updateField]
# iterate over rows and update field values with contents of dictionary
with arcpy.da.UpdateCursor(updateFC, updateFieldsList) as rows:
    for row in rows:
        if row[0] in valueDict:
            row[1] = valueDict[row[0]]
            rows.updaterow(row)

del valueDict
