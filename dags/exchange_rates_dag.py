from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import subprocess

# Definir los argumentos por defecto para la DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Definir la DAG
dag = DAG(
    'exchange_rates_dag',
    default_args=default_args,
    description='DAG para ejecutar main.py y cargar datos a Redshift',
    schedule_interval=timedelta(days=1),  # Ejecutar una vez al día
)

# Definir la tarea que ejecutará main.py
def run_main():
    subprocess.run(["python3", "/opt/airflow/main.py"], check=True)

run_task = PythonOperator(
    task_id='run_main_script',
    python_callable=run_main,
    dag=dag,
)

# Asignar la tarea a la DAG
run_task
