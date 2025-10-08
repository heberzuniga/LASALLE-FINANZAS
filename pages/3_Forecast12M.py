# pages/3_Forecast12M.py
import streamlit as st
import pandas as pd
import plotly.express as px
from core.forecast import generar_forecast
from core.calculations import calcular_van_tir, calcular_payback

# Configuración
st.set_page_config(page_title="Forecast 12M", layout="wide")

lang = st.session_state.get("lang", "Español")
st.title("📅 Forecast 12 Meses / 12-Month Forecast")

# === Entradas desde session_state ===
price = st.session_state["price_talla_m"]
cost_acai = st.session_state["cost_acai_m"]
cost_fruits = st.session_state["cost_fruits"]
cost_granola = st.session_state["cost_granola"]
variable_cost = cost_acai + cost_fruits + cost_granola
units_day = st.session_state["units_per_day"]
days = st.session_state["working_days"]
fixed_costs = st.session_state["fixed_costs"]
rate = st.session_state["discount_rate"]

# === NUEVO: Control de crecimiento mensual ===
if lang == "Español":
    st.subheader("📈 Crecimiento mensual proyectado de ventas (%)")
else:
    st.subheader("📈 Projected monthly sales growth (%)")

growth_rate = st.slider(
    "Crecimiento mensual (%) / Monthly growth (%)",
    min_value=0.0, max_value=100.0, value=25.0, step=1.0
)

# === Generar forecast base ===
base_df = generar_forecast(price, variable_cost, units_day, days, fixed_costs)

# === Aplicar crecimiento compuesto mes a mes ===
df_growth = base_df.copy()
df_growth["Crecimiento (%) / Growth (%)"] = 0.0

for i in range(1, len(df_growth)):
    df_growth.loc[i, "Ingresos [Bs]"] = df_growth.loc[i-1, "Ingresos [Bs]"] * (1 + growth_rate/100)
    df_growth.loc[i, "COGS [Bs]"] = df_growth.loc[i-1, "COGS [Bs]"] * (1 + growth_rate/100)
    df_growth.loc[i, "Utilidad Operativa [Bs]"] = df_growth.loc[i, "Ingresos [Bs]"] - df_growth.loc[i, "COGS [Bs]"] - fixed_costs
    df_growth.loc[i, "Crecimiento (%) / Growth (%)"] = growth_rate

df_growth["Utilidad Acumulada [Bs]"] = df_growth["Utilidad Operativa [Bs]"].cumsum()

# === Calcular VAN, TIR y Payback ===
flujos = df_growth["Utilidad Operativa [Bs]"].tolist()
van, tir = calcular_van_tir(flujos, rate)
payback = calcular_payback(flujos)

# === Mostrar KPIs ===
c1, c2, c3 = st.columns(3)
c1.metric("VAN / NPV [Bs]", f"{van:,.2f}")
c2.metric("TIR / IRR [%]", f"{tir*100:,.2f}")
c3.metric("Payback (meses)", f"{payback if payback else '—'}")

# === Mostrar tabla ===
df_fmt = df_growth.copy()
for col in df_fmt.select_dtypes(include=["number"]).columns:
    df_fmt[col] = df_fmt[col].map("{:,.2f}".format)
st.dataframe(df_fmt)

# === Mostrar gráfico ===
fig = px.bar(
    df_growth,
    x="Mes",
    y="Utilidad Operativa [Bs]",
    text_auto=".2s",
    title=f"Proyección de Utilidad Mensual con Crecimiento del {growth_rate:.0f}% / Monthly Profit Forecast ({growth_rate:.0f}% Growth)",
    color_discrete_sequence=["#6C63FF"]
)
st.plotly_chart(fig, use_container_width=True)
