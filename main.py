from openai import OpenAI
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import smtplib
import ssl
import config

openai_client = OpenAI(api_key=config.OPENAI_API_KEY)

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('google_sheets_credentials.json', scope)
gspread_client = gspread.authorize(creds)
sheet = gspread_client.open_by_key(config.SHEET_KEY).sheet1
data = sheet.get_all_records()


def send_email(name, email, questions):
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as server:
            server.ehlo()
            server.starttls(context=context)
            server.login(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)

            message = f"""Subject: Interview Questions Based on Your Bio
            Dear {name},

            Here are a few interview questions tailored to your bio:

            {questions}

            Best Regards,
            Daddy
            """

            server.sendmail(config.EMAIL_ADDRESS, email, message)

    except smtplib.SMTPException as error:
        print(f"Error sending email to {email}: {error}")


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
