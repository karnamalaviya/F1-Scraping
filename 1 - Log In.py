"""
SCRAPE FANTASY F1 WEBSITE

@author: Karna Malaviya
"""

# Import packages
import time
from selenium import webdriver
from random import randint
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


#  Define Log on URL
url_login = "https://account.formula1.com/#/en/login?redirect=https%3A%2F%2Ffantasy.formula1.com%2F"

#  Open Driver window to F1 Login Page
driver.get(url_login)

# Enter Username and Password
time.sleep(randint(3,5))
driver.find_element_by_xpath("//*[contains(@name, 'Login')]").send_keys(username)
driver.find_element_by_xpath("//*[contains(@name, 'Password')]").send_keys(password)
time.sleep(randint(3,5))

# Click Submit
actions.send_keys(Keys.PAGE_DOWN).perform()
time.sleep(randint(3,5))
driver.find_element_by_xpath("//*[contains(@type, 'submit')]").click()
time.sleep(randint(3,5))
