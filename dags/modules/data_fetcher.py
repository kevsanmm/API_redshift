import requests
import pandas as pd
from datetime import datetime

def obtener_datos():
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Error al obtener datos: {response.status_code}")
    
    data = response.json()
    rates_df = pd.DataFrame(list(data['rates'].items()), columns=['Currency', 'Rate'])
    base_currency = data['base']
    date = data['date']
    
    rates_df['Date'] = datetime.strptime(date, '%Y-%m-%d').date()
    return rates_df, base_currency, date
