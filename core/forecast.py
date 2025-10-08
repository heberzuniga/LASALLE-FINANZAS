# core/forecast.py
import pandas as pd

def generar_forecast(price, variable_cost, units_per_day, working_days, fixed_costs):
    """
    Genera un DataFrame con proyección de 12 meses de ingresos y utilidades.
    """
    meses = list(range(1, 13))
    datos = []

    for mes in meses:
        units_month = units_per_day * working_days
        revenue = price * units_month
        cogs = variable_cost * units_month
        gross_profit = revenue - cogs
        operating_profit = gross_profit - fixed_costs
        datos.append({
            "Mes": mes,
            "Unidades": units_month,
            "Ingresos [Bs]": revenue,
            "COGS [Bs]": cogs,
            "Utilidad Operativa [Bs]": operating_profit
        })

    df = pd.DataFrame(datos)
    df["Utilidad Acumulada [Bs]"] = df["Utilidad Operativa [Bs]"].cumsum()
    return df
