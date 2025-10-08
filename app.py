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
# (Evita KeyError en todas las páginas si se accede directamente)
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
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------------- SELECTOR DE IDIOMA GLOBAL ----------------------
language = st.sidebar.selectbox(
    "🌍 Language / Idioma",
    ["Español", "English"],
    index=0 if st.session_state["lang"] == "Español" else 1
)
st.session_state["lang"] = language

# ---------------------- BARRA SUPERIOR DE NAVEGACIÓN ----------------------
def navbar():
    """Barra superior fija con botones de navegación."""
    lang = st.session_state["lang"]
    if lang == "Español":
        pages = {
            "🏠 Inicio": "app.py",
            "📊 Supuestos": "1_Assumptions",
            "💸 Márgenes Unitarios": "2_UnitEconomics",
            "📅 Forecast 12M": "3_Forecast12M",
            "💰 Uso de Fondos": "4_UseOfFunds",
            "📈 Dashboard Ejecutivo": "5_ExecutiveDashboard",
        }
    else:
        pages = {
            "🏠 Home": "app.py",
            "📊 Assumptions": "1_Assumptions",
            "💸 Unit Economics": "2_UnitEconomics",
            "📅 12M Forecast": "3_Forecast12M",
            "💰 Use of Funds": "4_UseOfFunds",
            "📈 Executive Dashboard": "5_ExecutiveDashboard",
        }

    st.markdown(
        """
        <style>
        .navbar {
            position: sticky;
            top: 0;
            z-index: 999;
            background-color: white;
            border-bottom: 1px solid #EAEAEA;
            padding: 10px 0;
            display: flex;
            justify-content: center;
            gap: 15px;
            box-shadow: 0px 2px 4px rgba(0,0,0,0.05);
        }
        .nav-button {
            background-color: #6C63FF;
            color: white;
            border: none;
            padding: 8px 20px;
            border-radius: 25px;
            cursor: pointer;
            font-weight: 500;
            font-size: 14px;
            transition: 0.3s;
        }
        .nav-button:hover {
            background-color: #594FE3;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    nav_html = "<div class='navbar'>"
    for label, page in pages.items():
        nav_html += f"""
            <form action='/{page}' target='_self'>
                <button class='nav-button'>{label}</button>
            </form>
        """
    nav_html += "</div>"
    st.markdown(nav_html, unsafe_allow_html=True)

# Mostrar la barra
navbar()

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
    - **5️⃣ Dashboard Ejecutivo:** consolida todos los indicadores y genera reportes PDF/Excel.
    
    ---
    ### 🧠 Cómo usar
    1. Ve a la pestaña **Assumptions** y ajusta tus parámetros.
    2. Navega a **Forecast 12M** para ver resultados dinámicos.
    3. Presenta los indicadores en modo presentación 🎥.
    4. Exporta tus reportes desde el **Dashboard Ejecutivo**.
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
    - **5️⃣ Executive Dashboard:** consolidate all KPIs and export PDF/Excel reports.
    
    ---
    ### 🧠 How to use
    1. Go to the **Assumptions** tab and set your parameters.
    2. Navigate to **Forecast 12M** to view dynamic results.
    3. Present results in fullscreen 🎥 mode.
    4. Export reports from the **Executive Dashboard**.
    """)
