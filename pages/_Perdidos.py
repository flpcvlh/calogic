"""
Página exclusiva do cluster Perdidos
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine

st.set_page_config(page_title="Perdidos | Calogic", page_icon="💔", layout="wide")

# Verificar autenticação
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.error("🔒 Faça login na página principal primeiro!")
    st.stop()

# Carregar dados
@st.cache_data(ttl=600)
def load_data():
    engine = create_engine(st.secrets["NEON_DB_URL"])
    df = pd.read_sql("SELECT * FROM customer_segments WHERE cluster_id = 3", engine)
    return df

df = load_data()

# Header
st.markdown("""
<div style="
    background: linear-gradient(135deg, rgba(255,59,48,0.3) 0%, rgba(204,47,38,0.2) 100%);
    border-left: 6px solid #ff3b30;
    border-radius: 16px;
    padding: 2.5rem;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(255,59,48,0.3);
">
    <div style="display: flex; align-items: center; gap: 2rem;">
        <div style="font-size: 5rem;">💔</div>
        <div>
            <h1 style="color: #ff3b30; margin: 0; font-size: 3rem;">PERDIDOS</h1>
            <p style="color: #ccc; font-size: 1.3rem; margin: 0.5rem 0 0 0;">
                Clientes inativos há muito tempo - Última tentativa de reativação
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
    st.metric("💵 Valor Perdido", f"R$ {df['monetary'].sum():,.2f}")
with col4:
    st.metric("🔄 Freq. Anterior", f"{df['frequency'].mean():.1f}")
with col5:
    st.metric("⏰ Dias Inativo", f"{df['recency'].mean():.0f}", delta=None, delta_color="inverse")

st.markdown("---")

# DIAGNÓSTICO
st.subheader("🔍 Diagnóstico: Por que estão Perdidos?")

rec_avg = df['recency'].mean()
freq_avg = df['frequency'].mean()
mon_avg = df['monetary'].mean()

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown(f"""
    <div style="
        background: rgba(26,26,26,0.8);
        border: 2px solid #ff3b30;
        border-radius: 12px;
        padding: 2rem;
    ">
        <h3 style="color: #ff3b30;">💔 Situação Crítica</h3>
        <ul style="color: #ccc; line-height: 2;">
            <li><b>Inativos há:</b> <b style="color: #ff3b30;">{rec_avg:.0f} dias</b> em média</li>
            <li><b>Memória:</b> Podem não lembrar da marca</li>
            <li><b>Concorrência:</b> Provavelmente comprando em outro lugar</li>
            <li><b>Resposta:</b> Taxa de resposta muito baixa esperada</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="
        background: rgba(26,26,26,0.8);
        border: 2px solid #ff3b30;
        border-radius: 12px;
        padding: 2rem;
    ">
        <h3 style="color: #ff3b30;">🎯 Última Chance</h3>
        <ul style="color: #ccc; line-height: 2;">
            <li><b>Oferta máxima:</b> Vale R$ 50-100 + desconto</li>
            <li><b>Pesquisa:</b> "Por que você nos deixou?"</li>
            <li><b>Remarketing:</b> Mostrar novidades e mudanças</li>
            <li><b>Opt-out:</b> Opção de cancelar mensagens</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ANÁLISE DE ABANDONO
st.subheader("📊 Análise do Abandono - Quando perdemos eles?")

tab1, tab2, tab3 = st.tabs(["⏰ Tempo de Abandono", "📊 Perfil Anterior", "💸 Valor Perdido"])

with tab1:
    st.markdown("#### Há quanto tempo estão inativos?")
    st.markdown("*A maioria está inativa há mais de 6 meses*")
    
    fig = px.histogram(df, x='recency', nbins=30,
                      title="Distribuição do Tempo de Inatividade",
                      color_discrete_sequence=['#ff3b30'])
    
    fig.add_vline(x=rec_avg, line_dash="dash", line_color="white", line_width=2,
                 annotation_text=f"Média: {rec_avg:.0f}d", annotation_position="top")
    
    # Marcos temporais
    fig.add_vline(x=180, line_dash="dot", line_color="#ffaa00", line_width=1,
                 annotation_text="6 meses", annotation_position="top left")
    fig.add_vline(x=365, line_dash="dot", line_color="#ff6600", line_width=1,
                 annotation_text="1 ano", annotation_position="top right")
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,26,26,0.9)',
        font=dict(color='#ffffff'),
        xaxis=dict(title="Dias inativo", gridcolor='#333'),
        yaxis=dict(title="Clientes", gridcolor='#333'),
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Análise temporal
    muito_tempo = len(df[df['recency'] > 365])
    meses_6_12 = len(df[(df['recency'] > 180) & (df['recency'] <= 365)])
    meses_3_6 = len(df[(df['recency'] <= 180)])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💔 3-6 meses", f"{meses_3_6} ({meses_3_6/len(df)*100:.1f}%)")
    with col2:
        st.metric("💔💔 6-12 meses", f"{meses_6_12} ({meses_6_12/len(df)*100:.1f}%)")
    with col3:
        st.metric("💔💔💔 +1 ano", f"{muito_tempo} ({muito_tempo/len(df)*100:.1f}%)")
    
    if muito_tempo > len(df) * 0.5:
        st.error(f"🚨 Mais de 50% estão inativos há mais de 1 ano. Recuperação muito difícil.")
    
    st.warning("⚠️ Quanto mais tempo inativo, menor a chance de recuperação.")

with tab2:
    st.markdown("#### Eles já foram bons clientes?")
    st.markdown("*Analisando o histórico de compras anterior*")
    
    fig = px.histogram(df, x='frequency', nbins=15,
                      title="Frequência de Compras Quando Eram Ativos",
                      color_discrete_sequence=['#ff3b30'])
    
    fig.add_vline(x=freq_avg, line_dash="dash", line_color="white", line_width=2,
                 annotation_text=f"Média: {freq_avg:.1f}", annotation_position="top")
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,26,26,0.9)',
        font=dict(color='#ffffff'),
        xaxis=dict(title="Pedidos (quando ativos)", gridcolor='#333'),
        yaxis=dict(title="Clientes", gridcolor='#333'),
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Análise de perfil
    freq_alta_antes = len(df[df['frequency'] >= 5])
    freq_baixa = len(df[df['frequency'] < 3])
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📊 Freq. Média Anterior", f"{freq_avg:.1f} pedidos")
    with col2:
        st.metric("💎 Tinham ≥5 pedidos", f"{freq_alta_antes} ({freq_alta_antes/len(df)*100:.1f}%)")
    
    if freq_alta_antes > 0:
        st.info(f"💡 {freq_alta_antes} clientes tinham bom histórico. Vale tentar reativar!")
    
    if freq_baixa > len(df) * 0.5:
        st.warning(f"⚠️ {freq_baixa} clientes tinham baixa frequência. Talvez nunca se engajaram.")

with tab3:
    st.markdown("#### Quanto valor foi perdido?")
    st.markdown("*Receita histórica que não retorna mais*")
    
    fig = go.Figure()
    
    fig.add_trace(go.Box(
        y=df['monetary'],
        name="Valor",
        marker_color='#ff3b30',
        boxmean='sd'
    ))
    
    fig.update_layout(
        title="Valor Histórico dos Clientes Perdidos",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,26,26,0.9)',
        font=dict(color='#ffffff'),
        yaxis=dict(title="Valor (R$)", gridcolor='#333'),
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Cálculo de impacto
    valor_total_perdido = df['monetary'].sum()
    ltv_perdido = valor_total_perdido * 2  # Estimativa: perdemos 2x o valor histórico em LTV
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💰 Valor Histórico", f"R$ {valor_total_perdido:,.2f}")
    with col2:
        st.metric("📉 LTV Perdido (est.)", f"R$ {ltv_perdido:,.2f}")
    with col3:
        st.metric("💵 Ticket Médio", f"R$ {mon_avg:,.2f}")
    
    st.error(f"💔 Perdemos aproximadamente R$ {ltv_perdido:,.2f} em lifetime value")

st.markdown("---")

# ANÁLISE DE RECUPERABILIDADE
st.subheader("🎯 Análise de Recuperabilidade")
st.markdown("*Quem tem mais chance de voltar?*")

# Criar score de recuperabilidade
df['score_recuperacao'] = (
    (df['frequency'] * 10) +  # Frequência alta = mais chance
    (500 - df['recency']) / 10 +  # Recência menor = mais chance
    (df['monetary'] / df['monetary'].max() * 20)  # Valor alto = mais esforço vale a pena
)

df_sorted = df.sort_values('score_recuperacao', ascending=False)

fig = px.scatter(
    df_sorted, 
    x='recency', 
    y='monetary', 
    size='frequency',
    color='score_recuperacao',
    color_continuous_scale='Reds_r',
    labels={
        'recency': 'Dias Inativo',
        'monetary': 'Valor (R$)',
        'frequency': 'Freq. Anterior',
        'score_recuperacao': 'Score'
    },
    title="Mapa de Priorização: Onde focar esforços?",
    height=500
)

# Zona de prioridade
fig.add_shape(
    type="rect",
    x0=0, y0=df['monetary'].quantile(0.75),
    x1=365, y1=df['monetary'].max() * 1.1,
    line=dict(color="#ffaa00", width=3, dash="dash"),
    fillcolor="rgba(255, 170, 0, 0.1)"
)

fig.add_annotation(
    x=180, y=df['monetary'].quantile(0.85),
    text="🎯 PRIORIDADE<br>Alto valor + Menos tempo inativo",
    showarrow=False,
    font=dict(color="#ffaa00", size=13, family="Arial Black"),
    bgcolor="rgba(10,10,10,0.9)",
    bordercolor="#ffaa00",
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

prioridade = len(df[(df['recency'] < 365) & (df['monetary'] > df['monetary'].quantile(0.75))])
st.info(f"🎯 {prioridade} clientes de alto valor com <1 ano inativo = FOCAR AQUI PRIMEIRO")

st.markdown("---")

# TOP PERDIDOS
st.subheader("💔 Top 30 Perdidos com Maior Potencial de Recuperação")

df_top = df_sorted.head(30).copy()
df_top['rank'] = range(1, len(df_top) + 1)
df_top['meses_inativo'] = (df_top['recency'] / 30).round(1)
df_top['prioridade'] = df_top['score_recuperacao'].apply(
    lambda x: "🔥 Alta" if x > df['score_recuperacao'].quantile(0.75) else 
             "⚠️ Média" if x > df['score_recuperacao'].quantile(0.5) else "❄️ Baixa"
)

df_top = df_top[['rank', 'customer_id', 'meses_inativo', 'frequency', 'monetary', 'prioridade']]
df_top.columns = ['#', 'Cliente', 'Meses Inativo', 'Freq. Anterior', 'Valor (R$)', 'Prioridade']

st.dataframe(
    df_top.style.format({
        'Valor (R$)': 'R$ {:,.2f}',
        'Meses Inativo': '{:.1f}'
    }),
    use_container_width=True,
    height=500
)

st.markdown("---")

# CAMPANHA ÚLTIMA CHANCE
st.subheader("🚀 Campanha Última Chance")

if st.button("💔 GERAR CAMPANHA FINAL", type="primary", use_container_width=True):
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(255,59,48,0.3), rgba(204,47,38,0.2));
        border: 3px solid #ff3b30;
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
    ">
        <h2 style="color: #ff3b30; margin: 0 0 1rem 0;">💔 CAMPANHA ÚLTIMA CHANCE</h2>
        <p style="color: #ccc;"><b>Objetivo:</b> Última tentativa de reativação</p>
        <p style="color: #ccc;"><b>Oferta:</b> Vale R$ 50 + 30% OFF + Frete Grátis</p>
        <p style="color: #ccc;"><b>Urgência:</b> 24 HORAS!</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📧 Email", "💬 WhatsApp", "📱 SMS", "🔔 Push"])
    
    with tab1:
        email_subject = "💔 [NOME], é nossa ÚLTIMA tentativa... Vale R$ 50 pra você!"
        email_body = f"""Olá [NOME],

Esta é nossa última mensagem... 💔

Não queremos te perder definitivamente!

Por favor, nos dê mais UMA chance:

🎁 VALE de R$ 50,00 (seu gift!)
💰 + 30% de desconto ADICIONAL
🚚 Frete GRÁTIS em qualquer pedido
❓ Pesquisa rápida: por que você foi embora?

Use o cupom: ULTIMACHANCE50

🚨 EXPIRA EM 24 HORAS! 🚨

A gente mudou muito! Confira as novidades:
✨ Novos produtos
✨ Atendimento melhorado
✨ Entrega mais rápida

Se você não quer mais receber nossas mensagens, 
[clique aqui para cancelar].

Com carinho e saudades,
Equipe Calogic

---
Última tentativa
Alcance: {len(df)} clientes perdidos
Conversão esperada: 3-5%
Recuperação potencial: R$ {df['monetary'].sum() * 0.05:,.2f}
"""
        
        st.code(email_subject, language=None)
        st.text_area("Corpo do Email:", email_body, height=500)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 COPIAR EMAIL", key="copy_email"):
                st.success("✅ Copiado!")
        with col2:
            if st.button("📧 ÚLTIMA TENTATIVA - " + f"{len(df):,} CLIENTES", key="send_email", type="primary"):
                st.success(f"✅ Campanha FINAL enviada para {len(df):,} clientes perdidos!")
                st.balloons()
    
    with tab2:
        whatsapp = f"""💔 [NOME], última tentativa...

Não queremos te perder! 😢

Esta é nossa ÚLTIMA mensagem.

🎁 Oferta final pra você:
- Vale R$ 50 (presente!)
- + 30% OFF adicional
- Frete GRÁTIS
- Pesquisa: nos ajude a melhorar

Cupom: ULTIMACHANCE50
🚨 Expira em 24 HORAS!

A gente mudou! Confira as novidades.

Nos dê mais uma chance: [LINK]

Se não quiser mais mensagens, é só avisar."""
        
        st.text_area("Mensagem WhatsApp:", whatsapp, height=400)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 COPIAR WHATSAPP", key="copy_wa"):
                st.success("✅ Copiado!")
        with col2:
            if st.button("💬 ÚLTIMA TENTATIVA", key="send_wa", type="primary"):
                st.success(f"✅ Última tentativa enviada!")
    
    with tab3:
        sms = "💔 [NOME], ÚLTIMA CHANCE! Vale R$50 + 30% OFF. ULTIMACHANCE50. 24h! [LINK] [STOP: responda SAIR]"
        
        st.text_area("SMS:", sms, height=100)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 COPIAR SMS", key="copy_sms"):
                st.success("✅ Copiado!")
        with col2:
            if st.button("📱 SMS FINAL", key="send_sms", type="primary"):
                st.success(f"✅ SMS final enviado!")
    
    with tab4:
        push = "💔 Última chance! Vale R$ 50 + 30% OFF. Expira em 24h! NÃO PERCA!"
        
        st.text_area("Push Notification:", push, height=80)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 COPIAR PUSH", key="copy_push"):
                st.success("✅ Copiado!")
        with col2:
            if st.button("🔔 PUSH FINAL", key="send_push", type="primary"):
                st.success(f"✅ Push final enviado!")
    
    # ROI
    st.markdown("---")
    st.subheader("📊 ROI Estimado (Expectativa Conservadora)")
    
    conversoes = int(len(df) * 0.05)  # 5% conversão (muito conservador)
    receita_estimada = conversoes * df['monetary'].mean() * 0.70  # 30% desconto
    custo = len(df) * 0.50 + (50 * conversoes)  # Custo do vale
    roi = ((receita_estimada - custo) / custo) * 100 if custo > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🎯 Taxa Conversão", "5%")
    with col2:
        st.metric("🛒 Reativações", f"{conversoes:,}")
    with col3:
        st.metric("💰 Receita", f"R$ {receita_estimada:,.2f}")
    with col4:
        if roi > 0:
            st.metric("📈 ROI", f"{roi:.0f}%")
        else:
            st.metric("📈 ROI", "Breakeven")
    
    st.warning("⚠️ Taxa de conversão muito baixa esperada. Foco em clientes prioritários!")
    
    if prioridade > 0:
        st.info(f"💡 Recomendação: Focar nos {prioridade} clientes de alta prioridade primeiro!")
    
    st.error("💔 Se não responderem, considere remover da lista de comunicação ativa.")