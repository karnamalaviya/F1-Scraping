"""
SCRAPE HISTORICAL F1 DATA

@author: Karna Malaviya
"""

# Import packages
import os
import time
import datetime
from selenium import webdriver
import pandas as pd
from random import randint
from datetime import date

driver = webdriver.Chrome("C:/Users/karna/1_Projects/Formula1/scrape/chromedriver.exe")  

# Set working directory
path = "C:/Users/karna/1_Projects/Formula1/scrape/"
os.chdir(path)

# 1 - Open Home Webpage with All Results
race_urls = pd.read_csv("input/race_urls_for_loop.csv")

# 2 - Create Shell Dataframes for Race, Starting Grid, Qualy, and Starting Grid Results
race_df = pd.DataFrame()
grid_df = pd.DataFrame()
qualy_df = pd.DataFrame()
pit_df = pd.DataFrame()
nodata = pd.DataFrame()

# 3 - Note Today's Date: We Can Only Data for Races that have Happened
today = date.today()
sleep_min = 3
sleep_max = 5

# 4 - Run Through URLs for Each Race to Scrape Race Data
start = time.time()
race_urls = race_urls[race_urls.index.isin([38])]
for i, row in race_urls.iterrows():
    season = row['season']
    season = str(season)
    url    = row['race_url'] 
            
    # 4.1 - Go to Race Results Page
    driver.get(url)
    driver.maximize_window()   
    time.sleep(randint(2,4))
    
    # 4.2 - Dismiss Potential Pop-Up
    try : 
        driver.find_element_by_xpath("//*[contains(text(), 'Accept All')]").click()
    except : 
        pass
    try : 
        driver.find_element_by_xpath("//*[contains(@class, 'overlay-close')]").click()
    except :  
        pass

    # 4.3 - Collect Race Weekend Demographic Data
    circuit = driver.find_element_by_xpath("//*[contains(@class, 'circuit-info')]").get_attribute("innerText") 
    name = driver.find_element_by_xpath("//*[contains(@class, 'ResultsArchiveTitle')]").get_attribute("innerText")
    name = name.replace('- RACE RESULT', '').strip()
    race_date = driver.find_element_by_xpath("//*[contains(@class, 'full-date')]").get_attribute("innerText")     
    race_date = time.strptime(race_date, "%d %b %Y")
    race_date = datetime.date(year = race_date[0], month = race_date[1], day = race_date[2])
    race_date_str = str(race_date)
    
    # 4.3 Collect Data from Past Race Weekends
    if today > race_date : 

        # 4.3.1 - Store Race Results
        try : 
            driver.find_element_by_xpath("//*[contains(@data-value, 'race-result')]").click()
            time.sleep(randint(sleep_min, sleep_max))
            temp = pd.read_html(driver.page_source)[0]
            temp = temp.dropna(how = 'all', axis = 'columns')
            # temp.columns=['position', 'number', 'name', 'constructor', 'laps_completed', 'time', 'points'] # Drop This For Generality. Deal with Inconsistent Formatting later
            temp['track']    = circuit
            temp['date']     = race_date
            temp['datatype'] = 'race'
            
            # Append Race Results
            race_df = race_df.append(temp)
            print('Race Data Scraped For ' + name + ' on ' + race_date_str)
        
        except : 
            row['race']     = name
            row['season']   = season
            row['datatype'] = 'race'
            nodata = nodata.append(row)
            print('No Race Data For ' + name + ' on ' + race_date_str)

        # 4.3.2 - Store Starting Grid
        try : 
            driver.find_element_by_xpath("//*[contains(@data-value, 'starting-grid')]").click()
            time.sleep(randint(sleep_min, sleep_max))
            temp = pd.read_html(driver.page_source)[0]
            temp = temp.dropna(how = 'all', axis = 'columns')
            # temp.columns=['grid_position', 'number', 'name', 'constructor', 'qualy_time'] # Drop This For Generality. Deal with Inconsistent Formatting later
            temp['track']    = circuit
            temp['date']     = race_date
            temp['datatype'] = 'starting_grid'
            
            # Append Race Results
            grid_df = grid_df.append(temp)
            print('Starting Grid Data Scraped For ' + name + ' on ' + race_date_str)
        
        except : 
            row['race']     = name
            row['season']   = season
            row['datatype'] = 'starting_grid'
            nodata = nodata.append(row)
            print('No Starting Grid Data For ' + name + ' on ' + race_date_str)
            
        # 4.3.3 - Store Qualifying Data
        try : 
            driver.find_element_by_xpath("//*[contains(@data-value, 'qualifying')]").click()
            time.sleep(randint(sleep_min, sleep_max))
            temp = pd.read_html(driver.page_source)[0]
            temp = temp.dropna(how = 'all', axis = 'columns')
            # temp.columns=['qualy_position', 'number', 'name', 'constructor', 'qualy_time'] # Drop This for Generality. Deal with Inconsistent Formatting later
            temp['track']    = circuit
            temp['date']     = race_date
            temp['datatype'] = 'qualifying'
            
            # Append Race Results
            qualy_df = qualy_df.append(temp)
            print('Qualifying Data Scraped For ' + name + ' on ' + race_date_str)
        
        except : 
            row['race']     = name
            row['season']   = season
            row['datatype'] = 'qualy'
            nodata = nodata.append(row)
            print('No Qualy Data For ' + name + ' on ' + race_date_str)

        # 4.3.4 - Store Pit Stop Data
        try : 
            driver.find_element_by_xpath("//*[contains(@data-value, 'pit-stop-summary')]").click()
            time.sleep(randint(sleep_min, sleep_max))
            temp = pd.read_html(driver.page_source)[0]
            temp = temp.dropna(how = 'all', axis = 'columns')
            # temp.columns=['qualy_position', 'number', 'name', 'constructor', 'qualy_time'] # Drop This for Generality. Deal with Inconsistent Formatting later
            temp['track']    = circuit
            temp['date']     = race_date
            temp['datatype'] = 'pit_stop'
            
            # Append Race Results
            pit_df = pit_df.append(temp)
            print('Pit Stop Data Scraped For ' + name + ' on ' + race_date_str)
        
        except : 
            row['race']     = name
            row['season']   = season
            row['datatype'] = 'pit_stop'
            nodata = nodata.append(row)
            print('No Pit Stop Data For ' + name + ' on ' + race_date_str)

    else : 
        print(name + ' race on ' + race_date_str + ' has yet to occur')

driver.close() 
print((time.time() - start) / 60)

# 5 - Export Results as .csv
today_str = str(today)
dfs = {"race"          : race_df
     , "starting_grid" : grid_df
     , "qualifying"    : qualy_df
     , "pit_stops"     : pit_df}

for label, dataframe in dfs.items():
    dataframe.to_csv("raw/" + label + "_results_" + today_str + ".csv", index = False)
    
# 6 - Data Validation

# Most Missing Data is for Pit Stops
nodata.groupby(['datatype'])['datatype'].count()

# Among Non-Pit Stops...
nodata_nopit = nodata[nodata['datatype'] != 'pit_stop']

# Confirmed Occassional unavailability of Starting grid data in the 50's, Lack of Qualy Data for 1967 Belgian GP
nodata_nopit.groupby(['season','datatype'])['datatype'].count()

# 2020 Abu Dhabi is Concerning...



nodata.groupby(['datatype'])['datatype'].count()

nodata.groupby(['season']).count()



