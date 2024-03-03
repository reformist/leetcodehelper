from selenium import webdriver

driver = webdriver.Chrome()  # Ensure ChromeDriver is in your PATH or specify its path as an argument
driver.get("https://leetcode.com/accounts/login/")

username = driver.find_element_by_id("id_login")
password = driver.find_element_by_id("id_password")
submit = driver.find_element_by_xpath('//button[@type="submit"]')

username.send_keys("your_username")
password.send_keys("your_password")
submit.click()