import smtplib
import requests
import os
from email.mime.text import MIMEText

CHECK_URL = "https://www.idata.com.tr/de/en"

EMAIL_FROM     = os.environ["EMAIL_FROM"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
EMAIL_TO       = os.environ["EMAIL_TO"]

BLOCK_PHRASES = [
    "sorry, you have been blocked",
    "you have been blocked",
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
}

def send_email(subject, body):
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"]    = EMAIL_FROM
    msg["To"]      = EMAIL_TO
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())

def check_site():
    try:
        response   = requests.get(CHECK_URL, headers=HEADERS, timeout=30)
        full_text  = response.text.lower()
        is_blocked = any(phrase in full_text for phrase in BLOCK_PHRASES)

        print(f"HTTP Status: {response.status_code}")

        if response.status_code == 200 and not is_blocked:
            send_email(
                "iDATA is OPEN now!",
                f"Open it NOW!\n\nURL: {CHECK_URL}"
            )
            print("OPEN - Email sent!")
        else:
            print("BLOCKED or unavailable")

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    check_site()
