"""
app.py - Calogic Dashboard Principal
Apenas Login e Visão Geral 3D
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine

# Configuração
st.set_page_config(
    page_title="Calogic Insights",
    page_icon="🍋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS
def load_css():
    try:
        with open('style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except:
        pass

load_css()

# Funções de dados
@st.cache_resource
def get_db_connection():
    return create_engine(st.secrets["NEON_DB_URL"])

@st.cache_data(ttl=600)
def load_data():
    engine = get_db_connection()
    df_segments = pd.read_sql("SELECT * FROM customer_segments", engine)
    df_elbow = pd.read_sql("SELECT * FROM elbow_data ORDER BY k", engine)
    return df_segments, df_elbow

# Sistema de autenticação
def check_auth():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        show_login()
        st.stop()

def show_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 3rem 0 2rem 0;">
            <div style="
                background: linear-gradient(135deg, #a3ff12 0%, #8fd610 100%);
                width: 140px;
                height: 140px;
                border-radius: 50%;
                margin: 0 auto 2rem auto;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 15px 50px rgba(163, 255, 18, 0.4);
            ">
                <span style="font-size: 5rem;">🍋</span>
            </div>
            <h1 style="
                font-size: 4.5rem;
                font-weight: 700;
                color: #a3ff12;
                margin: 0;
                text-transform: uppercase;
                letter-spacing: 10px;
                text-shadow: 0 0 30px rgba(163, 255, 18, 0.3);
            ">CALOGIC</h1>
            <p style="
                color: #888;
                font-size: 1.3rem;
                margin-top: 1rem;
                letter-spacing: 3px;
            ">Data-Driven Marketing Intelligence</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login"):
            user = st.text_input("👤 Usuário", placeholder="admin")
            pwd = st.text_input("🔒 Senha", type="password", placeholder="admin123")
            
            if st.form_submit_button("🚀 ENTRAR", use_container_width=True):
                if user == st.secrets["APP_USER"] and pwd == st.secrets["APP_PASSWORD"]:
                    st.session_state.authenticated = True
                    st.session_state.username = user
                    st.rerun()
                else:
                    st.error("❌ Credenciais incorretas!")
        
        st.markdown("""
        <div style="text-align: center; color: #666; margin-top: 2rem;">
            <p>💡 Use: <code>admin</code> / <code>admin123</code></p>
        </div>
        """, unsafe_allow_html=True)

# Página principal
def main():
    check_auth()
    
    # Sidebar
    with st.sidebar:
        st.markdown('<h1 style="color: #a3ff12;">🍋 CALOGIC</h1>', unsafe_allow_html=True)
        st.markdown(f'<p style="color: #888;">Olá, <b>{st.session_state.username}</b></p>', unsafe_allow_html=True)
        st.markdown("---")
        st.info("📊 Navegue pelos clusters usando o menu lateral!")
        st.markdown("---")
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.rerun()
    
    # Carregar dados
    try:
        df, df_elbow = load_data()
    except:
        st.error("❌ Erro ao carregar dados. Execute setup_db.py e ml_engine.py")
        return
    
    # Header
    st.title("🏠 Visão Geral - Dashboard RFM")
    
    # Métricas globais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 Total de Clientes", f"{len(df):,}")
    with col2:
        st.metric("💰 Receita Total", f"R$ {df['monetary'].sum():,.2f}")
    with col3:
        st.metric("🔄 Freq. Média", f"{df['frequency'].mean():.1f}")
    with col4:
        st.metric("📅 Rec. Média", f"{df['recency'].mean():.0f} dias")
    
    st.markdown("---")
    
    # Gráfico 3D e Elbow
    col1, col2 = st.columns([2.5, 1])
    
    with col1:
        st.subheader("🎯 Visualização 3D dos Clusters")
        
        cluster_names = {
            0: "🏆 Campeões",
            1: "💎 Fiéis", 
            2: "⚠️ Em Risco",
            3: "💔 Perdidos"
        }
        
        df['cluster_name'] = df['cluster_id'].map(cluster_names)
        
        fig = px.scatter_3d(
            df, x='recency', y='frequency', z='monetary',
            color='cluster_name',
            color_discrete_map={
                "🏆 Campeões": "#a3ff12",
                "💎 Fiéis": "#00d4ff",
                "⚠️ Em Risco": "#ff9500",
                "💔 Perdidos": "#ff3b30"
            },
            labels={
                'recency': 'Recência (dias)',
                'frequency': 'Frequência', 
                'monetary': 'Valor (R$)',
                'cluster_name': 'Cluster'
            },
            height=650
        )
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff', size=12),
            scene=dict(
                bgcolor='rgba(0,0,0,0)',
                xaxis=dict(backgroundcolor='rgba(0,0,0,0)', gridcolor='#333'),
                yaxis=dict(backgroundcolor='rgba(0,0,0,0)', gridcolor='#333'),
                zaxis=dict(backgroundcolor='rgba(0,0,0,0)', gridcolor='#333')
            ),
            legend=dict(
                bgcolor='rgba(26,26,26,0.9)',
                bordercolor='#a3ff12',
                borderwidth=2
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📈 Método do Cotovelo")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_elbow['k'],
            y=df_elbow['inertia'],
            mode='lines+markers',
            line=dict(color='#a3ff12', width=3),
            marker=dict(size=12, color='#a3ff12', line=dict(color='#0a0a0a', width=2))
        ))
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(26,26,26,0.9)',
            font=dict(color='#ffffff'),
            xaxis=dict(title="Número de Clusters (k)", gridcolor='#333'),
            yaxis=dict(title="Inércia", gridcolor='#333'),
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.success("🎯 k=4 é o ponto ideal!")
        
        # Distribuição
        st.markdown("### 📊 Distribuição")
        
        for cid in sorted(df['cluster_id'].unique()):
            count = len(df[df['cluster_id'] == cid])
            pct = (count / len(df)) * 100
            name = cluster_names[cid]
            
            colors = {0: "#a3ff12", 1: "#00d4ff", 2: "#ff9500", 3: "#ff3b30"}
            
            st.markdown(f"""
            <div style="
                background: rgba(26,26,26,0.8);
                border-left: 4px solid {colors[cid]};
                padding: 0.5rem 1rem;
                margin: 0.5rem 0;
                border-radius: 8px;
            ">
                <b style="color: {colors[cid]};">{name}</b><br>
                <span style="color: #ccc;">{count} ({pct:.1f}%)</span>
            </div>
            """, unsafe_allow_html=True)
    
    # Cards de navegação
    st.markdown("---")
    st.subheader("🔍 Explore cada Cluster")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(163,255,18,0.2), rgba(143,214,16,0.1));
            border: 2px solid #a3ff12;
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
            cursor: pointer;
        ">
            <h1 style="font-size: 4rem; margin: 0;">🏆</h1>
            <h3 style="color: #a3ff12; margin: 0.5rem 0;">Campeões</h3>
            <p style="color: #888; font-size: 0.9rem;">Seus melhores clientes</p>
        </div>
        """, unsafe_allow_html=True)
        st.info("👈 Navegue pelo menu lateral")
    
    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(0,212,255,0.2), rgba(0,169,204,0.1));
            border: 2px solid #00d4ff;
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
        ">
            <h1 style="font-size: 4rem; margin: 0;">💎</h1>
            <h3 style="color: #00d4ff; margin: 0.5rem 0;">Fiéis</h3>
            <p style="color: #888; font-size: 0.9rem;">Clientes leais</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(255,149,0,0.2), rgba(204,119,0,0.1));
            border: 2px solid #ff9500;
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
        ">
            <h1 style="font-size: 4rem; margin: 0;">⚠️</h1>
            <h3 style="color: #ff9500; margin: 0.5rem 0;">Em Risco</h3>
            <p style="color: #888; font-size: 0.9rem;">Precisam de atenção</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(255,59,48,0.2), rgba(204,47,38,0.1));
            border: 2px solid #ff3b30;
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
        ">
            <h1 style="font-size: 4rem; margin: 0;">💔</h1>
            <h3 style="color: #ff3b30; margin: 0.5rem 0;">Perdidos</h3>
            <p style="color: #888; font-size: 0.9rem;">Reativação urgente</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()