from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow.models import DAG
# Operators; you need this to write tasks!
from airflow.operators.bash_operator import BashOperator
# This makes scheduling easy
from airflow.utils.dates import days_ago

default_args = {
    'owner' : 'alex',
    'start_date':days_ago(0),
    'email':['your_email'],
    'retries':1,
    'retry_delay':timedelta(minutes=5)
}

dag=DAG(
    'my-first-bash-dag',
    default_args=default_args,
    description='my first bash dag',
    schedule_interval=timedelta(days=1)
)

extract = BashOperator(
    task_id = 'extract',
    bash_command='cut -d":" -f1,3,6 /etc/passwd > /home/project/airflow/dags/extracted-data.txt',
    dag=dag
)

transform_and_load = BashOperator(
    task_id='transform',
    bash_command='tr ":" "," < /home/project/airflow/dags/extracted-data.txt > /home/project/airflow/dags/transformed-data.csv',
    dag=dag
)

extract >> transform_and_load