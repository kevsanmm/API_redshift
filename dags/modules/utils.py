import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def conectar_redshift():
    conn = psycopg2.connect(
        host=os.getenv('REDSHIFT_HOST'),
        port=os.getenv('REDSHIFT_PORT'),
        dbname=os.getenv('REDSHIFT_DBNAME'),
        user=os.getenv('REDSHIFT_USER'),
        password=os.getenv('REDSHIFT_PASSWORD')
    )
    cur = conn.cursor()
    return conn, cur

def eliminar_registros(cur, rates_df):
    delete_query = 'DELETE FROM exchange_rates WHERE currency = %s AND date = %s'
    unique_keys = rates_df[['Currency', 'Date']].drop_duplicates()
    for _, row in unique_keys.iterrows():
        cur.execute(delete_query, (row['Currency'], row['Date']))

def insertar_datos(cur, conn, rates_df, base_currency):
    insert_query = '''
    INSERT INTO exchange_rates (base, date, currency, rate, ingestion_time, country, region, continent, wealthy) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    '''
    for _, row in rates_df.iterrows():
        cur.execute(insert_query, (
            base_currency, row['Date'], row['Currency'], row['Rate'], row['Ingestion_Time'],
            row['Country'], row['Region'], row['Continent'], row['Wealthy']
        ))
    conn.commit()

def cerrar_conexion(cur, conn):
    cur.close()
    conn.close()
