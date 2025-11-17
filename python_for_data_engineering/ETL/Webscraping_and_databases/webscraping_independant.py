import requests
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup
from bs4.element import NavigableString

url = 'https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films'
db_name = 'Movies2.db'
table_name = 'NEW_Top_50'
csv_path = './NEW_top_50_films.csv'
df = pd.DataFrame(columns=["Average Rank","Film","Year","Year Rotten Tomatoes' Top 100"])
count = 0

html_page = requests.get(url).text
data = BeautifulSoup(html_page,'html.parser')
tables = data.find_all('tbody')
rows = tables[0].find_all('tr')

for row in rows:
    if count<25:
        col = row.find_all('td')
        if len(col)>4:
            col_year = col[2].contents[0]
            if isinstance(col_year,NavigableString):
                year_string = str(col_year).strip()
                if year_string.isdigit():
                    year = int(year_string)
                    if 1999 < year < 2010:
                        #test = type(col[2].contents[0])
                        #print(test)
                        data_dict = {"Average Rank": col[0].contents[0],
                        "Film": col[1].contents[0],
                        "Year": year,
                        "Rotten Tomatoes' Top 100":col[3].contents[0]}
                        df1 = pd.DataFrame(data_dict,index=[0])
                        df = pd.concat([df,df1],ignore_index=True)
                        count+=1

print(df.head())

df.to_csv(csv_path)
conn = sqlite3.connect(db_name)
df.to_sql(table_name,conn,if_exists='replace',index=False)
conn.close()

 

#only got 15 rows so need to have a re look at this