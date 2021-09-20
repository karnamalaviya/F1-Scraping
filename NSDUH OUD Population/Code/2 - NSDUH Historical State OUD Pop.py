"""""""""""""""""""""""""""""""""""""""""
SCRAPE OUD POPULATION FROM NSDUH WEBSITE 

@author: Karna Malaviya
"""""""""""""""""""""""""""""""""""""""""

##############
#   Set-Up   #
##############

# Import Packages
import os
import time
from selenium import webdriver
import pandas as pd
from random import randint
from datetime import date

# Set working directory
path = "C:/Users/Karna Malaviya/Desktop/OUD"
os.chdir(path)

# Define Location of Web Driver and Open It
driver = webdriver.Chrome('chromedriver.exe')  
driver.maximize_window()

# Import .csv File With List of NSDUH Queries
nsduh_queries = pd.read_csv("Input/State NSDUH Queries.csv").dropna()


############################
#   Scrape NSDUH Website   #
############################

# 1 - Create Empty Dataset for Results
oud_df = pd.DataFrame()

# 2 - Loop Through Each NSDUH Query
start = time.time()
for i, row in nsduh_queries.iterrows():
    
    # 3 - Store Query Information
    year_start = row['surveyyear1']
    year_end   = row['surveyyear2']
    year_start = str(year_start).replace('.0', '')
    year_end   = str(year_end).replace('.0', '')
    row_var    = row['rowvariable']
    col_var    = row['columnvariable']
    state      = row['state']
    wt_var     = row['weightvariable']
    query_num  = row['query_num']
    control    = row['controlvariable']
    
    # 3.1 - Add Control Variable if Query Calls for One
    if (control == "NONE") :
        control_url1 = ""
        control_url2 = ""
    else :
        control_url1 = "&control=" + control
        control_url2 = "%26" + control + "%3D0"
            
    # 3.2 Construct URL Based on Query Information
    url = ("https://rdas.samhsa.gov/#/survey/NSDUH-"            # Base
           + year_start + "-" + year_end + "-RD02YR?"           # Year Start and End
           + "column=" + col_var                                # Define Column Variable
           + control_url1                                       # Define Control Variable
           + "&filter=" + col_var + "%3D1"                      # Column Variable Filter == YES
           + control_url2                                       # Define Control Variable Value (= "NO/UNKNOWN")                          
           + "%26STNAME%3D" + state                             # Row Variable Filter
           + "&results_received=FALSE&"                         # Misc Filler
           + "row=" + row_var                                   # Define Row Variable
           + "&run_chisq=FALSE&"                                # Do Not Run Chi Square
           + "weight=" + wt_var)                                # Define Weighting Variable
    
    # 3.3 - Call Out Query Information
    pct_complete = round((i / len(nsduh_queries)) * 100, 2)
    pct_complete = str(pct_complete)
    time_elapsed = round((time.time() - start) / (60 * 60), 2)
    time_elapsed = str(time_elapsed)
    callout1 = (state 
                + " (" + year_start + "-" + year_end + ") " 
                + col_var + " with " 
                + control + " Control In Progress")
    callout2 =  "Time Elapsed = " + time_elapsed + " Hours: " + pct_complete + "% Complete"
    print(callout1)
    print(callout2)
 
    # 4 - Open NSDUH Crosstab Page
    driver.get(url)
    time.sleep(randint(5,7))

    # 4.1 - Uncheck Options For Statistics Other Than Weighted Counts
    driver.find_element_by_xpath("//*[contains(@id, 'crosstabDisplayOptionSE')]").click()
    driver.find_element_by_xpath("//*[contains(@id, 'crosstabDisplayOptionColPercent')]").click()
    driver.find_element_by_xpath("//*[contains(@id, 'crosstabDisplayOptionChiSq')]").click()
    driver.find_element_by_xpath("//*[contains(@id, 'crosstabDisplayOptionChart')]").click()

    # 4.2 - Click Button to Run CrossTab
    time.sleep(randint(1,3))
    driver.find_element_by_xpath("//*[contains(@class, 'primary button')]").click()
    time.sleep(randint(7,10))

    # 5 - Store Table Results
    table = driver.find_element_by_xpath("//*[contains(@id, 'crosstab-results')]")
    
    # 5.1 - Clean Results
    temp = table.get_attribute("innerText") 
    temp = temp.split("Standard Errors")
    temp = temp[1:]
    temp = "".join(temp).strip()
    temp = temp.split("Weighted Count")
    temp = temp[0]
    temp = "".join(temp).strip()
    temp = temp.split('\n')
    
    # 5.2 - Mark Suppressed Data
    # 5.2.1 - No Control Variable Selected 
    if (len(temp)  == 2) & (control == "NONE") : 
        state      = temp[1]
        population = temp[0]
    if (len(temp)  == 1) & (control == "NONE") :
        state      = temp[0]
        population = "Suppressed"
    if (len(temp) > 2) & (control == "NONE"):
        break 
    # 5.2.2 - Control Used    
    if (len(temp) == 3) & (control != "NONE"):
        state      = temp[2]
        population = temp[1]
    if (len(temp) == 2) & (control != "NONE"):
        state      = temp[1]
        population = "Suppressed"
    if (len(temp) > 3) & (control != "NONE"):
        break 
    
    # 6 - Save Results As Dataframe
    temp_df = pd.DataFrame({ row_var     : state, 
                            'year_start' : year_start,
                            'year_end'   : year_end,
                            'variable'   : col_var, 
                            'control'    : control,
                            'population' : population,
                            'query'      : query_num,
                            'wt_var'     : wt_var,
                            'url'        : url},
                             index=[i]
                             )
                                          
    # 6.1 - Append Results to Master Dataset
    oud_df = oud_df.append(temp_df)
    
    # 7 - Reset Browser
    reset = "data:,"
    driver.get(reset)
    time.sleep(randint(2,4))
    
# 8 - Close Browser
driver.close() 
print((time.time() - start) / (60 * 60))

# 9 - Clean Data
oud_df_clean = oud_df.reset_index(drop=True)

# 10 - Export as .csv    
today = str(date.today())
date = str(today)
oud_csv = "Output/state_oud_pop" + " " + date + ".csv"
oud_df_clean.to_csv(oud_csv, index = False)