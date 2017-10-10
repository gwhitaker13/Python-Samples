"""
Finds all RAW files and extracts contents to geodatabase tables.
Geodatatbase table used as GCDB_Points_to_Lines.py input
Greg Whitaker, GIS Analyst II
Lakewood, CO
2017
______________________________________________________________________________________
"""

#import modules
import os
import csv
import arcpy

#step 1: get paths to all .RAW files
arcpy.AddMessage('\nFinding .RAW files\n')
top = arcpy.GetParameterAsText(0)
rawList = []
for root, dirs, filenames in os.walk(top):
     for filename in filenames:
         if filename.endswith('.RAW') or filename.endswith('.raw'):
             rawList.append(os.path.join(root, filename))

#step 2: convert to csv with headers and save outputs to directory
arcpy.AddMessage('Formatting and saving .CSV files\n')
outFolder = arcpy.GetParameterAsText(1)
for rawPath in rawList:
	partOne = rawPath.split('\\')[-4] + rawPath.split('\\')[-3][-2:]
	partTwo = rawPath.split('\\')[-2][1:3]
	partThree = rawPath.split('\\')[-2][3].upper()
	partFour = rawPath.split('\\')[-2][4:6]
	partFive = rawPath.split('\\')[-2][-1].upper()
	try:
		plssid =  '{0}0{1}0{2}0{3}0{4}0'.format(partOne, partTwo, partThree, partFour, partFive)
	except:
		arcpy.AddMessage('Index error. Cannot save {0}\n'.format(rawPath))

	outPath = '{}\\{}.csv'.format(outFolder, plssid)
	with open(rawPath, 'rb') as raw, open(outPath , 'wb') as out:
		reader = csv.reader(raw, delimiter=' ')
		next(reader) #skip first three header rows
		next(reader) #
		next(reader) #
		writer = csv.writer(out, delimiter=',')
		writer.writerow(['FromPointID', 'ToPointID', 'ChainLength', 
		'Quadrant', 'Bearing', 'SurveyID']) #write header first
		for row in reader:
		    toWrite = [x for x in row if x <> '']
		    writer.writerow(toWrite)


#step 3: convert csv to gdb table and modify values
arcpy.AddMessage('Creating geodatabase and importing .CSV files\n')
csvList = os.listdir(outFolder)

arcpy.CreateFileGDB_management(outFolder, 'MASTER')
gdb = outFolder + '\\MASTER.gdb'
arcpy.env.workspace = gdb

for table in csvList:
	inPath = outFolder + '\\' + table
	outName = table.split('.')[0]
	arcpy.TableToTable_conversion(inPath, gdb, outName)

uTableList = arcpy.ListTables() #had trouble with unicode output
tableList = [str(t) for t in uTableList] #converted to string here
for table in tableList:
	exp1 = '"' + table + '"'
	arcpy.AddField_management(table, 'PLSSID', "TEXT",'','',50)
	arcpy.CalculateField_management(table, 'PLSSID', exp1, "PYTHON")

#step 4: merge tables and perform final calculations
arcpy.AddMessage('Merging tables\n')
arcpy.Merge_management(tableList, 'RAW_Master_Table') #can't use list brackets on input

temps = [['fromTemp', 'FromPointID'], ['toTemp', 'ToPointID']]
for temp in temps:

	arcpy.AddField_management('RAW_Master_Table', temp[0], "TEXT",'','',50)
	exp2 = '!' + temp[1] + '!'  
	arcpy.CalculateField_management('RAW_Master_Table', temp[0], exp2, "PYTHON")
	arcpy.DeleteField_management('RAW_Master_Table', temp[1])

	arcpy.AddField_management('RAW_Master_Table', temp[1], "TEXT",'','',50)
	exp3 = "!PLSSID! + '_' + !{0}!".format(temp[0])
	arcpy.CalculateField_management('RAW_Master_Table', temp[1], exp3, "PYTHON")
	arcpy.DeleteField_management('RAW_Master_Table', temp[0])
