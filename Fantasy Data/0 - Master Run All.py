"""
SCRAPE FANTASY F1 WEBSITE

@author: Karna Malaviya
"""

# Import All Packages
import os
import time
from selenium import webdriver
import pandas as pd
from random import randint
import numpy as np
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains



# Define Constants (Add 1 for Python's Range command)
# Number of Races Elapsed
race_number = 21
race_number = race_number + 1

# Number of Teams in League
number_of_teams = 17
number_of_teams = number_of_teams + 1

# Number of Choices Made to Create a Team
number_of_choices = 5
number_of_choices = number_of_choices + 1

# Set working directory
path = "C:/Users/Karna Malaviya/Desktop/f1/scrape"
os.chdir(path)

# Define location of web driver
driver = webdriver.Chrome('C:/Users/Karna Malaviya/Desktop/f1/scrape/chromedriver.exe')  
driver.maximize_window()

# Define Action Chains
actions = ActionChains(driver)

# Define credentials
username = "karna.malaviya@gmail.com"
password = "gimmejimmy"

# Run Files
# Log In
exec(open("code/Fantasy Data/1 - Log In.py").read())

# Race Results Data
exec(open("code/Fantasy Data/2 - Race Results Data.py").read())

# Team Choices Data
exec(open("code/Fantasy Data/3 - Team Selection Data_v3.py").read())

# Prices Data
exec(open("code/Fantasy Data/4 - Prices Data_v2.py").read())