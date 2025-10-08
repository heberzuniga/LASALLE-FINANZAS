# app.py
import streamlit as st

# ---------------------- CONFIGURACIÓN GENERAL ----------------------
st.set_page_config(
    page_title="Benessere Acai Lite - Executive Financial Report",
    page_icon="🍇",
    layout="wide"
)

# ---------------------- LOGO Y TÍTULO ----------------------
st.markdown("""
<h1 style='text-align: center; color: #6C63FF; font-size: 42px; margin-bottom: -10px;'>
    <b>Benessere</b>
</h1>
<p style='text-align: center; color: gray; font-size: 18px;'>
    Açaí Lite – Interactive Financial Dashboard
</p>
""", unsafe_allow_html=True)

# ---------------------- INICIALIZAR VARIABLES GLOBALES ----------------------
defaults = {
    "price_talla_m": 12.0,
    "cost_acai_m": 3.5,
    "cost_fruits": 2.0,
    "cost_granola": 1.5,
    "units_per_day": 100,
    "working_days": 26,
    "fixed_costs": 8000,
    "discount_rate": 0.15,
    "lang": "Español"
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------------- SELECTOR DE IDIOMA ----------------------
language = st.sidebar.selectbox(
    "🌍 Language / Idioma",
    ["Español", "English"],
    index=0 if st.session_state["lang"] == "Español" else 1
)
st.session_state["lang"] = language

# ---------------------- NAVBAR CON BOTONES STREAMLIT ----------------------
def navbar():
    st.markdown(
        """
        <style>
        div[data-testid="column"] {
            text-align: center;
        }
        button[kind="secondary"] {
            background-color: #6C63FF !important;
            color: white !important;
            border-radius: 25px !important;
            font-weight: 500 !important;
            border: none !important;
        }
        button[kind="secondary"]:hover {
            background-color: #594FE3 !important;
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(108,99,255,0.3);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    cols = st.columns(6)
    labels = [
        "🏠 Inicio" if language == "Español" else "🏠 Home",
        "📊 Supuestos" if language == "Español" else "📊 Assumptions",
        "💸 Márgenes" if language == "Español" else "💸 Unit Economics",
        "📅 Forecast 12M",
        "💰 Fondos" if language == "Español" else "💰 Use of Funds",
        "📈 Dashboard"
    ]
    pages = [
        "app.py",
        "pages/1_Assumptions.py",
        "pages/2_UnitEconomics.py",
        "pages/3_Forecast12M.py",
        "pages/4_UseOfFunds.py",
        "pages/5_ExecutiveDashboard.py"
    ]
    for i, col in enumerate(cols):
        if col.button(labels[i]):
            st.switch_page(pages[i])

navbar()

# ---------------------- CONTENIDO PRINCIPAL ----------------------
if language == "Español":
    st.markdown("""
    ---
    ### 💬 Resumen del proyecto

    **Benessere Açaí Lite** es un modelo financiero interactivo diseñado para visualizar en tiempo real 
    cómo las decisiones estratégicas impactan la rentabilidad y el flujo de fondos del negocio.  
    Permite ajustar precios, costos y escenarios operativos para analizar indicadores clave como el 
    **Margen Bruto**, **VAN**, **TIR** y **Payback**, ofreciendo una visión clara y profesional para 
    presentaciones ante inversionistas.

    ---
    ### 🧭 Navegación
    - **1️⃣ Supuestos (Assumptions):** modifica precios, costos y días laborales.  
    - **2️⃣ Márgenes Unitarios (Unit Economics):** analiza el margen por producto.  
    - **3️⃣ Forecast 12M:** visualiza ingresos, utilidades, VAN y TIR.  
    - **4️⃣ Uso de Fondos (Use of Funds):** distribuye capital inicial y genera gráfico de pastel.  
    - **5️⃣ Dashboard Ejecutivo:** consolida todos los indicadores y genera reportes PDF/Excel.

    ---
    ### 🧠 Cómo usar
    1. Ve a la pestaña **Assumptions** y ajusta tus parámetros.  
    2. Navega a **Forecast 12M** para ver resultados dinámicos.  
    3. Presenta los indicadores en modo presentación 🎥.  
    4. Exporta reportes desde el **Dashboard Ejecutivo**.
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    ---
    ### 💬 Project Summary

    **Benessere Açaí Lite** is an interactive financial model designed to visualize in real time 
    how strategic decisions impact profitability and cash flow.  
    It allows adjusting prices, costs, and operating scenarios to analyze key indicators such as 
    **Gross Margin**, **NPV**, **IRR**, and **Payback**, providing a clear and professional view 
    for investor presentations.

    ---
    ### 🧭 Navigation
    - **1️⃣ Assumptions:** modify prices, costs, and working days.  
    - **2️⃣ Unit Economics:** analyze per-product margins.  
    - **3️⃣ Forecast 12M:** view revenue, profit, NPV and IRR.  
    - **4️⃣ Use of Funds:** allocate initial capital and generate pie chart.  
    - **5️⃣ Executive Dashboard:** consolidate all KPIs and export PDF/Excel reports.

    ---
    ### 🧠 How to use
    1. Go to **Assumptions** and adjust your parameters.  
    2. Navigate to **Forecast 12M** for dynamic results.  
    3. Present in fullscreen 🎥 mode.  
    4. Export your reports from the **Executive Dashboard**.
    """, unsafe_allow_html=True)
