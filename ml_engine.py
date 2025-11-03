"""
ml_engine.py - Motor de Machine Learning para Segmentação RFM
Calcula métricas RFM, aplica K-Means e salva resultados
Execute uma vez após o setup_db.py
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from pathlib import Path
from datetime import datetime

def load_secrets():
    """Carrega as credenciais do arquivo secrets.toml"""
    secrets_path = Path('.streamlit/secrets.toml')
    
    if not secrets_path.exists():
        raise FileNotFoundError(
            "❌ Arquivo .streamlit/secrets.toml não encontrado!\n"
            "Certifique-se de criar o arquivo com a string de conexão NEON_DB_URL"
        )
    
    secrets = {}
    with open(secrets_path, 'r') as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                secrets[key] = value
    
    return secrets

def calculate_rfm_and_segment():
    """Calcula RFM e executa clusterização K-Means"""
    
    print("🧠 Iniciando Motor de ML - Segmentação RFM...")
    
    # Carregar credenciais
    try:
        secrets = load_secrets()
        db_url = secrets.get('NEON_DB_URL')
        if not db_url:
            raise ValueError("NEON_DB_URL não encontrado no secrets.toml")
        print("✅ Credenciais carregadas do secrets.toml")
    except Exception as e:
        print(f"❌ Erro ao carregar credenciais: {e}")
        return
    
    # Conexão com o banco
    try:
        engine = create_engine(db_url)
        print("✅ Conexão com Neon estabelecida!")
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return
    
    # Ler dados do banco (apenas pedidos concluídos)
    query = """
    SELECT 
        customer,
        created_at,
        total_amount,
        status
    FROM orders
    WHERE status = 'CONCLUDED'
    """
    
    try:
        df = pd.read_sql(query, engine)
        print(f"✅ {len(df)} pedidos CONCLUDED carregados")
        print(f"📊 Clientes únicos: {df['customer'].nunique()}")
        
        # DEBUG: Mostrar amostra dos dados
        print(f"\n🔍 Amostra dos dados carregados:")
        print(df.head())
        print(f"\n📊 Tipos de dados:")
        print(df.dtypes)
        
    except Exception as e:
        print(f"❌ Erro ao ler dados: {e}")
        print("💡 Certifique-se de que executou 'python setup_db.py' primeiro")
        return
    
    # Converter data
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
    
    # Tratar total_amount - pode estar como string ou ter vírgula como decimal
    print("\n🔧 Tratando coluna total_amount...")
    
    # Se for string, substituir vírgula por ponto
    if df['total_amount'].dtype == 'object':
        print("  ⚠️  total_amount é string, convertendo...")
        df['total_amount'] = df['total_amount'].astype(str).str.replace(',', '.', regex=False)
    
    # Converter para numérico
    df['total_amount'] = pd.to_numeric(df['total_amount'], errors='coerce')
    
    print(f"  📊 Valores não-nulos: {df['total_amount'].notna().sum()}")
    print(f"  ❌ Valores nulos: {df['total_amount'].isna().sum()}")
    print(f"  📈 Valores > 0: {(df['total_amount'] > 0).sum()}")
    
    # Se todos os valores forem nulos, há um problema no CSV
    if df['total_amount'].isna().all():
        print("\n❌ ERRO: Todos os valores de total_amount são nulos!")
        print("💡 Verifique o formato do CSV. Execute: python debug_csv.py")
        return
    
    # Remover linhas com total_amount nulo ou zero
    df_original = len(df)
    df = df[df['total_amount'].notna() & (df['total_amount'] > 0)]
    print(f"✅ Após limpeza: {len(df)} pedidos válidos (removidos {df_original - len(df)})")
    
    if len(df) == 0:
        print("\n❌ ERRO: Nenhum pedido válido após limpeza!")
        print("💡 Verifique o arquivo CSV e execute novamente o setup_db.py")
        return
    
    # Data de referência (última compra + 1 dia)
    reference_date = df['created_at'].max() + pd.Timedelta(days=1)
    print(f"📅 Data de referência: {reference_date}")
    
    # Calcular RFM
    print("\n📊 Calculando métricas RFM...")
    rfm = df.groupby('customer').agg({
        'created_at': lambda x: (reference_date - x.max()).days,  # Recency
        'status': 'count',  # Frequency
        'total_amount': 'sum'  # Monetary
    }).reset_index()
    
    rfm.columns = ['customer', 'recency', 'frequency', 'monetary']
    
    # Remover qualquer linha com valores nulos
    rfm_original_count = len(rfm)
    rfm = rfm.dropna()
    
    if len(rfm) < rfm_original_count:
        print(f"⚠️  {rfm_original_count - len(rfm)} clientes removidos por dados incompletos")
    
    print(f"✅ RFM calculado para {len(rfm)} clientes")
    
    if len(rfm) == 0:
        print("\n❌ ERRO: Nenhum cliente após cálculo RFM!")
        return
    
    # Estatísticas RFM
    print("\n📊 Estatísticas RFM:")
    print(rfm[['recency', 'frequency', 'monetary']].describe())
    
    # Preparar dados para clustering
    X = rfm[['recency', 'frequency', 'monetary']].values
    
    # Normalização
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    print("\n✅ Dados normalizados com StandardScaler")
    
    # Elbow Method (para justificar k=4)
    inertias = []
    K_range = range(2, min(11, len(rfm)))  # Garantir que k não seja maior que n_samples
    
    print("\n📈 Calculando Elbow Method...")
    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X_scaled)
        inertias.append(kmeans.inertia_)
        print(f"  k={k}: inertia={kmeans.inertia_:.2f}")
    
    # Salvar dados do Elbow para o app
    elbow_df = pd.DataFrame({'k': list(K_range), 'inertia': inertias})
    
    # K-Means com k=4 (ou menos se não houver clientes suficientes)
    k_clusters = min(4, len(rfm) - 1)
    print(f"\n🎯 Executando K-Means com k={k_clusters}...")
    kmeans = KMeans(n_clusters=k_clusters, random_state=42, n_init=10)
    rfm['cluster'] = kmeans.fit_predict(X_scaled)
    
    print("✅ Clusterização concluída!")
    print(f"\n📊 Distribuição dos clusters:")
    print(rfm['cluster'].value_counts().sort_index())
    
    # Análise dos clusters
    print("\n📊 Perfil dos Clusters:")
    cluster_profile = rfm.groupby('cluster').agg({
        'recency': 'mean',
        'frequency': 'mean',
        'monetary': 'mean'
    }).round(2)
    cluster_profile['count'] = rfm.groupby('cluster').size()
    print(cluster_profile)
    
    # Criar tabela de segmentos no banco
    with engine.connect() as conn:
        # Drop table if exists
        print("\n🗑️  Removendo tabela antiga 'customer_segments' (se existir)...")
        conn.execute(text("DROP TABLE IF EXISTS customer_segments"))
        conn.commit()
        
        # Criar tabela
        print("📦 Criando tabela 'customer_segments'...")
        create_table_query = """
        CREATE TABLE customer_segments (
            customer_id VARCHAR(100) PRIMARY KEY,
            recency INT,
            frequency INT,
            monetary DECIMAL(10, 2),
            cluster_id INT
        )
        """
        conn.execute(text(create_table_query))
        conn.commit()
        print("✅ Tabela 'customer_segments' criada")
    
    # Salvar resultados
    rfm_to_save = rfm[['customer', 'recency', 'frequency', 'monetary', 'cluster']].copy()
    rfm_to_save.columns = ['customer_id', 'recency', 'frequency', 'monetary', 'cluster_id']
    
    print(f"\n💾 Salvando {len(rfm_to_save)} segmentos...")
    rfm_to_save.to_sql('customer_segments', engine, if_exists='append', index=False)
    print(f"✅ {len(rfm_to_save)} segmentos salvos na tabela 'customer_segments'!")
    
    # Salvar dados do Elbow
    with engine.connect() as conn:
        print("\n🗑️  Removendo tabela antiga 'elbow_data' (se existir)...")
        conn.execute(text("DROP TABLE IF EXISTS elbow_data"))
        conn.commit()
        
        print("📦 Criando tabela 'elbow_data'...")
        create_elbow_query = """
        CREATE TABLE elbow_data (
            k INT,
            inertia DECIMAL(10, 2)
        )
        """
        conn.execute(text(create_elbow_query))
        conn.commit()
    
    print("💾 Salvando dados do Elbow Method...")
    elbow_df.to_sql('elbow_data', engine, if_exists='append', index=False)
    print("✅ Dados do Elbow Method salvos!")
    
    print("\n" + "="*60)
    print("🎉 SEGMENTAÇÃO CONCLUÍDA COM SUCESSO!")
    print("="*60)
    print("\n💡 Próximo passo: Execute 'streamlit run app.py'")
    print("\n📊 Resumo:")
    print(f"   • {len(rfm_to_save)} clientes segmentados")
    print(f"   • {len(rfm['cluster'].unique())} clusters criados")
    print(f"   • Tabelas criadas: customer_segments, elbow_data")
    print("\n✅ Tudo pronto para o dashboard!\n")

if __name__ == "__main__":
    try:
        calculate_rfm_and_segment()
    except Exception as e:
        print(f"\n❌ ERRO CRÍTICO: {e}")
        import traceback
        print("\n📋 Detalhes do erro:")
        traceback.print_exc()