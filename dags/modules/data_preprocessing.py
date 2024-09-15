from datetime import datetime
import pandas as pd

def procesar_datos(rates_df, date):
    # Filtrar las monedas específicas
    specific_currencies = {'USD', 'ARS', 'AUD', 'BDT', 'BRL', 'CAD', 'CNY', 'ETB', 'EUR', 'FJD', 'GBP', 'HTG', 'JPY', 'NGN', 'NIO', 'PGK', 'PYG', 'SLL', 'VUV', 'ZAR'}
    rates_df = rates_df[rates_df['Currency'].isin(specific_currencies)].copy()
    
    # Agregar columna temporal para el control de ingesta de datos
    rates_df['Ingestion_Time'] = datetime.now()
    
    # Diccionario de monedas a datos geográficos
    currency_to_geo = {
        'USD': {'Country': 'United States', 'Region': 'North America', 'Continent': 'America'},
        'CAD': {'Country': 'Canada', 'Region': 'North America', 'Continent': 'America'},
        'HTG': {'Country': 'Haiti', 'Region': 'Caribbean', 'Continent': 'America'},
        'NIO': {'Country': 'Nicaragua', 'Region': 'Central America', 'Continent': 'America'},
        'BRL': {'Country': 'Brazil', 'Region': 'South America', 'Continent': 'America'},
        'ARS': {'Country': 'Argentina', 'Region': 'South America', 'Continent': 'America'},
        'AUD': {'Country': 'Australia', 'Region': 'Oceania', 'Continent': 'Oceania'},
        'BDT': {'Country': 'Bangladesh', 'Region': 'South Asia', 'Continent': 'Asia'},
        'EUR': {'Country': 'Eurozone', 'Region': 'Europe', 'Continent': 'Europe'},
        'GBP': {'Country': 'United Kingdom', 'Region': 'Europe', 'Continent': 'Europe'},
        'FJD': {'Country': 'Fiji', 'Region': 'Melanesia', 'Continent': 'Oceania'},
        'JPY': {'Country': 'Japan', 'Region': 'East Asia', 'Continent': 'Asia'},
        'CNY': {'Country': 'China', 'Region': 'East Asia', 'Continent': 'Asia'},
        'NGN': {'Country': 'Nigeria', 'Region': 'West Africa', 'Continent': 'Africa'},
        'ETB': {'Country': 'Ethiopia', 'Region': 'East Africa', 'Continent': 'Africa'},
        'PGK': {'Country': 'Papua New Guinea', 'Region': 'Melanesia', 'Continent': 'Oceania'},
        'PYG': {'Country': 'Paraguay', 'Region': 'South America', 'Continent': 'America'},
        'SLL': {'Country': 'Sierra Leone', 'Region': 'West Africa', 'Continent': 'Africa'},
        'VUV': {'Country': 'Vanuatu', 'Region': 'Melanesia', 'Continent': 'Oceania'},
        'ZAR': {'Country': 'South Africa', 'Region': 'Southern Africa', 'Continent': 'Africa'}
    }
    
    # Agregar datos geográficos usando el diccionario
    geo_data = rates_df['Currency'].map(currency_to_geo)
    rates_df['Country'] = geo_data.apply(lambda x: x.get('Country') if isinstance(x, dict) else None)
    rates_df['Region'] = geo_data.apply(lambda x: x.get('Region') if isinstance(x, dict) else None)
    rates_df['Continent'] = geo_data.apply(lambda x: x.get('Continent') if isinstance(x, dict) else None)
    
    # Definir las monedas de los países ricos
    wealthy_currencies = {'USD', 'CAD', 'BRL', 'ARS', 'AUD', 'FJD', 'JPY', 'CNY', 'EUR', 'GBP', 'ZAR', 'ETB'}
    
    # Agregar columna Wealthy
    rates_df['Wealthy'] = rates_df['Currency'].apply(lambda x: 1 if x in wealthy_currencies else 0)
    
    # Eliminar duplicados (en caso de que existan en el DataFrame)
    rates_df = rates_df.drop_duplicates(subset=['Currency', 'Date'])
    
    return rates_df
