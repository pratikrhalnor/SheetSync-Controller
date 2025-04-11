import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Setup the credentials and client
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

# Open the spreadsheet
sheet = client.open("ThreadingDataSheet").sheet1

# Write and read a test value
sheet.update_acell("A1", "Hello from Python!")
value = sheet.acell("A1").value
print("✅ Sheet says:", value)
