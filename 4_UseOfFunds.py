# pages/4_UseOfFunds.py
import streamlit as st
import plotly.express as px
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Use of Funds", layout="wide")

# Idioma global desde session_state
lang = st.session_state.get("lang", "Español")

# Título
if lang == "Español":
    st.title("💰 Uso de Fondos / Use of Funds")
    st.subheader("🏗️ Asigna los montos en bolivianos para cada categoría:")
else:
    st.title("💰 Use of Funds / Capital Allocation")
    st.subheader("🏗️ Assign the amounts in Bolivianos (Bs) for each category:")

# Categorías base
categorias = [
    "Infraestructura / Infrastructure",
    "Equipamiento / Equipment",
    "Inventario Inicial / Initial Inventory",
    "Capital de Trabajo / Working Capital",
    "Contingencia / Contingency"
]

# Entrada de montos (interactiva)
montos = []
for c in categorias:
    valor = st.number_input(f"{c}", min_value=0.0, value=1000.0, step=100.0)
    montos.append(valor)

# Crear DataFrame
df = pd.DataFrame({
    "Categoría / Category": categorias,
    "Monto [Bs] / Amount [Bs]": montos
})

# Gráfico de pastel
fig = px.pie(
    df,
    values="Monto [Bs] / Amount [Bs]",
    names="Categoría / Category",
    title="Distribución de Fondos / Fund Allocation",
    color_discrete_sequence=px.colors.sequential.Purples
)

st.plotly_chart(fig, use_container_width=True)

# Mostrar tabla con formato seguro

# Formatear numéricamente sin usar .style (más estable en Streamlit Cloud)
df_formatted = df.copy()
for col in df_formatted.select_dtypes(include=["number"]).columns:
    df_formatted[col] = df_formatted[col].map("{:,.2f}".format)

st.dataframe(df_formatted)



# Mostrar total
total = df["Monto [Bs] / Amount [Bs]"].sum()
if lang == "Español":
    st.info(f"💵 **Total de fondos asignados:** Bs {total:,.2f}")
else:
    st.info(f"💵 **Total allocated funds:** Bs {total:,.2f}")
