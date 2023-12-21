import gspread
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient.discovery import build


# Set the path to your credentials JSON file
credentials_file = "first-project-408605-1f1b495d074d.json"


# Set the name of your Google Sheets spreadsheet
spreadsheet_name = "Testing"

# Authenticate with Google Sheets using credentials
credentials = service_account.Credentials.from_service_account_file(
    credentials_file,
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)
service = build('sheets', 'v4', credentials=credentials)
spreadsheet_id= '1HskniHuH8yZ4INrjg-vTd8VYsnT29Ns2_gF9v3_hb00'

# Get the answers from your Python variable (replace this with your actual data)
def insert_rows(data):
    # data = [[1, "answer1", "answer2",  "answer3"]]
    row=access_sheet()
    arr=[]
    data.insert(0,row)
    arr.append(data) 
    request= service.spreadsheets().values().update(
    spreadsheetId= spreadsheet_id,
    range = f"Sheet1!A{row}:D",
    valueInputOption = "RAW",
    body= {"values":arr}
    )

    response = request.execute()

def access_sheet():
    sheet=service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId= spreadsheet_id,
        range='Sheet1!A:A'
    ).execute()
    print(result)
    res = result.get('values', [])
    return len(res)+1