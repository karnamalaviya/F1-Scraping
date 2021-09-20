"""
SCRAPE FANTASY F1 WEBSITE

@author: Karna Malaviya
"""

# Create dataset of fantasy results
fantasy = pd.DataFrame()

# Define URLs
url = "https://fantasy.formula1.com/leaderboards/league?league_id=19778"

# Open Driver to League Standings Page
driver.get(url)

#  Scrape Results
for x in range(1, race_number):
    
    x = 1
    x = str(x)
    
    #  Go to League Website and click on dropdown
    time.sleep(randint(3,5))
    driver.find_element_by_xpath(("//*[contains(@id, 'dropdownMenu')]")).click()
    time.sleep(randint(3,5))

    # Create xpath for the race
    race_xpath = "//ul[contains(@class, 'dropdown-menu')]//li[@class = '" + x + "']"
    # Get Race Name
    race_name = driver.find_element_by_xpath(race_xpath)
    race_name = race_name.get_attribute("innerText")
    race_name = race_name.strip()
    
    # Get Fantasy Results for the Race
    time.sleep(randint(1,5))
    driver.find_element_by_xpath(race_xpath).click()
    time.sleep(randint(3,5))
    
    results = driver.find_element_by_xpath("//*[contains(@class, 'stripped-list')]")
    
    # Store and Clean Results
    temp_fantasy = results.get_attribute('innerText')    
    temp_fantasy = temp_fantasy.replace('(ver)stappen4nobody', 'verstappen4nobody').replace('karn on d kob(e bryan)', 'karn on d kobe bryan')
    temp_fantasy = temp_fantasy.replace('\n', '').replace('#', '\n').replace('(', ')').replace('  ', ' ').replace('COUNTRY', '').replace('POINTS', '').strip()
    temp_fantasy = temp_fantasy.split("\n")
    temp_fantasy = pd.DataFrame({'raw' : temp_fantasy})
    temp_fantasy['raw'] = temp_fantasy['raw'].str.strip()
    temp_fantasy = temp_fantasy['raw'].str.split(")", expand = True).rename(columns={0:'team_name', 1:'name', 2:'points'})
    temp_fantasy[['position', 'team_name']]= temp_fantasy['team_name'].str.split(' ', 1, expand = True)
    temp_fantasy['points'] = temp_fantasy['points'].str.strip()
    temp_fantasy['race_name'] = race_name
    temp_fantasy['race_number'] = x
    temp_fantasy['name'] = temp_fantasy['name'].str.strip()          
    
    # Append to Master Dataset
    fantasy = fantasy.append(temp_fantasy)

#Export data as csv
fantasy = fantasy.reset_index(drop=True)

fantasycsv = "raw/2019_fantasy_results" + ".csv"
fantasy.to_csv(fantasycsv, index = False)