from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time


#inicializando web scrapping
path = r'C:\Users\Lucia\Documents\Drivers\chromedriver.exe'
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)

def get_football_matches(year):
    web = f"https://en.wikipedia.org/wiki/{year}_FIFA_World_Cup"
    driver.get(web)
    
    time.sleep(2) #asignando una pausa al web scrapper, para la ejecucion por x seg
    
    matches = driver.find_elements(by='xpath', value='//*[@id="mw-content-text"]/div[1]/div[14]/table/tbody/tr[1]')
    #extrayendo cada elemnto de las filas de partidos 

    home = []
    score = []
    away = []

    for match in matches:
        home.append(match.find_element(by='xpath', value='.//th[1]').text)
        score.append(match.find_element(by='xpath', value='.//th[2]').text)
        away.append(match.find_element(by='xpath', value='.//th[3]').text)
    
    football_dict = {'home': home, 'score': score, 'away': away}
    football_df = pd.DataFrame(football_dict)
    football_df['year'] = year
    
    return football_df

years = [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 
                 1974, 1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006,
                 2010, 2014, 2018]

df_list = [get_football_matches(year) for year in years]

driver.quit()#cerrando driver de chrome

final_df = pd.concat(df_list, ignore_index=True)
final_df.to_csv("wolrdcup_final_data.csv", index=False)


    
   

