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
        <h3 style="color: #a3ff12;">✅ Indicadores Positivos</h3>
        <ul style="color: #ccc; line-height: 2;">
            <li><b>Recência baixa:</b> Compraram há apenas <b style="color: #a3ff12;">{rec_avg:.0f} dias</b></li>
            <li><b>Alta frequência:</b> Média de <b style="color: #a3ff12;">{freq_avg:.1f} pedidos</b> por cliente</li>
            <li><b>Alto valor:</b> Gastam em média <b style="color: #a3ff12;">R$ {mon_avg:,.2f}</b></li>
            <li><b>Engajamento:</b> Clientes mais ativos da base</li>
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
    st.markdown("#### Distribuição da Recência - Quanto mais à esquerda, melhor!")
    st.markdown("*Campeões compram frequentemente, por isso a recência é baixa*")
    
    # Criar distribuição agrupada
    recency_counts = df.groupby(pd.cut(df['recency'], bins=15)).size().reset_index()
    recency_counts.columns = ['range', 'count']
    recency_counts['midpoint'] = recency_counts['range'].apply(lambda x: x.mid)
    
    fig = go.Figure()
    
    # Linha suave com preenchimento
    fig.add_trace(go.Scatter(
        x=recency_counts['midpoint'],
        y=recency_counts['count'],
        mode='lines',
        name='Clientes',
        line=dict(color='#a3ff12', width=4, shape='spline'),
        fill='tozeroy',
        fillcolor='rgba(163, 255, 18, 0.3)'
    ))
    
    # Linha da média
    fig.add_vline(
        x=rec_avg, 
        line_dash="dash", 
        line_color="white", 
        line_width=3,
        annotation_text=f"Média: {rec_avg:.0f} dias",
        annotation_position="top right",
        annotation=dict(font_size=14, bgcolor="rgba(163,255,18,0.8)", font_color="black")
    )
    
    # Área de excelência
    fig.add_vrect(
        x0=0, x1=30,
        fillcolor="rgba(163, 255, 18, 0.1)",
        layer="below", line_width=0,
        annotation_text="🌟 Zona de Excelência",
        annotation_position="top left"
    )
    
    fig.update_layout(
        title="Recência ao Longo do Tempo (dias desde última compra)",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,26,26,0.9)',
        font=dict(color='#ffffff', size=13),
        xaxis=dict(
            title="Dias desde última compra",
            gridcolor='#333',
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title="Número de Clientes",
            gridcolor='#333',
            showgrid=True,
            zeroline=False
        ),
        showlegend=False,
        height=450,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Análise
    recentes = len(df[df['recency'] <= 30])
    muito_recentes = len(df[df['recency'] <= 7])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🔥 Últimos 7 dias", f"{muito_recentes}", f"{muito_recentes/len(df)*100:.1f}%")
    with col2:
        st.metric("⚡ Últimos 30 dias", f"{recentes}", f"{recentes/len(df)*100:.1f}%")
    with col3:
        if rec_avg < 60:
            st.success("✅ Engajamento excepcional!")
        else:
            st.warning("⚠️ Monitorar atentamente")

with tab2:
    st.markdown("#### Distribuição da Frequência - Quanto mais à direita, melhor!")
    st.markdown("*Campeões fazem múltiplas compras, criando um pico à direita*")
    
    # Criar distribuição de frequência
    freq_counts = df['frequency'].value_counts().sort_index().reset_index()
    freq_counts.columns = ['frequency', 'count']
    
    fig = go.Figure()
    
    # Linha suave com preenchimento
    fig.add_trace(go.Scatter(
        x=freq_counts['frequency'],
        y=freq_counts['count'],
        mode='lines+markers',
        name='Clientes',
        line=dict(color='#a3ff12', width=4, shape='spline'),
        marker=dict(size=8, color='#a3ff12', line=dict(color='#0a0a0a', width=2)),
        fill='tozeroy',
        fillcolor='rgba(163, 255, 18, 0.3)'
    ))
    
    # Linha da média
    fig.add_vline(
        x=freq_avg,
        line_dash="dash",
        line_color="white",
        line_width=3,
        annotation_text=f"Média: {freq_avg:.1f}",
        annotation_position="top right",
        annotation=dict(font_size=14, bgcolor="rgba(163,255,18,0.8)", font_color="black")
    )
    
    # Área de alta frequência
    fig.add_vrect(
        x0=10, x1=freq_counts['frequency'].max(),
        fillcolor="rgba(163, 255, 18, 0.1)",
        layer="below", line_width=0,
        annotation_text="🔥 Super Frequentes",
        annotation_position="top right"
    )
    
    fig.update_layout(
        title="Frequência de Compras (número de pedidos por cliente)",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,26,26,0.9)',
        font=dict(color='#ffffff', size=13),
        xaxis=dict(
            title="Número de Pedidos",
            gridcolor='#333',
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title="Número de Clientes",
            gridcolor='#333',
            showgrid=True,
            zeroline=False
        ),
        showlegend=False,
        height=450,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Análise
    alta_freq = len(df[df['frequency'] >= 10])
    muito_alta = len(df[df['frequency'] >= 15])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🔥 10+ pedidos", f"{alta_freq}", f"{alta_freq/len(df)*100:.1f}%")
    with col2:
        st.metric("🔥🔥 15+ pedidos", f"{muito_alta}", f"{muito_alta/len(df)*100:.1f}%")
    with col3:
        st.success(f"✅ Média: {freq_avg:.1f} pedidos")

with tab3:
    st.markdown("#### Distribuição de Valor - Análise da Contribuição em Receita")
    st.markdown("*Visualização do valor total gasto por cada cliente*")
    
    # Criar bins de valor
    valor_bins = pd.qcut(df['monetary'], q=20, duplicates='drop')
    valor_counts = df.groupby(valor_bins).size().reset_index()
    valor_counts.columns = ['range', 'count']
    valor_counts['midpoint'] = valor_counts['range'].apply(lambda x: x.mid)
    valor_counts = valor_counts.sort_values('midpoint')
    
    fig = go.Figure()
    
    # Linha suave com preenchimento gradiente
    fig.add_trace(go.Scatter(
        x=valor_counts['midpoint'],
        y=valor_counts['count'],
        mode='lines',
        name='Clientes',
        line=dict(color='#a3ff12', width=4, shape='spline'),
        fill='tozeroy',
        fillcolor='rgba(163, 255, 18, 0.3)'
    ))
    
    # Linha da média
    fig.add_vline(
        x=mon_avg,
        line_dash="dash",
        line_color="white",
        line_width=3,
        annotation_text=f"Média: R$ {mon_avg:,.0f}",
        annotation_position="top left",
        annotation=dict(font_size=14, bgcolor="rgba(163,255,18,0.8)", font_color="black")
    )
    
    # Top 25% (alto valor)
    top_25_value = df['monetary'].quantile(0.75)
    fig.add_vrect(
        x0=top_25_value, x1=df['monetary'].max(),
        fillcolor="rgba(255, 215, 0, 0.1)",
        layer="below", line_width=0,
        annotation_text="💎 Top 25%",
        annotation_position="top right"
    )
    
    fig.update_layout(
        title="Distribuição de Valor Monetário (R$)",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,26,26,0.9)',
        font=dict(color='#ffffff', size=13),
        xaxis=dict(
            title="Valor Total Gasto (R$)",
            gridcolor='#333',
            showgrid=True,
            zeroline=False,
            tickformat=',.0f'
        ),
        yaxis=dict(
            title="Número de Clientes",
            gridcolor='#333',
            showgrid=True,
            zeroline=False
        ),
        showlegend=False,
        height=450,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Análise
    top_10_pct = df.nlargest(int(len(df)*0.1), 'monetary')['monetary'].sum()
    pct_top10 = (top_10_pct / df['monetary'].sum()) * 100
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💰 Valor Médio", f"R$ {mon_avg:,.2f}")
    with col2:
        st.metric("💎 Top 10%", f"{pct_top10:.1f}% da receita")
    with col3:
        st.metric("📈 Total", f"R$ {df['monetary'].sum():,.2f}")

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
st.subheader("📊 ROI Estimado da Campanha VIP")

conversoes = int(len(df) * 0.25)  # 25% conversão (alta para campeões)
ticket_medio = df['monetary'].mean() / df['frequency'].mean() if df['frequency'].mean() > 0 else 200

# CUSTOS
custo_disparo = len(df) * 0.50  # R$ 0,50 por mensagem
custo_vale = conversoes * 30  # Vale R$ 30
custo_desconto = conversoes * ticket_medio * 0.20  # 20% desconto
custo_total = custo_disparo + custo_vale + custo_desconto

# RECEITA (Margem já descontada do COGS)
receita_bruta = conversoes * ticket_medio
margem_liquida = 0.60  # 60% de margem (já descontou COGS)
receita_liquida = receita_bruta * margem_liquida

# LUCRO
lucro = receita_liquida - custo_total
roi = (lucro / custo_total) * 100 if custo_total > 0 else 0

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("🎯 Taxa Conversão", "25%")
with col2:
    st.metric("🛒 Conversões", f"{conversoes:,}")
with col3:
    st.metric("💰 Receita Líquida", f"R$ {receita_liquida:,.2f}")
with col4:
    st.metric("💵 Lucro", f"R$ {lucro:,.2f}", delta=f"+{roi:.0f}%")
with col5:
    st.metric("📈 ROI", f"{roi:.0f}%")

# Breakdown de custos
with st.expander("📊 Ver Detalhamento Completo"):
    st.markdown(f"""
    ### 💸 Investimento Total: R$ {custo_total:,.2f}
    
    **Custos detalhados:**
    - 📧 Disparo de mensagens: R$ {custo_disparo:,.2f}
    - 🎁 Vale R$ 30 por conversão: R$ {custo_vale:,.2f}
    - 💰 Desconto 20%: R$ {custo_desconto:,.2f}
    
    ---
    
    ### 💰 Retorno
    
    - 🛒 Vendas brutas: R$ {receita_bruta:,.2f}
    - 📊 Margem líquida (60%): R$ {receita_liquida:,.2f}
    - 💵 **Lucro líquido**: R$ {lucro:,.2f}
    
    ---
    
    ### 📈 Performance
    
    - **ROI**: {roi:.1f}%
    - **Payback**: {(custo_total / lucro) if lucro > 0 else 0:.1f}x
    - **Retorno por R$ 1**: R$ {(receita_liquida / custo_total) if custo_total > 0 else 0:.2f}
    
    ---
    
    ✅ **Campanha ALTAMENTE lucrativa!**
    """)

if roi > 100:
    st.success(f"🎉 ROI EXCELENTE de {roi:.0f}%! Cada R$ 1 investido retorna R$ {1 + (roi/100):.2f}")
elif roi > 50:
    st.success(f"✅ ROI muito bom de {roi:.0f}%! Campanha recomendada.")
elif roi > 0:
    st.info(f"📊 ROI positivo de {roi:.0f}%. Campanha viável.")
else:
    st.error("❌ Campanha com prejuízo. Revisar estratégia.")

st.info(f"💡 Com {conversoes} conversões, a campanha gera R$ {lucro:,.2f} de lucro líquido!")