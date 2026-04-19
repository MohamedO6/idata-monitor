import os
import asyncio
import smtplib
from email.mime.text import MIMEText
from playwright.async_api import async_playwright

CHECK_URL = "https://www.idata.com.tr/de/en"

EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")

BLOCK_PHRASES = [
    "sorry, you have been blocked",
    "blocked"
]

def send_email(subject, body):
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            await page.goto(CHECK_URL, wait_until="domcontentloaded", timeout=60000)
            await page.wait_for_timeout(5000)

            body_text = await page.locator("body").inner_text()
            full_text = body_text.lower()

            is_blocked = any(phrase in full_text for phrase in BLOCK_PHRASES)

            if not is_blocked:
                send_email(
                    "iDATA is open now",
                    f"The blocked message was NOT found.\n\nURL: {CHECK_URL}\n\nCheck the website now."
                )
                print("OPEN")
            else:
                print("BLOCKED")

        except Exception as e:
            print(f"ERROR: {e}")

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
