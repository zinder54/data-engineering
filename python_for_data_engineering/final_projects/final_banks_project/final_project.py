# Code for ETL operations on Country-GDP data

# Importing the required libraries
import sqlite3
import pandas as pd 
import numpy as np 
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import lxml

url = 'https://web.archive.org/web/20230908091635 /https://en.wikipedia.org/wiki/List_of_largest_banks'
db_name = 'banks.db'
table_name = 'Largest_banks'
table_attribs = ['Name','MC_USD_Billion']
excahnge_rate_csv = './exchange_rate.csv'

csv_path = './Largest_banks_data.csv'
log_file = 'code_log.txt'

def log_progress(message):
    ''' This function logs the mentioned message of a given stage of the
    code execution to a log file. Function returns nothing'''

    now = datetime.now()
    timestamp = now.strftime("%Y-%b-%d-%H:%M:%S")
    with open(log_file,'a') as f:
        f.write(f"{timestamp}: {message} \n")

def extract(url, table_attribs):
    ''' This function aims to extract the required
    information from the website and save it to a data frame. The
    function returns the data frame for further processing. '''
    response = requests.get(url).text
    soup = BeautifulSoup(response,'html.parser')
    df = pd.DataFrame(columns = table_attribs)
    table = soup.find_all('tbody')
    rows = table[0].find_all('tr')
    for row in rows:
        col = row.find_all('td')
        if len(col) != 0:
            bank_name = col[1].find_all('a')[1]['title']
            market_cap = col[2].contents[0][:-1]
            data_dict = {'Name':bank_name,
                        'MC_USD_Billion':float(market_cap)}
            df1 = pd.DataFrame(data_dict,index=[0])
            df = pd.concat([df,df1],ignore_index=True)
    return df

def transform(df, csv_path):
    ''' This function accesses the CSV file for exchange rate
    information, and adds three columns to the data frame, each
    containing the transformed version of Market Cap column to
    respective currencies'''

    dataframe = pd.read_csv(csv_path)
    exchange_rate = dataframe.set_index('Currency').to_dict()['Rate']
    df['MC_GBP_Billion'] = [np.round(x*exchange_rate['GBP'],2) for x in df['MC_USD_Billion']]
    df['MC_EUR_Billion'] = [np.round(x*exchange_rate['EUR'],2) for x in df['MC_USD_Billion']]
    df['MC_INR_Billion'] = [np.round(x*exchange_rate['INR'],2) for x in df['MC_USD_Billion']]
    
    return df

def load_to_csv(df, output_path):
    ''' This function saves the final data frame as a CSV file in
    the provided path. Function returns nothing.'''

    df.to_csv(output_path)

def load_to_db(df, sql_connection, table_name):
    ''' This function saves the final data frame to a database
    table with the provided name. Function returns nothing.'''

    df.to_sql(table_name,sql_connection,if_exists ='replace',index=False)

def run_query(query_statement, sql_connection):
    ''' This function runs the query on the database table and
    prints the output on the terminal. Function returns nothing. '''

    query_output = pd.read_sql(query_statement,sql_connection)
    return query_output

''' Here, you define the required entities and call the relevant
functions in the correct order to complete the project. Note that this
portion is not inside any function.'''

log_progress("Preliminaries complete. Initiating ETL process")

log_progress("Data extraction complete. Initiating Transformation process")
df = extract(url,table_attribs)

log_progress("Data Transformation complete. Initiating Loading process")
transformed_data = transform(df,excahnge_rate_csv)

load_to_csv(transformed_data,csv_path)
log_progress("Data saved to CSV file")

log_progress("SQL Connection initiated")
conn = sqlite3.connect(db_name)

log_progress("Data loaded to Database as a table, Executing queries")
load_to_db(transformed_data, conn, table_name)

query_statement = "SELECT * FROM Largest_banks"
print(query_statement)
query_output = run_query(query_statement,conn)
print(query_output)
query_statement = "SELECT AVG(MC_GBP_Billion) FROM Largest_banks"
print(query_statement)
query_output = run_query(query_statement,conn)
print(query_output)
query_statement = "SELECT Name from Largest_banks LIMIT 5"
print(query_statement)
query_output = run_query(query_statement,conn)
print(query_output)
log_progress("Process Complete")

conn.close()
log_progress("Server Connection closed")
