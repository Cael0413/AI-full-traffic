import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

def add_to_sheet(user_id, user_message, tag="諮詢"):
    creds = ServiceAccountCredentials.from_json_keyfile_name("your-credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("LINE客戶留言紀錄").sheet1
    sheet.append_row([user_id, user_message, tag])
