import openpyxl

workbook = openpyxl.Workbook()

sheet = workbook.active


sheet["A1"] = 'First Name'
sheet["B1"] = 'Second name'
sheet["C1"] = 'Age'

sheet["A2"] = 'Jasur'
sheet["A3"] = 'Usmon'

sheet["B2"] = 'Zokirov'
sheet["B3"] = 'Umidullaxonov'

sheet["C2"] = '15'
sheet["C3"] = '10'

workbook.save('data.xlsx')