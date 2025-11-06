"""
Motor de Machine Learning - Análise RFM e K-Means Clustering
Calogic - Sistema de Segmentação de Clientes
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sqlalchemy import create_engine, text
import streamlit as st
from datetime import datetime

print("\n" + "="*70)
print("🤖 CALOGIC - MOTOR DE MACHINE LEARNING")
print("="*70)

# Conectar ao banco de dados
print("\n📊 Conectando ao banco de dados...")
engine = create_engine(st.secrets["NEON_DB_URL"])

# Verificar se a tabela orders existe
print("🔍 Verificando se a tabela 'orders' existe...")
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM orders"))
        total_orders = result.fetchone()[0]
        print(f"✅ Tabela 'orders' encontrada com {total_orders} pedidos!")
except Exception as e:
    print(f"\n❌ ERRO: Tabela 'orders' não encontrada!")
    print(f"Detalhes: {e}")
    print("\n💡 SOLUÇÃO: Execute primeiro: python setup_db.py")
    exit()

# Calcular RFM diretamente da tabela orders
print("\n🔬 Calculando métricas RFM dos pedidos...")

# Data de referência (hoje)
reference_date = datetime.now()
print(f"📅 Data de referência: {reference_date.strftime('%Y-%m-%d')}")

# Query para calcular RFM
rfm_query = f"""
WITH customer_metrics AS (
    SELECT 
        customer,
        MAX(created_at) as last_order_date,
        COUNT(*) as total_orders,
        SUM(total_amount) as total_spent
    FROM orders
    WHERE total_amount IS NOT NULL
    GROUP BY customer
)
SELECT 
    customer as customer_id,
    EXTRACT(DAY FROM (TIMESTAMP '{reference_date}' - last_order_date))::INTEGER as recency,
    total_orders as frequency,
    total_spent as monetary
FROM customer_metrics
WHERE total_spent > 0
ORDER BY customer
"""

print("📥 Executando query RFM...")
df = pd.read_sql(rfm_query, engine)

if len(df) == 0:
    print("\n❌ ERRO: Nenhum cliente encontrado com pedidos válidos!")
    print("💡 Verifique se há pedidos com total_amount válido na tabela orders")
    exit()

print(f"✅ {len(df)} clientes carregados com sucesso!")

# Validação dos dados
print("\n🔍 Validando dados...")
print(f"   - Valores nulos: {df.isnull().sum().sum()}")
print(f"   - Duplicatas: {df.duplicated().sum()}")

if df.isnull().sum().sum() > 0:
    print("⚠️  Removendo valores nulos...")
    df = df.dropna()

# Estatísticas básicas
print("\n📊 Estatísticas RFM:")
print(df[['recency', 'frequency', 'monetary']].describe())

# Preparar features para clustering
print("\n🔬 Preparando features para clustering...")
X = df[['recency', 'frequency', 'monetary']].values

# Normalizar dados
print("📐 Normalizando dados com StandardScaler...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Aplicar K-Means
print("\n🎯 Aplicando K-Means Clustering...")
print("   Número de clusters: 4")
print("   Algoritmo: K-Means++")
print("   Max iterações: 300")

kmeans = KMeans(
    n_clusters=4,
    init='k-means++',
    n_init=10,
    max_iter=300,
    random_state=42
)

df['cluster_id'] = kmeans.fit_predict(X_scaled)

print(f"✅ Clustering concluído!")
print(f"   Inércia: {kmeans.inertia_:.2f}")

# ====== MAPEAMENTO CORRETO DOS CLUSTERS ======
print("\n🔄 Aplicando mapeamento correto dos clusters...")

# Calcular médias por cluster ANTES do mapeamento
cluster_means = df.groupby('cluster_id').agg({
    'recency': 'mean',
    'frequency': 'mean',
    'monetary': 'mean'
}).round(2)

print("\n📊 Médias ANTES do remapeamento:")
print(cluster_means)

# Criar score RFM (quanto MAIOR, MELHOR o cluster)
cluster_means['score'] = (
    (1 / (cluster_means['recency'] + 1)) * 1000 +  # Recência baixa = bom
    cluster_means['frequency'] * 10 +               # Frequência alta = bom
    cluster_means['monetary'] / 100                 # Valor alto = bom
)

print("\n📈 Scores calculados:")
print(cluster_means[['score']].sort_values('score', ascending=False))

# Ordenar clusters por score (do MELHOR pro PIOR)
cluster_means = cluster_means.sort_values('score', ascending=False)

# Criar mapeamento CORRETO
# O cluster com MAIOR score vira 0 (Campeões)
# O cluster com MENOR score vira 3 (Perdidos)
cluster_mapping = {}
for i, cluster_original in enumerate(cluster_means.index):
    cluster_mapping[cluster_original] = i

print("\n🔄 Mapeamento aplicado:")
cluster_names = {0: "🏆 Campeões", 1: "💎 Fiéis", 2: "⚠️ Em Risco", 3: "💔 Perdidos"}
for old, new in cluster_mapping.items():
    print(f"   Cluster K-Means {old} → Cluster Final {new} ({cluster_names[new]})")

# Aplicar o mapeamento
df['cluster_id'] = df['cluster_id'].map(cluster_mapping)

print("\n✅ Clusters remapeados com sucesso!")

# Verificar resultado final
print("\n📊 Médias APÓS remapeamento:")
final_summary = df.groupby('cluster_id').agg({
    'recency': 'mean',
    'frequency': 'mean',
    'monetary': 'mean'
}).round(2)
print(final_summary)

# Análise por cluster
print("\n" + "="*70)
print("📈 ANÁLISE DETALHADA POR CLUSTER")
print("="*70)

for cluster_id in [0, 1, 2, 3]:
    cluster_df = df[df['cluster_id'] == cluster_id]
    
    print(f"\n{cluster_names[cluster_id]}:")
    print(f"   Clientes: {len(cluster_df)} ({len(cluster_df)/len(df)*100:.1f}%)")
    print(f"   Recência: {cluster_df['recency'].mean():.1f} dias")
    print(f"   Frequência: {cluster_df['frequency'].mean():.2f} pedidos")
    print(f"   Valor Médio: R$ {cluster_df['monetary'].mean():,.2f}")
    print(f"   Receita Total: R$ {cluster_df['monetary'].sum():,.2f}")

# Salvar no banco
print("\n💾 Salvando resultados no banco de dados...")

# Drop da tabela antiga se existir
with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS customer_segments"))
    conn.commit()

# Salvar nova tabela
df.to_sql('customer_segments', engine, if_exists='replace', index=False)
print("✅ Dados salvos na tabela 'customer_segments'!")

# Estatísticas finais
print("\n" + "="*70)
print("📊 RESUMO FINAL")
print("="*70)
print(f"Total de clientes segmentados: {len(df)}")
print(f"Receita total: R$ {df['monetary'].sum():,.2f}")
print(f"Ticket médio geral: R$ {df['monetary'].mean():,.2f}")
print(f"Frequência média geral: {df['frequency'].mean():.2f}")
print(f"Recência média geral: {df['recency'].mean():.1f} dias")

print("\n✅ Processamento concluído com sucesso!")
print("="*70 + "\n")