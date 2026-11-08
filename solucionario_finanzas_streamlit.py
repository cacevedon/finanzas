"""
Plataforma de Simulación e Ingeniería Financiera.

Convenciones del curso (apuntes S1–S6 y clases sincrónicas):
- Si el enunciado no dice "simple", se asume interés COMPUESTO.
- La tasa debe expresarse en la misma unidad de tiempo que los períodos/cuotas.
- Una tasa "mensual", "trimestral", "cuatrimestral", "semestral" o "anual" sin más
  especificación se trata como EFECTIVA de ese período: 1 + TE = (1 + i')^n.
- Una tasa NOMINAL anual con capitalización m se divide por m para obtener la tasa del período.
- Las cuotas de crédito son anualidades vencidas; cuota = amortización + interés.
- En las evaluaciones la tasa se responde en decimales (0,1696 y no 16,96 %).
"""
import io
import math

import numpy_financial as npf
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Simulación e Ingeniería Financiera",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .main-header {font-size: 2.2rem; color: #2F5496; font-weight: 700; margin-bottom: 0.2rem;}
    .sub-header {font-size: 1.1rem; color: #555; margin-bottom: 1.5rem;}
    .stButton>button {background-color: #2F5496; color: white; border-radius: 5px; font-weight: 600;}
</style>
""", unsafe_allow_html=True)

# =====================================================================
# Utilidades de formato y entrada (formato chileno: 1.234.567,89)
# =====================================================================

def parse_latam_number(val_str):
    """Convierte '1.050', '$3.545.900', '1,2%', '0.125', '100.000,50' a float."""
    if val_str is None or str(val_str).strip() == "":
        return 0.0
    s = str(val_str).strip().replace("$", "").replace("%", "").replace(" ", "")
    if "." in s and "," in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    elif "." in s:
        parts = s.split(".")
        if len(parts) > 2:
            s = s.replace(".", "")
        elif len(parts) == 2:
            entero = parts[0].lstrip("-")
            # "1.050" = mil cincuenta; "0.125" = decimal
            if len(parts[1]) == 3 and 1 <= len(entero) <= 3 and entero != "0":
                s = s.replace(".", "")
    try:
        return float(s)
    except ValueError:
        return 0.0


def fmt_currency(val):
    try:
        val = float(val)
    except (ValueError, TypeError):
        return "$0"
    neg = val < 0
    val = abs(val)
    if abs(val - round(val)) < 1e-7:
        s = f"{int(round(val)):,}".replace(",", ".")
    else:
        s = f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{'-' if neg else ''}${s}"


def fmt_num(val, dec=2):
    try:
        val = float(val)
    except (ValueError, TypeError):
        return "0"
    if abs(val - round(val)) < 1e-7:
        return f"{int(round(val)):,}".replace(",", ".")
    return f"{val:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def pct(dec_rate, d=4):
    return f"{dec_rate*100:.{d}f}%".replace(".", ",")


def fmt_tasa(dec_rate, d=4):
    """Muestra la tasa en % y en decimal (formato exigido en las solemnes)."""
    pct = f"{dec_rate*100:.{d}f}".replace(".", ",")
    dec = f"{dec_rate:.{d+2}f}".replace(".", ",")
    return f"{pct}% (decimal: {dec})"


def smart_num_input(label, default_val=0.0, key=None, is_currency=True, is_percent=False, help_text=None):
    if is_currency:
        init_str = fmt_currency(default_val) if default_val != 0 else "$0"
    elif is_percent:
        init_str = f"{default_val:.2f}%".replace(".", ",") if default_val != 0 else "0,0%"
    else:
        init_str = fmt_num(default_val) if default_val != 0 else "0"

    val_str = st.text_input(label, value=init_str, key=key, help=help_text or label)
    val_num = parse_latam_number(val_str)

    if is_currency:
        st.caption(f"📌 *Monto ingresado:* **{fmt_currency(val_num)}**")
    elif is_percent:
        st.caption(f"📌 *Tasa ingresada:* **{fmt_num(val_num, 4)}%**")
    else:
        st.caption(f"📌 *Valor ingresado:* **{fmt_num(val_num, 4)}**")
    return val_num


def excel_download(df, sheet, filename, label):
    """Exporta un DataFrame numérico a .xlsx en memoria."""
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet)
    st.download_button(label, buf.getvalue(), file_name=filename,
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# =====================================================================
# Núcleo financiero
# =====================================================================

# Duración de cada período en meses
PERIODOS = {
    "Diaria (año 360)": 12 / 360,
    "Mensual": 1,
    "Bimestral": 2,
    "Trimestral": 3,
    "Cuatrimestral": 4,
    "Semestral": 6,
    "Anual": 12,
}
TIPOS_TASA = ["Efectiva del período", "Nominal anual (capitalizable)"]


def tasa_a_periodo(tasa_dec, tipo, periodo_tasa, cap, periodo_destino):
    """
    Lleva una tasa a la tasa efectiva del período destino.
    - Efectiva del período: (1 + i_dest) = (1 + i)^(meses_dest / meses_tasa)
    - Nominal anual capitalizable 'cap': i' = j/m, luego se lleva al destino.
    """
    if tipo.startswith("Nominal"):
        m = 12 / PERIODOS[cap]
        i_cap = tasa_dec / m
        meses_origen = PERIODOS[cap]
    else:
        i_cap = tasa_dec
        meses_origen = PERIODOS[periodo_tasa]
    return (1 + i_cap) ** (PERIODOS[periodo_destino] / meses_origen) - 1


def selector_tasa(key, label="Tasa (%)", default_periodo="Mensual"):
    """Widget reutilizable: valor + tipo + período/capitalización."""
    c1, c2, c3 = st.columns(3)
    with c1:
        tasa = smart_num_input(label, default_val=0.0, key=f"{key}_val", is_currency=False, is_percent=True)
    with c2:
        tipo = st.selectbox("Tipo de tasa:", TIPOS_TASA, key=f"{key}_tipo")
    with c3:
        if tipo.startswith("Nominal"):
            per = "Anual"
            cap = st.selectbox("Capitalización:", list(PERIODOS.keys()),
                               index=list(PERIODOS).index("Mensual"), key=f"{key}_cap")
        else:
            per = st.selectbox("Período de la tasa:", list(PERIODOS.keys()),
                               index=list(PERIODOS).index(default_periodo), key=f"{key}_per")
            cap = per
    return tasa / 100.0, tipo, per, cap


def cuota_anualidad(vp, i, n):
    return vp / n if i == 0 else vp * i / (1 - (1 + i) ** (-n))


def vp_anualidad(r, i, n):
    return r * n if i == 0 else r * (1 - (1 + i) ** (-n)) / i


def vf_anualidad(r, i, n):
    return r * n if i == 0 else r * ((1 + i) ** n - 1) / i


def tabla_amortizacion(vp, i, n):
    cuota = cuota_anualidad(vp, i, n)
    saldo, filas = vp, []
    for k in range(1, n + 1):
        interes = saldo * i
        amort = cuota - interes
        saldo_fin = saldo - amort
        if abs(saldo_fin) < 1e-6:
            saldo_fin = 0.0
        filas.append({"Cuota N°": k, "Saldo Inicial ($)": saldo, "Cuota ($)": cuota,
                      "Interés ($)": interes, "Amortización ($)": amort, "Saldo Final ($)": saldo_fin})
        saldo = saldo_fin
    return cuota, pd.DataFrame(filas)


def vp_gradiente_aritmetico(a, g, i, n):
    """VP de A, A+G, ..., A+(n-1)G al final de los períodos 1..n."""
    if i == 0:
        return a * n + g * n * (n - 1) / 2
    p_a = (1 - (1 + i) ** (-n)) / i
    p_g = (1 / i) * (p_a - n / (1 + i) ** n)
    return a * p_a + g * p_g


def vp_gradiente_geometrico(a1, g, i, n):
    """VP de A1, A1(1+g), ..., A1(1+g)^(n-1)."""
    if abs(i - g) < 1e-12:
        return a1 * n / (1 + i)
    return a1 * (1 - ((1 + g) / (1 + i)) ** n) / (i - g)

# =====================================================================
# Encabezado y navegación
# =====================================================================
st.markdown('<div class="main-header">04 FINANZAS — Plataforma de Simulación e Ingeniería Financiera</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Calculadoras alineadas a la Unidad 1 y 2 del curso ICIO K002 (USS).</div>', unsafe_allow_html=True)

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
        "8. Calculadoras Especializadas y Simuladores",
    ],
)
st.sidebar.markdown("---")
st.sidebar.info("💡 Si el enunciado no dice *simple*, usa interés **compuesto**. "
                "La tasa siempre debe estar en la misma unidad que los períodos.")

# =====================================================================
# MÓDULO 1
# =====================================================================
if modulo == "1. Fundamentos y Decisiones":
    st.header("Fundamentos y Decisiones Financieras")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📚 Marco Teórico Clave")
        st.markdown("""
        - **Valor del dinero en el tiempo:** un peso hoy vale más que un peso mañana (intereses, inflación, riesgo). Montos de distintos períodos no se suman sin llevarlos a una misma fecha.
        - **Costo de oportunidad:** rendimiento de la mejor alternativa sacrificada.
        - **Decisiones financieras:** inversión (en qué se usan los recursos), financiamiento (de dónde salen) y dividendos/gestión de liquidez.
        - **Liquidez vs. rentabilidad:** a mayor liquidez inmediata, menor rendimiento.
        - **Tasa nominal vs. efectiva:** la efectiva incorpora la capitalización y es la única comparable.
        """)
    with col2:
        st.subheader("🎯 Evaluador de Excedente de Caja")
        monto_dec = smart_num_input("Capital o Excedente de Caja ($):", key="m1_monto")
        tasa_dec = smart_num_input("Tasa Efectiva Mensual (%):", key="m1_tasa", is_currency=False, is_percent=True)
        plazo_dec = smart_num_input("Plazo en Meses:", key="m1_plazo", is_currency=False)
        if monto_dec > 0 and tasa_dec > 0 and plazo_dec > 0:
            vf_dec = monto_dec * (1 + tasa_dec / 100.0) ** plazo_dec
            st.success(f"• **Valor Futuro Proyectado:** **{fmt_currency(vf_dec)}**")
            st.info(f"• **Intereses Generados:** **{fmt_currency(vf_dec - monto_dec)}**")
        else:
            st.info("Ingresa monto, tasa y plazo mayores a cero.")

# =====================================================================
# MÓDULO 2
# =====================================================================
elif modulo == "2. Interés Simple y Compuesto":
    st.header("Interés Simple e Interés Compuesto")
    st.caption("Cuatro variables (VP, VF, i, n): conociendo tres se despeja la cuarta. "
               "La tasa y el plazo deben estar en la misma unidad de tiempo.")

    regimen = st.radio("Régimen:", ["Interés Compuesto", "Interés Simple"], horizontal=True, key="m2_reg")
    incog = st.selectbox("¿Qué quieres calcular?", ["Valor Futuro (VF)", "Valor Presente (VP)",
                                                     "Tasa del período (i)", "Plazo (n)"], key="m2_incog")
    c1, c2, c3 = st.columns(3)
    vp = vf = i = n = 0.0
    with c1:
        if incog != "Valor Presente (VP)":
            vp = smart_num_input("Valor Presente (VP $):", key="m2_vp")
        if incog != "Valor Futuro (VF)":
            vf = smart_num_input("Valor Futuro (VF $):", key="m2_vf")
    with c2:
        if incog != "Tasa del período (i)":
            i = smart_num_input("Tasa del período (%):", key="m2_tasa", is_currency=False, is_percent=True) / 100.0
    with c3:
        if incog != "Plazo (n)":
            n = smart_num_input("Plazo (n períodos, admite decimales):", key="m2_n", is_currency=False)

    simple = regimen == "Interés Simple"
    res = None
    try:
        if incog == "Valor Futuro (VF)" and vp > 0 and n > 0:
            res = vp * (1 + i * n) if simple else vp * (1 + i) ** n
            st.success(f"**VF = {fmt_currency(res)}** · Intereses: {fmt_currency(res - vp)}")
            st.code("VF = VP·(1 + i·n)" if simple else "VF = VP·(1 + i)^n   |   Excel: =VF(i; n; ; -VP)")
        elif incog == "Valor Presente (VP)" and vf > 0 and n > 0:
            res = vf / (1 + i * n) if simple else vf / (1 + i) ** n
            st.success(f"**VP = {fmt_currency(res)}**")
            st.code("VP = VF / (1 + i·n)" if simple else "VP = VF / (1 + i)^n   |   Excel: =VA(i; n; ; -VF)")
        elif incog == "Tasa del período (i)" and vp > 0 and vf > 0 and n > 0:
            res = (vf / vp - 1) / n if simple else (vf / vp) ** (1 / n) - 1
            st.success(f"**i = {fmt_tasa(res)}** por período")
            st.code("i = (VF/VP − 1) / n" if simple else "i = (VF/VP)^(1/n) − 1   |   Excel: =TASA(n; ; -VP; VF)")
        elif incog == "Plazo (n)" and vp > 0 and vf > 0 and i > 0:
            res = (vf / vp - 1) / i if simple else math.log(vf / vp) / math.log(1 + i)
            st.success(f"**n = {fmt_num(res, 4)} períodos**")
            st.code("n = (VF/VP − 1) / i" if simple else "n = [log(VF) − log(VP)] / log(1 + i)   |   Excel: =NPER(i; ; -VP; VF)")
        else:
            st.info("Completa los tres datos conocidos (mayores a cero).")
    except (ValueError, ZeroDivisionError):
        st.error("Datos inconsistentes (por ejemplo, VF menor o igual que VP al despejar tasa o plazo).")

    st.markdown("---")
    st.subheader("📈 Comparación gráfica simple vs. compuesto")
    g1, g2, g3 = st.columns(3)
    with g1:
        vp_g = smart_num_input("Capital (VP $):", key="m2g_vp")
    with g2:
        i_g = smart_num_input("Tasa del período (%):", key="m2g_i", is_currency=False, is_percent=True) / 100.0
    with g3:
        n_g = smart_num_input("Períodos:", key="m2g_n", is_currency=False)
    if vp_g > 0 and n_g > 0:
        n_int = int(math.ceil(n_g))
        df_m2 = pd.DataFrame({
            "Período": range(0, n_int + 1),
            "Interés Simple ($)": [vp_g * (1 + i_g * t) for t in range(0, n_int + 1)],
            "Interés Compuesto ($)": [vp_g * (1 + i_g) ** t for t in range(0, n_int + 1)],
        })
        vf_s, vf_c = vp_g * (1 + i_g * n_g), vp_g * (1 + i_g) ** n_g
        m1, m2, m3 = st.columns(3)
        m1.metric("VF Simple", fmt_currency(vf_s))
        m2.metric("VF Compuesto", fmt_currency(vf_c))
        m3.metric("Diferencia por capitalización", fmt_currency(vf_c - vf_s))
        st.line_chart(df_m2.set_index("Período"))

# =====================================================================
# MÓDULO 3
# =====================================================================
elif modulo == "3. Conversión de Tasas (TNA/TEA)":
    st.header("Conversión y Comparación de Tasas")
    st.latex(r"1 + TE = (1 + i')^{n} \qquad i' = \frac{TN}{m}")

    st.subheader("🔄 Conversor universal")
    tasa, tipo, per, cap = selector_tasa("m3")
    destino = st.selectbox("Convertir a tasa efectiva:", list(PERIODOS.keys()),
                           index=list(PERIODOS).index("Anual"), key="m3_dest")
    if tasa > 0:
        res = tasa_a_periodo(tasa, tipo, per, cap, destino)
        if tipo.startswith("Nominal"):
            st.write(f"• Tasa del período de capitalización ({cap.lower()}): **{fmt_tasa(tasa / (12 / PERIODOS[cap]))}**")
        st.metric(f"Tasa efectiva {destino.lower()}", pct(res, 4))
        st.caption(f"Decimal: {res:.6f}".replace(".", ","))

    st.markdown("---")
    st.subheader("⚖️ Comparador de dos alternativas")
    st.caption("Ambas se llevan a tasa efectiva anual (TEA).")
    st.markdown("**Alternativa A**")
    ta, tpa, pa, ca = selector_tasa("m3a")
    st.markdown("**Alternativa B**")
    tb, tpb, pb, cb = selector_tasa("m3b")
    objetivo = st.radio("Se trata de:", ["Crédito (conviene la menor)", "Inversión (conviene la mayor)"],
                        horizontal=True, key="m3_obj")
    if ta > 0 and tb > 0:
        tea_a = tasa_a_periodo(ta, tpa, pa, ca, "Anual")
        tea_b = tasa_a_periodo(tb, tpb, pb, cb, "Anual")
        st.write(f"• **TEA A:** {fmt_tasa(tea_a)}")
        st.write(f"• **TEA B:** {fmt_tasa(tea_b)}")
        mejor = ("A" if tea_a < tea_b else "B") if objetivo.startswith("Crédito") else ("A" if tea_a > tea_b else "B")
        if abs(tea_a - tea_b) < 1e-12:
            st.info("Ambas alternativas son equivalentes.")
        else:
            st.success(f"Conviene la **Alternativa {mejor}** · diferencia: {fmt_num(abs(tea_a - tea_b)*100, 4)} puntos porcentuales")

# =====================================================================
# MÓDULO 4
# =====================================================================
elif modulo == "4. Anualidades y Amortización":
    st.header("Anualidades y Tablas de Amortización")
    tab1, tab2 = st.tabs(["💳 Crédito, cuota y tabla de desarrollo", "📐 VP / VF de anualidades"])

    with tab1:
        st.caption("Si la tasa no está en la periodicidad de las cuotas, se convierte automáticamente "
                   "(p. ej. cuotas mensuales con tasa cuatrimestral, o cuotas anuales con tasa semestral).")
        a1, a2, a3 = st.columns(3)
        with a1:
            vp_m4 = smart_num_input("Monto del Crédito (VP $):", key="m4_vp")
        with a2:
            n_m4 = smart_num_input("Número de cuotas (n):", key="m4_n", is_currency=False)
        with a3:
            per_cuota = st.selectbox("Periodicidad de las cuotas:", list(PERIODOS.keys()),
                                     index=list(PERIODOS).index("Mensual"), key="m4_percuota")
        tasa, tipo, per, cap = selector_tasa("m4")

        if vp_m4 > 0 and tasa > 0 and n_m4 > 0:
            n_int = int(n_m4)
            i_c = tasa_a_periodo(tasa, tipo, per, cap, per_cuota)
            cuota, df_amort = tabla_amortizacion(vp_m4, i_c, n_int)
            st.write(f"• **Tasa efectiva {per_cuota.lower()} aplicada:** {fmt_tasa(i_c)}")
            m1, m2, m3 = st.columns(3)
            m1.metric("Cuota (R)", fmt_currency(cuota))
            m2.metric("Total pagado (R·n)", fmt_currency(cuota * n_int))
            m3.metric("Intereses totales (R·n − VP)", fmt_currency(cuota * n_int - vp_m4))
            st.code("R = VP · i / (1 − (1 + i)^−n)   |   Excel: =PAGO(i; n; -VP)")

            k = int(smart_num_input("Consultar cuota N° k:", key="m4_k", is_currency=False))
            if 1 <= k <= n_int:
                fila = df_amort.iloc[k - 1]
                q1, q2, q3 = st.columns(3)
                q1.metric(f"Interés cuota {k}", fmt_currency(fila["Interés ($)"]))
                q2.metric(f"Amortización (capital) cuota {k}", fmt_currency(fila["Amortización ($)"]))
                q3.metric(f"Saldo tras pagar cuota {k}", fmt_currency(fila["Saldo Final ($)"]))
            elif k > n_int:
                st.warning("k no puede superar el número de cuotas.")

            st.markdown("#### Tabla de desarrollo")
            disp = df_amort.copy()
            for col in disp.columns[1:]:
                disp[col] = disp[col].apply(fmt_currency)
            st.dataframe(disp, hide_index=True)
            excel_download(df_amort, "Amortización", "tabla_amortizacion.xlsx",
                           "📥 Exportar tabla a Excel (.xlsx)")
        else:
            st.info("Ingresa monto, número de cuotas y tasa.")

    with tab2:
        b1, b2, b3 = st.columns(3)
        with b1:
            r_v = smart_num_input("Renta o cuota periódica (R $):", key="m4b_r")
        with b2:
            i_v = smart_num_input("Tasa efectiva del período (%):", key="m4b_i", is_currency=False, is_percent=True) / 100.0
        with b3:
            n_v = int(smart_num_input("Número de pagos (n):", key="m4b_n", is_currency=False))
        tipo_a = st.selectbox("Tipo de anualidad:", ["Vencida u ordinaria", "Anticipada", "Diferida (vencida)"],
                              key="m4b_tipo")
        k_dif = 0
        if tipo_a.startswith("Diferida"):
            k_dif = int(smart_num_input("Períodos de diferimiento (k):", key="m4b_k", is_currency=False,
                                        help_text="Los pagos comienzan al final del período k+1"))
        if r_v > 0 and n_v > 0:
            vp_o, vf_o = vp_anualidad(r_v, i_v, n_v), vf_anualidad(r_v, i_v, n_v)
            if tipo_a == "Anticipada":
                vp_r, vf_r = vp_o * (1 + i_v), vf_o * (1 + i_v)
                st.code("VP = R·[1 − (1+i)^−n]/i · (1+i)     VF = R·[(1+i)^n − 1]/i · (1+i)")
            elif tipo_a.startswith("Diferida"):
                vp_r, vf_r = vp_o / (1 + i_v) ** k_dif, vf_o
                st.code("VP = R·[1 − (1+i)^−n]/i · (1+i)^−k     (el VF al último pago no cambia)")
            else:
                vp_r, vf_r = vp_o, vf_o
                st.code("VP = R·[1 − (1+i)^−n]/i     VF = R·[(1+i)^n − 1]/i")
            c1, c2 = st.columns(2)
            c1.metric("Valor Presente (t = 0)", fmt_currency(vp_r))
            c2.metric("Valor Futuro (al último pago)" if tipo_a != "Anticipada" else "Valor Futuro (fin del período n)",
                      fmt_currency(vf_r))

# =====================================================================
# MÓDULO 5
# =====================================================================
elif modulo == "5. Gradientes Financieros":
    st.header("Gradientes Financieros (Series Variables)")
    st.latex(r"VP_{arit} = A\frac{1-(1+i)^{-n}}{i} + \frac{G}{i}\left[\frac{1-(1+i)^{-n}}{i} - \frac{n}{(1+i)^{n}}\right]")
    st.latex(r"VP_{geom} = A_1\,\frac{1-\left(\frac{1+g}{1+i}\right)^{n}}{i-g}\quad (i\neq g),\qquad VP=\frac{nA_1}{1+i}\quad (i=g)")

    tipo_g = st.radio("Tipo de gradiente:", ["Aritmético (+G constante)", "Geométrico (+g % constante)"],
                      horizontal=True, key="m5_tipo")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        a_base = smart_num_input("Primer flujo (A o A₁ $):", key="m5_base")
    with c2:
        if tipo_g.startswith("Aritmético"):
            grad = smart_num_input("Gradiente G ($, negativo si decrece):", key="m5_g")
        else:
            grad = smart_num_input("Crecimiento g (%):", key="m5_gpct", is_currency=False, is_percent=True) / 100.0
    with c3:
        i_g = smart_num_input("Tasa efectiva del período (%):", key="m5_i", is_currency=False, is_percent=True) / 100.0
    with c4:
        n_g = int(smart_num_input("Número de flujos (n):", key="m5_n", is_currency=False))
    k_g = int(smart_num_input("Diferimiento: el primer flujo ocurre al final del período k+1 (k):",
                              key="m5_k", is_currency=False))

    if a_base != 0 and n_g > 0:
        if tipo_g.startswith("Aritmético"):
            flujos = [a_base + (t - 1) * grad for t in range(1, n_g + 1)]
            vp_serie = vp_gradiente_aritmetico(a_base, grad, i_g, n_g)
        else:
            flujos = [a_base * (1 + grad) ** (t - 1) for t in range(1, n_g + 1)]
            vp_serie = vp_gradiente_geometrico(a_base, grad, i_g, n_g)
        vp_hoy = vp_serie / (1 + i_g) ** k_g
        vf_fin = vp_serie * (1 + i_g) ** n_g
        m1, m2, m3 = st.columns(3)
        m1.metric("VP de la serie (t = k)" if k_g else "VP (t = 0)", fmt_currency(vp_serie))
        m2.metric("VP hoy (t = 0)", fmt_currency(vp_hoy))
        m3.metric("VF al último flujo", fmt_currency(vf_fin))
        st.write(f"• Último flujo de la serie: **{fmt_currency(flujos[-1])}** · Suma nominal: {fmt_currency(sum(flujos))}")

        if tipo_g.startswith("Geométrico") and i_g > grad:
            st.caption(f"Perpetuidad creciente (si n → ∞): VP = A₁/(i − g) = {fmt_currency(a_base / (i_g - grad))}")

        df_g = pd.DataFrame({"Período": [k_g + t for t in range(1, n_g + 1)], "Flujo ($)": flujos,
                             "VP del flujo ($)": [f / (1 + i_g) ** (k_g + t) for t, f in enumerate(flujos, 1)]})
        st.bar_chart(df_g.set_index("Período")[["Flujo ($)", "VP del flujo ($)"]])
        disp = df_g.copy()
        for col in ["Flujo ($)", "VP del flujo ($)"]:
            disp[col] = disp[col].apply(fmt_currency)
        st.dataframe(disp, hide_index=True)
    else:
        st.info("Ingresa el primer flujo y el número de flujos.")

# =====================================================================
# MÓDULO 6
# =====================================================================
elif modulo == "6. Presupuesto y Flujo de Caja":
    st.header("Presupuesto y Control de Caja Operacional")
    st.subheader("📊 Simulador de presupuesto mensual a 12 meses con inflación")
    pc1, pc2, pc3, pc4 = st.columns(4)
    with pc1:
        v_base = smart_num_input("Ventas Mes 1 ($):", key="m6_vbase")
    with pc2:
        g_ventas = smart_num_input("Crecimiento ventas mensual (%):", key="m6_gventas", is_currency=False, is_percent=True)
    with pc3:
        inf_m = smart_num_input("Inflación costos mensual (%):", key="m6_inf", is_currency=False, is_percent=True)
    with pc4:
        caja_ini = smart_num_input("Caja inicial ($):", key="m6_caja")
    pc5, pc6, pc7 = st.columns(3)
    with pc5:
        pct_cv = smart_num_input("Costo variable (% de ventas, mes 1):", default_val=40.0, key="m6_pcv",
                                 is_currency=False, is_percent=True)
    with pc6:
        gf_base = smart_num_input("Gastos fijos mes 1 ($):", default_val=5000.0, key="m6_gf")
    with pc7:
        imp = smart_num_input("Impuesto sobre utilidad (%):", default_val=27.0, key="m6_imp",
                              is_currency=False, is_percent=True)

    if v_base > 0:
        p_data, caja_acum = [], caja_ini
        for m in range(1, 13):
            v_m = v_base * (1 + g_ventas / 100.0) ** (m - 1)
            c_m = v_m * (pct_cv / 100.0) * (1 + inf_m / 100.0) ** (m - 1)
            f_m = gf_base * (1 + inf_m / 100.0) ** (m - 1)
            r_op = v_m - c_m - f_m
            r_neto = r_op - max(0.0, r_op) * imp / 100.0
            caja_acum += r_neto
            p_data.append({"Mes": f"Mes {m}", "Ventas ($)": v_m, "Costos variables ($)": c_m,
                           "Gastos fijos ($)": f_m, "Resultado operacional ($)": r_op,
                           "Resultado neto ($)": r_neto, "Caja acumulada ($)": caja_acum})
        df_pres = pd.DataFrame(p_data)
        df_pres["Mes"] = pd.Categorical(df_pres["Mes"], categories=[f"Mes {i}" for i in range(1, 13)], ordered=True)

        tot_neto = df_pres["Resultado neto ($)"].sum()
        (st.success if tot_neto >= 0 else st.error)(f"Resultado neto anual: **{fmt_currency(tot_neto)}**")
        disp = df_pres.copy()
        for col in disp.columns[1:]:
            disp[col] = disp[col].apply(fmt_currency)
        st.dataframe(disp, hide_index=True)
        st.caption("Simplificación: el resultado neto se usa como proxy del flujo de caja "
                   "(no separa depreciación ni desfases de cobro/pago).")
        st.bar_chart(df_pres.set_index("Mes")[["Ventas ($)", "Costos variables ($)", "Gastos fijos ($)"]])
        st.line_chart(df_pres.set_index("Mes")[["Caja acumulada ($)"]])
        excel_download(df_pres.astype({"Mes": str}), "Presupuesto", "presupuesto_12m.xlsx",
                       "📥 Exportar presupuesto a Excel (.xlsx)")
    else:
        st.info("Ingresa las ventas del mes 1 para generar el presupuesto.")

# =====================================================================
# MÓDULO 7
# =====================================================================
elif modulo == "7. Evaluación de Proyectos (VAN/TIR)":
    st.header("Evaluación Financiera de Proyectos")
    st.subheader("🎯 Punto de equilibrio operacional")
    eq1, eq2, eq3 = st.columns(3)
    with eq1:
        cf_val = smart_num_input("Costos fijos totales ($):", key="m7_cf")
    with eq2:
        p_val = smart_num_input("Precio unitario ($):", key="m7_p")
    with eq3:
        cv_val = smart_num_input("Costo variable unitario ($):", key="m7_cv")
    if cf_val > 0 and p_val > cv_val:
        q_eq = cf_val / (p_val - cv_val)
        st.success(f"• **Punto de equilibrio:** **{fmt_num(q_eq)} unidades** · Ingreso: **{fmt_currency(q_eq * p_val)}**")
    else:
        st.info("Ingresa costos fijos, precio y costo variable (precio > costo variable).")

    st.markdown("---")
    st.subheader("💰 VAN y TIR")
    inv_ini = smart_num_input("Inversión inicial ($):", key="m7_inv")
    tmar_val = smart_num_input("TMAR / tasa de descuento efectiva por período (%):", key="m7_tmar",
                               is_currency=False, is_percent=True)
    n_fl = int(smart_num_input("Número de períodos con flujo:", default_val=5.0, key="m7_nfl", is_currency=False))
    n_fl = max(1, min(n_fl, 30))
    flujos = []
    cols = st.columns(5)
    for idx in range(n_fl):
        with cols[idx % 5]:
            flujos.append(smart_num_input(f"Flujo período {idx+1} ($):", key=f"m7_f_{idx}"))

    if inv_ini > 0 and tmar_val > 0 and any(f != 0 for f in flujos):
        tmar_dec = tmar_val / 100.0
        van_val = npf.npv(tmar_dec, [-inv_ini] + flujos)
        tir_val = npf.irr([-inv_ini] + flujos)
        c1, c2 = st.columns(2)
        c1.metric("VAN", fmt_currency(van_val), delta="Viable" if van_val > 0 else "No viable",
                  delta_color="normal" if van_val > 0 else "inverse")
        if tir_val is None or math.isnan(tir_val):
            c2.metric("TIR", "No definida")
        else:
            c2.metric("TIR", pct(tir_val, 2), delta="TIR > TMAR" if tir_val > tmar_dec else "TIR < TMAR",
                      delta_color="normal" if tir_val > tmar_dec else "inverse")
        st.caption("Tip: los flujos con gradiente pueden generarse en el Módulo 5.")

# =====================================================================
# MÓDULO 8
# =====================================================================
elif modulo == "8. Calculadoras Especializadas y Simuladores":
    st.header("Calculadoras Especializadas")
    herramientas = [
        "I. Desglose de Interés y Amortización para Cuota k con Convertidor",
        "II. Valor Futuro con Interés Compuesto (Plazos Enteros y Fraccionados)",
        "III. Valor Futuro de Anualidades y Fondos de Ahorro",
        "IV. Valuación de Flujos Múltiples e Irregulares (VP y VF)",
        "V. Despeje de Plazo Requerido (n) y Tasa Implícita",
        "VI. Conversión Avanzada de Tasas Nominales/Efectivas",
        "VII. Valor Presente (VP) de Pagos Futuros Específicos Discretos",
        "VIII. Valor Futuro (VF) de Depósitos Proyectados Discretos (Tasas Variables)",
        "IX. Comparador de Ofertas Bancarias a Plazo Fijo (Múltiples Bancos y Tasas)",
        "X. Crédito Comercial / Bienes de Capital",
        "XI. Tasa Implícita Anual para Créditos o Inversiones de Pago Único",
        "XII. Valor Presente de Pago Único / Descuento (4 Decimales)",
        "XIII. Calculadora Universal de Cuotas e Intereses de Préstamos (4 Decimales)",
        "XIV. Calculadora de Costo Financiero Total (CFT) y Comisiones",
    ]
    h_sel = st.selectbox("Selecciona la herramienta:", herramientas)

    # ---------------- I ----------------
    if h_sel.startswith("I. "):
        st.subheader("I. Desglose de interés y amortización para la cuota k")
        c1, c2, c3 = st.columns(3)
        with c1:
            vp_h1 = smart_num_input("Monto del préstamo ($):", key="h1_vp")
        with c2:
            n_h1 = int(smart_num_input("Número de cuotas (n):", key="h1_n", is_currency=False))
        with c3:
            k_h1 = int(smart_num_input("Cuota a consultar (k):", key="h1_k", is_currency=False))
        per_c = st.selectbox("Periodicidad de las cuotas:", list(PERIODOS.keys()),
                             index=list(PERIODOS).index("Mensual"), key="h1_percuota")
        tasa, tipo, per, cap = selector_tasa("h1")
        if k_h1 > n_h1 > 0:
            st.warning("La cuota k no puede ser mayor que n.")
        elif vp_h1 > 0 and tasa > 0 and n_h1 > 0 and k_h1 > 0:
            i_c = tasa_a_periodo(tasa, tipo, per, cap, per_c)
            pmt, df = tabla_amortizacion(vp_h1, i_c, n_h1)
            f = df.iloc[k_h1 - 1]
            st.write(f"• Tasa efectiva {per_c.lower()} aplicada: **{fmt_tasa(i_c)}**")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Cuota (R)", fmt_currency(pmt))
            m2.metric(f"Interés cuota {k_h1}", fmt_currency(f["Interés ($)"]))
            m3.metric(f"Amortización cuota {k_h1}", fmt_currency(f["Amortización ($)"]))
            m4.metric(f"Saldo tras cuota {k_h1}", fmt_currency(f["Saldo Final ($)"]))
        else:
            st.info("Ingresa los datos del préstamo.")

    # ---------------- II ----------------
    elif h_sel.startswith("II. "):
        st.subheader("II. Valor futuro con interés compuesto")
        c1, c2, c3 = st.columns(3)
        with c1:
            vp_h2 = smart_num_input("Capital inicial (VP $):", key="h2_vp")
        with c2:
            tasa_h2 = smart_num_input("Tasa efectiva anual (%):", key="h2_tasa", is_currency=False, is_percent=True)
        with c3:
            meses_h2 = smart_num_input("Plazo en meses:", key="h2_meses", is_currency=False)
        if vp_h2 > 0 and tasa_h2 > 0 and meses_h2 > 0:
            vf_h2 = vp_h2 * (1 + tasa_h2 / 100.0) ** (meses_h2 / 12.0)
            st.success(f"• **Valor futuro:** **{fmt_currency(vf_h2)}** · intereses {fmt_currency(vf_h2 - vp_h2)}")

    # ---------------- III ----------------
    elif h_sel.startswith("III. "):
        st.subheader("III. Valor futuro de anualidades y fondos de ahorro")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            r_h3 = smart_num_input("Aporte periódico (R $):", key="h3_r")
        with c2:
            tasa_h3 = smart_num_input("Tasa efectiva del período (%):", key="h3_tasa", is_currency=False, is_percent=True)
        with c3:
            n_h3 = int(smart_num_input("Número de períodos (n):", key="h3_n", is_currency=False))
        with c4:
            tipo_h3 = st.selectbox("Modalidad:", ["Vencida (fin de período)", "Anticipada (inicio de período)"], key="h3_tipo")
        if r_h3 > 0 and tasa_h3 > 0 and n_h3 > 0:
            i_dec = tasa_h3 / 100.0
            vf_h3 = vf_anualidad(r_h3, i_dec, n_h3) * ((1 + i_dec) if "Anticipada" in tipo_h3 else 1)
            st.success(f"• **Valor futuro acumulado:** **{fmt_currency(vf_h3)}** · aportado {fmt_currency(r_h3 * n_h3)}")

    # ---------------- IV ----------------
    elif h_sel.startswith("IV. "):
        st.subheader("IV. Flujos múltiples consecutivos (períodos 1..N)")
        c1, c2 = st.columns(2)
        with c1:
            tasa_h4 = smart_num_input("Tasa efectiva del período (%):", key="h4_tasa", is_currency=False, is_percent=True)
        with c2:
            n_cant = int(smart_num_input("Cantidad de flujos:", key="h4_cant", is_currency=False))
        if n_cant > 0 and tasa_h4 > 0:
            flujos_h4 = []
            f_cols = st.columns(min(n_cant, 5))
            for idx in range(n_cant):
                with f_cols[idx % 5]:
                    flujos_h4.append(smart_num_input(f"Flujo período {idx+1} ($):", key=f"h4_f_{idx}"))
            r_dec = tasa_h4 / 100.0
            vp_tot = sum(f / (1 + r_dec) ** (idx + 1) for idx, f in enumerate(flujos_h4))
            st.metric("Valor presente (t = 0)", fmt_currency(vp_tot))
            st.metric(f"Valor futuro (t = {n_cant})", fmt_currency(vp_tot * (1 + r_dec) ** n_cant))
            st.caption("Para flujos en meses no consecutivos usa las herramientas VII (VP) y VIII (VF).")

    # ---------------- V ----------------
    elif h_sel.startswith("V. "):
        st.subheader("V. Despeje de plazo (n) y tasa implícita — interés compuesto")
        c1, c2 = st.columns(2)
        with c1:
            vp_h5 = smart_num_input("Capital inicial (VP $):", key="h5_vp")
        with c2:
            vf_h5 = smart_num_input("Meta de capital (VF $):", key="h5_vf")
        c3, c4 = st.columns(2)
        with c3:
            tasa_h5 = smart_num_input("Tasa efectiva anual (%) → calcula plazo:", key="h5_tasa",
                                      is_currency=False, is_percent=True)
        with c4:
            plazo_h5 = smart_num_input("Plazo en años → calcula tasa:", key="h5_plazo", is_currency=False)
        if vp_h5 > 0 and vf_h5 > vp_h5:
            if tasa_h5 > 0:
                n_anos = math.log(vf_h5 / vp_h5) / math.log(1 + tasa_h5 / 100.0)
                st.success(f"• **Plazo requerido:** **{fmt_num(n_anos, 4)} años** ({fmt_num(n_anos * 12, 2)} meses)")
            if plazo_h5 > 0:
                i_impl = (vf_h5 / vp_h5) ** (1.0 / plazo_h5) - 1.0
                st.success(f"• **Tasa efectiva anual implícita:** **{fmt_tasa(i_impl)}**")

    # ---------------- VI ----------------
    elif h_sel.startswith("VI. "):
        st.subheader("VI. Conversión de tasa nominal (frecuencia libre) a TEA")
        c1, c2 = st.columns(2)
        with c1:
            tna_h6 = smart_num_input("Tasa nominal anual (%):", key="h6_tna", is_currency=False, is_percent=True)
        with c2:
            m_h6 = smart_num_input("Capitalizaciones por año (m):", key="h6_m", is_currency=False)
        if tna_h6 > 0 and m_h6 > 0:
            i_per = tna_h6 / 100.0 / m_h6
            st.write(f"• Tasa del período: **{fmt_tasa(i_per)}**")
            st.metric("TEA", pct(((1 + i_per) ** m_h6 - 1), 4))

    # ---------------- VII ----------------
    elif h_sel.startswith("VII. "):
        st.subheader("VII. Valor presente de pagos en meses específicos")
        c1, c2 = st.columns(2)
        with c1:
            tasa_h7 = smart_num_input("Tasa efectiva mensual (%):", key="h7_tasa", is_currency=False, is_percent=True)
        with c2:
            n_cant = int(smart_num_input("Cantidad de pagos:", key="h7_cant", is_currency=False))
        if n_cant > 0 and tasa_h7 > 0:
            pagos = []
            for idx in range(n_cant):
                cm, cv = st.columns(2)
                with cm:
                    m_pago = int(smart_num_input(f"Mes del pago #{idx+1}:", key=f"h7_m_{idx}", is_currency=False))
                with cv:
                    v_pago = smart_num_input(f"Monto pago #{idx+1} ($):", key=f"h7_v_{idx}")
                pagos.append((m_pago, v_pago))
            r_dec = tasa_h7 / 100.0
            vp_tot = sum(v / (1 + r_dec) ** m for m, v in pagos if m >= 0)
            st.success(f"• **Valor presente consolidado (t = 0):** **{fmt_currency(vp_tot)}**")

    # ---------------- VIII ----------------
    elif h_sel.startswith("VIII. "):
        st.subheader("VIII. Valor futuro de depósitos discretos con cambio de tasa")
        c1, c2, c3 = st.columns(3)
        with c1:
            N_int = int(smart_num_input("Horizonte total en meses (N):", key="h8_horizonte", is_currency=False))
        with c2:
            tasa_ini = smart_num_input("Tasa inicial mensual (%):", key="h8_tasa_ini", is_currency=False, is_percent=True)
        with c3:
            modo = st.selectbox("Momento del depósito:", ["Fin del mes (vencido)", "Inicio del mes (anticipado)"], key="h8_modo")
        c4, c5 = st.columns(2)
        with c4:
            m_camb = int(smart_num_input("Mes desde el cual rige la nueva tasa:", key="h8_mcamb", is_currency=False))
        with c5:
            tasa_new = smart_num_input("Nueva tasa mensual (%):", key="h8_tnueva", is_currency=False, is_percent=True)
        n_deps = int(smart_num_input("Cantidad de depósitos:", key="h8_cdeps", is_currency=False))

        if N_int > 0 and tasa_ini > 0 and n_deps > 0:
            deps = {}
            d_cols = st.columns(min(n_deps, 4))
            for d in range(n_deps):
                with d_cols[d % 4]:
                    m_dep = int(smart_num_input(f"Mes depósito #{d+1}:", key=f"h8_mdep_{d}", is_currency=False))
                    v_dep = smart_num_input(f"Monto depósito #{d+1} ($):", key=f"h8_vdep_{d}")
                    if 0 < m_dep <= N_int and v_dep > 0:
                        deps[m_dep] = deps.get(m_dep, 0.0) + v_dep
            tasas = [(tasa_new if (m_camb > 0 and m >= m_camb and tasa_new > 0) else tasa_ini) / 100.0
                     for m in range(1, N_int + 1)]
            vencido = modo.startswith("Fin")
            filas = []
            for m_dep, monto in sorted(deps.items()):
                desde = m_dep + 1 if vencido else m_dep
                factor = math.prod(1 + tasas[m - 1] for m in range(desde, N_int + 1))
                filas.append({"Mes del depósito": m_dep, "Monto ($)": monto,
                              "Meses capitalizados": N_int - desde + 1, "VF ($)": monto * factor})
            if filas:
                df8 = pd.DataFrame(filas)
                disp = df8.copy()
                for col in ["Monto ($)", "VF ($)"]:
                    disp[col] = disp[col].apply(fmt_currency)
                st.dataframe(disp, hide_index=True)
                st.success(f"• **Valor futuro total (t = {N_int}):** **{fmt_currency(df8['VF ($)'].sum())}**")

    # ---------------- IX ----------------
    elif h_sel.startswith("IX. "):
        st.subheader("IX. Comparador de depósitos a plazo")
        c1, c2 = st.columns(2)
        with c1:
            monto_h9 = smart_num_input("Monto del depósito ($):", key="h9_monto")
        with c2:
            plazo_h9 = smart_num_input("Plazo total en meses:", key="h9_plazo_m", is_currency=False)
        n_b = max(2, min(5, int(smart_num_input("Cantidad de bancos (2 a 5):", default_val=2.0, key="h9_n_bancos",
                                                is_currency=False))))
        regimen_h9 = ["Compuesto", "Simple"]
        if monto_h9 > 0 and plazo_h9 > 0:
            datos = []
            for idx in range(n_b):
                st.markdown(f"**Banco #{idx+1}**")
                b_name = st.text_input(f"Nombre banco #{idx+1}:", value="", placeholder=f"Banco {idx+1}", key=f"h9_name_{idx}")
                reg = st.selectbox(f"Régimen banco #{idx+1}:", regimen_h9, key=f"h9_reg_{idx}")
                tasa, tipo, per, cap = selector_tasa(f"h9_{idx}")
                if tasa > 0:
                    if reg == "Simple":
                        # tasa simple del período → simple anual proporcional
                        tasa_anual = tasa * (12 / PERIODOS[per])
                        vf_b = monto_h9 * (1 + tasa_anual * plazo_h9 / 12.0)
                        tea_b = (vf_b / monto_h9) ** (12 / plazo_h9) - 1
                    else:
                        tea_b = tasa_a_periodo(tasa, tipo, per, cap, "Anual")
                        vf_b = monto_h9 * (1 + tea_b) ** (plazo_h9 / 12.0)
                    datos.append({"Banco": b_name.strip() or f"Banco {idx+1}",
                                  "Tasa ofrecida": f"{tasa*100:.4f}% {tipo.split()[0].lower()} ({per.lower() if not tipo.startswith('Nominal') else 'cap. ' + cap.lower()}) · {reg.lower()}",
                                  "TEA equivalente": pct(tea_b, 4),
                                  "Monto final ($)": vf_b, "Intereses ($)": vf_b - monto_h9})
            if datos:
                df9 = pd.DataFrame(datos).sort_values("Monto final ($)", ascending=False)
                mejor = df9["Monto final ($)"].iloc[0]
                df9["Diferencia vs. mejor"] = ["🥇 Mejor oferta" if mejor - v < 1e-6 else f"-{fmt_currency(mejor - v)}"
                                               for v in df9["Monto final ($)"]]
                for col in ["Monto final ($)", "Intereses ($)"]:
                    df9[col] = df9[col].apply(fmt_currency)
                st.dataframe(df9, hide_index=True)

    # ---------------- X ----------------
    elif h_sel.startswith("X. "):
        st.subheader("X. Crédito comercial con tasa semestral")
        c1, c2, c3 = st.columns(3)
        with c1:
            monto_h10 = smart_num_input("Monto del préstamo ($):", key="hx_monto")
        with c2:
            tasa_sem = smart_num_input("Tasa efectiva semestral (%):", key="hx_tsem", is_currency=False, is_percent=True)
        with c3:
            anos = int(smart_num_input("Plazo en años:", key="hx_anos", is_currency=False))
        if monto_h10 > 0 and tasa_sem > 0 and anos > 0:
            tea = (1 + tasa_sem / 100.0) ** 2 - 1
            tem = (1 + tea) ** (1 / 12.0) - 1
            pmt_a, pmt_m = cuota_anualidad(monto_h10, tea, anos), cuota_anualidad(monto_h10, tem, anos * 12)
            st.metric("TEA", pct(tea, 4))
            st.metric("Cuota anual", fmt_currency(pmt_a))
            st.write(f"• Intereses totales con cuota anual: **{fmt_currency(pmt_a * anos - monto_h10)}**")
            st.metric("Cuota mensual equivalente", fmt_currency(pmt_m))
            st.write(f"• Intereses totales con cuota mensual: **{fmt_currency(pmt_m * anos * 12 - monto_h10)}**")

    # ---------------- XI ----------------
    elif h_sel.startswith("XI. "):
        st.subheader("XI. Tasa implícita de pago único (en trimestres)")
        c1, c2, c3 = st.columns(3)
        with c1:
            vp_h11 = smart_num_input("Monto inicial ($):", key="hxi_vp")
        with c2:
            vf_h11 = smart_num_input("Monto final ($):", key="hxi_vf")
        with c3:
            trim = smart_num_input("Plazo en trimestres:", key="hxi_trim", is_currency=False)
        if vp_h11 > 0 and vf_h11 > vp_h11 and trim > 0:
            i_t = (vf_h11 / vp_h11) ** (1.0 / trim) - 1.0
            st.metric("Tasa trimestral implícita", pct(i_t, 4))
            st.metric("TEA implícita", pct(((1 + i_t) ** 4 - 1), 4))
            st.caption(f"Decimal TEA: {(1 + i_t) ** 4 - 1:.6f}".replace(".", ","))

    # ---------------- XII ----------------
    elif h_sel.startswith("XII. "):
        st.subheader("XII. Valor presente de un pago único")
        c1, c2, c3 = st.columns(3)
        with c1:
            vf_h12 = smart_num_input("Monto futuro (VF $):", key="h12_vf")
        with c2:
            tea_h12 = smart_num_input("TEA (%):", key="h12_tea", is_currency=False, is_percent=True)
        with c3:
            meses_h12 = smart_num_input("Plazo en meses:", key="h12_meses", is_currency=False)
        if vf_h12 > 0 and tea_h12 > 0 and meses_h12 > 0:
            vp_h12 = vf_h12 / (1 + tea_h12 / 100.0) ** (meses_h12 / 12.0)
            st.success(f"• **Valor presente:** **{vp_h12:.4f}** ({fmt_currency(vp_h12)})")

    # ---------------- XIII ----------------
    elif h_sel.startswith("XIII. "):
        st.subheader("XIII. Cuota de préstamo (tasa y cuotas de igual periodicidad)")
        c1, c2, c3 = st.columns(3)
        with c1:
            vp_h13 = smart_num_input("Monto del préstamo ($):", key="h13_vp")
        with c2:
            tasa_h13 = smart_num_input("Tasa efectiva del período (%):", key="h13_tasa", is_currency=False, is_percent=True)
        with c3:
            n_h13 = int(smart_num_input("Número de cuotas (n):", key="h13_n", is_currency=False))
        if vp_h13 > 0 and tasa_h13 > 0 and n_h13 > 0:
            pmt = cuota_anualidad(vp_h13, tasa_h13 / 100.0, n_h13)
            st.write(f"• **Cuota exacta:** **{pmt:.4f}**")
            st.success(f"• **Cuota:** **{fmt_currency(pmt)}** · intereses totales {fmt_currency(pmt * n_h13 - vp_h13)}")

    # ---------------- XIV ----------------
    elif h_sel.startswith("XIV. "):
        st.subheader("XIV. Costo financiero total (CFT) y comisiones")
        c1, c2, c3 = st.columns(3)
        with c1:
            monto_h14 = smart_num_input("Monto del préstamo ($):", key="h14_monto")
        with c2:
            tea_h14 = smart_num_input("TEA (%):", key="h14_tea", is_currency=False, is_percent=True)
        with c3:
            com_h14 = smart_num_input("Comisión anual ($):", key="h14_com")
        if monto_h14 > 0:
            pct_com = com_h14 / monto_h14 * 100.0
            st.metric("Comisión sobre el crédito", f"{pct_com:.2f}%")
            st.metric("CFT", f"{tea_h14 + pct_com:.2f}%")
            st.metric("Costo total en dinero (1 año)", fmt_currency(monto_h14 * tea_h14 / 100.0 + com_h14))
            st.caption("Aproximación del curso (horizonte de 1 año): CFT ≈ TEA + comisión/monto. "
                       "Para créditos en cuotas, el CFT exacto es la TIR de los flujos netos.")

st.markdown("---")
st.caption("Plataforma de Simulación e Ingeniería Financiera")
