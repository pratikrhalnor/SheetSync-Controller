import threading
import time
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("ThreadingDataSheet").sheet1  # Your Google Sheet name

# Global flag
stop_thread1 = False

# Writer Thread
def thread1_writer():
    global stop_thread1
    count = 1
    while not stop_thread1:
        value = f"Data {count} at {datetime.datetime.now().strftime('%H:%M:%S')}"
        print(f"📝 Thread 1: Writing to A3 → {value}")
        try:
            sheet.update('A3', [[value]])  # ✅ FIXED: Use list of lists
        except Exception as e:
            print("❌ Error writing to A3:", e)
        count += 1
        time.sleep(2)

# Reader Thread
def thread2_reader():
    global stop_thread1
    while True:
        try:
            a5_value = sheet.acell('A5').value
            print(f"🔍 Thread 2: Read A5 = {a5_value}")
            if a5_value == '1':
                stop_thread1 = True
                print("♻️ Restarting Thread 1!")
                time.sleep(2)
                stop_thread1 = False
                threading.Thread(target=thread1_writer).start()
                sheet.update('A5', [[0]])  # ✅ FIXED: Use list of lists
        except Exception as e:
            print("❌ Error reading A5:", e)
        time.sleep(3)

# Start both threads
threading.Thread(target=thread1_writer).start()
threading.Thread(target=thread2_reader).start()
