# pages/5_ExecutiveDashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
from core.calculations import calcular_van_tir, calcular_payback
from core.forecast import generar_forecast
import io
from datetime import datetime
from fpdf import FPDF

# ---------------- CONFIGURACIÓN ----------------
st.set_page_config(page_title="Executive Dashboard", layout="wide")

lang = st.session_state.get("lang", "Español")
st.title("📊 Dashboard Financiero Ejecutivo / Executive Financial Dashboard")

# ---------------- VARIABLES BASE (seguros) ----------------
price = st.session_state.get("price_talla_m", 12.0)
cost_acai = st.session_state.get("cost_acai_m", 3.5)
cost_fruits = st.session_state.get("cost_fruits", 2.0)
cost_granola = st.session_state.get("cost_granola", 1.5)
variable_cost = cost_acai + cost_fruits + cost_granola
units_day = st.session_state.get("units_per_day", 100)
days = st.session_state.get("working_days", 26)
fixed_costs = st.session_state.get("fixed_costs", 8000)
rate = st.session_state.get("discount_rate", 0.15)

# ---------------- FORECAST BASE ----------------
df_base = generar_forecast(price, variable_cost, units_day, days, fixed_costs)

# Crecimiento mensual del escenario base (25%)
growth_base = 25.0
for i in range(1, len(df_base)):
    df_base.loc[i, "Ingresos [Bs]"] = df_base.loc[i - 1, "Ingresos [Bs]"] * (1 + growth_base / 100)
    df_base.loc[i, "COGS [Bs]"] = df_base.loc[i - 1, "COGS [Bs]"] * (1 + growth_base / 100)
    df_base.loc[i, "Utilidad Operativa [Bs]"] = (
        df_base.loc[i, "Ingresos [Bs]"] - df_base.loc[i, "COGS [Bs]"] - fixed_costs
    )
df_base["Utilidad Acumulada [Bs]"] = df_base["Utilidad Operativa [Bs]"].cumsum()

# ---------------- CÁLCULOS CLAVE ----------------
flujos = df_base["Utilidad Operativa [Bs]"].tolist()
van, tir = calcular_van_tir(flujos, rate)
payback = calcular_payback(flujos)
total_ingresos = df_base["Ingresos [Bs]"].sum()
total_utilidad = df_base["Utilidad Operativa [Bs]"].sum()
promedio_crecimiento = (df_base["Ingresos [Bs]"].pct_change().mean()) * 100
margen_promedio = (total_utilidad / total_ingresos) * 100

# ---------------- SECCIÓN 1: KPIs ----------------
st.markdown("### 💡 Indicadores Financieros Clave / Key Financial Indicators")
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric("VAN / NPV [Bs]", f"{van:,.2f}")
kpi2.metric("TIR / IRR [%]", f"{tir*100:,.2f}")
kpi3.metric("Payback (meses)", f"{payback if payback else '—'}")
kpi4.metric("Margen Promedio / Avg Margin [%]", f"{margen_promedio:,.2f}")
kpi5.metric("Crecimiento Promedio / Avg Growth [%]", f"{promedio_crecimiento:,.2f}")

# ---------------- SECCIÓN 2: INGRESOS Y UTILIDAD ----------------
st.markdown("### 💰 Proyección Base / Base Scenario Overview")
fig_income = px.bar(
    df_base,
    x="Mes",
    y=["Ingresos [Bs]", "Utilidad Operativa [Bs]"],
    barmode="group",
    title="Ingresos y Utilidad Mensual / Monthly Revenue & Profit",
    color_discrete_sequence=["#6C63FF", "#4F81BD"]
)
st.plotly_chart(fig_income, use_container_width=True)

# ---------------- SECCIÓN 3: ESTRUCTURA DE FONDOS ----------------
st.markdown("### 🧱 Estructura de Inversión / Fund Allocation Overview")
use_of_funds = {
    "Infraestructura / Infrastructure": 10000,
    "Equipamiento / Equipment": 8000,
    "Inventario Inicial / Initial Inventory": 6000,
    "Capital de Trabajo / Working Capital": 4000,
    "Contingencia / Contingency": 2000,
}
df_funds = pd.DataFrame(list(use_of_funds.items()), columns=["Categoría / Category", "Monto [Bs] / Amount [Bs]"])
fig_funds = px.pie(
    df_funds,
    values="Monto [Bs] / Amount [Bs]",
    names="Categoría / Category",
    color_discrete_sequence=px.colors.sequential.Purples,
    title="Distribución de Fondos / Fund Distribution",
)
st.plotly_chart(fig_funds, use_container_width=True)

# ---------------- SECCIÓN 4: RESUMEN ANUAL ----------------
st.markdown("### 📅 Resumen Anual / Annual Summary")
df_resumen = df_base.copy()
df_resumen["Año"] = 1
df_annual = (
    df_resumen.groupby("Año")
    .agg({"Ingresos [Bs]": "sum", "COGS [Bs]": "sum", "Utilidad Operativa [Bs]": "sum"})
    .reset_index()
)
df_annual["Margen [%]"] = (df_annual["Utilidad Operativa [Bs]"] / df_annual["Ingresos [Bs]"]) * 100
df_fmt = df_annual.copy()
for col in df_fmt.select_dtypes(include=["number"]).columns:
    df_fmt[col] = df_fmt[col].map("{:,.2f}".format)
st.dataframe(df_fmt)

# ---------------- SECCIÓN 5: RESUMEN EJECUTIVO ----------------
if lang == "Español":
    st.success(
        f"""
    ### 🧠 Conclusión Ejecutiva
    - El modelo *Benessere Açaí Lite* proyecta un crecimiento mensual promedio del **{promedio_crecimiento:.1f}%**, alcanzando una utilidad acumulada de **Bs {total_utilidad:,.2f}** en 12 meses.  
    - Con un VAN de **Bs {van:,.2f}** y una TIR del **{tir*100:,.1f}%**, se considera un proyecto **financieramente viable**.  
    - El margen promedio del **{margen_promedio:.1f}%** sugiere alta eficiencia operativa.  
    - Se recomienda priorizar la expansión gradual con foco en el escenario *Base (25%)*.
    """
    )
else:
    st.success(
        f"""
    ### 🧠 Executive Summary
    - The *Benessere Açaí Lite* model projects an average monthly growth of **{promedio_crecimiento:.1f}%**, reaching an accumulated profit of **Bs {total_utilidad:,.2f}** over 12 months.  
    - With an NPV of **Bs {van:,.2f}** and an IRR of **{tir*100:,.1f}%**, the project is **financially viable**.  
    - The average margin of **{margen_promedio:.1f}%** indicates strong operational efficiency.  
    - Recommended focus: scale under the *Base (25%)* scenario for sustainable expansion.
    """
    )

# ---------------- EXPORTAR REPORTE ----------------
st.markdown("---")
st.markdown("### 📤 Exportar Reporte / Export Report")

# Generar Excel
excel_buffer = io.BytesIO()
with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
    df_base.to_excel(writer, sheet_name="Forecast_12M", index=False)
    df_funds.to_excel(writer, sheet_name="Use_of_Funds", index=False)
    df_annual.to_excel(writer, sheet_name="Annual_Summary", index=False)
excel_data = excel_buffer.getvalue()

st.download_button(
    label="📊 Descargar Excel / Download Excel",
    data=excel_data,
    file_name=f"Benessere_Financial_Report_{datetime.now().strftime('%Y%m%d')}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)

# ---------------- GENERAR PDF (Unicode + Logo + Encabezado) ----------------
class PDF(FPDF):
    def header(self):
        # Fuente Unicode DejaVu
        self.add_font("DejaVu", "", fname="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", uni=True)
        self.add_font("DejaVu", "B", fname="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", uni=True)
        self.set_font("DejaVu", "B", 16)

        # Logo (opcional)
        try:
            self.image("assets/logo_benessere.png", 10, 8, 25)
        except:
            pass

        # Encabezado
        self.set_text_color(108, 99, 255)
        self.cell(0, 10, "Benessere Acai Lite - Executive Financial Report", ln=True, align="C")
        self.ln(2)
        self.set_font("DejaVu", "", 11)
        self.set_text_color(90, 90, 90)
        self.cell(0, 8, datetime.now().strftime("Generated on %d/%m/%Y"), ln=True, align="C")
        self.ln(4)
        self.set_draw_color(200, 200, 200)
        self.line(10, 28, 200, 28)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Benessere © {datetime.now().year}  |  Confidential Financial Report", align="C")

pdf = PDF()
pdf.add_page()
pdf.set_font("DejaVu", "", 11)

pdf.multi_cell(
    0,
    8,
    f"""
Resumen Ejecutivo Financiero ({datetime.now().strftime('%d/%m/%Y')})

VAN: Bs {van:,.2f}
TIR: {tir*100:,.2f}%
Payback: {payback if payback else '—'} meses
Margen promedio: {margen_promedio:.2f}%
Crecimiento promedio: {promedio_crecimiento:.2f}%

Ingresos totales proyectados: Bs {total_ingresos:,.2f}
Utilidad total proyectada: Bs {total_utilidad:,.2f}
""",
)

pdf.ln(5)
pdf.set_font("DejaVu", "B", 12)
pdf.set_text_color(108, 99, 255)
pdf.cell(0, 8, "Conclusión Ejecutiva", ln=True)
pdf.set_font("DejaVu", "", 11)
pdf.set_text_color(0, 0, 0)

if lang == "Español":
    pdf.multi_cell(
        0,
        8,
        f"""El modelo Benessere Açaí Lite presenta una proyección de crecimiento saludable,
manteniendo rentabilidad positiva en todos los escenarios evaluados.
El escenario base ofrece un equilibrio sólido entre rentabilidad y escalabilidad operativa.""",
    )
else:
    pdf.multi_cell(
        0,
        8,
        f"""The Benessere Açaí Lite model shows a healthy growth projection,
maintaining positive profitability across all evaluated scenarios.
The base scenario offers a solid balance between profitability and scalability.""",
    )

# Guardar PDF en memoria
pdf_buffer = io.BytesIO()
pdf.output(pdf_buffer)
pdf_data = pdf_buffer.getvalue()

st.download_button(
    label="📄 Descargar PDF / Download PDF",
    data=pdf_data,
    file_name=f"Benessere_Financial_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
    mime="application/pdf",
)
