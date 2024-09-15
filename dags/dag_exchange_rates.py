from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import pandas as pd
from airflow.utils.email import send_email

from modules.data_fetcher import obtener_datos
from modules.data_preprocessing import procesar_datos
from modules.utils import conectar_redshift, eliminar_registros, insertar_datos, cerrar_conexion

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email': ['airflowdocker@gmail.com'],  # Dirección de correo electrónico para alertas
    'email_on_failure': True,  # Enviar correo para fallas en tareas individuales
    'email_on_retry': False,   # Deshabilitar correo para reintentos
    'email_on_success': False,  # Deshabilitar correo para éxito en tareas individuales
}

def fetch_data(**kwargs):
    try:
        rates_df, base_currency, date = obtener_datos()
        kwargs['ti'].xcom_push(key='rates_df', value=rates_df.to_json())
        kwargs['ti'].xcom_push(key='base_currency', value=base_currency)
        kwargs['ti'].xcom_push(key='date', value=date)
    except Exception as e:
        raise ValueError(f"Error fetching data: {e}")

def process_data(**kwargs):
    try:
        rates_df_json = kwargs['ti'].xcom_pull(task_ids='fetch_data', key='rates_df')
        rates_df = pd.read_json(rates_df_json)
        date = kwargs['ti'].xcom_pull(task_ids='fetch_data', key='date')
        processed_df = procesar_datos(rates_df, date)
        kwargs['ti'].xcom_push(key='processed_df', value=processed_df.to_json())
        kwargs['ti'].xcom_push(key='base_currency', value=kwargs['ti'].xcom_pull(task_ids='fetch_data', key='base_currency'))
    except Exception as e:
        raise ValueError(f"Error processing data: {e}")

def load_to_redshift(**kwargs):
    try:
        processed_df_json = kwargs['ti'].xcom_pull(task_ids='process_data', key='processed_df')
        processed_df = pd.read_json(processed_df_json)
        base_currency = kwargs['ti'].xcom_pull(task_ids='process_data', key='base_currency')
        date = kwargs['ti'].xcom_pull(task_ids='fetch_data', key='date')
        
        conn, cur = conectar_redshift()
        
        eliminar_registros(cur, processed_df)
        insertar_datos(cur, conn, processed_df, base_currency, date)
        
        cerrar_conexion(cur, conn)
    except Exception as e:
        raise ValueError(f"Error loading data to Redshift: {e}")

def send_success_email(**kwargs):
    send_email(
        to='airflowdocker@gmail.com',
        subject='DAG Success Confirmation',
        html_content='The DAG has completed successfully, and the email notification was sent.'
    )

def on_failure_callback(context):
    send_email(
        to='airflowdocker@gmail.com',
        subject='DAG Failure Notification',
        html_content='The DAG has failed. Please check the logs for details.'
    )

dag = DAG(
    'exchange_rates_dag',
    default_args=default_args,
    description='A DAG to fetch, process, and load exchange rates',
    schedule_interval='@daily',
    on_failure_callback=on_failure_callback,
)

fetch_task = PythonOperator(
    task_id='fetch_data',
    python_callable=fetch_data,
    provide_context=True,
    dag=dag,
)

process_task = PythonOperator(
    task_id='process_data',
    python_callable=process_data,
    provide_context=True,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_to_redshift',
    python_callable=load_to_redshift,
    provide_context=True,
    dag=dag,
)

email_success_task = PythonOperator(
    task_id='email_success_sent',
    python_callable=send_success_email,
    provide_context=True,
    dag=dag,
)

start = DummyOperator(
    task_id='start',
    dag=dag,
)

end = DummyOperator(
    task_id='end',
    dag=dag,
)

start >> fetch_task >> process_task >> load_task >> email_success_task >> end
