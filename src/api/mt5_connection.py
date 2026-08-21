import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import logging

# Configuración de logging para monitorear la conexión en consola
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def init_mt5_connection() -> bool:
    """
    Inicializa la conexión con el terminal de MetaTrader 5.
    Retorna True si es exitosa, False en caso contrario.
    """
    if not mt5.initialize():
        logging.error(f"Fallo al inicializar MT5. Código de error: {mt5.last_error()}")
        return False
    logging.info("Conexión con MetaTrader 5 establecida correctamente.")
    return True

def get_historical_deals(start_date: datetime, end_date: datetime=datetime.now()) -> pd.DataFrame:
    """
    Extrae el historial de operaciones (deals) en un rango de fechas (por defecto hasta el dia actual).
    Devuelve un DataFrame de pandas.
    """
    deals = mt5.history_deals_get(start_date, end_date)
    
    if deals is None or len(deals) == 0:
        logging.warning("No se encontraron operaciones en el rango de fechas.")
        return pd.DataFrame()
        
    # Convertir la tupla de datos a un DataFrame
    df = pd.DataFrame(list(deals), columns=deals[0]._asdict().keys())
    
    # Formateo básico de fechas (de segundos UNIX a datetime)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    
    return df

def close_mt5_connection():
    """Cierra la conexión con la terminal de MT5."""
    mt5.shutdown()
    logging.info("Conexión con MetaTrader 5 cerrada.")