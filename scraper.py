from bs4 import BeautifulSoup as bs
import pandas as pd
import requests


S = requests.get('https://www.ufo-hunters.com/sightings/country/POL/Poland')
soup = bs(S.content, 'lxml')

# scraping all <tr> and <td> tags from website table:
table = soup.find('table', id='tabledata')
tmp=[]

for row in table.find_all('tr'):
    cols = row.find_all('td')
    
    for item in cols:
        tmp.append(item.text.strip())

# slicing resulting list into smaller lists of four items:
results=[tmp[i:i+4] for i in range(0, len(tmp), 4)]
   
#preparing dataframe and .csv file:
columns = ['Location', 'Sighted on', 'Shape', 'Duration']
df = pd.DataFrame(results, columns=columns)
df.to_csv('./assets/data/UFO_raw.csv')
