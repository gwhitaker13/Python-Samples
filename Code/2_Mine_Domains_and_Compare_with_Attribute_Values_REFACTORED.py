"""
Extracts geodatabase domain information and compares to exisiting attribute values, 
reports inconsistencies
Greg Whitaker, GIS Analyst II
Lakewood, CO
2017
______________________________________________________________________________________
"""

# build main function
def main(*args):
	# import module(s)
	import arcpy

	# get arguments
	fc = arcpy.GetParameterAsText(0)
	gdb = arcpy.GetParameterAsText(1)

	# get all gdb domians, all fc fields
	allDomains = arcpy.da.ListDomains(gdb)
	allFields = arcpy.ListFields(fc)

	# put subset of allFields that have a domain in dict
	fcFieldsDomains = {field.name : field.domain for field in allFields if field.domain}

	# put subset of allDomains and respective values in list
	listDomainsValues = []
	for domain in allDomains:
		if domain.name in fcFieldsDomains.values() and domain.domainType == 'CodedValue':
			for val, desc in domain.codedValues.items():
				listDomainsValues.append([domain.name, val])

	# format new subset as a dict structure for use in main operation
	fcDomainsValues = {}
	for line in listDomainsValues:
		if line[0] in fcDomainsValues:
			fcDomainsValues[line[0]].append(line[1])
		else:
			fcDomainsValues[line[0]] = [line[1]]

	# iterate over each row, compare table value to respective field domain values
	fields = fcFieldsDomains.keys()
	with arcpy.da.SearchCursor(fc, fields) as cursor:
		for row in cursor:
			index = range(len(fields))

			for i, field in enumerate(fields):
				tableValue = row[i]
				dKey = fcFieldsDomains.get(field) # resolve key error using .get()
				codedValues = fcDomainsValues.get(dKey) # same here

				if tableValue <> None and tableValue not in codedValues:
					arcpy.AddWarning('\n{0}: {1}'.format(field, tableValue))
					for codedValue in codedValues:
						arcpy.AddWarning('    {0}'.format(codedValue))

# execute main
if __name__ == '__main__':
    argv = tuple(arcpy.GetParameterAsText(i) for i in range(arcpy.GetArgumentCount()))
    main(*argv)
