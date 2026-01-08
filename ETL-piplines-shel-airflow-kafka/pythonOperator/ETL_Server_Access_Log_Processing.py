from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow.models import DAG
# Operators; you need this to write tasks!
from airflow.operators.python import PythonOperator

# This makes scheduling easy
from airflow.utils.dates import days_ago
import requests

input_file = "external_file.txt"
extracted_file="extracted_data.txt"
transformed_file="Transformed_data.txt"
output_file="output_data.txt"

def download_file():
    url="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Apache%20Airflow/Build%20a%20DAG%20using%20Airflow/web-server-access-log.txt"
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(external_file,'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    print(f"File downloaded successfully: {input_file}")

def extract():
    global input_file
    print('inside extract')
    with open(input_file,'r') as infile, \
            open(extracted_file,'w') as outfile:
        for line in infile:
            fields = line.split('#')
            if len(fields) >= 4:
                field_1 = fields[0]
                field_4 = fields[3]
                outfile.write(field_1 + '#' + field_4 + '\n')

def transform():
    global extracted_file,transformed_file
    print('inside transform')
    with open(extracted_file,'r') as input_file, \
            open(transformed_file,'w') as output_file:
        for line in infile:
            processed_line = line.upper()
            outfile.write(processed_line + '\n')

def load():
    global transformed_file,output_file
    print('inside load')
    with open(transformed_file,'r') as infile, \
            open(output_file,'w') as outfile:
        for line in infile:
            outfile.write(line + '\n')

def check():
    global output_file
    print('inside check')
    with open(output_file,'r') as file:
        for line in file:
            print(line)

default_args = {
    'owner': 'alex',
    'start_date': days_ago(0),
    'email': ['your email'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'my-second-dag',
    default_args=default_args,
    description='my second dag',
    schedule_interval=timedelta(days=1),
)

download = PythonOperator(
    task_id='download',
    python_callable = download_file,
    dag=dag,
)

execute_extract = PythonOperator(
    task_id='extract',
    python_callable=extract,
    dag=dag,
)

execute_transform = PythonOperator(
    task_id='transform',
    python_callable=transform,
    dag=dag,
)

execute_load = PythonOperator(
    task_id='load',
    python_callable=load,
    dag=dag
)

execute_check = PythonOperator(
    task_id = 'check',
    python_callable=check,
    dag=dag
)

download >> execute_extract >> execute_transform >> execute_load >> execute_check