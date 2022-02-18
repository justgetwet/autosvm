import gspread
from google.oauth2.service_account import Credentials


def input_sheet(data):
    scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
    credentials = Credentials.from_service_account_file("token.json", scopes=scope)

    gc = gspread.authorize(credentials)

    SPREADSHEET_KEY = '1OUtQYK76rSXTbLgLDl-l0o1er8VsuzVZ42jrWZdx11o'
    workbook = gc.open_by_key(SPREADSHEET_KEY)

    worksheets = workbook.worksheets()
    sheet = worksheets[2]
    sheet.append_row([data, data])
    sheet.update_cell(2, 3, data)

input_sheet(123)