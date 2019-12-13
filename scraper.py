import time
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
import os

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'https://www.onepa.sg/cat/water-sports/subcat/kayaking'
driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(5)

wait5secs = WebDriverWait(driver, 5)
VACANCY_SPAN_XPATH = '//span[@id="spanVacancy"]'

# get first page
driver.get(url)
wait5secs.until(EC.presence_of_element_located((By.XPATH, VACANCY_SPAN_XPATH)))
time.sleep(2)
pages = [driver.page_source]
print("Scraped page %d" % len(pages))

# loop to get all subsequent pages
try:
    NEXT_BUTTON_XPATH = '//li[@class="pager-next"]/span'
    MAX_PAGES_TO_SCRAPE = 40
    
    while len(pages) < MAX_PAGES_TO_SCRAPE:
    
        button = wait5secs.until(EC.element_to_be_clickable((By.XPATH, NEXT_BUTTON_XPATH)))
        button.click()
        
        time.sleep(2)
        wait5secs.until(EC.presence_of_element_located((By.XPATH, VACANCY_SPAN_XPATH)))
        time.sleep(2)
        pages.append(driver.page_source)
        print("Scraped page %d" % len(pages))

except TimeoutException:
    pass
    
finally:
    driver.close()
    
print("Scraping completed!\nProcessing course info...")

course_list = []

for page in pages: # loop each scraped page
    
    bs = BeautifulSoup(page, 'html.parser')
    courses = bs.find_all("div", class_='gridContent')
    
    for course in courses: # loop each course in the page
        
        # gets code, title, start_date, end_date, location and vacancy of course
        keywords = ["spanCode", "spanTitle", "spanStartDate", "spanEndDate", "spanLocation", "spanVacancy"]
        details = [course.find("span", id=keyword).text for keyword in keywords]
        course_list.append(details)

df = pd.DataFrame(course_list, columns=['Code','Title','Start_Date','End_Date','Location','Vacancy'])

df = df[df['Vacancy'] != 'Unlimited'] # removes all the PA interest group courses

# if there are duplicates in df
# df = df.loc[~df.index.duplicated(keep='first')]

def createPeriod(row):
    startDateStr = str(datetime.strptime(row.Start_Date, '%d %b %Y').strftime('%m/%d'))
    endDateStr = str(datetime.strptime(row.End_Date, '%d %b %Y').strftime('%m/%d'))
    return startDateStr + ' - ' + endDateStr

# alternative: period_list = sorted_df.apply(lambda x: str(datetime.strptime(x.Start_Date, '%d %b %Y').strftime('%d/%m')) + ' - ' + str(datetime.strptime(x.End_Date, '%d %b %Y').strftime('%d/%m')), axis=1)
period_list = df.apply(createPeriod, axis=1)
df.insert(3, 'Period(MM/DD)', period_list, True) # creates Period column 

df['Location'] = df['Location'].apply(lambda venue: venue.split(' @ ')[-1]) # edits Location column

print("Creating txt file...\n")

sorted_df = df.set_index('Code').sort_values(by=['Title','Period(MM/DD)'])

# saves all the course info into a txt file
course_file = './courses.txt'

with open(course_file, 'w') as f:
    f.write('[FOR MORE INFO, GO TO www.onepa.sg/class/details/<course code>]\n\n')
    
    f.write('KAYAKING 1 STAR AWARD\n\n')
    sorted_df[sorted_df.Title == 'KAYAKING 1 STAR AWARD'][['Period(MM/DD)','Location','Vacancy']].to_string(f)
    
    f.write('\n\nKAYAKING 2 STAR AWARD\n\n')
    sorted_df[sorted_df.Title == 'KAYAKING 2 STAR AWARD'][['Period(MM/DD)','Location','Vacancy']].to_string(f)

# prints out the content file onto the terminal
if os.path.exists(course_file):    
    content = open(course_file, 'r').read()
    print(content)

print("\nSuccess! Exiting code...")