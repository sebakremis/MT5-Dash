import logging
from typing import Tuple
from src.api.mt5_connection import get_symbol_info

def get_base_quote(symbol: str) -> Tuple[str, str]:
    """
    Dado un par de divisas (ej. 'EURUSD'), devuelve la moneda base y la moneda quote.
    """
    # Se limpia el string por si el bróker usa sufijos (ej. 'EURUSD.m')
    clean_symbol = symbol.split('.')[0].replace('-', '') 
    
    if len(clean_symbol) >= 6:
        base_currency = clean_symbol[:3]
        quote_currency = clean_symbol[3:6]
        return base_currency, quote_currency
    else:
        raise ValueError(f"Formato de símbolo no reconocido para Forex: {symbol}")


def get_pip_value(symbol: str) -> float:
    """
    Calcula el valor monetario de un pip (para 1 lote estándar) en la moneda 
    de la cuenta actual utilizando los datos del servidor de MT5.
    """
    symbol_info = get_symbol_info(symbol)
    
    if symbol_info is None:
        logging.error(f"No se pudo encontrar información para el símbolo: {symbol}")
        return 0.0

    # 1. Determinar el tamaño de un pip estándar según el par
    # Los pares con JPY (ej. USDJPY) tienen pips de 2 decimales (0.01)
    # El resto de pares estándar tienen pips de 4 decimales (0.0001)
    base, quote = get_base_quote(symbol)
    pip_size = 0.01 if quote == 'JPY' or base == 'JPY' else 0.0001
    
    # 2. Extraer datos del servidor
    tick_value = symbol_info['trade_tick_value'].iloc[0] # Valor de 1 tick en la moneda de la cuenta
    tick_size = symbol_info['trade_tick_size'].iloc[0]   # Tamaño del tick (ej. 0.00001 en brókers de 5 dígitos)
    
    # Prevenir divisiones por cero en caso de desconexión
    if tick_size == 0:
        return 0.0
        
    # 3. Calcular el valor del pip
    # Si el bróker es de 5 dígitos (tick_size = 0.00001), 1 pip equivale a 10 ticks.
    ticks_per_pip = pip_size / tick_size
    pip_value = tick_value * ticks_per_pip
    
    return pip_value


def calculate_position_size(balance: float, stop_loss_pips: float, pip_value: float, risk_percentage: float = 1.0) -> float:
    """
    Calcula el tamaño de lote (volumen) óptimo para una nueva posición.
    
    Args:
        balance (float): El capital actual o balance de la cuenta.
        stop_loss_pips (float): La distancia desde el precio de entrada hasta el Stop Loss en pips.
        pip_value (float): El valor monetario de un pip para el instrumento operado (varía por par).
        risk_percentage (float): Porcentaje del capital a arriesgar. Por defecto 1.0 (1%).
        
    Returns:
        float: El tamaño de la posición en lotes.
    """
    if stop_loss_pips <= 0 or pip_value <= 0:
        logging.error("El Stop Loss y el valor del pip deben ser mayores a cero.")
        return 0.0

    # 1. Calcular el monto en dinero que representa el riesgo
    capital_at_risk = balance * (risk_percentage / 100.0)
    
    # 2. Calcular el tamaño de la posición
    # Fórmula: (Capital en Riesgo) / (Stop Loss en pips * Valor de 1 pip por lote estándar)
    position_size = capital_at_risk / (stop_loss_pips * pip_value)
    
    # Redondear a 2 decimales (estándar para microlotes en MT5)
    return round(position_size, 2)