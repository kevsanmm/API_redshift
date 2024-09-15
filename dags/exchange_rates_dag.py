from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator
from datetime import datetime, timedelta
import subprocess

# Definir los argumentos por defecto para la DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email': ['airflowdocker@gmail.com'],  # El correo proporcionado
    'email_on_failure': True,
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

# Definir la tarea de envío de correo en caso de éxito
success_email = EmailOperator(
    task_id='send_success_email',
    to='airflowdocker@gmail.com',  # El correo proporcionado
    subject='DAG exchange_rates_dag ejecutado correctamente',
    html_content='<p>La DAG exchange_rates_dag se ejecutó exitosamente.</p>',
    dag=dag,
)

# Definir la tarea de envío de correo en caso de fallo
failure_email = EmailOperator(
    task_id='send_failure_email',
    to='airflowdocker@gmail.com',  # El correo proporcionado
    subject='DAG exchange_rates_dag ha fallado',
    html_content='<p>La DAG exchange_rates_dag ha fallado.</p>',
    trigger_rule='one_failed',  # Enviar solo si la tarea falla
    dag=dag,
)

# Configurar las dependencias
run_task >> success_email
run_task >> failure_email