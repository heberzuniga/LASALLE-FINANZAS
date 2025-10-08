# app.py
import streamlit as st

# ---------------------- CONFIGURACIÓN GENERAL ----------------------
st.set_page_config(

    page_title=self.cell(0, 10, "Benessere Acai Lite - Executive Financial Report", ln=True, align="C"),
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

# ---------------------- SELECTOR DE IDIOMA GLOBAL ----------------------
if "lang" not in st.session_state:
    st.session_state["lang"] = "Español"

language = st.sidebar.selectbox(
    "🌍 Language / Idioma",
    ["Español", "English"],
    index=0 if st.session_state["lang"] == "Español" else 1
)
st.session_state["lang"] = language

# ---------------------- BOTÓN DE MODO PRESENTACIÓN ----------------------
if st.sidebar.button("🎥 Iniciar modo presentación / Start presentation mode"):
    st.markdown("""
        <script>
            var elem = document.documentElement;
            if (elem.requestFullscreen) {
                elem.requestFullscreen();
            } else if (elem.mozRequestFullScreen) {
                elem.mozRequestFullScreen();
            } else if (elem.webkitRequestFullscreen) {
                elem.webkitRequestFullscreen();
            } else if (elem.msRequestFullscreen) {
                elem.msRequestFullscreen();
            }
        </script>
    """, unsafe_allow_html=True)

# ---------------------- CONTENIDO DE PORTADA ----------------------
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
    
    ---
    ### 🧠 Cómo usar
    1. Ve a la pestaña **Assumptions** y ajusta tus parámetros.
    2. Navega a **Forecast 12M** para ver resultados dinámicos.
    3. Presenta los indicadores en modo presentación 🎥.
    """)
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
    
    ---
    ### 🧠 How to use
    1. Go to the **Assumptions** tab and set your parameters.
    2. Navigate to **Forecast 12M** to view dynamic results.
    3. Present results in fullscreen 🎥 mode.
    """)
