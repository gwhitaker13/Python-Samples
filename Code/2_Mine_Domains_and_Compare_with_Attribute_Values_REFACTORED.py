def checkDomainValues(fc, gdb):
	"""
	mine field domains and compare coded values to existing values.

	ex:
	errors = checkDomainValues(fc, gdb)
	returns {field name : [objectid,...]}

	use objectids to select/rectify bad values.
	full geoprocessing tool to come.
	"""

	# get all gdb domians, all fc fields
	allDomains = arcpy.da.ListDomains(gdb)
	allFields = arcpy.ListFields(fc)

	# put subset of allFields that have a domain in dict
	fcFieldsDomains = {field.name : field.domain
					   for field in allFields
					   if field.domain}

	# get subset of allDomains and respective values-REFACTORED
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

	# compare table value to respective field domain values-REFACTORED
	oidFields = ['OBJECTID'] + fcFieldsDomains.keys()
	errors = {}
	with arcpy.da.SearchCursor(fc, oidFields) as cursor:
		for row in cursor:
			# get all fields and indicies
			for i, field in enumerate(oidFields):
				oid = row[0]
				tableValue = row[i]
				# exclude oid field from loop, chain fields/domains to get coded values
				if field <> 'OBJECTID':
					dKey = fcFieldsDomains.get(field) # resolve key error using .get()
					codedValues = fcDomainsValues.get(dKey) # same here
					# exclude nulls and evaluate, put errors in dictionary
					if tableValue <> None and tableValue not in codedValues:
						if field in errors:
							errors[field].append(oid)
						else:
							errors[field] = [oid]

	# return dictionary {field name : [objectid,...]}
	return errors
