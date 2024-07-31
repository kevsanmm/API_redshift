-- Crear la tabla exchange_rates con las columnas iniciales
CREATE TABLE exchange_rates (
    base VARCHAR(10),
    date DATE,
    currency VARCHAR(10),
    rate FLOAT,
    ingestion_time TIMESTAMP,
    country VARCHAR(255),
    region VARCHAR(255),
    continent VARCHAR(255)
);

-- Añadir la columna wealthy a la tabla existente
ALTER TABLE exchange_rates
ADD COLUMN wealthy BOOLEAN;
