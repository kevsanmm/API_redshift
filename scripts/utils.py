import psycopg2
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

def conectar_redshift():
    """Conectar a la base de datos Redshift utilizando credenciales del archivo .env."""
    # Obtener credenciales de las variables de entorno
    host = os.getenv('REDSHIFT_HOST')
    port = os.getenv('REDSHIFT_PORT')
    dbname = os.getenv('REDSHIFT_DBNAME')
    user = os.getenv('REDSHIFT_USER')
    password = os.getenv('REDSHIFT_PASSWORD')

    # Conectar a Redshift
    conn = psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password
    )
    cur = conn.cursor()
    return conn, cur

def eliminar_registros(cur, rates_df):
    """Eliminar registros existentes en la tabla 'exchange_rates' basado en la clave primaria compuesta (currency, date)."""
    delete_query = 'DELETE FROM exchange_rates WHERE currency = %s AND date = %s'
    unique_keys = rates_df[['Currency', 'Date']].drop_duplicates()
    for _, row in unique_keys.iterrows():
        cur.execute(delete_query, (row['Currency'], row['Date']))

def insertar_datos(cur, conn, rates_df, base_currency, date):
    """Insertar datos en la tabla 'exchange_rates'."""
    insert_query = '''
    INSERT INTO exchange_rates (base, date, currency, rate, ingestion_time, country, region, continent, wealthy) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    '''
    # Convertir la fecha a un objeto datetime
    ingestion_time = date
    for _, row in rates_df.iterrows():
        cur.execute(insert_query, (
            base_currency, row['Date'], row['Currency'], row['Rate'], row['Ingestion_Time'],
            row['Country'], row['Region'], row['Continent'], row['Wealthy']
        ))

    # Confirmar los cambios
    conn.commit()

def cerrar_conexion(cur, conn):
    """Cerrar el cursor y la conexión a la base de datos."""
    cur.close()
    conn.close()
