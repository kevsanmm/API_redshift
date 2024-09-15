from datetime import datetime
import pandas as pd

def procesar_datos(rates_df):
    specific_currencies = {'USD', 'ARS', 'AUD', 'BDT', 'BRL', 'CAD', 'CNY', 'ETB', 'EUR', 'FJD', 'GBP', 'HTG', 'JPY', 'NGN', 'NIO', 'PGK', 'PYG', 'SLL', 'VUV', 'ZAR'}
    rates_df = rates_df[rates_df['Currency'].isin(specific_currencies)].copy()
    
    rates_df['Ingestion_Time'] = datetime.now()
    
    currency_to_geo = {
        'USD': {'Country': 'United States', 'Region': 'North America', 'Continent': 'America'},
        'CAD': {'Country': 'Canada', 'Region': 'North America', 'Continent': 'America'}
    }
    
    geo_data = rates_df['Currency'].map(currency_to_geo)
    rates_df['Country'] = geo_data.apply(lambda x: x.get('Country') if isinstance(x, dict) else None)
    rates_df['Region'] = geo_data.apply(lambda x: x.get('Region') if isinstance(x, dict) else None)
    rates_df['Continent'] = geo_data.apply(lambda x: x.get('Continent') if isinstance(x, dict) else None)
    
    wealthy_currencies = {'USD', 'CAD', 'BRL', 'ARS', 'AUD', 'FJD', 'JPY', 'CNY', 'EUR', 'GBP', 'ZAR', 'ETB'}
    rates_df['Wealthy'] = rates_df['Currency'].apply(lambda x: 1 if x in wealthy_currencies else 0)
    
    rates_df = rates_df.drop_duplicates(subset=['Currency', 'Date'])
    
    return rates_df
