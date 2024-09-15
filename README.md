# **Proyecto de Ingesta y Procesamiento de Datos de Tasas de Cambio**

Este proyecto tiene como objetivo obtener datos de tasas de cambio de una API pública, procesarlos para agregar información geográfica y de riqueza, y cargarlos en una base de datos Amazon Redshift para su posterior análisis.

## **Estructura del Proyecto**

El proyecto está dividido en varios archivos de Python, cada uno con responsabilidades específicas:

- **`dag_exchange_rate.py`**: Orquesta la obtención, procesamiento e inserción de los datos en Redshift utilizando Apache Airflow.
- **`data_fetcher.py`**: Contiene la función `obtener_datos`, que realiza la solicitud a la API de tasas de cambio y convierte la respuesta en un DataFrame de pandas.
- **`data_preprocessing.py`**: Contiene la función `procesar_datos`, encargada de limpiar y transformar los datos, agregar información geográfica y marcar si un país es rico.
- **`utils.py`**: Proporciona funciones auxiliares para:
  - **`conectar_redshift`**: Establece la conexión con Amazon Redshift utilizando credenciales almacenadas en un archivo `.env`.
  - **`eliminar_registros`**: Elimina registros existentes en la tabla `exchange_rates` basados en la clave primaria compuesta de `currency` y `date`.
  - **`insertar_datos`**: Inserta los datos procesados en la tabla `exchange_rates`.
  - **`cerrar_conexion`**: Cierra la conexión a la base de datos.

## **Creación de la Tabla en Redshift**

La tabla `exchange_rates` fue creada en Amazon Redshift utilizando el siguiente script SQL:

```sql
CREATE TABLE exchange_rates (
    base VARCHAR(10) NOT NULL,          -- Columna para la moneda base
    date DATE NOT NULL,                 -- Columna para la fecha
    currency VARCHAR(10) NOT NULL,      -- Columna para la moneda
    rate FLOAT,                         -- Columna para la tasa de cambio
    ingestion_time TIMESTAMP,           -- Columna para la hora de ingestión
    country VARCHAR(255),               -- Columna para el país
    region VARCHAR(255),                -- Columna para la región
    continent VARCHAR(255),             -- Columna para el continente
    wealthy INTEGER,                    -- Columna para indicar si el país es rico
    PRIMARY KEY (currency, date)        -- Clave primaria compuesta
);

Flujo de Trabajo:
1. Conexión a la API: dag_exchange_rate.py llama a obtener_datos para obtener las tasas de cambio desde la API pública.
2. Procesamiento de Datos: Los datos se procesan con procesar_datos, donde se filtran y se agregan columnas adicionales.
3. Conexión a Redshift: Se establece una conexión con Amazon Redshift usando conectar_redshift.
4. Eliminación de Registros: Se eliminan registros existentes en Redshift con la misma clave primaria.
5. Inserción de Datos: Los datos procesados se insertan en la tabla exchange_rates.
6. Cierre de Conexión: La conexión a Redshift se cierra al finalizar.

Requisitos
Python 3.7+
Pandas
Psycopg2
Requests
Archivo .env con las credenciales para Redshift.

Ejecución del Proyecto
1. Clonar este repositorio.
2. Configurar un archivo .env con las credenciales de Redshift.
3. Ejecutar dag_exchange_rate.py usando Apache Airflow para orquestar la ingesta, procesamiento y carga de los datos en Redshift.

Configuración con Docker
Este proyecto también puede ser ejecutado usando Docker y Docker Compose. Asegúrate de tener Docker y Docker Compose instalados.

1. Configurar el archivo .env: Asegúrate de que el archivo .env esté correctamente configurado con las credenciales de Redshift.

2. Construir y ejecutar los contenedores:
docker-compose build
docker-compose up 

Esto iniciará los servicios necesarios, incluidos el servidor de Airflow, el planificador y la base de datos PostgreSQL.

3. Inicializar Airflow:
docker-compose run --rm airflow-init

4. Acceder a la interfaz web de Airflow: Abre tu navegador y ve a http://localhost:8080 para acceder a la interfaz de Airflow.

Este README ahora incluye toda la información necesaria sobre el flujo de trabajo, requisitos, ejecución del proyecto y configuración con Docker.

