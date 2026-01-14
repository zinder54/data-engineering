from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'Fred',
    'start_date':days_ago(0),
    'email':['fred@your_email.com'],
    'email_on_failure':'True',
    'email_on_retry':'True',
    'retries':1,
    'retry_delay':timedelta(minutes=5),
}
##tar -xf /home/project/airflow/dags/finalassignment/tolldata.tgz -C /home/project/
dag = DAG(
    'ETL_toll_data',
    default_args=default_args,
    description='Apache Airflow Final Assignment',
    schedule_interval=timedelta(days=1),
)

unzip_data = BashOperator(
    task_id = 'unzip_data',
    bash_command = 'tar -xf tolldata.tgz -C /home/project/airflow/dags/',
    dag=dag
)

extract_data_from_csv = BashOperator(
    task_id = 'extract_data_from_csv',
    bash_command = 'cut -d"," -f1-4 vehicle-data.csv > /home/project/airflow/dags/csv_data.csv',
    dag=dag
)

extract_data_from_tsv = BashOperator(
    task_id='extract_data_from_tsv',
    bash_command='cut -f5-7 tollplaza-data.tsv | tr "\t" ","> tsv_data.csv',
    dag=dag
)

extract_data_from_fixed_width = BashOperator(
    task_id='extract_data_from_fixed_width',
    bash_command="awk '{ print $(NF-1), $NF }' OFS=',' payment-data.txt > /home/project/airflow/dags/fixed_width_data.csv",
    dag=dag,
)

consolidate_data = BashOperator(
    task_id='consolidate_data',
    bash_command='paste -d"," csv_data.csv tsv_data.csv fixed_width_data.csv > /home/project/airflow/dags/extracted_data.csv',
    dag=dag
)

transform_data = BashOperator(
    task_id='transform_data',
    bash_command="tr '[:lower:]' '[:upper:]' < extracted_data.csv > /home/project/airflow/dags/transformed_data.csv",
    dag=dag
)

unzip_data >> extract_data_from_csv >> extract_data_from_tsv >> extract_data_from_fixed_width >> consolidate_data >> transform_data