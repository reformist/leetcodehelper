from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

# for privacy concerns
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

driver = webdriver.Chrome()  # Or the appropriate driver for your browser
# optimal param: executable_path=r'C:\path\to\chromedriver.exe'

driver.get("https://leetcode.com/accounts/login/")

username = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "id_login"))
)
password = driver.find_element(By.ID, "id_password")

username.send_keys(USERNAME)
password.send_keys(PASSWORD)

driver.find_element(By.ID, "signin_btn").click()

# This is an example; the actual code might be in a different element
'''
code_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "CodeMirror-code"))
)
code_text = code_element.text
print(code_text)
'''

# navigate to the problem page (for now)
problem_slug = 'two-sum'  # Replace with the slug of the problem you want to navigate to
leetcode_url = f'https://leetcode.com/problems/{problem_slug}/'
driver.get(leetcode_url)

code_element = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'CodeMirror-code'))
)

# The code might be spread across multiple divs inside the code element.
# We need to iterate through them to reconstruct the entire code snippet.
lines = code_element.find_elements(By.XPATH, ".//span[@role='presentation']")
code_text = "\n".join([line.text for line in lines])

print(code_text)

driver.quit()