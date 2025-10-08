# pages/3_Forecast12M.py
import streamlit as st
import plotly.express as px
from core.forecast import generar_forecast
from core.calculations import calcular_van_tir, calcular_payback

st.set_page_config(page_title="Forecast 12M", layout="wide")

lang = st.session_state.get("lang", "Español")
st.title("📅 Forecast 12 Meses / 12-Month Forecast")

# Entradas del estado
price = st.session_state["price_talla_m"]
cost_acai = st.session_state["cost_acai_m"]
cost_fruits = st.session_state["cost_fruits"]
cost_granola = st.session_state["cost_granola"]
variable_cost = cost_acai + cost_fruits + cost_granola
units_day = st.session_state["units_per_day"]
days = st.session_state["working_days"]
fixed_costs = st.session_state["fixed_costs"]
rate = st.session_state["discount_rate"]

# Generar forecast
df = generar_forecast(price, variable_cost, units_day, days, fixed_costs)

# Calcular VAN y TIR
flujos = df["Utilidad Operativa [Bs]"].tolist()
van, tir = calcular_van_tir(flujos, rate)
payback = calcular_payback(flujos)

# Mostrar KPIs
c1, c2, c3 = st.columns(3)
c1.metric("VAN / NPV [Bs]", f"{van:,.2f}")
c2.metric("TIR / IRR [%]", f"{tir*100:,.2f}")
c3.metric("Payback (meses)", f"{payback if payback else '—'}")

# Mostrar tabla y gráfico
st.dataframe(df.style.format("{:.2f}"))
fig = px.bar(df, x="Mes", y="Utilidad Operativa [Bs]",
             title="Utilidad Operativa Mensual [Bs] / Monthly Operating Profit [Bs]",
             text_auto=".2s", color_discrete_sequence=["#6C63FF"])
st.plotly_chart(fig, use_container_width=True)
