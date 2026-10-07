import streamlit as st
import pandas as pd
from src.metrics.risk_calculator import *

def display_kpis(balance:float, deals:pd.DataFrame):
    st.metric(label="Balance Actual", value=f"${balance:,.2f}")


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