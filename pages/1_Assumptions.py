# pages/1_Assumptions.py
import streamlit as st
from core.assumptions import get_default_assumptions

st.set_page_config(page_title="Assumptions", layout="wide")

lang = st.session_state.get("lang", "Español")
defaults = get_default_assumptions()

st.title("📊 Supuestos / Assumptions")

col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 Precios y Costos Variables")
    st.session_state["price_talla_m"] = st.number_input(
        "Precio por bowl Talla M [Bs] / Price M [Bs]",
        value=defaults["price_talla_m"], min_value=10.0, step=0.5)
    st.session_state["price_talla_s"] = st.number_input(
        "Precio por bowl Talla S [Bs] / Price S [Bs]",
        value=defaults["price_talla_s"], min_value=10.0, step=0.5)

    st.session_state["cost_acai_m"] = st.number_input("Costo Açaí Talla M [Bs] / Açaí Cost M [Bs]",
        value=defaults["cost_acai_m"], min_value=0.0, step=0.5)
    st.session_state["cost_acai_s"] = st.number_input("Costo Açaí Talla S [Bs] / Açaí Cost S [Bs]",
        value=defaults["cost_acai_s"], min_value=0.0, step=0.5)

    st.session_state["cost_fruits"] = st.number_input("Costo Frutas [Bs] / Fruits Cost [Bs]",
        value=defaults["cost_fruits"], min_value=0.0, step=0.2)
    st.session_state["cost_granola"] = st.number_input("Costo Granola [Bs] / Granola Cost [Bs]",
        value=defaults["cost_granola"], min_value=0.0, step=0.2)

with col2:
    st.subheader("⚙️ Operación")
    st.session_state["units_per_day"] = st.number_input(
        "Unidades por día / Units per day",
        value=defaults["units_per_day"], min_value=1)
    st.session_state["working_days"] = st.slider(
        "Días laborales por mes / Working days per month",
        min_value=20, max_value=30, value=defaults["working_days"])
    st.session_state["fixed_costs"] = st.number_input(
        "Costos Fijos Mensuales [Bs] / Monthly Fixed Costs [Bs]",
        value=defaults["fixed_costs"], min_value=0.0, step=100.0)
    st.session_state["discount_rate"] = st.slider(
        "Tasa de descuento (%) / Discount rate (%)",
        min_value=5.0, max_value=20.0, value=defaults["discount_rate"]*100, step=0.5) / 100

st.success("✅ Parámetros actualizados / Parameters updated")
