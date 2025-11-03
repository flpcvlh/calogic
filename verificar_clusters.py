"""
Script para verificar se os clusters estão corretos
"""

from sqlalchemy import create_engine
import pandas as pd
import streamlit as st

# Conectar ao banco
engine = create_engine(st.secrets["NEON_DB_URL"])

# Carregar dados
df = pd.read_sql("SELECT * FROM customer_segments", engine)

# Analisar cada cluster
print("\n" + "="*60)
print("🔍 VERIFICAÇÃO DOS CLUSTERS")
print("="*60)

for cluster_id in sorted(df['cluster_id'].unique()):
    df_cluster = df[df['cluster_id'] == cluster_id]
    
    print(f"\n📊 CLUSTER {cluster_id}:")
    print(f"   Clientes: {len(df_cluster)}")
    print(f"   📅 Recência Média: {df_cluster['recency'].mean():.1f} dias")
    print(f"   🔄 Frequência Média: {df_cluster['frequency'].mean():.1f}")
    print(f"   💰 Valor Médio: R$ {df_cluster['monetary'].mean():.2f}")
    print(f"   💵 Receita Total: R$ {df_cluster['monetary'].sum():.2f}")

print("\n" + "="*60)
print("✅ INTERPRETAÇÃO ESPERADA:")
print("="*60)
print("Cluster 0 (Campeões):  Recência BAIXA + Frequência ALTA + Valor ALTO")
print("Cluster 1 (Fiéis):     Recência MÉDIA + Frequência BOA + Valor BOM")
print("Cluster 2 (Em Risco):  Recência ALTA + Frequência MÉDIA + Valor MÉDIO")
print("Cluster 3 (Perdidos):  Recência MUITO ALTA + Frequência BAIXA + Valor VARIADO")
print("="*60 + "\n")