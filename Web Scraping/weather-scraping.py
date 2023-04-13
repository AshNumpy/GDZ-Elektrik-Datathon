from playwright.sync_api import sync_playwright
import pandas as pd
import numpy as np

df = pd.read_csv('./Datasets/sample_submission.csv')
df['Tarih'] = pd.to_datetime(arg=df['Tarih'], format='%Y-%m-%d')
unique_dates = df['Tarih'].dt.strftime('%Y-%m-%d').unique().tolist()

# Personal Settings
location = 'izmir'
url = f'https://www.worldweatheronline.com/{location}-weather-history/{location}/tr.aspx'

# Scrapping
for date_value in unique_dates:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        
        # fill the date field
        page.locator(selector="#ctl00_MainContentHolder_txtPastDate").fill(date_value)
        page.get_by_role("button", name="Get Weather").click()
        
        # Get the weather data
        weather_data = page.locator('.days-box:nth-child(3) .days-collapse-temp').text_content()

        # Append the data to weather_list
        liste = [[date_value, weather_data]]
        liste = np.array(object=liste)
        liste_df = pd.DataFrame(data=liste, columns=['date','weather_info'])
        
        # read weather data
        weather_df = pd.read_csv('./Datasets/weather.csv')

        # overwrite the data
        weather_df = weather_df.append(liste_df, ignore_index=True)

        # export the data
        weather_df.to_csv('./Web Scraping/weather.csv', index=False)
        
        browser.close()

