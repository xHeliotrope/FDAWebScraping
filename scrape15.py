from bs4 import BeautifulSoup as bs
import urllib.request
import csv

with urllib.request.urlopen('http://www.fda.gov/BiologicsBloodVaccines/DevelopmentApprovalProcess/BiologicalApprovalsbyYear/ucm434961.htm') as url:
    s = url.read()

soup = bs(s, "html.parser")
drugs = []


table = soup.find("tbody")
for row in table.findAll("tr"):
    cells = row.findAll("td")
    try:
        tradename = cells[0].find("strong").text.strip()
    except AttributeError:
        tradename = ""
    try:
        my_extract = cells[0].a.replace_with('')	
        subname = cells[0].text.strip()
    except AttributeError:
        subname = "None"
    comp = cells[3].findAll(text=True)
    cells = [ele.text.strip() for ele in cells]
    drug = [tradename, subname, cells[1], cells[2], cells[4]]
    company = [x for x in comp]
    x = 4 - len(company)
    i = 0
    while(x > i):
        company.insert(1, '')
        x -= 1
        print("prepended empty address line")
    drug.extend(company)
    drugdic = {"Tradename": drug[0], "Propername": drug[1], "Indication": drug[2], "STN": drug[3], "Approval Date": drug[4], "Manufacturer": drug[5], "Address1":drug[6], "Address2":drug[7], "License No":drug[8]}
    drugs.append(drugdic)


with open('2015drugs.csv', 'w', newline='') as csvfile:
    fieldnames = ['Tradename', 'Propername', 'Indication', 'STN', 'Approval Date', 'Manufacturer', 'Address1', 'Address2', 'License No']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter= ',')
    writer.writeheader()
    for x in drugs:
        print(x)
        writer.writerow(x)
