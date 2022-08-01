from selenium import webdriver
from selenium.webdriver.common.by import By

import pandas as pd

import gspread
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials


## Scraper ##

# Start up ChromeDriver.
driver = webdriver.Chrome(executable_path='/Users/myles/desktop/projects/selenium-scraper/chromedriver')

# Enter URL from YouTube channel's 'VIDEOS' page.
URL = 'https://www.youtube.com/c/JordanPetersonVideos/videos?view=0&sort=dd&flow=grid'
driver.get(URL)

# Locate video data and organize into dataframe.
placards = driver.find_elements(By.CLASS_NAME, 'style-scope ytd-grid-video-renderer')
all_videos = []

for placard in placards:
    title = placard.find_element(By.XPATH, './/*[@id="video-title"]').text
    views = placard.find_element(By.XPATH, './/*[@id="metadata-line"]/span[1]').text
    posted = placard.find_element(By.XPATH, './/*[@id="metadata-line"]/span[2]').text
    length = placard.find_element(By.XPATH, './/*[@id="text"]').text                           

    video_data = {
        'Video Title': title,
        'Views': views,
        'Time-Ago Posted': posted,
        'Length': length
    }
    all_videos.append(video_data)

df = pd.DataFrame(data=all_videos)
#print df


## Database ##

# Define APIs being accessed.
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

# Service account authenticates to APIs via key file.
credentials = ServiceAccountCredentials.from_json_keyfile_name('key.json', scope)
client = gspread.authorize(credentials)

# Identify target spreadsheet and worksheet.
# Sort video category by popular/newest/oldest via YouTube's 'SORT BY' feature.
spreadsheet_key = '1sz65hZuFaZomwZrqBmEUzanQtCVj_drUJYkmSNuEqmM'
worksheet_name = 'Newest'
d2g.upload(df, spreadsheet_key, worksheet_name, credentials=credentials, row_names=True)







