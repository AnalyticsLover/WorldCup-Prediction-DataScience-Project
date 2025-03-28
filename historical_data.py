from bs4 import BeautifulSoup
import requests
import pandas as pd

mundial_years = [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 
                 1974, 1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006,
                 2010, 2014, 2018]

# WEB SCRAPPING

def get_matches(year):

    web = f'https://en.wikipedia.org/wiki/{year}_FIFA_World_Cup'
    

    response = requests.get(web) #mandando una solicitud a la pagina web con el modulo requests
    #cada vez q se genera una solicitud recibimos una respuesta de la pag

    content = response.text #obteniendo texto de la respuesta(archivo html)

    soup = BeautifulSoup(content, 'lxml') #extrayendo data de la web

    matches = soup.find_all('div', class_='footballbox')
    #matches va a ser una lista de coincidencias con las palabras clave div y footballbox
    #que dentro de la parte de inspeccionar al cliquear un partido en la web, se repite como patron
    #o sea que la lista va a contener todas las filas html que contengan esas palabras

    home= []
    score = []
    away = []


    for match in matches:
        #realizar mismo proceso para identificar/extraer y almacenar en listas:
        home.append(match.find("th", class_="fhome").get_text()) # equipo local
        score.append(match.find("th", class_="fscore").get_text()) #score
        away.append(match.find("th", class_="faway").get_text()) #visitante
        
    matches_dict = {"home": home, "score": score, "away": away}
    matches_df = pd.DataFrame(matches_dict)
    matches_df["year"] = year

    return matches_df

#la funcion get_matches toma parametro un año en el que se realizo el mundial
#y devuelve un dataframe con la informacion de los partidos.

    
total_data = [get_matches(year) for year in mundial_years]  
#extrayendo la data de todos los mundiales y almacenando en lista

final_df = pd.concat(total_data, ignore_index=True)#concatenando todos los dataframes

final_df.to_csv("worldcup_historical_data.csv", index=False)
#exportando el dataframe final a archivo csv

#creando fixture, no se puede usar funcion porque la web cambia totalmente para el mundia 2022
web1 = "https://web.archive.org/web/20221115040351/https://en.wikipedia.org/wiki/2022_FIFA_World_Cup"

response1 = requests.get(web1)
content1 = response1.text 
soup1 = BeautifulSoup(content1, 'lxml')
matches1 = soup1.find_all('div', class_='footballbox')

home1= []
score1 = []
away1 = []

for match in matches1:   
    home1.append(match.find("th", class_="fhome").get_text()) 
    score1.append(match.find("th", class_="fscore").get_text()) 
    away1.append(match.find("th", class_="faway").get_text()) 
        
matches_dict1 = {"home": home1, "score": score1, "away": away1}
df_fixture = pd.DataFrame(matches_dict1)
df_fixture["year"] = 2022
df_fixture.to_csv('worldcup_fixture.csv', index=False)

#se hace lo mismo q en la funcion, lo q en el codigo original seria:
#df_fixture = get_matches("2022")






