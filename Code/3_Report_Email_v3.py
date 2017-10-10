"""
Searches image and document directories, creates formatted report,
emails results. Hard code project paths and run as scheduled task.
Greg Whitaker, GIS Analyst II
Lakewood, CO
2015
______________________________________________________________________________________
"""

# import module(s)
import os
import fnmatch
import smtplib
import string
import datetime

time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

# get all records in directory
imgPath = r'\\point\to\image\folder'
list = os.listdir(imgPath)
list.sort()

# get subset of mapped records
mapped = fnmatch.filter(list, '*xx*')
mapped.sort()
last = mapped[-1]

# get numbers
records = len(list)
examined = list.index(last)
remaining = records - examined
completion = round((examined + 0.0) / records, 3)

# get pdfs
pdfPath = r'\\point\to\pdf\folder'
list = os.listdir(pdfPath)
pdfList = []

for item in list:
    if item.endswith('.pdf'):
        pdfList.append(item)

pdfNum = len(pdfList)

# format output
results = """
STATE STATUS {0}\n
---------------------------------------------------------\n
Images: {1}, Examined: {2}, Mapped: {3}, Remaining: {4}\n\n

Total Documents: {5}\n\n

Total Split Estate Completion: {6}\n\n

These figures were computed and sent by the reporting robot.\n
Thanks and have a nice day!
""".format(time, records, examined, len(mapped), remaining, pdfNum, completion)

# send email containing results
SUBJECT = "FMO Auto-Report"
TO = ["recipient1@email.com", "recipient2@email.com"]
FROM = "sender@email.com"
text = results
BODY = string.join(("From: %s" % FROM,"To: %s" % TO,"Subject: %s" % SUBJECT ,"",text), "\r\n")
server = smtplib.SMTP('emailServer.com')

server.sendmail(FROM, TO, BODY)
server.quit()
