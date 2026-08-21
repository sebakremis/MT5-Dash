import logging
import MetaTrader5 as mt5

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def get_latest_rate(symbol: str) -> float:
    """
    Obtiene el precio actual (Bid) directamente de la terminal MT5.
    Refleja el precio exacto del broker.
    """
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        logging.error(f"No se pudo obtener el precio de MT5 para {symbol}. ¿Está habilitado en el Market Watch?")
        return None
    return tick.bid