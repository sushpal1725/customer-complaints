import csv
from decimal import *

productComplaints = {}

with open('complaints.csv', 'r') as csvfile:
    complaintsReader = csv.reader(csvfile, delimiter=',')
    complaintsReader.next()
    for row in complaintsReader:
        productName = row[1].lower()
        date = row[0].split('-')[0]
        companyName = row[7]
        uniqueIdentity = productName + '-' + date

        if productComplaints.has_key(uniqueIdentity):
            productComplaint = productComplaints[uniqueIdentity]
            productCompanies = productComplaint["companies"]
            if productCompanies.has_key(companyName):
                productCompanies[companyName] = productCompanies[companyName] + 1
            else:
                productCompany = { companyName : 1 }
                productCompanies.update(productCompany)
        else:
            productComplaint = { uniqueIdentity: { "date": date, "companies": { companyName : 1 } } }
            productComplaints.update(productComplaint)
with open('report.csv', 'w') as outputFile:
    writer = csv.writer(outputFile, delimiter=',')
    for eachKey in productComplaints:
        uniqueIdentity = eachKey.split('-')
        productName = uniqueIdentity[0]
        date = uniqueIdentity[1]
        totalComplaints = 0
        totalComapaniesWithComplaints = 0
        productCompanies = productComplaints[eachKey]["companies"]
        highestComplaintsPerCompany = 0
        for eachCompany in productCompanies:
            complaints = productCompanies[eachCompany]
            if complaints > 0 :
                totalComplaints = totalComplaints + complaints
                totalComapaniesWithComplaints = totalComapaniesWithComplaints + 1
                if complaints > highestComplaintsPerCompany:
                    highestComplaintsPerCompany = complaints
        percentage = int(round((Decimal(highestComplaintsPerCompany)/Decimal(totalComplaints)) * 100))
        writer.writerow([productName, date, totalComplaints, totalComapaniesWithComplaints, percentage])
