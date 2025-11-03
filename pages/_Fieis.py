"""
Página exclusiva do cluster Fiéis
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine

st.set_page_config(page_title="Fiéis | Calogic", page_icon="💎", layout="wide")

# Verificar autenticação
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.error("🔒 Faça login na página principal primeiro!")
    st.stop()

# Carregar dados
@st.cache_data(ttl=600)
def load_data():
    engine = create_engine(st.secrets["NEON_DB_URL"])
    df = pd.read_sql("SELECT * FROM customer_segments WHERE cluster_id = 1", engine)
    return df

df = load_data()

# Header
st.markdown("""
<div style="
    background: linear-gradient(135deg, rgba(0,212,255,0.3) 0%, rgba(0,169,204,0.2) 100%);
    border-left: 6px solid #00d4ff;
    border-radius: 16px;
    padding: 2.5rem;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(0,212,255,0.2);
">
    <div style="display: flex; align-items: center; gap: 2rem;">
        <div style="font-size: 5rem;">💎</div>
        <div>
            <h1 style="color: #00d4ff; margin: 0; font-size: 3rem;">FIÉIS</h1>
            <p style="color: #ccc; font-size: 1.3rem; margin: 0.5rem 0 0 0;">
                Clientes leais com bom histórico - Potencial para virar Campeões!
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Métricas
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("👥 Total", f"{len(df):,}")
with col2:
    st.metric("💰 Ticket Médio", f"R$ {df['monetary'].mean():,.2f}")
with col3:
    st.metric("💵 Receita Total", f"R$ {df['monetary'].sum():,.2f}")
with col4:
    st.metric("🔄 Freq. Média", f"{df['frequency'].mean():.1f}")
with col5:
    st.metric("📅 Rec. Média", f"{df['recency'].mean():.0f} dias")

st.markdown("---")

# DIAGNÓSTICO
st.subheader("🔬 Diagnóstico: Por que são Fiéis?")

rec_avg = df['recency'].mean()
freq_avg = df['frequency'].mean()
mon_avg = df['monetary'].mean()

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown(f"""
    <div style="
        background: rgba(26,26,26,0.8);
        border: 2px solid #00d4ff;
        border-radius: 12px;
        padding: 2rem;
    ">
        <h3 style="color: #00d4ff;">✅ Características</h3>
        <ul style="color: #ccc; line-height: 2;">
            <li><b>Recência:</b> Moderada - <b style="color: #00d4ff;">{rec_avg:.0f} dias</b></li>
            <li><b>Frequência:</b> Boa - <b style="color: #00d4ff;">{freq_avg:.1f} pedidos</b></li>
            <li><b>Ticket:</b> Satisfatório - <b style="color: #00d4ff;">R$ {mon_avg:,.2f}</b></li>
            <li><b>Status:</b> Relacionamento estável e duradouro</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="
        background: rgba(26,26,26,0.8);
        border: 2px solid #00d4ff;
        border-radius: 12px;
        padding: 2rem;
    ">
        <h3 style="color: #00d4ff;">🎯 Oportunidades de Upgrade</h3>
        <ul style="color: #ccc; line-height: 2;">
            <li><b>Frequência:</b> Incentivar mais pedidos</li>
            <li><b>Ticket:</b> Aumentar valor médio</li>
            <li><b>Cross-sell:</b> Novos produtos</li>
            <li><b>Objetivo:</b> Transformar em Campeões</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# GRÁFICOS DIAGNÓSTICOS
st.subheader("📊 Análise de Oportunidades")

tab1, tab2, tab3 = st.tabs(["📅 Análise de Recência", "🔄 Potencial de Frequência", "💰 Crescimento de Valor"])

with tab1:
    st.markdown("#### Onde estão os riscos de churn?")
    st.markdown("*Clientes com recência alta precisam de atenção*")
    
    fig = px.histogram(df, x='recency', nbins=25,
                      title="Distribuição de Recência - Identificando Riscos",
                      color_discrete_sequence=['#00d4ff'])
    
    fig.add_vline(x=rec_avg, line_dash="dash", line_color="white", line_width=2,
                 annotation_text=f"Média: {rec_avg:.0f}d", annotation_position="top")
    
    # Linha de alerta (120 dias)
    fig.add_vline(x=120, line_dash="dot", line_color="#ff9500", line_width=2,
                 annotation_text="Zona de Risco", annotation_position="bottom")
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,26,26,0.9)',
        font=dict(color='#ffffff'),
        xaxis=dict(title="Dias desde última compra", gridcolor='#333'),
        yaxis=dict(title="Número de clientes", gridcolor='#333'),
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Análise de risco
    em_risco = len(df[df['recency'] > 120])
    ativos = len(df[df['recency'] <= 60])
    moderados = len(df[(df['recency'] > 60) & (df['recency'] <= 120)])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("✅ Ativos (<60d)", f"{ativos} ({ativos/len(df)*100:.1f}%)")
    with col2:
        st.metric("⚠️ Moderados (60-120d)", f"{moderados} ({moderados/len(df)*100:.1f}%)")
    with col3:
        if em_risco > 0:
            st.metric("🚨 Em Risco (>120d)", f"{em_risco} ({em_risco/len(df)*100:.1f}%)")
            st.warning(f"⚠️ {em_risco} clientes precisam de campanha de reativação!")
        else:
            st.success("✅ Nenhum cliente em risco!")

with tab2:
    st.markdown("#### Quem pode comprar mais vezes?")
    st.markdown("*Meta: Aumentar para 10+ pedidos para virar Campeões*")
    
    fig = px.histogram(df, x='frequency', nbins=20,
                      title="Distribuição de Frequência - Potencial de Crescimento",
                      color_discrete_sequence=['#00d4ff'])
    
    fig.add_vline(x=freq_avg, line_dash="dash", line_color="white", line_width=2,
                 annotation_text=f"Atual: {freq_avg:.1f}", annotation_position="top")
    
    # Meta de Campeões
    fig.add_vline(x=10, line_dash="dot", line_color="#a3ff12", line_width=2,
                 annotation_text="Meta: 10+", annotation_position="bottom")
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,26,26,0.9)',
        font=dict(color='#ffffff'),
        xaxis=dict(title="Número de pedidos", gridcolor='#333'),
        yaxis=dict(title="Número de clientes", gridcolor='#333'),
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Análise de potencial
    proximos_campeoes = len(df[(df['frequency'] >= 8) & (df['recency'] < 60)])
    baixa_freq = len(df[df['frequency'] < 5])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🎯 Próximos de Campeões", f"{proximos_campeoes} ({proximos_campeoes/len(df)*100:.1f}%)")
    with col2:
        st.metric("📊 Frequência Média", f"{freq_avg:.1f} pedidos")
    with col3:
        st.metric("💡 Baixa Frequência (<5)", f"{baixa_freq} ({baixa_freq/len(df)*100:.1f}%)")
    
    if proximos_campeoes > 0:
        st.success(f"🎯 {proximos_campeoes} clientes estão próximos de virar Campeões!")
        st.info("💡 Estratégia: Programa de pontos dobrados para incentivar frequência")

with tab3:
    st.markdown("#### Distribuição de Valor - Onde crescer?")
    st.markdown("*Oportunidade de upsell e cross-sell*")
    
    fig = go.Figure()
    
    fig.add_trace(go.Box(
        y=df['monetary'],
        name="Valor",
        marker_color='#00d4ff',
        boxmean='sd'
    ))
    
    fig.update_layout(
        title="Análise de Valor Monetário",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,26,26,0.9)',
        font=dict(color='#ffffff'),
        yaxis=dict(title="Valor Total Gasto (R$)", gridcolor='#333'),
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Análise de valor
    alto_valor = len(df[df['monetary'] > df['monetary'].quantile(0.75)])
    medio_valor = len(df[(df['monetary'] > df['monetary'].quantile(0.25)) & 
                         (df['monetary'] <= df['monetary'].quantile(0.75))])
    baixo_valor = len(df[df['monetary'] <= df['monetary'].quantile(0.25)])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💎 Alto Valor", f"{alto_valor} ({alto_valor/len(df)*100:.1f}%)")
    with col2:
        st.metric("💰 Médio Valor", f"{medio_valor} ({medio_valor/len(df)*100:.1f}%)")
    with col3:
        st.metric("💵 Baixo Valor", f"{baixo_valor} ({baixo_valor/len(df)*100:.1f}%)")

st.markdown("---")

# MAPA DE OPORTUNIDADES
st.subheader("🎯 Mapa de Oportunidades: Recência × Frequência")
st.markdown("*Clientes na zona verde têm maior potencial de virar Campeões*")

fig = px.scatter(
    df, x='recency', y='frequency', size='monetary',
    color='monetary', color_continuous_scale='Blues',
    labels={
        'recency': 'Recência (dias)',
        'frequency': 'Frequência (pedidos)',
        'monetary': 'Valor (R$)'
    },
    height=500
)

# Zona de Oportunidade (Campeões em potencial)
fig.add_shape(
    type="rect",
    x0=0, y0=8, x1=60, y1=20,
    line=dict(color="#a3ff12", width=3, dash="dash"),
    fillcolor="rgba(163, 255, 18, 0.1)"
)

fig.add_annotation(
    x=30, y=14,
    text="🎯 ZONA CAMPEÕES<br>Alta frequência + Recência baixa",
    showarrow=False,
    font=dict(color="#a3ff12", size=14, family="Arial Black"),
    bgcolor="rgba(10,10,10,0.8)",
    bordercolor="#a3ff12",
    borderwidth=2
)

fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(26,26,26,0.9)',
    font=dict(color='#ffffff'),
    xaxis=dict(gridcolor='#333'),
    yaxis=dict(gridcolor='#333')
)

st.plotly_chart(fig, use_container_width=True)

potenciais = len(df[(df['recency'] < 60) & (df['frequency'] >= 8)])
st.success(f"🎯 {potenciais} clientes estão na ZONA CAMPEÕES e podem ser promovidos!")

st.markdown("---")

# TOP CLIENTES
st.subheader("🌟 Top 30 Fiéis por Valor")

df_top = df.nlargest(30, 'monetary').copy()
df_top['rank'] = range(1, len(df_top) + 1)
df_top['potencial'] = df_top.apply(
    lambda x: "🎯 Potencial Campeão" if (x['recency'] < 60 and x['frequency'] >= 8) else "💎 Fiel",
    axis=1
)
df_top = df_top[['rank', 'customer_id', 'recency', 'frequency', 'monetary', 'potencial']]
df_top.columns = ['#', 'Cliente', 'Recência', 'Frequência', 'Valor (R$)', 'Status']

st.dataframe(
    df_top.style.format({'Valor (R$)': 'R$ {:,.2f}'}),
    use_container_width=True,
    height=500
)

st.markdown("---")

# GERADOR DE CAMPANHA
st.subheader("🚀 Campanha de Upgrade para Fiéis")

if st.button("✨ GERAR CAMPANHA DIAMANTE", type="primary", use_container_width=True):
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(0,212,255,0.2), rgba(0,169,204,0.1));
        border: 3px solid #00d4ff;
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
    ">
        <h2 style="color: #00d4ff; margin: 0 0 1rem 0;">💎 CAMPANHA CLIENTE DIAMANTE</h2>
        <p style="color: #ccc;"><b>Objetivo:</b> Aumentar frequência e ticket médio</p>
        <p style="color: #ccc;"><b>Oferta:</b> 15% OFF + Pontos em Dobro</p>
        <p style="color: #ccc;"><b>Urgência:</b> Válido por 5 dias</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📧 Email", "💬 WhatsApp", "📱 SMS", "🔔 Push"])
    
    with tab1:
        email_subject = "💎 Você é um Cliente Diamante! Pontos em Dobro + 15% OFF"
        email_body = f"""Olá [NOME],

Que alegria ter você conosco! 💎

Você é um cliente especial e merece recompensas exclusivas:

🎯 15% de desconto no próximo pedido
⭐ PONTOS EM DOBRO (acumule mais rápido!)
🎁 Brinde surpresa no seu próximo pedido
💚 Programa de fidelidade premium

Use o cupom: DIAMANTE15

Válido até: [DATA +5 dias]

Quanto mais você pede, mais benefícios você ganha!
Continue sendo incrível! 💙

Equipe Calogic

---
Alcance: {len(df)} clientes Fiéis
Potencial de upgrade para Campeões: {potenciais} clientes
Receita estimada: R$ {df['monetary'].sum() * 0.20:,.2f}
"""
        
        st.code(email_subject, language=None)
        st.text_area("Corpo do Email:", email_body, height=400)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 COPIAR EMAIL", key="copy_email"):
                st.success("✅ Copiado!")
        with col2:
            if st.button("📧 DISPARAR PARA " + f"{len(df):,} CLIENTES", key="send_email", type="primary"):
                st.success(f"✅ Campanha enviada para {len(df):,} Fiéis!")
                st.balloons()
    
    with tab2:
        whatsapp = f"""💎 Oi [NOME]!

Cliente especial = Benefícios especiais! 

🎁 Seu presente:
- 15% OFF
- Pontos em DOBRO ⭐⭐
- Brinde surpresa
- Programa fidelidade

Cupom: DIAMANTE15
Válido: 5 dias

Quanto mais você pede, mais você ganha! 💙

Aproveite: [LINK]"""
        
        st.text_area("Mensagem WhatsApp:", whatsapp, height=300)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 COPIAR WHATSAPP", key="copy_wa"):
                st.success("✅ Copiado!")
        with col2:
            if st.button("💬 DISPARAR VIA WHATSAPP", key="send_wa", type="primary"):
                st.success(f"✅ Enviando para {len(df):,} Fiéis!")
    
    with tab3:
        sms = "💎 [NOME], você é Diamante! 15% OFF + Pontos em Dobro. Use: DIAMANTE15. 5 dias! [LINK]"
        
        st.text_area("SMS:", sms, height=100)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 COPIAR SMS", key="copy_sms"):
                st.success("✅ Copiado!")
        with col2:
            if st.button("📱 DISPARAR SMS", key="send_sms", type="primary"):
                st.success(f"✅ SMS para {len(df):,} Fiéis!")
    
    with tab4:
        push = "💎 Pontos em DOBRO + 15% OFF! Seu presente de cliente Diamante. Toque aqui!"
        
        st.text_area("Push Notification:", push, height=80)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 COPIAR PUSH", key="copy_push"):
                st.success("✅ Copiado!")
        with col2:
            if st.button("🔔 DISPARAR PUSH", key="send_push", type="primary"):
                st.success(f"✅ Notificações enviadas!")
    
    # ROI
    st.markdown("---")
    st.subheader("📊 ROI Estimado da Campanha")
    
    conversoes = int(len(df) * 0.15)  # 15% conversão
    receita_estimada = conversoes * df['monetary'].mean() * 0.85  # 15% desconto
    custo = len(df) * 0.50
    roi = ((receita_estimada - custo) / custo) * 100
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🎯 Taxa Conversão", "15%")
    with col2:
        st.metric("🛒 Conversões", f"{conversoes:,}")
    with col3:
        st.metric("💰 Receita", f"R$ {receita_estimada:,.2f}")
    with col4:
        st.metric("📈 ROI", f"{roi:.0f}%")
    
    st.info(f"💡 Foco: {potenciais} clientes têm potencial de virar Campeões com esta campanha!")