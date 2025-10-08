# pages/2_UnitEconomics.py
import streamlit as st
import pandas as pd
from core.calculations import calc_unit_economics

st.set_page_config(page_title="Unit Economics", layout="wide")

lang = st.session_state.get("lang", "Español")
st.title("📈 Unit Economics / Márgenes Unitarios")

if "price_talla_m" not in st.session_state:
    st.warning("Por favor, configure los supuestos en la pestaña Assumptions / Set assumptions first.")
else:
    results = []
    m = calc_unit_economics(
        st.session_state["price_talla_m"],
        st.session_state["cost_acai_m"],
        st.session_state["cost_fruits"],
        st.session_state["cost_granola"])
    s = calc_unit_economics(
        st.session_state["price_talla_s"],
        st.session_state["cost_acai_s"],
        st.session_state["cost_fruits"],
        st.session_state["cost_granola"])

    df = pd.DataFrame([m, s], index=["Talla M / Size M", "Talla S / Size S"])
    st.dataframe(df.style.format("{:.2f}"))
