import openpyxl

workbook = openpyxl.Workbook()

sheet = workbook.active

user_info = {
    "name": "John Doe",
    "age": 30,
    "address": "123 Main Street"
}
import openpyxl

workbook = openpyxl.Workbook()

sheet = workbook.active


sheet["A1"] = 'First Name'
sheet["B1"] = 'Second name'
sheet["C1"] = 'Age'

sheet["A2"] = 'Jasur'
sheet["A3"] = 'Usmon'
sheet["A4"] = 'Behruz'
sheet["A5"] = 'Ibrohim'

sheet["B2"] = 'Zokirov'
sheet["B3"] = 'Umidullaxonov'
sheet["B4"] = 'Jorayev'
sheet["B5"] = 'Komilov'

sheet["C2"] = '15'
sheet["C3"] = '10'
sheet["C4"] = '15'
sheet["C5"] = '15'

workbook.save('users.xlsx')