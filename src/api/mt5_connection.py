import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import logging
from typing import Optional

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


def get_historical_deals(start_date: Optional[datetime] = None, 
                         end_date: Optional[datetime] = None) -> pd.DataFrame:
    """
    Extrae el historial de operaciones (deals) en un rango de fechas.
    Por defecto (None, None), extrae todo el historial histórico hasta el instante actual.
    """
    # 1. Asignar 'el inicio de los tiempos' para MT5 si no se provee fecha
    if start_date is None:
        start_date = datetime(2010, 1, 1)
        
    # 2. Capturar el instante exacto de la ejecución si no se provee fecha
    if end_date is None:
        end_date = datetime.now()

    # Extraer operaciones desde la terminal MT5
    deals = mt5.history_deals_get(start_date, end_date)
    
    if deals is None or len(deals) == 0:
        logging.warning("No se encontraron operaciones en el rango de fechas.")
        return pd.DataFrame()
        
    # Convertir a DataFrame dinámicamente
    df = pd.DataFrame(list(deals), columns=deals[0]._asdict().keys())
    
    # Formateo básico de fechas (de segundos UNIX a datetime)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    
    return df


def get_account_info()->pd.DataFrame:
    """
    Obtiene la información de la cuenta conectada en MT5.
    """
    # Obtener info como namedtuple
    account_info = mt5.account_info()
    if account_info is not None:
        # Convertir a diccionario
        account_info_dict = account_info._asdict()
 
        # Convertir a DataFrame (1 fila, N columnas) pasando el dict en una lista
        df=pd.DataFrame([account_info_dict])
        return df
    else:
        logging.error(f"No se pudo obtener información de la cuenta, código de error = {mt5.last_error()}")
        return pd.DataFrame()


def get_symbol_info(symbol:str):
    """
    Obtener información de un par Forex.
    """
    # Forzar que el símbolo esté habilitado en el Market Watch
    mt5.symbol_select(symbol, True)
    
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is not None:
        symbol_info_dict = symbol_info._asdict()
        df = pd.DataFrame([symbol_info_dict])
        return df
    else:
            logging.error(f"No se pudo obtener información para el símbolo {symbol}, código de error = {mt5.last_error()}")
            return pd.DataFrame()


def close_mt5_connection():
    """Cierra la conexión con la terminal de MT5."""
    mt5.shutdown()
    logging.info("Conexión con MetaTrader 5 cerrada.")