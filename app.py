import streamlit as st
st.set_page_config(page_title="📊 MT5 - Dash", layout="wide")

from src.api.mt5_connection import *
from src.ui.dashboard_display import *


# Envolver la extracción de trades en caché para evitar consultas redundantes
@st.cache_data(ttl=300) # El caché expirará y buscará datos nuevos cada 5 minutos
def load_historical_deals() -> pd.DataFrame:
    return get_historical_deals()


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
        # Extraer trades de memoria y obtener el balance de cuenta
        deals = load_historical_deals()
        balance = account_info['balance'].iloc[0]

        # Mostrar las secciones del dashboard
        display_kpis(balance, deals)
        display_sidebar(balance)

    else:
        st.error("No se pudo obtener la información de la cuenta de MetaTrader 5.")


if __name__ == "__main__":
    main()