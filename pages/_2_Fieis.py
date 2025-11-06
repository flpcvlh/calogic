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
                Clientes leais com bom histórico - Base sólida do negócio!
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
        <h3 style="color: #00d4ff;">🎯 Oportunidades de Crescimento</h3>
        <ul style="color: #ccc; line-height: 2;">
            <li><b>Frequência:</b> Incentivar mais pedidos</li>
            <li><b>Ticket:</b> Aumentar valor médio</li>
            <li><b>Cross-sell:</b> Novos produtos</li>
            <li><b>Fidelização:</b> Reforçar lealdade</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# GRÁFICOS DIAGNÓSTICOS
st.subheader("📊 Análise de Oportunidades")

tab1, tab2, tab3 = st.tabs(["📅 Análise de Recência", "🔄 Análise de Frequência", "💰 Análise de Valor"])

with tab1:
    st.markdown("#### Distribuição da Recência - Identificando Padrões")
    st.markdown("*Clientes Fiéis mantêm uma recência estável e moderada*")
    
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
        line=dict(color='#00d4ff', width=4, shape='spline'),
        fill='tozeroy',
        fillcolor='rgba(0, 212, 255, 0.3)'
    ))
    
    # Linha da média
    fig.add_vline(
        x=rec_avg, 
        line_dash="dash", 
        line_color="white", 
        line_width=3,
        annotation_text=f"Média: {rec_avg:.0f} dias",
        annotation_position="top right",
        annotation=dict(font_size=14, bgcolor="rgba(0,212,255,0.8)", font_color="black")
    )
    
    # Área de atenção
    fig.add_vline(x=120, line_dash="dot", line_color="#ff9500", line_width=2,
                 annotation_text="⚠️ Zona de Alerta", annotation_position="bottom right")
    
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
    
    # Análise de risco
    em_risco = len(df[df['recency'] > 120])
    ativos = len(df[df['recency'] <= 60])
    moderados = len(df[(df['recency'] > 60) & (df['recency'] <= 120)])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("✅ Ativos (<60d)", f"{ativos}", f"{ativos/len(df)*100:.1f}%")
    with col2:
        st.metric("⚠️ Moderados (60-120d)", f"{moderados}", f"{moderados/len(df)*100:.1f}%")
    with col3:
        if em_risco > 0:
            st.metric("🚨 Em Risco (>120d)", f"{em_risco}", f"{em_risco/len(df)*100:.1f}%")
            st.warning(f"⚠️ {em_risco} clientes precisam de reativação!")
        else:
            st.success("✅ Nenhum em risco!")

with tab2:
    st.markdown("#### Distribuição da Frequência - Potencial de Crescimento")
    st.markdown("*Analisando quantas vezes cada cliente compra*")
    
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
        line=dict(color='#00d4ff', width=4, shape='spline'),
        marker=dict(size=8, color='#00d4ff', line=dict(color='#0a0a0a', width=2)),
        fill='tozeroy',
        fillcolor='rgba(0, 212, 255, 0.3)'
    ))
    
    # Linha da média
    fig.add_vline(
        x=freq_avg,
        line_dash="dash",
        line_color="white",
        line_width=3,
        annotation_text=f"Média: {freq_avg:.1f}",
        annotation_position="top right",
        annotation=dict(font_size=14, bgcolor="rgba(0,212,255,0.8)", font_color="black")
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
    
    # Análise de potencial
    alta_freq = len(df[df['frequency'] >= 8])
    baixa_freq = len(df[df['frequency'] < 5])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🔥 Alta Frequência (8+)", f"{alta_freq}", f"{alta_freq/len(df)*100:.1f}%")
    with col2:
        st.metric("📊 Frequência Média", f"{freq_avg:.1f} pedidos")
    with col3:
        st.metric("💡 Baixa Frequência (<5)", f"{baixa_freq}", f"{baixa_freq/len(df)*100:.1f}%")
    
    if alta_freq > 0:
        st.success(f"🎯 {alta_freq} clientes já têm alta frequência!")
        st.info("💡 Estratégia: Programa de pontos dobrados para aumentar ainda mais")

with tab3:
    st.markdown("#### Distribuição de Valor - Análise da Contribuição")
    st.markdown("*Visualização do valor total gasto por cliente*")
    
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
        line=dict(color='#00d4ff', width=4, shape='spline'),
        fill='tozeroy',
        fillcolor='rgba(0, 212, 255, 0.3)'
    ))
    
    # Linha da média
    fig.add_vline(
        x=mon_avg,
        line_dash="dash",
        line_color="white",
        line_width=3,
        annotation_text=f"Média: R$ {mon_avg:,.0f}",
        annotation_position="top left",
        annotation=dict(font_size=14, bgcolor="rgba(0,212,255,0.8)", font_color="black")
    )
    
    # Top 25% (alto valor)
    top_25_value = df['monetary'].quantile(0.75)
    fig.add_vrect(
        x0=top_25_value, x1=df['monetary'].max(),
        fillcolor="rgba(0, 212, 255, 0.15)",
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
    
    # Análise de valor
    alto_valor = len(df[df['monetary'] > df['monetary'].quantile(0.75)])
    medio_valor = len(df[(df['monetary'] > df['monetary'].quantile(0.25)) & 
                         (df['monetary'] <= df['monetary'].quantile(0.75))])
    baixo_valor = len(df[df['monetary'] <= df['monetary'].quantile(0.25)])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💎 Alto Valor", f"{alto_valor}", f"{alto_valor/len(df)*100:.1f}%")
    with col2:
        st.metric("💰 Médio Valor", f"{medio_valor}", f"{medio_valor/len(df)*100:.1f}%")
    with col3:
        st.metric("💵 Baixo Valor", f"{baixo_valor}", f"{baixo_valor/len(df)*100:.1f}%")

st.markdown("---")

# MAPA DE OPORTUNIDADES - CORRIGIDO
st.subheader("🎯 Mapa de Oportunidades: Recência × Frequência")
st.markdown("*Visualização do comportamento dos clientes Fiéis*")

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

# Calcular limites dinâmicos baseados nos dados reais
rec_p25 = df['recency'].quantile(0.25)  # 25% menores recências
freq_p75 = df['frequency'].quantile(0.75)  # 25% maiores frequências

# Zona de Oportunidade (adaptada aos dados reais)
fig.add_shape(
    type="rect",
    x0=0, y0=freq_p75, x1=rec_p25, y1=df['frequency'].max() + 1,
    line=dict(color="#00d4ff", width=3, dash="dash"),
    fillcolor="rgba(0, 212, 255, 0.15)"
)

fig.add_annotation(
    x=rec_p25/2, y=freq_p75 + (df['frequency'].max() - freq_p75)/2,
    text="💎 MELHOR DESEMPENHO<br>Baixa recência + Alta frequência",
    showarrow=False,
    font=dict(color="#00d4ff", size=13, family="Arial Black"),
    bgcolor="rgba(10,10,10,0.9)",
    bordercolor="#00d4ff",
    borderwidth=2
)

# Zona de Atenção
fig.add_shape(
    type="rect",
    x0=df['recency'].quantile(0.75), y0=0, 
    x1=df['recency'].max(), y1=df['frequency'].quantile(0.25),
    line=dict(color="#ff9500", width=2, dash="dot"),
    fillcolor="rgba(255, 149, 0, 0.1)"
)

fig.add_annotation(
    x=df['recency'].quantile(0.85), y=df['frequency'].quantile(0.15),
    text="⚠️ ATENÇÃO<br>Risco de churn",
    showarrow=False,
    font=dict(color="#ff9500", size=11),
    bgcolor="rgba(10,10,10,0.8)",
    bordercolor="#ff9500",
    borderwidth=1
)

fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(26,26,26,0.9)',
    font=dict(color='#ffffff'),
    xaxis=dict(gridcolor='#333'),
    yaxis=dict(gridcolor='#333')
)

st.plotly_chart(fig, use_container_width=True)

# Análise dinâmica
clientes_melhor_desempenho = len(df[(df['recency'] <= rec_p25) & (df['frequency'] >= freq_p75)])
clientes_atencao = len(df[(df['recency'] >= df['recency'].quantile(0.75)) & 
                          (df['frequency'] <= df['frequency'].quantile(0.25))])

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("💎 Melhor Desempenho", f"{clientes_melhor_desempenho}", 
             f"{clientes_melhor_desempenho/len(df)*100:.1f}%")
    st.caption("Baixa recência + Alta frequência")
with col2:
    st.metric("📊 Desempenho Médio", f"{len(df) - clientes_melhor_desempenho - clientes_atencao}",
             f"{(len(df) - clientes_melhor_desempenho - clientes_atencao)/len(df)*100:.1f}%")
    st.caption("Comportamento estável")
with col3:
    st.metric("⚠️ Requer Atenção", f"{clientes_atencao}",
             f"{clientes_atencao/len(df)*100:.1f}%")
    st.caption("Alta recência + Baixa frequência")

if clientes_melhor_desempenho > 0:
    st.success(f"💎 {clientes_melhor_desempenho} clientes Fiéis têm excelente desempenho!")
if clientes_atencao > 0:
    st.warning(f"⚠️ {clientes_atencao} clientes precisam de campanhas de reengajamento")

st.markdown("---")

# TOP CLIENTES
st.subheader("🌟 Top 30 Fiéis por Valor")

df_top = df.nlargest(30, 'monetary').copy()
df_top['rank'] = range(1, len(df_top) + 1)
df_top['status_freq'] = df_top['frequency'].apply(
    lambda x: "🔥 Alta Freq." if x >= 8 else "📊 Boa Freq." if x >= 5 else "💡 Crescer"
)
df_top = df_top[['rank', 'customer_id', 'recency', 'frequency', 'monetary', 'status_freq']]
df_top.columns = ['#', 'Cliente', 'Recência (dias)', 'Frequência', 'Valor (R$)', 'Status']

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
Clientes com melhor desempenho: {clientes_melhor_desempenho}
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
st.subheader("📊 ROI Estimado da Campanha de Upgrade")

conversoes = int(len(df) * 0.18)  # 18% conversão
ticket_medio = df['monetary'].mean() / df['frequency'].mean() if df['frequency'].mean() > 0 else 180

# CUSTOS
custo_disparo = len(df) * 0.50
custo_desconto = conversoes * ticket_medio * 0.15  # 15% desconto
custo_pontos = conversoes * 10  # Custo fixo de pontos R$ 10
custo_total = custo_disparo + custo_desconto + custo_pontos

# RECEITA
receita_bruta = conversoes * ticket_medio
margem_liquida = 0.60
receita_liquida = receita_bruta * margem_liquida

# LUCRO
lucro = receita_liquida - custo_total
roi = (lucro / custo_total) * 100 if custo_total > 0 else 0

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("🎯 Taxa Conversão", "18%")
with col2:
    st.metric("🛒 Conversões", f"{conversoes:,}")
with col3:
    st.metric("💰 Receita Líquida", f"R$ {receita_liquida:,.2f}")
with col4:
    st.metric("💵 Lucro", f"R$ {lucro:,.2f}", delta=f"+{roi:.0f}%")
with col5:
    st.metric("📈 ROI", f"{roi:.0f}%")

with st.expander("📊 Ver Detalhamento"):
    st.markdown(f"""
    ### 💸 Investimento: R$ {custo_total:,.2f}
    
    - 📧 Disparo: R$ {custo_disparo:,.2f}
    - 💰 Desconto 15%: R$ {custo_desconto:,.2f}
    - ⭐ Pontos em dobro: R$ {custo_pontos:,.2f}
    
    ### 💰 Retorno: R$ {receita_liquida:,.2f}
    
    - Vendas: R$ {receita_bruta:,.2f}
    - Margem 60%: R$ {receita_liquida:,.2f}
    
    ### 📈 Lucro: R$ {lucro:,.2f}
    
    **ROI: {roi:.1f}%** | Retorno: R$ {(receita_liquida/custo_total) if custo_total > 0 else 0:.2f} por R$ 1
    """)

if roi > 80:
    st.success(f"🎉 ROI EXCELENTE de {roi:.0f}%! Campanha altamente recomendada!")
elif roi > 40:
    st.success(f"✅ ROI muito bom de {roi:.0f}%!")
elif roi > 0:
    st.info(f"📊 ROI positivo de {roi:.0f}%.")
else:
    st.warning("⚠️ ROI negativo. Ajustar oferta.")

st.success(f"💎 Campanha focada em manter {len(df)} clientes Fiéis engajados e aumentar frequência!")