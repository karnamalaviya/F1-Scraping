"""
SCRAPE FANTASY F1 WEBSITE

@author: Karna Malaviya
"""

# Define information for URLs
url = "https://fantasy.formula1.com/leaderboards/league?league_id=19778"

# Create dataset of fantasy results
choice = pd.DataFrame()

# Open Driver to League Standings Page
driver.get(url)


# Loop Through Overall Standings (17 Players)
for t in range(1, number_of_teams):
    if t == 1 :         
    # Define Xpath for 1st Place Team, use Sibling for the Rest
        team_xpath = "//ul[contains(@class, 'stripped-list')]//li[contains(@class, 'list-row league-row')]"
    else : 
        team_xpath = team_xpath + "//following-sibling::li"        
    
    # Identify Team Name
    time.sleep(randint(1,5))
    temp_team_name = driver.find_element_by_xpath(team_xpath)
    temp_team_name = temp_team_name.get_attribute("innerText")
    temp_team_name = temp_team_name.replace('(ver)stappen4nobody', 'verstappen4nobody').replace('karn on d kob(e bryan)', 'karn on d kobe bryan')
    team_name = temp_team_name.split('(', 1)[0] 
    team_name = re.sub('#[0-9][0-9] ', '', team_name)
    team_name = re.sub('#[0-9] ', '', team_name)
    team_name = team_name.strip()
    season_points = temp_team_name.split('POINTS', 1)[1].strip()
    
    # Click On Team 
    time.sleep(randint(1,5))
    driver.find_element_by_xpath(team_xpath).click()
    time.sleep(randint(1,5))
    
# Loop through to all races (range(x,y) represents integers from x to y-1)
    # Find Driver and Constructor Choices (Each Player Makes 6 Choices)
    for z in range(1, number_of_choices):
        z = str(z)
        if z == "1" :
            # If z == 1, get constructor choice separately
            choice_xpath = "//*[contains(@class, '" + z + "CR')]"
            time.sleep(randint(1,5))
            temp_choice = driver.find_element_by_xpath(choice_xpath)            
            temp_choice = temp_choice.get_attribute("innerText")
            temp_choice = temp_choice.split("\n")
            temp_choice = list(filter(None, temp_choice))    
            temp_choice = pd.DataFrame({'raw' : temp_choice})
            temp_choice['id'] = 1
            temp_choice['col'] = temp_choice.index + 1
            temp_choice = temp_choice.pivot(index='id', columns = 'col', values='raw')   
            temp_choice.columns=['type', 'name', 'points']
            temp_choice['team_name'] = team_name
            temp_choice['season_points'] = season_points
            choice = choice.append(temp_choice)
            
            # Then define Driver choice xpaths
            choice_xpath = "//*[contains(@class, '" + z + "DR')]"
        else :
            choice_xpath = "//*[contains(@class, '" + z + "DR')]"
        
        time.sleep(randint(1,5))
        temp_choice = driver.find_element_by_xpath(choice_xpath)            
        temp_choice = temp_choice.get_attribute("innerText")
        temp_choice = temp_choice.split("\n")
        temp_choice = list(filter(None, temp_choice))    
        temp_choice = pd.DataFrame({'raw' : temp_choice})
        temp_choice['id'] = 1
        temp_choice['col'] = temp_choice.index + 1
        temp_choice = temp_choice.pivot(index='id', columns = 'col', values='raw')   
        temp_choice.columns=['type', 'name', 'points']
        temp_choice['team_name'] = team_name
        temp_choice['season_points'] = season_points
        choice = choice.append(temp_choice)
    
    driver.back()

#Export data as csv
choice = choice.reset_index(drop=True)

choicecsv = "raw/2019_choices" + ".csv"
choice.to_csv(choicecsv, index = False)