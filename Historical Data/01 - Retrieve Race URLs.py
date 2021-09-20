"""
CREATE LIST OF F1 RACE URLS TO SCRAPE FROM

@author: Karna Malaviya
"""

%reset

# Import packages
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from random import randint
import datetime
from datetime import date

driver = webdriver.Chrome("C:/Users/karna/1_Projects/Formula1/scrape/chromedriver.exe")  

# Set working directory
path = "C:/Users/karna/1_Projects/Formula1/scrape/"
os.chdir(path)

# 1 - Open Home Webpage with All Results
start = time.time()
home_url = "https://www.formula1.com/en/results.html"
driver.get(home_url)
driver.maximize_window()   
time.sleep(randint(1,3))
driver.find_element_by_xpath("//*[contains(text(), 'Accept All')]").click()

# 2 - Create Dataframe with URLs to Individual Season Results
season_urls = pd.DataFrame()
temp = driver.find_elements_by_xpath("//*[contains(@class, 'resultsarchive-filter ResultFilterScrollable')]")
temp = temp[0].find_elements_by_tag_name('a')
counter = 1
for x in temp:
    temp_url = x.get_attribute('href')
    temp_url = pd.DataFrame({'season_url' : temp_url}, index = [counter])
    season_urls = season_urls.append(temp_url)
    counter = counter + 1

season_urls['season'] = season_urls['season_url'].str.extract('([1,2][0,1,9][0-9][0-9])').astype(int)

# 3 - Loop Through Each Season's Results, Retrieving Links to Individual Race Results
race_urls = pd.DataFrame()
for i, row in season_urls.iterrows():
    season = row['season']
    url    = row['season_url']
    print("Retrieving Links to Races from " + str(season) + " Season.")
    
    # 3.1 - Dismiss Possible Pop-Up
    driver.get(url)
    time.sleep(randint(1,3))
    try : 
        driver.find_element_by_xpath("//*[contains(text(), 'Accept All')]").click()
    except : 
        pass
    try : 
        driver.find_element_by_xpath("//*[contains(@class, 'overlay-close')]").click()
    except : 
        pass
    
    # 3.2 - Create Dataframe of Race Links from Given Season
    temp_df = pd.DataFrame()
    temp = driver.find_elements_by_xpath("//*[contains(@class, 'resultsarchive-filter ResultFilterScrollable')]")
    temp = temp[2].find_elements_by_tag_name('a')
    counter = 1
    for x in temp:
        temp_url = x.get_attribute('href')
        temp_url = pd.DataFrame({'race_url' : temp_url}, index = [counter])
        temp_url['season'] = season
        temp_url['season_url'] = url
        temp_df = temp_df.append(temp_url)
        counter = counter + 1
    
    # 3.3 - Append to Dataframe Combining All Seasons
    race_urls = race_urls.append(temp_df)

print((time.time() - start) / 60)
driver.close()

# 4 - Clean Appended Dataframe
race_urls = race_urls[['season', 'season_url', 'race_url']]
race_urls = race_urls[race_urls['race_url'].str.contains('/race-result.html', na = False)]

# 5 - Export as .csv File
race_urls.reset_index(drop = True, inplace = True)
race_urls.to_csv("input/race_urls_for_loop.csv", index = False)
