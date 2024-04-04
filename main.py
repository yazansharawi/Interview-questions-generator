from openai import OpenAI
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import config
from email_utils import send_email

openai_client = OpenAI(api_key=config.OPENAI_API_KEY)

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('google_sheets_credentials.json', scope)
gspread_client = gspread.authorize(creds)
sheet = gspread_client.open_by_key(config.SHEET_KEY).sheet1
data = sheet.get_all_records()


email_count = 0
for person in data:
    name = person['Name']
    email = person['Email']
    bio = person['Bio']

    prompt = f"Based on this bio, generate a few relevant interview questions for {name}: {bio}"
    res = openai_client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )

    questions = res.choices[0].message.content
    send_email(name, email, questions) 
    email_count += 1

print(email_count, "emails sent successfully") 
