import requests
import pandas as pd
from datetime import datetime

def obtener_datos():
    # URL de la API
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    
    # Realizar la solicitud GET
    response = requests.get(url)
    
    # Verificar si la solicitud fue exitosa
    if response.status_code != 200:
        raise Exception(f"Error al obtener datos: {response.status_code}")
    
    # Convertir la respuesta JSON a un diccionario
    data = response.json()
    
    # Convertir los datos de tasas de cambio en un DataFrame
    rates_df = pd.DataFrame(list(data['rates'].items()), columns=['Currency', 'Rate'])
    
    base_currency = data['base']
    date = data['date']
    
    # Agregar columna de fecha
    rates_df['Date'] = datetime.strptime(date, '%Y-%m-%d').date()
    
    return rates_df, base_currency, date
