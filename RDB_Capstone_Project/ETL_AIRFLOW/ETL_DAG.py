
# used the below command to download the source file for the following ETL process
#wget -O /home/project/airflow/dags/capstone/accesslog.txt https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0321EN-SkillsNetwork/ETL/accesslog.txt

#import relevant modules
from datetime import timedelta, datetime
from airflow.models import DAG
from airflow.operators.python import PythonOperator
import tarfile

#define the dag
default_args = {
    'owner':'alex',
    'start_date':datetime(2024,1,1),
    'email':'someone@email.com',
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": True,
    "email_on_retry": False,
}

dag = DAG(
    'process_web_log',
    default_args=default_args,
    description = 'process to get ip from log file',
    schedule_interval = timedelta(days=1),
    catchup=False
)

#extract data function
def extract_data():
    with open("/home/project/airflow/dags/accesslog.txt",'r')as f, \
        open("/home/project/airflow/dags/extracted_data.txt",'w') as wf:
    
        for line in f:
            ip = line.split(" ")[0]
            wf.write(ip + "\n")

#transform data function
def transform_data():
    skip_ip = "198.46.149.143"

    with open("/home/project/airflow/dags/extracted_data.txt",'r')as f, \
        open("/home/project/airflow/dags/transform_data.txt",'w') as wf:
        
        for line in f:
            ip = line.strip()
            if ip != skip_ip:
                wf.write(ip + "\n")

#load data function
def load_data():
    transform_file = "/home/project/airflow/dags/transform_data.txt"
    tar_file = "/home/project/airflow/dags/weblog.tar"

    with tarfile.open(tar_file,'w') as tar:
        tar.add(transform_file, arcname="transform_data.txt")

#dag task creation
execute_extract_data = PythonOperator(
    task_id="extract_data",
    python_callable=extract_data,
    dag=dag
)

execute_transform_data = PythonOperator(
    task_id="transform_data",
    python_callable=transform_data,
    dag=dag
)
execute_load_data = PythonOperator(
    task_id="load_data",
    python_callable=load_data,
    dag=dag
)

execute_extract_data >> execute_transform_data >> execute_load_data