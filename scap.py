import time
import datetime
import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Replace with the path to your chromedriver executable
s = Service("/path/to/chromedriver")

driver = webdriver.Chrome(service=s, options=options)
wait = WebDriverWait(driver, 10)

url = "https://chartink.com/screener/opstest-pe"

driver.get(url)

wait.until(EC.presence_of_element_located((By.ID, "DataTables_Table_0_wrapper")))

table = driver.find_element(By.ID, "DataTables_Table_0")

rows = table.find_elements(By.TAG_NAME, "tr")

email_body = ""
for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    data = []
    for cell in cells:
        data.append(cell.text.strip())
    if len(data)>0:
        email_body += f"{data[2]} - {datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5, minutes=30))).strftime('%Y-%m-%d %H:%M:%S IST')}\n"
    else:
        pass

driver.quit()

# Replace with your email and password
sender_email = "demonirmal1@gmail.com"
sender_password = "awamklmsqtgmrqsr"
receiver_email = "nethajinirmal13@gmail.com"
message = MIMEText(email_body)
message['Subject'] = "Latest data from chartink"
message['From'] = sender_email
message['To'] = receiver_email

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, message.as_string())
