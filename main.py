from scripts.data_fetcher import obtener_datos
from scripts.data_preprocessing import procesar_datos
from scripts.utils import conectar_redshift, eliminar_registros, insertar_datos, cerrar_conexion

def main():
    try:
        # Obtener los datos desde la API
        rates_df, base_currency, date = obtener_datos()
        
        # Procesar los datos obtenidos
        rates_df = procesar_datos(rates_df, date)
        
        # Conectar a Redshift
        conn, cur = conectar_redshift()
        
        try:
            # Eliminar registros existentes
            eliminar_registros(cur, rates_df)
            
            # Insertar los datos en Redshift
            insertar_datos(cur, conn, rates_df, base_currency, date)
            
        except Exception as e:
            print(f"Error durante el procesamiento o la inserción de datos: {e}")
            conn.rollback()  # Hacer rollback en caso de error
        
        finally:
            # Asegúrate de cerrar la conexión incluso si hubo un error
            cerrar_conexion(cur, conn)
    
    except Exception as e:
        print(f"Error en la función principal: {e}")
    
    else:
        print("Datos insertados correctamente en Redshift")

if __name__ == "__main__":
    main()
