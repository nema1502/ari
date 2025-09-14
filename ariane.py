import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Calculadora Financiera Completa",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Estilo CSS personalizado ---
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-bottom: 1rem;
    }
    .metric-container {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .formula-box {
        background-color: #fff8dc;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #ddd;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# --- Funciones de Cálculo ---

def interes_simple_vf(capital, tasa_anual, tiempo, unidad_tiempo="Años"):
    """Calcula el Valor Futuro con Interés Simple"""
    # Convertir tiempo a años
    if unidad_tiempo == "Meses":
        tiempo_anos = tiempo / 12
    elif unidad_tiempo == "Días":
        tiempo_anos = tiempo / 365
    else:
        tiempo_anos = tiempo
    
    # VF = C(1 + rt)
    valor_futuro = capital * (1 + tasa_anual * tiempo_anos)
    interes_ganado = valor_futuro - capital
    return valor_futuro, interes_ganado

def interes_simple_vp(valor_futuro, tasa_anual, tiempo, unidad_tiempo="Años"):
    """Calcula el Valor Presente con Interés Simple"""
    # Convertir tiempo a años
    if unidad_tiempo == "Meses":
        tiempo_anos = tiempo / 12
    elif unidad_tiempo == "Días":
        tiempo_anos = tiempo / 365
    else:
        tiempo_anos = tiempo
    
    # VP = VF / (1 + rt)
    valor_presente = valor_futuro / (1 + tasa_anual * tiempo_anos)
    interes_total = valor_futuro - valor_presente
    return valor_presente, interes_total

def interes_compuesto_vf(capital, tasa_anual, tiempo, capitalizacion, unidad_tiempo="Años"):
    """Calcula el Valor Futuro con Interés Compuesto"""
    # Convertir tiempo a años
    if unidad_tiempo == "Meses":
        tiempo_anos = tiempo / 12
    elif unidad_tiempo == "Días":
        tiempo_anos = tiempo / 365
    else:
        tiempo_anos = tiempo
    
    # Frecuencia de capitalización
    n_map = {"Anual": 1, "Semestral": 2, "Trimestral": 4, "Mensual": 12, "Diario": 365}
    n = n_map[capitalizacion]
    
    # VF = C(1 + r/n)^(nt)
    valor_futuro = capital * (1 + tasa_anual/n)**(n * tiempo_anos)
    interes_ganado = valor_futuro - capital
    return valor_futuro, interes_ganado

def interes_compuesto_vp(valor_futuro, tasa_anual, tiempo, capitalizacion, unidad_tiempo="Años"):
    """Calcula el Valor Presente con Interés Compuesto"""
    # Convertir tiempo a años
    if unidad_tiempo == "Meses":
        tiempo_anos = tiempo / 12
    elif unidad_tiempo == "Días":
        tiempo_anos = tiempo / 365
    else:
        tiempo_anos = tiempo
    
    # Frecuencia de capitalización
    n_map = {"Anual": 1, "Semestral": 2, "Trimestral": 4, "Mensual": 12, "Diario": 365}
    n = n_map[capitalizacion]
    
    # VP = VF / (1 + r/n)^(nt)
    valor_presente = valor_futuro / (1 + tasa_anual/n)**(n * tiempo_anos)
    interes_total = valor_futuro - valor_presente
    return valor_presente, interes_total

def crear_grafico_comparacion(capital, tasa, tiempo_max, capitalizacion="Anual"):
    """Crea gráfico comparativo interactivo"""
    periodos = np.arange(0, tiempo_max + 1, 1)
    
    # Calcular valores para cada período
    valores_simple = []
    valores_compuesto = []
    
    for t in periodos:
        if t == 0:
            valores_simple.append(capital)
            valores_compuesto.append(capital)
        else:
            vf_simple, _ = interes_simple_vf(capital, tasa, t)
            vf_compuesto, _ = interes_compuesto_vf(capital, tasa, t, capitalizacion)
            valores_simple.append(vf_simple)
            valores_compuesto.append(vf_compuesto)
    
    # Crear gráfico con Plotly
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=periodos, 
        y=valores_simple,
        mode='lines+markers',
        name='Interés Simple',
        line=dict(color='#ff7f0e', width=3),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=periodos, 
        y=valores_compuesto,
        mode='lines+markers',
        name='Interés Compuesto',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title=f'Comparación de Crecimiento: Simple vs Compuesto',
        xaxis_title='Tiempo (Años)',
        yaxis_title='Valor ($)',
        hovermode='x unified',
        template='plotly_white',
        height=500
    )
    
    return fig

# --- Interfaz Principal ---
st.markdown('<h1 class="main-header">💰 Calculadora Financiera Completa</h1>', unsafe_allow_html=True)
st.markdown("---")

# --- SIDEBAR para navegación ---
with st.sidebar:
    st.image("https://via.placeholder.com/200x100/1f77b4/ffffff?text=Finanzas", width=200)
    st.markdown("### 📊 Navegación")
    
    # Información contextual
    with st.expander("ℹ️ Información"):
        st.markdown("""
        **Fórmulas utilizadas:**
        
        **Interés Simple:**
        - VF = C(1 + rt)
        - VP = VF/(1 + rt)
        
        **Interés Compuesto:**
        - VF = C(1 + r/n)^(nt)
        - VP = VF/(1 + r/n)^(nt)
        """)

# --- PESTAÑAS PRINCIPALES ---
tab1, tab2, tab3 = st.tabs([
    "🧮 **Calculadora de Interés**",
    "📊 **Análisis Comparativo**", 
    "📚 **Ejemplos Prácticos**"
])

# === PESTAÑA 1: CALCULADORA DE INTERÉS ===
with tab1:
    st.markdown('<h2 class="sub-header">Calculadora de Interés: Valor Futuro y Presente</h2>', unsafe_allow_html=True)
    
    # Sub-pestañas para diferentes tipos de cálculo
    subtab1, subtab2, subtab3, subtab4 = st.tabs([
        "🚀 Interés Compuesto VF",
        "🏦 Interés Compuesto VP", 
        "📈 Interés Simple VF",
        "💵 Interés Simple VP"
    ])
    
    # --- INTERÉS COMPUESTO VALOR FUTURO ---
    with subtab1:
        st.markdown("### Interés Compuesto - Valor Futuro")
        st.markdown("*Calcula cuánto valdrá tu inversión en el futuro*")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### 📝 Datos de Entrada")
            ic_vf_capital = st.number_input("Capital Inicial ($):", min_value=0.0, value=10000.0, step=500.0, key="ic_vf_c")
            ic_vf_tasa = st.number_input("Tasa de Interés Anual (%):", min_value=0.0, value=8.0, step=0.1, key="ic_vf_r")
            
            col_t1, col_t2 = st.columns([2, 1])
            with col_t1:
                ic_vf_tiempo = st.number_input("Tiempo:", min_value=0.0, value=5.0, step=0.1, key="ic_vf_t")
            with col_t2:
                ic_vf_unidad = st.selectbox("Unidad:", ("Años", "Meses", "Días"), key="ic_vf_u")
            
            ic_vf_cap = st.selectbox("Capitalización:", ("Anual", "Semestral", "Trimestral", "Mensual", "Diario"), key="ic_vf_cap")
        
        with col2:
            st.markdown("#### 📊 Resultados")
            if ic_vf_capital > 0 and ic_vf_tasa > 0 and ic_vf_tiempo > 0:
                tasa_decimal = ic_vf_tasa / 100
                vf, interes = interes_compuesto_vf(ic_vf_capital, tasa_decimal, ic_vf_tiempo, ic_vf_cap, ic_vf_unidad)
                
                st.metric("💰 Valor Futuro", f"${vf:,.2f}", delta=f"+${interes:,.2f}")
                st.metric("📈 Interés Ganado", f"${interes:,.2f}")
                st.metric("📊 Rendimiento %", f"{((vf/ic_vf_capital - 1) * 100):.2f}%")
                
                # Fórmula utilizada
                st.markdown(f"""
                <div class="formula-box">
                <b>Fórmula:</b> VF = ${ic_vf_capital:,.2f} × (1 + {tasa_decimal:.4f}/{ic_vf_cap})^({ic_vf_cap} × {ic_vf_tiempo})
                <br><b>Resultado:</b> ${vf:,.2f}
                </div>
                """, unsafe_allow_html=True)
    
    # --- INTERÉS COMPUESTO VALOR PRESENTE ---
    with subtab2:
        st.markdown("### Interés Compuesto - Valor Presente")
        st.markdown("*Calcula cuánto debes invertir hoy para obtener un monto futuro*")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### 📝 Datos de Entrada")
            ic_vp_vf = st.number_input("Valor Futuro Deseado ($):", min_value=0.0, value=15000.0, step=500.0, key="ic_vp_vf")
            ic_vp_tasa = st.number_input("Tasa de Interés Anual (%):", min_value=0.0, value=8.0, step=0.1, key="ic_vp_r")
            
            col_t1, col_t2 = st.columns([2, 1])
            with col_t1:
                ic_vp_tiempo = st.number_input("Tiempo:", min_value=0.0, value=5.0, step=0.1, key="ic_vp_t")
            with col_t2:
                ic_vp_unidad = st.selectbox("Unidad:", ("Años", "Meses", "Días"), key="ic_vp_u")
            
            ic_vp_cap = st.selectbox("Capitalización:", ("Anual", "Semestral", "Trimestral", "Mensual", "Diario"), key="ic_vp_cap")
        
        with col2:
            st.markdown("#### 📊 Resultados")
            if ic_vp_vf > 0 and ic_vp_tasa > 0 and ic_vp_tiempo > 0:
                tasa_decimal = ic_vp_tasa / 100
                vp, interes_total = interes_compuesto_vp(ic_vp_vf, tasa_decimal, ic_vp_tiempo, ic_vp_cap, ic_vp_unidad)
                
                st.metric("🏦 Valor Presente (Inversión Hoy)", f"${vp:,.2f}")
                st.metric("💰 Valor Futuro", f"${ic_vp_vf:,.2f}", delta=f"+${interes_total:,.2f}")
                st.metric("📈 Interés Total a Ganar", f"${interes_total:,.2f}")
                
                # Fórmula utilizada
                st.markdown(f"""
                <div class="formula-box">
                <b>Fórmula:</b> VP = ${ic_vp_vf:,.2f} ÷ (1 + {tasa_decimal:.4f}/{ic_vp_cap})^({ic_vp_cap} × {ic_vp_tiempo})
                <br><b>Resultado:</b> ${vp:,.2f}
                </div>
                """, unsafe_allow_html=True)
    
    # --- INTERÉS SIMPLE VALOR FUTURO ---
    with subtab3:
        st.markdown("### Interés Simple - Valor Futuro")
        st.markdown("*Cálculo lineal de crecimiento de capital*")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### 📝 Datos de Entrada")
            is_vf_capital = st.number_input("Capital Inicial ($):", min_value=0.0, value=10000.0, step=500.0, key="is_vf_c")
            is_vf_tasa = st.number_input("Tasa de Interés Anual (%):", min_value=0.0, value=8.0, step=0.1, key="is_vf_r")
            
            col_t1, col_t2 = st.columns([2, 1])
            with col_t1:
                is_vf_tiempo = st.number_input("Tiempo:", min_value=0.0, value=5.0, step=0.1, key="is_vf_t")
            with col_t2:
                is_vf_unidad = st.selectbox("Unidad:", ("Años", "Meses", "Días"), key="is_vf_u")
        
        with col2:
            st.markdown("#### 📊 Resultados")
            if is_vf_capital > 0 and is_vf_tasa > 0 and is_vf_tiempo > 0:
                tasa_decimal = is_vf_tasa / 100
                vf, interes = interes_simple_vf(is_vf_capital, tasa_decimal, is_vf_tiempo, is_vf_unidad)
                
                st.metric("💰 Valor Futuro", f"${vf:,.2f}", delta=f"+${interes:,.2f}")
                st.metric("📈 Interés Ganado", f"${interes:,.2f}")
                st.metric("📊 Rendimiento %", f"{((vf/is_vf_capital - 1) * 100):.2f}%")
                
                # Fórmula utilizada
                st.markdown(f"""
                <div class="formula-box">
                <b>Fórmula:</b> VF = ${is_vf_capital:,.2f} × (1 + {tasa_decimal:.4f} × {is_vf_tiempo})
                <br><b>Resultado:</b> ${vf:,.2f}
                </div>
                """, unsafe_allow_html=True)
    
    # --- INTERÉS SIMPLE VALOR PRESENTE ---
    with subtab4:
        st.markdown("### Interés Simple - Valor Presente")
        st.markdown("*Calcula la inversión inicial necesaria con interés simple*")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### 📝 Datos de Entrada")
            is_vp_vf = st.number_input("Valor Futuro Deseado ($):", min_value=0.0, value=15000.0, step=500.0, key="is_vp_vf")
            is_vp_tasa = st.number_input("Tasa de Interés Anual (%):", min_value=0.0, value=8.0, step=0.1, key="is_vp_r")
            
            col_t1, col_t2 = st.columns([2, 1])
            with col_t1:
                is_vp_tiempo = st.number_input("Tiempo:", min_value=0.0, value=5.0, step=0.1, key="is_vp_t")
            with col_t2:
                is_vp_unidad = st.selectbox("Unidad:", ("Años", "Meses", "Días"), key="is_vp_u")
        
        with col2:
            st.markdown("#### 📊 Resultados")
            if is_vp_vf > 0 and is_vp_tasa > 0 and is_vp_tiempo > 0:
                tasa_decimal = is_vp_tasa / 100
                vp, interes_total = interes_simple_vp(is_vp_vf, tasa_decimal, is_vp_tiempo, is_vp_unidad)
                
                st.metric("🏦 Valor Presente (Inversión Hoy)", f"${vp:,.2f}")
                st.metric("💰 Valor Futuro", f"${is_vp_vf:,.2f}", delta=f"+${interes_total:,.2f}")
                st.metric("📈 Interés Total a Ganar", f"${interes_total:,.2f}")
                
                # Fórmula utilizada
                st.markdown(f"""
                <div class="formula-box">
                <b>Fórmula:</b> VP = ${is_vp_vf:,.2f} ÷ (1 + {tasa_decimal:.4f} × {is_vp_tiempo})
                <br><b>Resultado:</b> ${vp:,.2f}
                </div>
                """, unsafe_allow_html=True)

# === PESTAÑA 2: ANÁLISIS COMPARATIVO ===
with tab2:
    st.markdown('<h2 class="sub-header">Análisis Comparativo: Simple vs Compuesto</h2>', unsafe_allow_html=True)
    
    # Configuración para comparación
    col_config1, col_config2, col_graph = st.columns([1, 1, 2])
    
    with col_config1:
        st.markdown("#### ⚙️ Configuración")
        comp_capital = st.number_input("Capital Inicial ($):", min_value=0.0, value=10000.0, step=1000.0, key="comp_c")
        comp_tasa = st.number_input("Tasa Anual (%):", min_value=0.0, value=8.0, step=0.5, key="comp_r")
        comp_tiempo = st.slider("Tiempo (Años):", 1, 20, 10, key="comp_t")
        comp_cap = st.selectbox("Capitalización:", ("Anual", "Semestral", "Trimestral", "Mensual"), key="comp_cap")
    
    with col_config2:
        st.markdown("#### 📊 Resumen de Resultados")
        if comp_capital > 0 and comp_tasa > 0:
            tasa_dec = comp_tasa / 100
            
            # Calcular valores finales
            vf_simple, int_simple = interes_simple_vf(comp_capital, tasa_dec, comp_tiempo)
            vf_compuesto, int_compuesto = interes_compuesto_vf(comp_capital, tasa_dec, comp_tiempo, comp_cap)
            diferencia = vf_compuesto - vf_simple
            
            st.metric("📈 Simple - Valor Final", f"${vf_simple:,.2f}")
            st.metric("🚀 Compuesto - Valor Final", f"${vf_compuesto:,.2f}", delta=f"+${diferencia:,.2f}")
            st.metric("💡 Ventaja del Compuesto", f"${diferencia:,.2f}")
            
            # Porcentaje de ventaja
            if vf_simple > 0:
                ventaja_pct = (diferencia / vf_simple) * 100
                st.success(f"**Ventaja:** {ventaja_pct:.2f}% más rentable")
    
    with col_graph:
        st.markdown("#### 📈 Gráfico Comparativo")
        if comp_capital > 0 and comp_tasa > 0:
            fig = crear_grafico_comparacion(comp_capital, tasa_dec, comp_tiempo, comp_cap)
            st.plotly_chart(fig, use_container_width=True)
    
    # Tabla comparativa detallada
    if comp_capital > 0 and comp_tasa > 0:
        st.markdown("#### 📋 Tabla Comparativa Detallada")
        
        # Crear datos para la tabla
        años = list(range(0, comp_tiempo + 1, max(1, comp_tiempo // 10)))
        datos_tabla = []
        
        for año in años:
            if año == 0:
                simple = compuesto = comp_capital
            else:
                simple, _ = interes_simple_vf(comp_capital, tasa_dec, año)
                compuesto, _ = interes_compuesto_vf(comp_capital, tasa_dec, año, comp_cap)
            
            diferencia = compuesto - simple
            datos_tabla.append({
                "Año": año,
                "Interés Simple": f"${simple:,.2f}",
                "Interés Compuesto": f"${compuesto:,.2f}",
                "Diferencia": f"${diferencia:,.2f}",
                "Ventaja %": f"{(diferencia/simple*100):.2f}%" if simple > 0 else "0.00%"
            })
        
        df = pd.DataFrame(datos_tabla)
        st.dataframe(df, use_container_width=True)

# === PESTAÑA 3: EJEMPLOS PRÁCTICOS ===
with tab3:
    st.markdown('<h2 class="sub-header">Ejemplos Prácticos y Casos de Uso</h2>', unsafe_allow_html=True)
    
    # Ejemplos basados en los documentos proporcionados
    ejemplo_col1, ejemplo_col2 = st.columns(2)
    
    with ejemplo_col1:
        st.markdown("### 🏭 Casos Empresariales")
        
        with st.expander("💼 Financiamiento de Inventario - Salsa de Tomate"):
            st.markdown("**Empresa necesita financiar materia prima**")
            st.markdown("""
            - **Capital:** $10,000
            - **Tasa:** 10% anual  
            - **Tiempo:** 3 meses
            - **Tipo:** Interés Simple
            """)
            
            vf_ej1, int_ej1 = interes_simple_vf(10000, 0.10, 3, "Meses")
            st.success(f"**Interés a pagar:** ${int_ej1:.2f}")
            st.info(f"**Total a devolver:** ${vf_ej1:.2f}")
        
        with st.expander("👟 Importación de Tenis New Balance"):
            st.markdown("**Financiamiento para compra en EE.UU.**")
            st.markdown("""
            - **Capital:** $10,000
            - **Tasa:** 5% anual
            - **Tiempo:** 3 meses  
            - **Tipo:** Interés Simple
            """)
            
            vf_ej2, int_ej2 = interes_simple_vf(10000, 0.05, 3, "Meses")
            st.success(f"**Costo de financiamiento:** ${int_ej2:.2f}")
            st.info(f"**Total a pagar:** ${vf_ej2:.2f}")
        
        with st.expander("📄 Cuentas por Cobrar - Interés por Mora"):
            st.markdown("**Interés sobre facturas vencidas**")
            st.markdown("""
            - **Factura:** $500
            - **Tasa:** 2% mensual
            - **Retraso:** 15 días
            - **Tipo:** Interés Simple
            """)
            
            vf_ej3, int_ej3 = interes_simple_vf(500, 0.02, 15, "Días")
            st.success(f"**Interés por mora:** ${int_ej3:.2f}")
            st.info(f"**Total a cobrar:** ${vf_ej3:.2f}")
    
    with ejemplo_col2:
        st.markdown("### 💰 Casos de Inversión")
        
        with st.expander("📈 Ahorros para Expansión - Interés Compuesto"):
            st.markdown("**Inversión a largo plazo para crecimiento**")
            st.markdown("""
            - **Inversión:** $10,000
            - **Tasa:** 8% anual
            - **Tiempo:** 5 años
            - **Capitalización:** Anual
            """)
            
            vf_ej4, int_ej4 = interes_compuesto_vf(10000, 0.08, 5, "Anual")
            st.success(f"**Valor final:** ${vf_ej4:.2f}")
            st.info(f"**Ganancia total:** ${int_ej4:.2f}")
        
        with st.expander("🏦 Préstamo para Crecimiento"):
            st.markdown("**Préstamo con interés compuesto**")
            st.markdown("""
            - **Préstamo:** $20,000
            - **Tasa:** 5% anual
            - **Tiempo:** 3 años
            - **Capitalización:** Anual
            """)
            
            vf_ej5, int_ej5 = interes_compuesto_vf(20000, 0.05, 3, "Anual")
            st.warning(f"**Total a pagar:** ${vf_ej5:.2f}")
            st.error(f"**Interés total:** ${int_ej5:.2f}")
        
        with st.expander("💡 Valor Presente - Planificación"):
            st.markdown("**¿Cuánto invertir hoy para tener $20,000 en 2 años?**")
            st.markdown("""
            - **Objetivo:** $20,000
            - **Tasa:** 6% anual
            - **Tiempo:** 2 años
            - **Tipo:** Interés Compuesto
            """)
            
            vp_ej6, _ = interes_compuesto_vp(20000, 0.06, 2, "Anual")
            st.success(f"**Inversión necesaria hoy:** ${vp_ej6:.2f}")
    
    # Calculadora rápida integrada
    st.markdown("---")
    st.markdown("### 🧮 Calculadora Rápida")
    
    calc_col1, calc_col2, calc_col3 = st.columns(3)
    
    with calc_col1:
        calc_capital = st.number_input("Capital ($):", value=5000.0, key="calc_c")
        calc_tasa = st.number_input("Tasa (%):", value=7.0, key="calc_r")
    
    with calc_col2:
        calc_tiempo = st.number_input("Tiempo:", value=2.0, key="calc_t")
        calc_unidad = st.selectbox("Unidad:", ("Años", "Meses"), key="calc_u")
    
    with calc_col3:
        if st.button("🚀 Calcular Ambos", type="primary"):
            tasa_d = calc_tasa / 100
            
            # Interés Simple
            vf_s, int_s = interes_simple_vf(calc_capital, tasa_d, calc_tiempo, calc_unidad)
            
            # Interés Compuesto (mensual)
            vf_c, int_c = interes_compuesto_vf(calc_capital, tasa_d, calc_tiempo, "Mensual", calc_unidad)
            
            st.metric("Simple VF", f"${vf_s:,.2f}")
            st.metric("Compuesto VF", f"${vf_c:,.2f}", delta=f"+${vf_c-vf_s:,.2f}")

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p><strong>Calculadora Financiera Completa</strong> | Desarrollada con ❤️ usando Streamlit</p>
    <p><em>Herramienta educativa para cálculos de interés simple y compuesto</em></p>
</div>
""", unsafe_allow_html=True)
