from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from modules.data_fetcher import obtener_datos
from modules.data_preprocessing import procesar_datos
from modules.utils import conectar_redshift, eliminar_registros, insertar_datos, cerrar_conexion

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 9, 14),
    'email': ['airflowdocker@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def task_obtener_datos(**kwargs):
    rates_df, base_currency, _ = obtener_datos()
    if rates_df is None:
        raise ValueError("El DataFrame obtenido es None.")
    kwargs['ti'].xcom_push(key='rates_df', value=rates_df)
    kwargs['ti'].xcom_push(key='base_currency', value=base_currency)

def task_procesar_datos(**kwargs):
    rates_df = kwargs['ti'].xcom_pull(key='rates_df')
    if rates_df is None:
        raise ValueError("El DataFrame recibido es None.")
    processed_df = procesar_datos(rates_df)
    kwargs['ti'].xcom_push(key='processed_df', value=processed_df)

def task_eliminar_registros(**kwargs):
    processed_df = kwargs['ti'].xcom_pull(key='processed_df')
    conn, cur = conectar_redshift()  # Crear la conexión y el cursor aquí
    eliminar_registros(cur, processed_df)
    conn.commit()  # Asegurarse de hacer commit si es necesario

def task_insertar_datos(**kwargs):
    processed_df = kwargs['ti'].xcom_pull(key='processed_df')
    base_currency = kwargs['ti'].xcom_pull(key='base_currency')
    conn, cur = conectar_redshift()  # Crear la conexión y el cursor aquí
    insertar_datos(cur, conn, processed_df, base_currency)
    conn.commit()  # Asegurarse de hacer commit si es necesario

def task_cerrar_conexion(**kwargs):
    conn, cur = conectar_redshift()  # Crear la conexión y el cursor aquí
    cerrar_conexion(cur, conn)

with DAG(
    'procesar_e_insertar_datos_completo',
    default_args=default_args,
    description='DAG para obtener, procesar e insertar datos de tasas de cambio en Redshift',
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:

    obtener_datos_task = PythonOperator(
        task_id='obtener_datos_de_api',
        python_callable=task_obtener_datos,
        provide_context=True
    )

    procesar_datos_task = PythonOperator(
        task_id='procesar_datos',
        python_callable=task_procesar_datos,
        provide_context=True
    )

    eliminar_registros_task = PythonOperator(
        task_id='eliminar_registros_antiguos',
        python_callable=task_eliminar_registros,
        provide_context=True
    )

    insertar_datos_task = PythonOperator(
        task_id='insertar_datos_nuevos',
        python_callable=task_insertar_datos,
        provide_context=True
    )

    cerrar_conexion_task = PythonOperator(
        task_id='cerrar_conexion_redshift',
        python_callable=task_cerrar_conexion,
        provide_context=True
    )

    obtener_datos_task >> procesar_datos_task >> eliminar_registros_task >> insertar_datos_task >> cerrar_conexion_task
