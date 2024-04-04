import smtplib
import ssl
import config

def send_email(name, email, questions):
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as server:
            server.ehlo()
            server.starttls(context=context)
            server.login(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)

            message = f"""Subject: Interview Questions Tailored to Your Background

                Dear {name},

                I hope this email finds you well.

                I came across your bio and was inspired to generate a few interview questions that might be helpful based on your experience:

                {questions}

                I hope these questions assist you in your interview preparation.  

                Best regards,
                Yazan Sharawi
            """

            server.sendmail(config.EMAIL_ADDRESS, email, message)

    except smtplib.SMTPException as error:
        print(f"Error sending email to {email}: {error.strerror}")
