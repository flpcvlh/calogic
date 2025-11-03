"""
Página exclusiva do cluster Em Risco
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine

st.set_page_config(page_title="Em Risco | Calogic", page_icon="⚠️", layout="wide")

# Verificar autenticação
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.error("🔒 Faça login na página principal primeiro!")
    st.stop()

# Carregar dados
@st.cache_data(ttl=600)
def load_data():
    engine = create_engine(st.secrets["NEON_DB_URL"])
    df = pd.read_sql("SELECT * FROM customer_segments WHERE cluster_id = 2", engine)
    return df

df = load_data()

# Header
st.markdown("""
<div style="
    background: linear-gradient(135deg, rgba(255,149,0,0.3) 0%, rgba(204,119,0,0.2) 100%);
    border-left: 6px solid #ff9500;
    border-radius: 16px;
    padding: 2.5rem;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(255,149,0,0.3);
">
    <div style="display: flex; align-items: center; gap: 2rem;">
        <div style="font-size: 5rem;">⚠️</div>
        <div>
            <h1 style="color: #ff9500; margin: 0; font-size: 3rem;">EM RISCO</h1>
            <p style="color: #ccc; font-size: 1.3rem; margin: 0.5rem 0 0 0;">
                🚨 ALERTA! Clientes se afastando - Ação imediata necessária!
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Métricas
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("👥 Total", f"{len(df):,}", delta=None, delta_color="inverse")
with col2:
    st.metric("💰 Ticket Médio", f"R$ {df['monetary'].mean():,.2f}")
with col3:
    st.metric("💵 Receita em Risco", f"R$ {df['monetary'].sum():,.2f}", delta=None, delta_color="inverse")
with col4:
    st.metric("🔄 Freq. Média", f"{df['frequency'].mean():.1f}")
with col5:
    st.metric("⏰ Rec. Média", f"{df['recency'].mean():.0f} dias", delta=None, delta_color="inverse")

st.markdown("---")

# DIAGNÓSTICO DE RISCO
st.subheader("🔍 Diagnóstico: Por que estão em Risco?")

rec_avg = df['recency'].mean()
freq_avg = df['frequency'].mean()
mon_avg = df['monetary'].mean()

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown(f"""
    <div style="
        background: rgba(26,26,26,0.8);
        border: 2px solid #ff9500;
        border-radius: 12px;
        padding: 2rem;
    ">
        <h3 style="color: #ff9500;">🚨 Sinais de Alerta</h3>
        <ul style="color: #ccc; line-height: 2;">
            <li><b>Recência ALTA:</b> <b style="color: #ff9500;">{rec_avg:.0f} dias</b> sem comprar</li>
            <li><b>Desengajamento:</b> Perdendo conexão com a marca</li>
            <li><b>Risco de Churn:</b> Podem migrar para concorrentes</li>
            <li><b>Urgência:</b> Janela de recuperação está fechando</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="
        background: rgba(26,26,26,0.8);
        border: 2px solid #ff9500;
        border-radius: 12px;
        padding: 2rem;
    ">
        <h3 style="color: #ff9500;">🎯 Estratégia de Recuperação</h3>
        <ul style="color: #ccc; line-height: 2;">
            <li><b>Winback agressivo:</b> 25-30% de desconto</li>
            <li><b>Urgência:</b> Ofertas com prazo de 48-72h</li>
            <li><b>Personalização:</b> "Sentimos sua falta"</li>
            <li><b>Feedback:</b> Pesquisa de satisfação</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ANÁLISE DA LINHA DO TEMPO
st.subheader("📊 Análise da Linha do Tempo - Por que se afastaram?")

tab1, tab2, tab3 = st.tabs(["⏰ Evolução da Recência", "📉 Declínio de Frequência", "💔 Perda de Valor"])

with tab1:
    st.markdown("#### Quanto tempo faz desde a última compra?")
    st.markdown("*Quanto mais à direita, maior o risco de perda definitiva*")
    
    fig = px.histogram(df, x='recency', nbins=25,
                      title="Distribuição de Recência - Tempo de Inatividade",
                      color_discrete_sequence=['#ff9500'])
    
    fig.add_vline(x=rec_avg, line_dash="dash", line_color="white", line_width=2,
                 annotation_text=f"Média: {rec_avg:.0f}d", annotation_position="top")
    
    # Zonas de risco
    fig.add_vrect(x0=0, x1=90, fillcolor="#ffaa00", opacity=0.1, 
                 annotation_text="Risco Moderado", annotation_position="top left")
    fig.add_vrect(x0=90, x1=180, fillcolor="#ff7700", opacity=0.1,
                 annotation_text="Alto Risco", annotation_position="top left")
    fig.add_vrect(x0=180, x1=500, fillcolor="#ff3b30", opacity=0.1,
                 annotation_text="Risco Crítico", annotation_position="top left")
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,26,26,0.9)',
        font=dict(color='#ffffff'),
        xaxis=dict(title="Dias sem comprar", gridcolor='#333'),
        yaxis=dict(title="Número de clientes", gridcolor='#333'),
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Análise por gravidade
    moderado = len(df[(df['recency'] >= 0) & (df['recency'] < 90)])
    alto_risco = len(df[(df['recency'] >= 90) & (df['recency'] < 180)])
    critico = len(df[df['recency'] >= 180])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("⚠️ Risco Moderado", f"{moderado} ({moderado/len(df)*100:.1f}%)")
        st.caption("< 90 dias")
    with col2:
        st.metric("🔶 Alto Risco", f"{alto_risco} ({alto_risco/len(df)*100:.1f}%)")
        st.caption("90-180 dias")
    with col3:
        st.metric("🚨 Crítico", f"{critico} ({critico/len(df)*100:.1f}%)")
        st.caption("> 180 dias")
    
    if critico > 0:
        st.error(f"🚨 URGENTE: {critico} clientes em risco CRÍTICO! Campanha imediata necessária!")

with tab2:
    st.markdown("#### Frequência em declínio")
    st.markdown("*Compravam antes, mas pararam - por quê?*")
    
    fig = px.histogram(df, x='frequency', nbins=15,
                      title="Histórico de Frequência - Eles já foram ativos",
                      color_discrete_sequence=['#ff9500'])
    
    fig.add_vline(x=freq_avg, line_dash="dash", line_color="white", line_width=2,
                 annotation_text=f"Média: {freq_avg:.1f}", annotation_position="top")
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,26,26,0.9)',
        font=dict(color='#ffffff'),
        xaxis=dict(title="Número de pedidos (histórico)", gridcolor='#333'),
        yaxis=dict(title="Clientes", gridcolor='#333'),
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Insights
    tinha_freq_alta = len(df[df['frequency'] >= 5])
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📊 Frequência Média Anterior", f"{freq_avg:.1f} pedidos")
    with col2:
        st.metric("💔 Tinham boa frequência", f"{tinha_freq_alta} ({tinha_freq_alta/len(df)*100:.1f}%)")
    
    st.warning(f"⚠️ Estes clientes JÁ compraram {freq_avg:.1f} vezes em média. Eles CONHECEM e GOSTAVAM da marca!")
    st.info("💡 Estratégia: Lembrar os benefícios + oferta irresistível para reconquistar")

with tab3:
    st.markdown("#### Valor em Risco de Perda")
    st.markdown("*Receita que pode ser perdida se não agirmos*")
    
    fig = go.Figure()
    
    fig.add_trace(go.Box(
        y=df['monetary'],
        name="Valor",
        marker_color='#ff9500',
        boxmean='sd'
    ))
    
    fig.update_layout(
        title="Distribuição de Valor - Receita em Risco",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,26,26,0.9)',
        font=dict(color='#ffffff'),
        yaxis=dict(title="Valor Total Gasto (R$)", gridcolor='#333'),
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Cálculo de perda potencial
    receita_historica = df['monetary'].sum()
    receita_anual_perdida = receita_historica * 0.30  # Estimativa: 30% de recompra anual
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💰 Valor Histórico", f"R$ {receita_historica:,.2f}")
    with col2:
        st.metric("📉 Perda Anual Estimada", f"R$ {receita_anual_perdida:,.2f}", delta=None, delta_color="inverse")
    with col3:
        st.metric("💵 Ticket Médio", f"R$ {mon_avg:,.2f}")
    
    st.error(f"🚨 Se não agirmos, podemos perder até R$ {receita_anual_perdida:,.2f} em receita anual!")

st.markdown("---")

# MAPA DE URGÊNCIA
st.subheader("🎯 Mapa de Urgência: Recência × Valor")
st.markdown("*Quadrante superior direito = Maior urgência (alto valor + muitos dias inativos)*")

fig = px.scatter(
    df, x='recency', y='monetary', size='frequency',
    color='frequency', color_continuous_scale='Oranges',
    labels={
        'recency': 'Dias Inativo (quanto maior, pior)',
        'monetary': 'Valor Total (R$)',
        'frequency': 'Frequência'
    },
    height=500
)

# Zona de Urgência Máxima
fig.add_shape(
    type="rect",
    x0=150, y0=df['monetary'].quantile(0.75), 
    x1=500, y1=df['monetary'].max() * 1.1,
    line=dict(color="#ff3b30", width=3, dash="dash"),
    fillcolor="rgba(255, 59, 48, 0.15)"
)

fig.add_annotation(
    x=250, y=df['monetary'].quantile(0.85),
    text="🚨 URGÊNCIA MÁXIMA<br>Alto valor + Muito tempo inativo",
    showarrow=False,
    font=dict(color="#ff3b30", size=14, family="Arial Black"),
    bgcolor="rgba(10,10,10,0.9)",
    bordercolor="#ff3b30",
    borderwidth=3
)

fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(26,26,26,0.9)',
    font=dict(color='#ffffff'),
    xaxis=dict(gridcolor='#333'),
    yaxis=dict(gridcolor='#333')
)

st.plotly_chart(fig, use_container_width=True)

urgencia_maxima = len(df[(df['recency'] > 150) & (df['monetary'] > df['monetary'].quantile(0.75))])
st.error(f"🚨 {urgencia_maxima} clientes de ALTO VALOR estão há muito tempo inativos!")

st.markdown("---")

# TOP EM RISCO
st.subheader("🚨 Top 30 Clientes em Maior Risco (por valor)")

df_top = df.nlargest(30, 'monetary').copy()
df_top['rank'] = range(1, len(df_top) + 1)
df_top['nivel_risco'] = df_top['recency'].apply(
    lambda x: "🚨 Crítico" if x >= 180 else "🔶 Alto" if x >= 90 else "⚠️ Moderado"
)
df_top['dias_inativo'] = df_top['recency']
df_top = df_top[['rank', 'customer_id', 'dias_inativo', 'frequency', 'monetary', 'nivel_risco']]
df_top.columns = ['#', 'Cliente', 'Dias Inativo', 'Freq. Anterior', 'Valor (R$)', 'Nível de Risco']

st.dataframe(
    df_top.style.format({'Valor (R$)': 'R$ {:,.2f}'}),
    use_container_width=True,
    height=500
)

st.markdown("---")

# GERADOR DE CAMPANHA WINBACK
st.subheader("🚀 Campanha de Winback Urgente")

if st.button("⚠️ GERAR CAMPANHA DE RECUPERAÇÃO", type="primary", use_container_width=True):
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(255,149,0,0.3), rgba(204,119,0,0.2));
        border: 3px solid #ff9500;
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
    ">
        <h2 style="color: #ff9500; margin: 0 0 1rem 0;">⚠️ CAMPANHA WINBACK - SENTIMOS SUA FALTA</h2>
        <p style="color: #ccc;"><b>Objetivo:</b> Reativar clientes em risco de churn</p>
        <p style="color: #ccc;"><b>Oferta:</b> 25% OFF + Brinde Surpresa + Frete Grátis</p>
        <p style="color: #ccc;"><b>Urgência:</b> 48 HORAS APENAS!</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📧 Email", "💬 WhatsApp", "📱 SMS", "🔔 Push"])
    
    with tab1:
        email_subject = "😢 [NOME], sentimos MUITO sua falta... Volta pra gente?"
        email_body = f"""Olá [NOME],

Notamos que faz tempo que você não está por aqui... 😢
Está tudo bem?

A gente sente MUITO a sua falta e quer muito ter você de volta!

Por isso, preparamos uma oferta ESPECIAL só pra você:

🎁 25% OFF em qualquer pedido
💝 BRINDE SURPRESA no seu pedido
🚚 FRETE GRÁTIS
💬 Nos conte: o que podemos melhorar?

Use o cupom: VOLTAPRAMIM25

⚠️ ATENÇÃO: Válido APENAS por 48 HORAS!
Não deixe essa chance passar!

Queremos você de volta! 💚
Equipe Calogic

PS: Se houver algum problema, por favor nos conte. Queremos melhorar!

---
Urgência: 48h
Alcance: {len(df)} clientes em risco
Receita recuperável: R$ {df['monetary'].sum() * 0.10:,.2f} (estimativa conservadora)
"""
        
        st.code(email_subject, language=None)
        st.text_area("Corpo do Email:", email_body, height=450)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 COPIAR EMAIL", key="copy_email"):
                st.success("✅ Copiado!")
        with col2:
            if st.button("📧 DISPARAR URGENTE PARA " + f"{len(df):,} CLIENTES", key="send_email", type="primary"):
                st.success(f"✅ Campanha URGENTE disparada para {len(df):,} clientes em risco!")
                st.balloons()
    
    with tab2:
        whatsapp = f"""⚠️ Oi [NOME]...

Sentimos MUITA sua falta! 😢

Faz tempo que você não pede...
Está tudo bem?

🎁 Oferta ESPECIAL de volta:
- 25% OFF
- Brinde surpresa 💝
- Frete GRÁTIS
- Nos conte o que melhorar

Cupom: VOLTAPRAMIM25
⏰ Válido SÓ 48 HORAS!

A gente quer você de volta! 💚

Peça agora: [LINK]"""
        
        st.text_area("Mensagem WhatsApp:", whatsapp, height=350)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 COPIAR WHATSAPP", key="copy_wa"):
                st.success("✅ Copiado!")
        with col2:
            if st.button("💬 DISPARAR URGENTE", key="send_wa", type="primary"):
                st.success(f"✅ Disparos urgentes iniciados!")
    
    with tab3:
        sms = "😢 [NOME], sentimos sua falta! 25% OFF + Brinde. VOLTAPRAMIM25. SÓ 48h! Volta: [LINK]"
        
        st.text_area("SMS:", sms, height=100)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 COPIAR SMS", key="copy_sms"):
                st.success("✅ Copiado!")
        with col2:
            if st.button("📱 DISPARAR SMS URGENTE", key="send_sms", type="primary"):
                st.success(f"✅ SMS urgentes enviados!")
    
    with tab4:
        push = "⚠️ Sentimos sua falta! 25% OFF + Brinde. SÓ 48h! Volta pra gente! 💚"
        
        st.text_area("Push Notification:", push, height=80)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 COPIAR PUSH", key="copy_push"):
                st.success("✅ Copiado!")
        with col2:
            if st.button("🔔 DISPARAR PUSH URGENTE", key="send_push", type="primary"):
                st.success(f"✅ Push urgente enviado!")
    
    # ROI
    st.markdown("---")
    st.subheader("📊 ROI Estimado da Campanha de Recuperação")
    
    conversoes = int(len(df) * 0.08)  # 8% conversão (conservador)
    receita_estimada = conversoes * df['monetary'].mean() * 0.75  # 25% desconto
    custo = len(df) * 0.50
    roi = ((receita_estimada - custo) / custo) * 100
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🎯 Taxa Conversão", "8%")
    with col2:
        st.metric("🛒 Reativações", f"{conversoes:,}")
    with col3:
        st.metric("💰 Receita", f"R$ {receita_estimada:,.2f}")
    with col4:
        st.metric("📈 ROI", f"{roi:.0f}%")
    
    st.warning("⚠️ Estimativa conservadora. Taxa real pode ser maior com boa execução!")
    st.info(f"💡 Mesmo com 8% de conversão, recuperamos {conversoes} clientes e R$ {receita_estimada:,.2f}!")