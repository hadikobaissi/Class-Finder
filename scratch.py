from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# Email setup
email_user = ''  # Your email
email_password = ''  # Your email password
email_send = ''  # Recipient's email

# Set up the path to ChromeDriver
driver_path = r'C:\Users\hkoba\Downloads\chromedriver.exe' # replace with your own path to chromedriver
service = Service(driver_path)
options = Options()
driver = webdriver.Chrome(service=service, options=options)

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_user, email_password)
    server.sendmail(email_user, email_send, text)
    server.quit()

try:
    driver.get("https://coursebook.utdallas.edu/guidedsearch")

    while True:
        try:
            # Select dropdown options
            instructor = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "combobox_instructor"))
            )
            selectI = Select(instructor)

            number = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "combobox_cnum"))
            )
            selectNum = Select(number)

            prefix = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "combobox_cp"))
            )
            selectP = Select(prefix)

            selectP.select_by_visible_text("CS - Computer Science") # replace this with whatever the course starts with
            selectNum.select_by_visible_text("3377") # replace this with course number
            selectI.select_by_visible_text("Dollinger, Scott") # replace this with professor name

            search_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Search Classes']"))
            )

            time.sleep(3)
            search_button.click()

            sections = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//span[contains(@class, 'section-closed') or contains(@class, 'section-open')]"))
            )

            for section in sections:
                status_text = section.text
                print(f"Section status: {status_text}")

                # Send an email if the section is open
                if "Open" in status_text:
                    print("Found an open section!")
                    send_email("Class Section Open", f"A section has opened in CS 3377: {status_text}")

        except Exception as e:
            print("Error checking section status:", e)

        time.sleep(150)  # Check every 2.5 minutes
        driver.refresh()

finally:
    driver.quit()
