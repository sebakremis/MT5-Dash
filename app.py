import streamlit as st
st.set_page_config(page_title="📊 MT5 - Dash", layout="wide")

from src.api.mt5_connection import *
from src.metrics.risk_calculator import *

# Envolver la extracción pesada en caché para evitar consultas redundantes
@st.cache_data(ttl=300) # El caché expirará y buscará datos nuevos cada 5 minutos
def load_historical_deals() -> pd.DataFrame:
    return get_historical_deals()

def display_sidebar(balance:float):
    with st.sidebar:
        st.header("Position Size Calculator")
        symbol = st.text_input("Símbolo", value="EURUSD.sml")
        stop_loss_pips = st.number_input("Stop Loss en pips", min_value=1.0, value=100.0)
        risk = st.number_input("Riesgo (%)", min_value=0.1, value=1.0, step=0.1)
        button = st.button("Calcular")

        if button:
            pip_value = get_pip_value(symbol)
            position_size = calculate_position_size(
                balance=balance, 
                stop_loss_pips=stop_loss_pips, 
                pip_value=pip_value, 
                risk_percentage=risk
                )
            st.success(f"Lotes sugeridos: **{position_size}**")


def main():
    st.title("📊 MT5 Dash")
    st.markdown("---")

    # Conectar a MT5 y obtener datos
    # Inicializar la conexión una sola vez utilizando el estado de sesión
    if 'mt5_connected' not in st.session_state:
        init_mt5_connection()
        st.session_state['mt5_connected'] = True

    # Consulta sin caché
    account_info = get_account_info()

    if not account_info.empty:
        balance = account_info['balance'].iloc[0]
        st.metric(label="Balance Actual", value=f"${balance:,.2f}")

        deals = load_historical_deals()
        st.dataframe(deals, width='stretch')

        display_sidebar(balance)

    else:
        st.error("No se pudo obtener la información de la cuenta de MetaTrader 5.")


if __name__ == "__main__":
    main()