"""
Página exclusiva do cluster Campeões
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine

st.set_page_config(page_title="Campeões | Calogic", page_icon="🏆", layout="wide")

# Verificar autenticação
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.error("🔒 Faça login na página principal primeiro!")
    st.stop()

# Carregar dados
@st.cache_data(ttl=600)
def load_data():
    engine = create_engine(st.secrets["NEON_DB_URL"])
    df = pd.read_sql("SELECT * FROM customer_segments WHERE cluster_id = 0", engine)
    return df

df = load_data()

# Header
st.markdown("""
<div style="
    background: linear-gradient(135deg, rgba(163,255,18,0.3) 0%, rgba(143,214,16,0.2) 100%);
    border-left: 6px solid #a3ff12;
    border-radius: 16px;
    padding: 2.5rem;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(163,255,18,0.2);
">
    <div style="display: flex; align-items: center; gap: 2rem;">
        <div style="font-size: 5rem;">🏆</div>
        <div>
            <h1 style="color: #a3ff12; margin: 0; font-size: 3rem;">CAMPEÕES</h1>
            <p style="color: #ccc; font-size: 1.3rem; margin: 0.5rem 0 0 0;">
                Seus clientes mais valiosos - Alta frequência, alto valor e ativos!
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
st.subheader("🔬 Diagnóstico: Por que são Campeões?")

rec_avg = df['recency'].mean()
freq_avg = df['frequency'].mean()
mon_avg = df['monetary'].mean()

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown(f"""
    <div style="
        background: rgba(26,26,26,0.8);
        border: 2px solid #a3ff12;
        border-radius: 12px;
        padding: 2rem;
    ">
        <h3 style="color: #a3ff12;">✅ Características Positivas</h3>
        <ul style="color: #ccc; line-height: 2;">
            <li><b>Recência:</b> Compraram há apenas <b style="color: #a3ff12;">{rec_avg:.0f} dias</b></li>
            <li><b>Frequência:</b> Média de <b style="color: #a3ff12;">{freq_avg:.1f} pedidos</b> por cliente</li>
            <li><b>Ticket:</b> Gastam em média <b style="color: #a3ff12;">R$ {mon_avg:,.2f}</b></li>
            <li><b>Status:</b> Clientes mais engajados da base</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="
        background: rgba(26,26,26,0.8);
        border: 2px solid #a3ff12;
        border-radius: 12px;
        padding: 2rem;
    ">
        <h3 style="color: #a3ff12;">🎯 Estratégia Recomendada</h3>
        <ul style="color: #ccc; line-height: 2;">
            <li><b>Retenção:</b> Manter satisfação sempre alta</li>
            <li><b>Programa VIP:</b> Benefícios exclusivos premium</li>
            <li><b>Upsell:</b> Oferecer produtos de maior valor</li>
            <li><b>Advocacy:</b> Transformar em promotores da marca</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# GRÁFICOS DIAGNÓSTICOS
st.subheader("📊 Análise Visual Detalhada")

tab1, tab2, tab3 = st.tabs(["📅 Análise de Recência", "🔄 Análise de Frequência", "💰 Análise de Valor"])

with tab1:
    st.markdown("#### Por que a recência está baixa?")
    st.markdown("*Clientes que compraram recentemente estão mais engajados*")
    
    fig = px.histogram(df, x='recency', nbins=25, 
                      title="Distribuição de Recência (dias desde última compra)",
                      color_discrete_sequence=['#a3ff12'])
    
    fig.add_vline(x=rec_avg, line_dash="dash", line_color="white", line_width=2,
                 annotation_text=f"Média: {rec_avg:.0f}d", annotation_position="top")
    
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
    
    # Análise
    recentes = len(df[df['recency'] <= 30])
    muito_recentes = len(df[df['recency'] <= 7])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📅 Últimos 7 dias", f"{muito_recentes} ({muito_recentes/len(df)*100:.1f}%)")
    with col2:
        st.metric("📅 Últimos 30 dias", f"{recentes} ({recentes/len(df)*100:.1f}%)")
    with col3:
        if rec_avg < 60:
            st.success("✅ Excelente engajamento!")
        else:
            st.warning("⚠️ Monitorar clientes inativos")

with tab2:
    st.markdown("#### Por que a frequência está alta?")
    st.markdown("*Clientes que compram mais vezes são mais leais*")
    
    fig = px.histogram(df, x='frequency', nbins=20,
                      title="Distribuição de Frequência de Compras",
                      color_discrete_sequence=['#a3ff12'])
    
    fig.add_vline(x=freq_avg, line_dash="dash", line_color="white", line_width=2,
                 annotation_text=f"Média: {freq_avg:.1f}", annotation_position="top")
    
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
    
    # Análise
    alta_freq = len(df[df['frequency'] >= 10])
    muito_alta = len(df[df['frequency'] >= 15])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🔥 10+ pedidos", f"{alta_freq} ({alta_freq/len(df)*100:.1f}%)")
    with col2:
        st.metric("🔥🔥 15+ pedidos", f"{muito_alta} ({muito_alta/len(df)*100:.1f}%)")
    with col3:
        st.success(f"✅ Frequência média: {freq_avg:.1f} pedidos")

with tab3:
    st.markdown("#### Distribuição de Valor Gasto")
    st.markdown("*Análise do quanto cada cliente contribui em receita*")
    
    fig = go.Figure()
    
    fig.add_trace(go.Box(
        y=df['monetary'],
        name="Valor",
        marker_color='#a3ff12',
        boxmean='sd'
    ))
    
    fig.update_layout(
        title="Distribuição de Valor Monetário (R$)",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,26,26,0.9)',
        font=dict(color='#ffffff'),
        yaxis=dict(title="Valor Total Gasto (R$)", gridcolor='#333'),
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Análise
    top_10_pct = df.nlargest(int(len(df)*0.1), 'monetary')['monetary'].sum()
    pct_top10 = (top_10_pct / df['monetary'].sum()) * 100
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💰 Valor Médio", f"R$ {mon_avg:,.2f}")
    with col2:
        st.metric("💎 Top 10% geram", f"{pct_top10:.1f}% da receita")
    with col3:
        st.metric("📈 Total do cluster", f"R$ {df['monetary'].sum():,.2f}")

st.markdown("---")

# TOP CLIENTES
st.subheader("🌟 Top 30 Campeões por Valor")

df_top = df.nlargest(30, 'monetary').copy()
df_top['rank'] = range(1, len(df_top) + 1)
df_top = df_top[['rank', 'customer_id', 'recency', 'frequency', 'monetary']]
df_top.columns = ['#', 'Cliente', 'Recência (dias)', 'Frequência', 'Valor Total (R$)']

st.dataframe(
    df_top.style.format({'Valor Total (R$)': 'R$ {:,.2f}'}),
    use_container_width=True,
    height=500
)

st.markdown("---")

# GERADOR DE CAMPANHA
st.subheader("🚀 Campanha Exclusiva para Campeões")

if st.button("✨ GERAR CAMPANHA PROGRAMA VIP", type="primary", use_container_width=True):
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(163,255,18,0.2), rgba(143,214,16,0.1));
        border: 3px solid #a3ff12;
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
    ">
        <h2 style="color: #a3ff12; margin: 0 0 1rem 0;">🏆 PROGRAMA VIP EXCLUSIVO</h2>
        <p style="color: #ccc;"><b>Objetivo:</b> Manter engajamento máximo e aumentar lifetime value</p>
        <p style="color: #ccc;"><b>Oferta:</b> Benefícios VIP Exclusivos + 20% OFF + Acesso Antecipado</p>
        <p style="color: #ccc;"><b>Urgência:</b> Válido por 7 dias</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📧 Email", "💬 WhatsApp", "📱 SMS", "🔔 Push"])
    
    with tab1:
        email_subject = "🏆 Bem-vindo ao Programa VIP! Seus Benefícios Exclusivos"
        email_body = f"""Olá [NOME],

É com muito orgulho que te convidamos para o nosso PROGRAMA VIP EXCLUSIVO! 🏆

Você foi selecionado por ser um dos nossos clientes mais especiais e valiosos.

🌟 SEUS BENEFÍCIOS VIP:

✨ 20% de desconto permanente em TODO o cardápio
🚚 Frete GRÁTIS em todos os pedidos
🎯 Acesso ANTECIPADO aos novos lançamentos (você vê primeiro!)
💎 Atendimento prioritário VIP dedicado
🎁 Brindes exclusivos em datas especiais
⭐ Pontos de fidelidade em TRIPLO

Use o cupom VIP: VIP20EXCLUSIVO

Este benefício é PERMANENTE enquanto você continuar sendo nosso VIP!

Você faz toda a diferença para nós! 💚
Continue sendo incrível!

Com carinho,
Equipe Calogic

---
Programa VIP Exclusivo
Alcance: {len(df)} Campeões selecionados
Impacto esperado: +30% em frequência e ticket
Receita incremental estimada: R$ {df['monetary'].sum() * 0.30:,.2f}
"""
        
        st.code(email_subject, language=None)
        st.text_area("Corpo do Email:", email_body, height=450)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 COPIAR EMAIL", key="copy_email"):
                st.success("✅ Copiado!")
        with col2:
            if st.button("📧 DISPARAR PARA " + f"{len(df):,} CAMPEÕES VIP", key="send_email", type="primary"):
                st.success(f"✅ Programa VIP ativado para {len(df):,} Campeões!")
                st.balloons()
    
    with tab2:
        whatsapp = f"""🏆 Olá [NOME]!

VOCÊ É VIP AGORA! 💚

Bem-vindo ao nosso Programa VIP Exclusivo!

🌟 Seus benefícios:
- 20% OFF permanente
- Frete GRÁTIS sempre
- Acesso antecipado
- Atendimento VIP
- Pontos em TRIPLO
- Brindes exclusivos

Cupom VIP: VIP20EXCLUSIVO

Benefício PERMANENTE! 🎯

Você merece! 💎

Aproveite: [LINK]"""
        
        st.text_area("Mensagem WhatsApp:", whatsapp, height=350)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 COPIAR WHATSAPP", key="copy_wa"):
                st.success("✅ Copiado!")
        with col2:
            if st.button("💬 DISPARAR CONVITE VIP", key="send_wa", type="primary"):
                st.success(f"✅ Convites VIP enviados!")
    
    with tab3:
        sms = "🏆 [NOME], você é VIP! 20% OFF permanente + Frete Grátis sempre. VIP20EXCLUSIVO. Benefício vitalício! [LINK]"
        
        st.text_area("SMS:", sms, height=100)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 COPIAR SMS", key="copy_sms"):
                st.success("✅ Copiado!")
        with col2:
            if st.button("📱 DISPARAR SMS VIP", key="send_sms", type="primary"):
                st.success(f"✅ SMS VIP enviados!")
    
    with tab4:
        push = "🏆 Você é VIP agora! 20% OFF permanente + benefícios exclusivos. Toque para conhecer!"
        
        st.text_area("Push Notification:", push, height=80)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 COPIAR PUSH", key="copy_push"):
                st.success("✅ Copiado!")
        with col2:
            if st.button("🔔 DISPARAR PUSH VIP", key="send_push", type="primary"):
                st.success(f"✅ Notificação VIP enviada!")
    
    # ROI
    st.markdown("---")
    st.subheader("📊 Impacto Esperado do Programa VIP")
    
    # Campeões têm alta taxa de engajamento
    aumento_frequencia = 0.30  # 30% mais compras
    aumento_ticket = 0.20  # 20% mais valor por pedido
    
    receita_atual = df['monetary'].sum()
    receita_incremental = receita_atual * (aumento_frequencia + aumento_ticket)
    custo_desconto = receita_incremental * 0.20  # 20% de desconto
    custo_operacional = len(df) * 12  # R$ 12/cliente/ano em custos VIP
    custo_total = custo_desconto + custo_operacional
    receita_liquida = receita_incremental - custo_total
    roi = (receita_liquida / custo_total) * 100
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📈 Aumento Frequência", "+30%")
    with col2:
        st.metric("💰 Aumento Ticket", "+20%")
    with col3:
        st.metric("💵 Receita Incremental", f"R$ {receita_incremental:,.2f}")
    with col4:
        st.metric("📊 ROI Líquido", f"{roi:.0f}%")
    
    st.success("🎯 Programa VIP mantém seus melhores clientes engajados e aumenta seu valor vitalício!")
    st.info(f"💡 Com apenas {len(df)} Campeões gerando R$ {receita_atual:,.2f}, o potencial é de +R$ {receita_liquida:,.2f} líquidos!")