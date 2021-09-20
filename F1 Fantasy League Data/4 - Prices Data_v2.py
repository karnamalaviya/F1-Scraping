"""
SCRAPE FANTASY F1 WEBSITE

@author: Karna Malaviya
"""

# Import packages
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from random import randint
import numpy as np
import re

#  Define information for URLs
url = "https://fantasy.formula1.com/edit-team/slot/1"

#  Create dataset of fantasy results
prices = pd.DataFrame()

# Open Driver to Team Selection Page
driver.get(url)


# Create Path to Prices List to Scroll Down With
time.sleep(randint(3,5))
scroll_xpath = "//div[contains(@id, 'ember') and contains(@class, 'list-wrapper')]"
time.sleep(randint(3,5))
driver.find_element_by_xpath(scroll_xpath).click()

# Define Number of Times to do Down Arrow:
for x in range(1, 9):
    
    # Get 10 results in the list
    for y in range(1, 11):

    # For the first entry, set xpath of first row    
        if y == 1 : 
           prices_xpath = "//div[contains(@id, 'ember') and contains(@class, 'double-row')]"
    
        # Otherwise, use Sibling
        else:
           prices_xpath = prices_xpath + "//following-sibling::div[contains(@id, 'ember') and contains(@class, 'double-row')]" 
    
        # Clean Scraped Price
        time.sleep(randint(1,3))
        temp_prices = driver.find_element_by_xpath(prices_xpath)
        temp_prices = temp_prices.get_attribute("innerText")
        temp_prices = re.sub("\s\s+" , " ", temp_prices)
        temp_prices = re.sub(" Pts" , "Pts", temp_prices)
        temp_prices = temp_prices.strip().replace('. ', '')
        temp_prices = temp_prices.replace('Red Bull', 'RedBull') \
        .replace('Alfa Romeo', 'AlfaRomeo').replace('Racing Point', 'RacingPoint') \
        .replace('Toro Rosso', 'ToroRosso')
        temp_prices = temp_prices.split()
        temp_prices = list(filter(None, temp_prices))    
        temp_prices = pd.DataFrame({'raw' : temp_prices})
        temp_prices['id'] = 1
        temp_prices['col'] = temp_prices.index + 1
        temp_prices = temp_prices.pivot(index='id', columns = 'col', values='raw')   
        temp_prices.columns=['type', 'team_name', 'team_name_abrev', 'points', 'price', 'share_owned']
        prices = prices.append(temp_prices)
    
    # Scroll Down Before Proceding to Next Element
    driver.find_element_by_xpath(scroll_xpath).click()
    actions.send_keys(Keys.ARROW_DOWN).perform()

# Do the same with opposite sorted list
time.sleep(randint(3,5))
driver.get(url)
time.sleep(randint(3,5))
# Sort to opposite list
sort_xpath = "//*[contains(@class, 'sort-icon')]"
driver.find_element_by_xpath(sort_xpath).click()
time.sleep(randint(3,5))
# Click on scroll bar
driver.find_element_by_xpath(scroll_xpath).click()

# Define Number of Times to do Down Arrow:
for x in range(1, 9):
    
    # Get 10 results in the list
    for y in range(1, 11):

    # For the first entry, set xpath of first row    
        if y == 1 : 
           prices_xpath = "//div[contains(@id, 'ember') and contains(@class, 'double-row')]"
    
        # Otherwise, use Sibling
        else:
           prices_xpath = prices_xpath + "//following-sibling::div[contains(@id, 'ember') and contains(@class, 'double-row')]" 
    
        # Clean Scraped Price
        time.sleep(randint(1,3))
        temp_prices = driver.find_element_by_xpath(prices_xpath)
        temp_prices = temp_prices.get_attribute("innerText")
        temp_prices = re.sub("\s\s+" , " ", temp_prices)
        temp_prices = re.sub(" Pts" , "Pts", temp_prices)
        temp_prices = temp_prices.strip().replace('. ', '')
        temp_prices = temp_prices.replace('Red Bull', 'RedBull') \
        .replace('Alfa Romeo', 'AlfaRomeo').replace('Racing Point', 'RacingPoint') \
        .replace('Toro Rosso', 'ToroRosso')
        temp_prices = temp_prices.split()
        temp_prices = list(filter(None, temp_prices))    
        temp_prices = pd.DataFrame({'raw' : temp_prices})
        temp_prices['id'] = 1
        temp_prices['col'] = temp_prices.index + 1
        temp_prices = temp_prices.pivot(index='id', columns = 'col', values='raw')   
        temp_prices.columns=['type', 'team_name', 'team_name_abrev', 'points', 'price', 'share_owned']
        prices = prices.append(temp_prices)
    
    # Scroll Down Before Proceding to Next Element
    driver.find_element_by_xpath(scroll_xpath).click()
    actions.send_keys(Keys.ARROW_DOWN).perform()


# Drop Duplicates To Get 30 Results
prices = prices.drop_duplicates()  

# Clean Names for Export
#Constructor Names
prices['team_name'] = prices['team_name'].str.replace('RedBull', 'Red Bull')\
.str.replace('AlfaRomeo', 'Alfa Romeo').str.replace('RacingPoint', 'Racing Point')\
.str.replace('ToroRosso', 'Toro Rosso')

# Driver Names 
prices['team_name'] = np.where(prices['type'] == 'DR', prices['team_name'].str[0] + ". " + prices['team_name'].str[1:], prices['team_name'])

#Export data as csv
prices = prices.reset_index(drop=True)

pricescsv = "raw/2019_prices" + ".csv"
prices.to_csv(pricescsv, index = False)

driver.close()