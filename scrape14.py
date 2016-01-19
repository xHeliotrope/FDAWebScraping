from bs4 import BeautifulSoup as bs
import urllib.request
import csv

with urllib.request.urlopen('http://www.fda.gov/BiologicsBloodVaccines/DevelopmentApprovalProcess/BiologicalApprovalsbyYear/ucm385847.htm') as url:
    s = url.read()

soup = bs(s, "html.parser")
drugs = []

first_rows = 0

table = soup.find("tbody")
for row in table.findAll("tr"):
    cells = row.findAll("td")
    tradename = ""
    subname = ""
    names = cells[0].findAll("p")
    if len(names) == 1:
        subname = names[0].text
    else:
        try:
            tradename = names[0].find("strong").text.strip()
        except AttributeError:
            tradename = names[0].find("a").text.strip()
        subname = names[1].text.strip()

    comp = cells[3].findAll(text=True)
    cells = [ele.text.strip() for ele in cells]
    drug = [tradename, subname, cells[1], cells[2], cells[4]]
    company = [x for x in comp]
        
    if first_rows < 3:
        del company[-1]
    first_rows += 1

    x = 4 - len(company)
    i = 0
    while(x > i):
        company.insert(1, '')
        x -= 1
        #print("prepended empty address line")
    if len(company) == 5:
        company[2:4] = [' '.join(company[2:4])]

    drug.extend(company)
    drugdic = {
        "Tradename": drug[0], "Propername": drug[1], "Indication": drug[2], 
        "STN": drug[3], "Approval Date": drug[4], "Manufacturer": drug[5], 
        "Address1":drug[6], "Address2":drug[7], "License No":drug[8]
    }
    drugs.append(drugdic)


with open('2014drugs.csv', 'w', newline='') as csvfile:
    fieldnames = ['Tradename', 'Propername', 'Indication', 'STN', 
        'Approval Date', 'Manufacturer', 'Address1', 'Address2', 'License No']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter= ',')
    writer.writeheader()
    for x in drugs:
        writer.writerow(x)
