"""
Module with simple algorithms for common tasks
Greg Whitaker, GIS Analyst II
Lakewood, CO
2017
______________________________________________________________________________________
"""

# Select multipart features
def selectMultipartRecords(fc):
	# make a list of multipart feature OIDs
	multipartRecords = []
	with arcpy.da.SearchCursor(fc, ["OBJECTID", "SHAPE@"]) as cursor:
		for row in cursor:
			if row[1].isMultipart:
				multipartRecords.append(row[0])
	# select all OIDs in list			
	for record in multipartRecords:
		arcpy.SelectLayerByAttribute_management(fc, "ADD_TO_SELECTION", "OBJECTID = {0}".format(record))


# Check value lengths
def checkValueLength(fc, field, length):
	with arcpy.da.SearchCursor(fc, ["OBJECTID", field]) as cursor:
		for row in cursor:
			if len(row[1]) <> length:
				print row[0], row[1], len(row[1])


# Check PLSSID w/SecondDivision value
def plssidMismatch(fc, plssid, secdivno):
	with arcpy.da.SearchCursor(fc, ["OBJECTID", plssid, secdivno]) as cursor:
		for row in cursor:
			if (row[2] is not None) or (row[2] <> ''):
				i = len(row[2])
				if row[1][-i:] <> row[2]:
					print row[0], row[1], row[2]
			else:
				pass

# Print all gdb domains
def printDomains(gdb):
	domains = arcpy.da.ListDomains(gdb)
	for domain in domains:
	    print('\n\nDomain name: {0}'.format(domain.name))
	    if domain.domainType == 'CodedValue':
	        coded_values = domain.codedValues
	        for val, desc in coded_values.items():
	            print('{0} : {1}'.format(val, desc))
	    elif domain.domainType == 'Range':
	        print('Min: {0}'.format(domain.range[0]))
	        print('Max: {0}'.format(domain.range[1]))
