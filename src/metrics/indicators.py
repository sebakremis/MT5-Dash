import pandas as pd

def kpis_calculator(deals:pd.DataFrame):
    # Filtrar operaciones (Type 0: venta / Type 1: compra)
    ops = deals[deals.type < 2]
    n_trades = ops.shape[0]

    # Calcular operaciones con ganancia y perdida
    wins = ops[ops.profit > 0]
    n_wins = wins.shape[0]
    win_rate = (n_wins / n_trades) * 100
    gross_profits =  wins['profit'].sum()

    losses = ops[ops.profit < 0]
    n_losses = losses.shape[0]
    gross_losses =  losses['profit'].sum()

    profit_factor = gross_profits / abs(gross_losses)

    return n_trades, win_rate, profit_factor
