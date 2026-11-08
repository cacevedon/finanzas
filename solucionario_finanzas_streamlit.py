import streamlit as st
import numpy as np
import pandas as pd
import numpy_financial as npf
import math
import io

# Configuración de página
st.set_page_config(
    page_title="04 Finanzas — Plataforma Web & Solucionario de Ingeniería Financiera",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        color: #2F5496;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #555;
        margin-bottom: 1.5rem;
    }
    .val-badge {
        background-color: #E2EFDA;
        color: #276A3C;
        padding: 5px 12px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.9rem;
        margin-top: -6px;
        margin-bottom: 14px;
        display: inline-block;
    }
    .card-box {
        background-color: #F8F9FA;
        border-left: 5px solid #2F5496;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 15px;
    }
    .stButton>button {
        background-color: #2F5496;
        color: white;
        border-radius: 5px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Helper para parsing de números ingresados por el usuario
def parse_num(val_str, default_val=0.0):
    if val_str is None:
        return float(default_val)
    s = str(val_str).strip().replace("$", "").replace(" ", "")
    if not s:
        return float(default_val)
    
    if "." in s and "," in s:
        s = s.replace(".", "").replace(",", ".")
    elif "." in s:
        parts = s.split(".")
        if len(parts) > 2:
            s = s.replace(".", "")
        elif len(parts) == 2:
            if len(parts[1]) == 3 and len(parts[0]) <= 3:
                s = s.replace(".", "")
            elif len(parts[1]) == 3:
                s = s.replace(".", "")
    elif "," in s:
        parts = s.split(",")
        if len(parts) > 2:
            s = s.replace(",", "")
        elif len(parts) == 2:
            if len(parts[1]) == 3 and len(parts[0]) <= 3:
                s = s.replace(",", "")
            else:
                s = s.replace(",", ".")
    
    try:
        return float(s)
    except:
        return float(default_val)

# Helper para formateo de miles en formato latino (punto para miles, coma para decimales)
def fmt_m(val, dec=2):
    try:
        val = float(val)
        formatted = f"{val:,.{dec}f}"
        return formatted.replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return str(val)

def fmt_n(val, dec=2):
    try:
        val = float(val)
        if dec == 0:
            formatted = f"{int(round(val)):,d}"
            return formatted.replace(",", ".")
        else:
            formatted = f"{val:,.{dec}f}"
            return formatted.replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return str(val)

# Callback para formatear la casilla al cambiar el valor
def format_input_cb(key, default_val):
    val_str = st.session_state.get(key, "")
    parsed = parse_num(val_str, default_val)
    if parsed.is_integer():
        st.session_state[key] = fmt_n(parsed, 0)
    else:
        st.session_state[key] = fmt_n(parsed, 2)

# Widget inteligente de casilla numérica con separador de miles
def smart_num_input(label, default_val, key, help_text=None):
    if key not in st.session_state:
        st.session_state[key] = fmt_n(default_val, 0 if float(default_val).is_integer() else 2)
    
    st.text_input(
        label,
        key=key,
        on_change=format_input_cb,
        args=(key, default_val),
        help=help_text
    )
    
    val_str = st.session_state.get(key, "")
    return parse_num(val_str, default_val)

# Helper para exportación segura a Excel (.xlsx) o CSV (.csv)
def export_dataframe_button(df, filename_prefix="tabla_desarrollo"):
    try:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="Desarrollo")
        excel_data = output.getvalue()
        
        st.download_button(
            label="📥 Exportar Tabla a Excel (.xlsx)",
            data=excel_data,
            file_name=f"{filename_prefix}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception:
        csv_data = df.to_csv(index=False, sep=";", decimal=",").encode('utf-8-sig')
        st.download_button(
            label="📥 Exportar Tabla a CSV (.csv)",
            data=csv_data,
            file_name=f"{filename_prefix}.csv",
            mime="text/csv"
        )

# Encabezado Principal
st.markdown('<div class="main-header">04 FINANZAS — Plataforma de Simulación & Solucionario Web</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Solucionario interactivo y calculadoras financieras avanzadas optimizadas para exámenes, ejercicios y solemnes.</div>', unsafe_allow_html=True)

# Barra lateral de navegación
st.sidebar.title("📌 Navegación del Curso")
modulo = st.sidebar.radio(
    "Selecciona un Módulo:",
    [
        "1. Fundamentos y Decisiones",
        "2. Interés Simple y Compuesto",
        "3. Conversión de Tasas (TNA/TEA)",
        "4. Anualidades y Amortización",
        "5. Gradientes Financieros",
        "6. Presupuesto y Flujo de Caja",
        "7. Evaluación de Proyectos (VAN/TIR)",
        "8. Banco de Preguntas & Calculadoras Especializadas"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Modifica los parámetros en tiempo real para obtener cálculos instantáneos con hasta 4 decimales de precisión.")

# ==========================================
# MÓDULO 1: FUNDAMENTOS
# ==========================================
if modulo == "1. Fundamentos y Decisiones":
    st.header("Unidad 1: Fundamentos y Decisiones Financieras")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📚 Marco Teórico Clave")
        st.markdown("""
        - **Valor del Dinero en el Tiempo (VDT):** Un peso hoy vale más que un peso mañana debido a la capacidad de generar intereses, la inflación y el riesgo.
        - **Costo de Oportunidad:** El rendimiento de la mejor alternativa sacrificada al tomar una decisión financiera.
        - **Liquidez vs. Rentabilidad:** A mayor liquidez inmediata, menor suele ser el rendimiento generado.
        - **Intermediación Financiera:** Bancos e instituciones canalizan el ahorro de agentes superavitarios hacia agentes deficitarios.
        """)
        
    with col2:
        st.subheader("🎯 Matriz de Decisiones Cotidianas")
        caso = st.selectbox("Selecciona un Caso Práctico:", [
            "Caso 1: Lucía y el bono de $500.000",
            "Caso 2: Carlos y la compra a crédito",
            "Caso 3: Presupuesto familiar con imprevisto (15%)",
            "Caso 4: Excedente de caja en Pyme Rápido"
        ])
        
        if "Lucía" in caso:
            st.info("**Situación:** Lucía recibe un bono de $500.000 y duda entre gastarlo en vacaciones o depositarlo a plazo fijo al 0.6% mensual.")
            st.success("**Recomendación Financiera:** Depositar a plazo o invertir en un fondo mutuo conservador. En 12 meses obtendría $537.026. Prioriza acumulación de capital y VDT.")
        elif "Carlos" in caso:
            st.info("**Situación:** Carlos evalúa comprar una laptop al contado ($600.000) o en 12 cuotas de $62.000 (Total $744.000).")
            st.warning("**Recomendación Financiera:** Comprar al contado si cuenta con liquidez. La alternativa a crédito implica un costo financiero total (CAE) implícito superior al 40% anual.")
        elif "Presupuesto" in caso:
            st.info("**Situación:** Familia con ingresos de $1.200.000 sufre un gasto médico imprevisto equivalente al 15% de sus ingresos ($180.000).")
            st.error("**Recomendación Financiera:** Recurrir al fondo de emergencia. Si no existe, reestructurar gastos prescindibles del mes y evitar créditos rotativos de tarjeta.")
        else:
            st.info("**Situación:** Pyme Rápido tiene $5.000.000 ociosos en la cuenta corriente operativa.")
            st.success("**Recomendación Financiera:** Colocar el 60% en pactos diarios o fondos de liquidez inmediata para rentabilizar el saldo sin perder operatividad.")

# ==========================================
# MÓDULO 2: INTERÉS SIMPLE Y COMPUESTO
# ==========================================
elif modulo == "2. Interés Simple y Compuesto":
    st.header("Unidad 2: Interés Simple e Interés Compuesto")
    
    st.subheader("⚙️ Calculadora Interactiva de Interés")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        vp_input = st.number_input("Capital Inicial (VP):", value=1000000.0, step=50000.0)
    with c2:
        tasa_input = st.number_input("Tasa Periódica (%):", value=1.5, step=0.1) / 100.0
    with c3:
        n_input = st.number_input("Plazo (Periodos):", value=12, min_value=1, max_value=120)
    with c4:
        regimen = st.selectbox("Régimen:", ["Interés Compuesto", "Interés Simple", "Comparar Ambos"])
        
    vf_simple = vp_input * (1 + tasa_input * n_input)
    vf_compuesto = vp_input * ((1 + tasa_input) ** n_input)
    
    res_df = pd.DataFrame({
        "Periodo": list(range(0, n_input + 1)),
        "Interés Simple ($)": [vp_input * (1 + tasa_input * t) for t in range(0, n_input + 1)],
        "Interés Compuesto ($)": [vp_input * ((1 + tasa_input) ** t) for t in range(0, n_input + 1)]
    })
    
    st.markdown("#### Resultados Proyectados")
    mc1, mc2, mc3 = st.columns(3)
    mc1.metric("Valor Futuro (Simple)", f"${vf_simple:,.2f}")
    mc2.metric("Valor Futuro (Compuesto)", f"${vf_compuesto:,.2f}")
    mc3.metric("Diferencia por Capitalización", f"${(vf_compuesto - vf_simple):,.2f}")
    
    st.line_chart(res_df.set_index("Periodo"))

# ==========================================
# MÓDULO 3: CONVERSIÓN DE TASAS
# ==========================================
elif modulo == "3. Conversión de Tasas (TNA/TEA)":
    st.header("Unidad 3: Conversión y Decodificación de Tasas")
    
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        st.subheader("🔄 Conversor TNA ➔ TEA")
        tna_val = st.number_input("Tasa Nominal Anual (TNA %):", value=24.0, step=0.5) / 100.0
        freq_dict = {
            "Mensual (m=12)": 12,
            "Bimestral (m=6)": 6,
            "Trimestral (m=4)": 4,
            "Semestral (m=2)": 2,
            "Diaria (m=360)": 360
        }
        freq_sel = st.selectbox("Frecuencia de Capitalización (m):", list(freq_dict.keys()))
        m_val = freq_dict[freq_sel]
        
        i_per = tna_val / m_val
        tea_calc = ((1 + i_per) ** m_val) - 1.0
        
        st.write(f"• **Tasa Periódica ($i$):** {i_per*100:.4f}%")
        st.metric("Tasa Efectiva Anual (TEA Equivalent)", f"{tea_calc*100:.4f}%")

    with col_t2:
        st.subheader("⚖️ Comparador de Inversiones (TNA Capitalizable vs TEA)")
        tna_inv = smart_num_input("Inversión A: TNA (%)", 15.0, key="m3_tna_inv") / 100.0
        m_inv = st.selectbox("Frecuencia Inversión A:", ["Semestral (m=2)", "Trimestral (m=4)", "Mensual (m=12)"], key="m3_m_inv")
        m_num = 2.0 if "Semestral" in m_inv else (4.0 if "Trimestral" in m_inv else 12.0)
        tea_inv_a = ((1 + tna_inv / m_num) ** m_num) - 1.0
        
        tea_inv_b = smart_num_input("Inversión B: TEA (%)", 14.5, key="m3_tea_inv_b") / 100.0
        
        diff_tea = abs(tea_inv_a - tea_inv_b) * 100.0
        
        st.markdown(f"• **TEA Inversión A:** **{fmt_n(tea_inv_a*100, 4)}%**")
        st.markdown(f"• **TEA Inversión B:** **{fmt_n(tea_inv_b*100, 4)}%**")
        st.success(f"🎯 **Diferencia Positiva de Rendimiento:** **{fmt_n(diff_tea, 4)}%**")

# ==========================================
# MÓDULO 4: ANUALIDADES
# ==========================================
elif modulo == "4. Anualidades y Amortización":
    st.header("Unidad 4: Anualidades y Tablas de Amortización")
    
    st.subheader("💳 Simulador de Préstamos y Amortización (Método Francés)")
    
    ac1, ac2, ac3 = st.columns(3)
    with ac1:
        monto_prestamo = smart_num_input("Monto del Préstamo ($):", 15000.0, key="m4_vp")
    with ac2:
        tasa_mensual_anu = smart_num_input("Tasa Anual o Periódica (%):", 8.0, key="m4_tasa") / 100.0
    with ac3:
        plazo_meses = int(smart_num_input("Número de Cuotas (n):", 36.0, key="m4_n"))
        
    if plazo_meses > 0 and tasa_mensual_anu > 0:
        cuota_fija = monto_prestamo * (tasa_mensual_anu / (1 - (1 + tasa_mensual_anu)**(-plazo_meses)))
        
        m_c1, m_c2 = st.columns(2)
        m_c1.metric("Cuota Calculada (2 Decimales)", f"${fmt_m(cuota_fija, 2)}")
        m_c2.metric("Cuota Calculada (4 Decimales)", f"{fmt_n(cuota_fija, 4)}")
        
        saldo = monto_prestamo
        amort_data = []
        for mes in range(1, plazo_meses + 1):
            interes_mes = saldo * tasa_mensual_anu
            capital_mes = cuota_fija - interes_mes
            saldo_final = max(0.0, saldo - capital_mes)
            amort_data.append({
                "Mes": mes,
                "Saldo Inicial ($)": saldo,
                "Cuota ($)": cuota_fija,
                "Interés ($)": interes_mes,
                "Amortización ($)": capital_mes,
                "Saldo Final ($)": saldo_final
            })
            saldo = saldo_final
            
        df_amort = pd.DataFrame(amort_data)
        st.dataframe(df_amort, hide_index=True)
        export_dataframe_button(df_amort, "amortizacion_prestamo")

# ==========================================
# MÓDULO 5: GRADIENTES
# ==========================================
elif modulo == "5. Gradientes Financieros":
    st.header("Unidad 5: Gradientes Financieros (Series Variables)")
    
    st.subheader("📈 Comparativa de Series: Constante vs Aritmética vs Geométrica")
    
    gc1, gc2, gc3 = st.columns(3)
    with gc1:
        base_a = st.number_input("Flujo Base Inicial (A):", value=1000.0, step=100.0)
    with gc2:
        grad_g = st.number_input("Gradiente Aritmético (G $):", value=200.0, step=50.0)
    with gc3:
        grad_pct = st.number_input("Gradiente Geométrico (g %):", value=10.0, step=1.0) / 100.0
        
    periodos_g = 10
    grad_df = pd.DataFrame({
        "Año": list(range(1, periodos_g + 1)),
        "Serie Constante": [base_a] * periodos_g,
        "Gradiente Aritmético (+G)": [base_a + (t - 1) * grad_g for t in range(1, periodos_g + 1)],
        "Gradiente Geométrico (+g)": [base_a * ((1 + grad_pct)**(t - 1)) for t in range(1, periodos_g + 1)]
    })
    
    st.line_chart(grad_df.set_index("Año"))

# ==========================================
# MÓDULO 6: PRESUPUESTOS
# ==========================================
elif modulo == "6. Presupuesto y Flujo de Caja":
    st.header("Unidad 6: Presupuestos y Control de Caja Operacional")
    
    pc1, pc2, pc3 = st.columns(3)
    with pc1:
        v_base = st.number_input("Ventas Mes 1 ($):", value=15000.0, step=1000.0)
    with pc2:
        g_ventas = st.number_input("Crecimiento Ventas Mensual (%):", value=1.5, step=0.1) / 100.0
    with pc3:
        inf_mensual = st.number_input("Inflación Costos Mensual (%):", value=0.5, step=0.1) / 100.0
        
    meses_p = 12
    p_data = []
    caja_acum = 8000.0
    
    for m in range(1, meses_p + 1):
        ventas_m = v_base * ((1 + g_ventas)**(m - 1))
        costos_m = (ventas_m * 0.40) * ((1 + inf_mensual)**(m - 1))
        fijos_m = 7000.0 * ((1 + inf_mensual)**(m - 1))
        reserva_m = ventas_m * 0.05
        egresos_total = costos_m + fijos_m + reserva_m
        flujo_neto = ventas_m - egresos_total
        caja_acum += flujo_neto
        
        p_data.append({
            "Mes": f"Mes {m}",
            "Ventas ($)": ventas_m,
            "Total Egresos ($)": egresos_total,
            "Flujo Neto ($)": flujo_neto,
            "Caja Acumulada ($)": caja_acum
        })
        
    df_pres = pd.DataFrame(p_data)
    st.dataframe(df_pres, hide_index=True)

# ==========================================
# MÓDULO 7: EVALUACIÓN DE PROYECTOS
# ==========================================
elif modulo == "7. Evaluación de Proyectos (VAN/TIR)":
    st.header("Unidad 7: Evaluación Financiera de Proyectos")
    
    inv_ini = st.number_input("Inversión Inicial ($):", value=500000.0, step=10000.0)
    tmar_val = st.number_input("Tasa de Descuento / TMAR (%):", value=10.0, step=0.5) / 100.0
    
    st.write("Ingresa los flujos proyectados a 5 años:")
    fc_cols = st.columns(5)
    flujos = []
    for idx, col in enumerate(fc_cols):
        with col:
            f_val = st.number_input(f"Año {idx+1} ($):", value=140000.0 + idx*10000.0, step=5000.0)
            flujos.append(f_val)
            
    van_val = npf.npv(tmar_val, [0] + flujos) - inv_ini
    tir_val = npf.irr([-inv_ini] + flujos)
    
    col_v1, col_v2 = st.columns(2)
    col_v1.metric("Valor Actual Neto (VAN)", f"${van_val:,.2f}", delta="Viable" if van_val > 0 else "No Viable")
    col_v2.metric("Tasa Interna de Retorno (TIR)", f"{tir_val*100:.2f}%", delta="TIR > TMAR" if tir_val > tmar_val else "TIR < TMAR")

# ==========================================
# MÓDULO 8: BANCO DE PREGUNTAS & CALCULADORAS ESPECIALIZADAS
# ==========================================
else:
    st.header("Unidad 8: Banco de Preguntas Solemnes & Calculadoras Financieras Avanzadas")
    
    calc_option = st.selectbox(
        "Selecciona la Herramienta o Caso a Evaluar:",
        [
            "I. Desglose de Interés y Amortización para una Cuota Específica (k)",
            "II. Valor Futuro con Interés Compuesto (Plazos Enteros y Fraccionados)",
            "III. Valor Futuro de Anualidades y Fondos de Ahorro (Ordinarias y Anticipadas)",
            "IV. Valuación de Flujos Múltiples e Irregulares (VP y VF)",
            "V. Despeje de Plazo Requerido (n) y Tasa Implícita para Metas de Capital",
            "VI. Conversión Avanzada de Tasas Nominales/Efectivas y Spread Financiero",
            "VII. Valor Presente (VP) de Pagos Futuros Específicos Discretos en Meses",
            "VIII. Valor Futuro (VF) de Depósitos Proyectados Discretos en Meses Específicos (Tasas Variables)",
            "IX. Comparador de Ofertas Bancarias a Plazo Fijo / Depósitos (Múltiples Bancos y Tipos de Tasa)",
            "X. Crédito Comercial / Bienes de Capital (Pagos Anuales & Cuota Mensual)",
            "XI. Tasa Implícita Anual para Créditos o Inversiones de Pago Único",
            "XII. Valor Presente de Cero / Descuento (4 Decimales de Precisión)",
            "XIII. Calculadora de Cuota Fija de Préstamo (Precisión 4 Decimales)",
            "XIV. Calculadora de Costo Financiero Total (CFT % y $)"
        ]
    )
    
    # -------------------------------------------------------------
    # HERRAMIENTA XIII: CUOTA FIJA DE PRÉSTAMO
    # -------------------------------------------------------------
    if calc_option.startswith("XIII. "):
        st.subheader("🛠️ XIII. Calculadora de Cuota Fija de Préstamo (Precisión 4 Decimales)")
        st.caption("Calcula el valor exacto de la cuota fija (PMT) para préstamos de 36, 45 o N períodos con precisión configurable.")
        
        c_p1, c_p2, c_p3 = st.columns(3)
        with c_p1:
            vp_cuota = smart_num_input("Monto del Préstamo (VP $):", 12000.0, key="c13_vp")
        with c_p2:
            n_cuotas = int(smart_num_input("Número de Cuotas (n):", 45.0, key="c13_n"))
        with c_p3:
            tasa_cuota = smart_num_input("Tasa de Interés Periódica/Anual (%):", 5.0, key="c13_tasa") / 100.0
            
        if n_cuotas > 0 and tasa_cuota > 0:
            pmt_val = vp_cuota * (tasa_cuota / (1 - (1 + tasa_cuota)**(-n_cuotas)))
            
            m1, m2 = st.columns(2)
            m1.metric("Cuota Fija (2 Decimales)", f"${fmt_m(pmt_val, 2)}")
            m2.metric("Cuota Fija Exacta (4 Decimales)", f"{fmt_n(pmt_val, 4)}")
            
            st.info(f"Fórmula aplicada: $R = {fmt_m(vp_cuota)} \\times \\frac{{{fmt_n(tasa_cuota*100, 2)}\\%}}{{1 - (1 + {fmt_n(tasa_cuota*100, 2)}\\%)^{{-{n_cuotas}}}}} = \\mathbf{{{fmt_n(pmt_val, 4)}}}$")

    # -------------------------------------------------------------
    # HERRAMIENTA XIV: COSTO FINANCIERO TOTAL (CFT)
    # -------------------------------------------------------------
    elif calc_option.startswith("XIV. "):
        st.subheader("🛠️ XIV. Calculadora de Costo Financiero Total (CFT % y $)")
        st.caption("Calcula la Tasa de Costo Financiero Total incorporando comisiones directas y gastos administrativos.")
        
        cf1, cf2, cf3 = st.columns(3)
        with cf1:
            monto_cft = smart_num_input("Monto del Crédito ($):", 1000000.0, key="c14_monto")
        with cf2:
            tea_cft = smart_num_input("Tasa Efectiva Anual (TEA %):", 18.0, key="c14_tea") / 100.0
        with cf3:
            comision_cft = smart_num_input("Comisión o Gastos Anuales ($):", 20000.0, key="c14_comision")
            
        pct_comision = comision_cft / monto_cft
        cft_pct = tea_cft + pct_comision
        interes_dinero = monto_cft * tea_cft
        cft_dinero = interes_dinero + comision_cft
        
        cm1, cm2, cm3 = st.columns(3)
        cm1.metric("CFT Porcentual Anual", f"{fmt_n(cft_pct*100, 2)}%")
        cm2.metric("CFT en Dinero ($)", f"${fmt_m(cft_dinero, 2)}")
        cm3.metric("% Comisión sobre Crédito", f"{fmt_n(pct_comision*100, 2)}%")
        
        st.success(f"**Resultado Estándar:** Costo Financiero Total = **{fmt_n(cft_pct*100, 2)}%** (${fmt_m(cft_dinero)} anual).")

    # -------------------------------------------------------------
    # HERRAMIENTA VIII: VF DE DEPÓSITOS PROYECTADOS (TASAS VARIABLES)
    # -------------------------------------------------------------
    elif calc_option.startswith("VIII. "):
        st.subheader("🛠️ VIII. Valor Futuro (VF) de Depósitos Proyectados Discretos en Meses Específicos (Tasas Variables)")
        st.caption("Proyecta la acumulación de depósitos discretos permitiendo tasas variables y desglose del VF individual de cada abono.")
        
        col_v1, col_v2, col_v3 = st.columns(3)
        with col_v1:
            n_meses_v8 = int(smart_num_input("Horizonte Total de Meses (N):", 12.0, key="c8_nmeses"))
        with col_v2:
            momento_dep = st.selectbox("Momento del Depósito:", ["Fin del Mes / Vencido (por defecto)", "Inicio del Mes / Anticipado"], key="c8_momento")
        with col_v3:
            modo_tasa = st.selectbox("Estructura de Tasas:", ["Cambio de Tasa desde un Mes Específico", "Matriz / Tabla de Tasa por Mes", "Tasa Fija Mensual"], key="c8_modotasa")
            
        dep_dict = {}
        st.markdown("##### 💵 Ingreso de Depósitos en Meses Específicos:")
        col_d1, col_d2, col_d3, col_d4 = st.columns(4)
        with col_d1:
            d1 = smart_num_input("Depósito Mes 1 ($):", 30000000.0, key="c8_d1")
            if d1 > 0: dep_dict[1] = d1
        with col_d2:
            d2 = smart_num_input("Depósito Mes 2 ($):", 40000000.0, key="c8_d2")
            if d2 > 0: dep_dict[2] = d2
        with col_d3:
            d3 = smart_num_input("Depósito Mes 3 ($):", 50000000.0, key="c8_d3")
            if d3 > 0: dep_dict[3] = d3
        with col_d4:
            d4 = smart_num_input("Depósito Mes 4 ($):", 50000000.0, key="c8_d4")
            if d4 > 0: dep_dict[4] = d4
            
        col_d5, col_d6 = st.columns(2)
        with col_d5:
            d8 = smart_num_input("Depósito Mes 8 ($ - opcional):", 40000000.0, key="c8_d8")
            if d8 > 0: dep_dict[8] = d8
            
        # Configuración de Tasas
        tasas_mes = [0.03] * (n_meses_v8 + 1)
        if "Cambio de Tasa" in modo_tasa:
            tc1, tc2, tc3 = st.columns(3)
            with tc1:
                tasa_ini = smart_num_input("Tasa Inicial (% Mensual):", 3.0, key="c8_tini") / 100.0
            with tc2:
                mes_cambio = int(smart_num_input("Mes de Cambio de Tasa:", 6.0, key="c8_mcambio"))
            with tc3:
                tasa_nueva = smart_num_input("Nueva Tasa (% Mensual):", 4.0, key="c8_tnueva") / 100.0
                
            for m in range(1, n_meses_v8 + 1):
                tasas_mes[m] = tasa_ini if m < mes_cambio else tasa_nueva
        elif "Tasa Fija" in modo_tasa:
            tfija = smart_num_input("Tasa Única (% Mensual):", 3.0, key="c8_tfija") / 100.0
            for m in range(1, n_meses_v8 + 1): tasas_mes[m] = tfija
            
        # Simulación Mes a Mes
        is_anticipado = "Anticipado" in momento_dep
        saldo = 0.0
        filas_sim = []
        tot_dep = sum(dep_dict.values())
        tot_int = 0.0
        
        for m in range(1, n_meses_v8 + 1):
            s_ini = saldo
            dep_m = dep_dict.get(m, 0.0)
            tasa_m = tasas_mes[m]
            
            if is_anticipado:
                base_int = s_ini + dep_m
                int_m = base_int * tasa_m
                s_fin = base_int + int_m
            else:
                int_m = s_ini * tasa_m
                s_fin = s_ini + int_m + dep_m
                
            tot_int += int_m
            saldo = s_fin
            
            filas_sim.append({
                "Mes": m,
                "Saldo Inicial ($)": s_ini,
                "Tasa Aplicada (%)": tasa_m * 100.0,
                "Interés del Mes ($)": int_m,
                "Depósito Ingresado ($)": dep_m,
                "Saldo Final ($)": s_fin
            })
            
        df_sim_v8 = pd.DataFrame(filas_sim)
        
        # Desglose Individual de Depósitos
        filas_ind = []
        for idx, (m_dep, monto_dep) in enumerate(sorted(dep_dict.items()), 1):
            if is_anticipado:
                meses_cap = n_meses_v8 - m_dep + 1
                factor = 1.0
                for m in range(m_dep, n_meses_v8 + 1):
                    factor *= (1.0 + tasas_mes[m])
            else:
                meses_cap = n_meses_v8 - m_dep
                factor = 1.0
                for m in range(m_dep + 1, n_meses_v8 + 1):
                    factor *= (1.0 + tasas_mes[m])
                    
            vf_ind = monto_dep * factor
            pct_part = (vf_ind / saldo) * 100.0 if saldo > 0 else 0.0
            
            filas_ind.append({
                "Depósito #": idx,
                "Mes Abono": m_dep,
                "Monto Depósito ($)": monto_dep,
                "Meses Capitalizados": meses_cap,
                "Factor Acumulado": factor,
                "Valor Futuro Individual ($)": vf_ind,
                "Participación en VF (%)": pct_part
            })
            
        df_ind_v8 = pd.DataFrame(filas_ind)
        
        # Métricas de Salida
        m_vf1, m_vf2, m_vf3 = st.columns(3)
        m_vf1.metric("Valor Futuro Acumulado (t=N)", f"${fmt_m(saldo, 2)}")
        m_vf2.metric("Total Depósitos Aportados", f"${fmt_m(tot_dep, 2)}")
        m_vf3.metric("Total Intereses Ganados", f"${fmt_m(tot_int, 2)}")
        
        st.markdown("#### 📌 Desglose del Valor Futuro Individual por Depósito")
        st.dataframe(df_ind_v8, hide_index=True)
        
        st.markdown("#### 📅 Evolución Mensual del Fondo de Ahorro")
        st.dataframe(df_sim_v8, hide_index=True)
        export_dataframe_button(df_sim_v8, "desarrollo_depositos_variables")

    # -------------------------------------------------------------
    # HERRAMIENTA IX: COMPARADOR BANCARIO (MÚLTIPLES BANCOS Y TASAS)
    # -------------------------------------------------------------
    elif calc_option.startswith("IX. "):
        st.subheader("🛠️ IX. Comparador de Ofertas Bancarias a Plazo Fijo / Depósitos (Múltiples Bancos y Tipos de Tasa)")
        st.caption("Compara el rendimiento de hasta 5 ofertas bancarias simultáneas homogeneizándolas a TEA y Tasa Mensual Equivalente (TEM).")
        
        b1, b2 = st.columns(2)
        with b1:
            monto_inv_ix = smart_num_input("Monto a Invertir ($):", 17000000.0, key="c9_monto")
        with b2:
            plazo_meses_ix = int(smart_num_input("Plazo de Inversión (Meses):", 24.0, key="c9_plazo"))
            
        n_bancos = int(st.slider("Número de Bancos a Comparar:", min_value=2, max_value=5, value=3, key="c9_nbancos"))
        
        opciones_tasa = [
            "TEA (Efectiva Anual)",
            "TEC (Efectiva Cuatrimestral)",
            "TES (Efectiva Semestral)",
            "TET (Efectiva Trimestral)",
            "TEB (Efectiva Bimestral)",
            "TEM (Efectiva Mensual)",
            "TED (Efectiva Diaria)",
            "TNC (Nominal Cuatrimestral - Cap. Mensual m=4)",
            "TNC (Nominal Cuatrimestral - Cap. Diaria m=120)",
            "TNS (Nominal Semestral - Cap. Mensual m=6)",
            "TNT (Nominal Trimestral - Cap. Mensual m=3)",
            "TNA (Nominal Anual)",
            "Tasa Simple Cuatrimestral",
            "Tasa Simple Anual",
            "Tasa Simple Semestral",
            "Tasa Simple Trimestral",
            "Tasa Simple Mensual"
        ]
        
        datos_bancos = []
        for i in range(1, n_bancos + 1):
            st.markdown(f"##### 🏦 Datos del Banco #{i}:")
            col_b1, col_b2, col_b3 = st.columns(3)
            with col_b1:
                nom_b = st.text_input(f"Nombre del Banco #{i}:", value="", placeholder=f"Banco {i}", key=f"c9_nom_{i}")
                if not nom_b.strip(): nom_b = f"Banco {i}"
            with col_b2:
                tipo_t = st.selectbox(f"Tipo de Tasa ({nom_b}):", opciones_tasa, key=f"c9_tipo_{i}")
            with col_b3:
                val_t = smart_num_input(f"Tasa Ingresada (%):", 12.5 if i==1 else (4.1 if i==2 else 1.0), key=f"c9_val_{i}") / 100.0
                
            # Cálculo de TEA equivalente
            if tipo_t == "TEA (Efectiva Anual)":
                tea_eq = val_t
            elif tipo_t == "TEC (Efectiva Cuatrimestral)":
                tea_eq = ((1.0 + val_t) ** 3.0) - 1.0
            elif tipo_t == "TES (Efectiva Semestral)":
                tea_eq = ((1.0 + val_t) ** 2.0) - 1.0
            elif tipo_t == "TET (Efectiva Trimestral)":
                tea_eq = ((1.0 + val_t) ** 4.0) - 1.0
            elif tipo_t == "TEB (Efectiva Bimestral)":
                tea_eq = ((1.0 + val_t) ** 6.0) - 1.0
            elif tipo_t == "TEM (Efectiva Mensual)":
                tea_eq = ((1.0 + val_t) ** 12.0) - 1.0
            elif tipo_t == "TED (Efectiva Diaria)":
                tea_eq = ((1.0 + val_t) ** 360.0) - 1.0
            elif "TNC (Nominal Cuatrimestral - Cap. Mensual" in tipo_t:
                i_per = val_t / 4.0
                tea_eq = ((1.0 + i_per) ** 12.0) - 1.0
            elif "TNC (Nominal Cuatrimestral - Cap. Diaria" in tipo_t:
                i_per = val_t / 120.0
                tea_eq = ((1.0 + i_per) ** 360.0) - 1.0
            elif "TNS (Nominal Semestral" in tipo_t:
                i_per = val_t / 6.0
                tea_eq = ((1.0 + i_per) ** 12.0) - 1.0
            elif "TNT (Nominal Trimestral" in tipo_t:
                i_per = val_t / 3.0
                tea_eq = ((1.0 + i_per) ** 12.0) - 1.0
            elif tipo_t == "TNA (Nominal Anual)":
                tea_eq = ((1.0 + val_t / 12.0) ** 12.0) - 1.0
            elif "Simple Cuatrimestral" in tipo_t:
                tna_s = val_t * 3.0
                tea_eq = tna_s
            elif "Simple Anual" in tipo_t:
                tea_eq = val_t
            elif "Simple Semestral" in tipo_t:
                tea_eq = val_t * 2.0
            elif "Simple Trimestral" in tipo_t:
                tea_eq = val_t * 4.0
            else:
                tea_eq = val_t * 12.0
                
            tem_eq = ((1.0 + tea_eq) ** (1.0 / 12.0)) - 1.0
            anos_ix = plazo_meses_ix / 12.0
            vf_banco = monto_inv_ix * ((1.0 + tea_eq) ** anos_ix)
            int_banco = vf_banco - monto_inv_ix
            
            datos_bancos.append({
                "Entidad Bancaria": nom_b,
                "Tasa Ofrecida": f"{fmt_n(val_t*100, 2)}% ({tipo_t.split('(')[0].strip()})",
                "TEA Equivalente (%)": tea_eq * 100.0,
                "Tasa Mensual Equivalente (%)": tem_eq * 100.0,
                "Monto Final Acumulado ($)": vf_banco,
                "Intereses Ganados ($)": int_banco
            })
            
        df_bancos = pd.DataFrame(datos_bancos)
        df_bancos = df_bancos.sort_values(by="Monto Final Acumulado ($)", ascending=False).reset_index(drop=True)
        
        best_vf = df_bancos.loc[0, "Monto Final Acumulado ($)"]
        df_bancos["Diferencia vs. Mejor ($)"] = df_bancos["Monto Final Acumulado ($)"].apply(
            lambda x: "🥇 Mejor Oferta" if abs(x - best_vf) < 0.01 else f"-${fmt_m(best_vf - x, 2)}"
        )
        
        st.success(f"🏆 **Banco Ganador:** **{df_bancos.loc[0, 'Entidad Bancaria']}** con un Monto Final de **${fmt_m(df_bancos.loc[0, 'Monto Final Acumulado ($)'], 2)}** (TEA = {fmt_n(df_bancos.loc[0, 'TEA Equivalente (%)'], 4)}%, TEM = {fmt_n(df_bancos.loc[0, 'Tasa Mensual Equivalente (%)'], 4)}%).")
        
        st.markdown("#### 📊 Tabla Comparativa Ordenada por Rentabilidad:")
        st.dataframe(df_bancos, hide_index=True)
        export_dataframe_button(df_bancos, "comparativa_bancaria")

    # -------------------------------------------------------------
    # HERRAMIENTAS I - VII, X, XI, XII (Resto del Banco)
    # -------------------------------------------------------------
    elif calc_option.startswith("I. "):
        st.subheader("🛠️ I. Desglose de Interés y Amortización para una Cuota Específica (k)")
        st.info("Calcula el interés y la amortización de capital para una cuota k dada.")
    elif calc_option.startswith("II. "):
        st.subheader("🛠️ II. Valor Futuro con Interés Compuesto")
        st.info("Fórmula: $VF = VP \\times (1 + i)^{n/12}$. Ej. USD 1.000 a 16 meses al 5% anual = USD 1.067,25.")
    elif calc_option.startswith("VII. "):
        st.subheader("🛠️ VII. Valor Presente (VP) de Pagos Futuros Específicos Discretos en Meses")
        st.info("Descuenta compromisos puntuales en meses específicos a su valor equivalente en t=0.")
    elif calc_option.startswith("X. "):
        st.subheader("🛠️ X. Crédito Comercial / Bienes de Capital")
        st.info("Evalúa préstamos comerciales con cuotas anuales o mensuales equivalentes.")
    elif calc_option.startswith("XI. "):
        st.subheader("🛠️ XI. Tasa Implícita Anual para Créditos de Pago Único")
        st.info("Determina la TEA y TNA implícita dada una inversión inicial y un retorno único al vencimiento.")
    else:
        st.subheader("🛠️ XII. Valor Presente de Cero / Descuento (4 Decimales)")
        st.info("Calcula el Valor Presente exacto con precisión de 4 decimales.")

st.markdown("---")
st.caption("Plataforma de Simulación & Cálculo Financiero — Actualizado para Gemini Notebook")
