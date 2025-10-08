# pages/4_UseOfFunds.py
import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Use of Funds", layout="wide")

lang = st.session_state.get("lang", "Español")
st.title("💰 Uso de Fondos / Use of Funds")

categorias = ["Infraestructura", "Equipamiento", "Inventario Inicial", "Capital de Trabajo", "Contingencia"]
montos = []

st.subheader("🏗️ Asigna los montos (Bs)")
for c in categorias:
    montos.append(st.number_input(f"{c}", min_value=0.0, value=1000.0, step=100.0))

df = pd.DataFrame({"Categoría": categorias, "Monto [Bs]": montos})
fig = px.pie(df, values="Monto [Bs]", names="Categoría",
             title="Distribución de Fondos / Fund Allocation",
             color_discrete_sequence=px.colors.sequential.Purples)
st.plotly_chart(fig, use_container_width=True)
st.dataframe(df.style.format("{:.2f}"))
