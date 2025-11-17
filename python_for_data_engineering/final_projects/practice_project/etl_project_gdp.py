# Code for ETL operations on Country-GDP data
# Importing the required libraries
import sqlite3
import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
from datetime import datetime 

url = 'https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'
#liveurl = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'

csv_path = './Countries_by_GDP.csv'
log_file = './etl_project_log.txt'
db_name = 'World_Economies.db'
table_name = 'Countries_by_GDP'
table_attribs = ['Country','GDP_USD_millions']

def extract(url, table_attribs):

    ''' This function extracts the required

    information from the website and saves it to a dataframe. The

    function returns the dataframe for further processing. '''

    response = requests.get(url).text
    data = BeautifulSoup(response,'html.parser')
    df = pd.DataFrame(columns=table_attribs)
    table = data.find_all('tbody')
    rows =  table[2].find_all('tr')
    count = 0

    for row in rows:
        col = row.find_all('td')
        if len(col) != 0:
            #if col[0].find('a') is not none and '—' not in col[2]:
            href_check = col[0].find('a')
            if not href_check:
                continue
            third_col_check = col[2].get_text(strip=True)
            if third_col_check == '—':
                continue
            data_dict = {"Country":col[0].get_text(strip=True),"GDP_USD_millions":col[2].contents[0]}
            #print(data_dict)
            #print(count)
            df1 = pd.DataFrame(data_dict,index=[0])
            df = pd.concat([df,df1],ignore_index=True)
            count+=1

    return df

def transform(df):

    ''' This function converts the GDP information from Currency

    format to float value, transforms the information of GDP from

    USD (Millions) to USD (Billions) rounding to 2 decimal places.

    The function returns the transformed dataframe.'''

    GDP_list = df["GDP_USD_millions"].tolist()
    GDP_list = [float("".join(x.split(','))) for x in GDP_list]
    GDP_list = [np.round(x/1000,2) for x in GDP_list]
    df["GDP_USD_millions"] = GDP_list
    df = df.rename(columns = {"GDP_USD_millions":"GDP_USD_billions"})

    return df

 

def load_to_csv(df, csv_path):

    ''' This function saves the final dataframe as a `CSV` file

    in the provided path. Function returns nothing.'''

    df.to_csv(csv_path)

 

def load_to_db(df, sql_connection, table_name):

    ''' This function saves the final dataframe as a database table

    with the provided name. Function returns nothing.'''

    df.to_sql(table_name,sql_connection,if_exists='replace',index=False)

 

def run_query(query_statement, sql_connection):

    ''' This function runs the stated query on the database table and

    prints the output on the terminal. Function returns nothing. '''

    print(query_statement)
    db_output = pd.read_sql(query_statement,sql_connection)
    print(db_output)

 

def log_progress(message):

    ''' This function logs the mentioned message at a given stage of the code execution to a log file. Function returns nothing'''

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d-%H:%M:%S")
    with open(log_file,'a')as f:
        f.write(f"{timestamp}: {message} \n")

 

''' Here, you define the required entities and call the relevant

functions in the correct order to complete the project. Note that this

portion is not inside any function.'''

 

log_progress("Declaring Known Values")
log_progress("Preliminaries complete. Initiating ETL process.")

log_progress("starting date extraction")
df = extract(url,table_attribs)
log_progress("Data extraction complete. Initiating Transformation process.")

log_progress("Starting Data transformation")
df = transform(df)
log_progress("Data transformation complete. Initiating loading process.")

log_progress("Loading data to csv file")
load_to_csv(df,csv_path)
log_progress("Data saved to CSV file.")

log_progress("Connecting to database")
conn = sqlite3.connect('World_Economies.db')
log_progress("SQL Connection initiated.")

log_progress("Loading data to database")
load_to_db(df,conn,table_name)
log_progress("Data loaded to Database as table. Running the query.")

log_progress("Sending query to databse")
statement = f"SELECT * from {table_name} WHERE GDP_USD_billions >= 100"
query_output = run_query(statement,conn)
print(query_output)

log_progress('Process Complete.')

conn.close()

