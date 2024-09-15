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
