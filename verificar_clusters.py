"""
Script para verificar se os clusters estão corretos
"""

from sqlalchemy import create_engine
import pandas as pd
import streamlit as st

print("\n" + "="*70)
print("🔍 VERIFICAÇÃO COMPLETA DOS CLUSTERS")
print("="*70)

# Conectar ao banco
engine = create_engine(st.secrets["NEON_DB_URL"])

# Verificar se a tabela existe
try:
    df = pd.read_sql("SELECT * FROM customer_segments", engine)
    print(f"\n📊 Total de clientes na base: {len(df)}")
    print(f"📊 Clusters encontrados: {sorted(df['cluster_id'].unique())}")
except Exception as e:
    print(f"\n❌ ERRO: Tabela 'customer_segments' não encontrada!")
    print(f"Detalhes: {e}")
    print("\n💡 SOLUÇÃO: Execute primeiro: python ml_engine.py")
    exit()

print("\n" + "="*70)
print("📈 ANÁLISE DETALHADA POR CLUSTER")
print("="*70)

# Analisar cada cluster
for cluster_id in sorted(df['cluster_id'].unique()):
    cluster_df = df[df['cluster_id'] == cluster_id]
    
    rec_avg = cluster_df['recency'].mean()
    freq_avg = cluster_df['frequency'].mean()
    mon_avg = cluster_df['monetary'].mean()
    
    print(f"\n{'='*70}")
    print(f"🎯 CLUSTER {cluster_id}")
    print(f"{'='*70}")
    print(f"   👥 Total de Clientes: {len(cluster_df)} ({len(cluster_df)/len(df)*100:.1f}%)")
    print(f"   📅 Recência Média: {rec_avg:.1f} dias")
    print(f"   🔄 Frequência Média: {freq_avg:.2f} pedidos")
    print(f"   💰 Valor Médio: R$ {mon_avg:,.2f}")
    print(f"   💵 Receita Total: R$ {cluster_df['monetary'].sum():,.2f}")
    
    # Análise de distribuição
    print(f"\n   📊 Distribuição de Recência:")
    print(f"      Min: {cluster_df['recency'].min():.0f} dias")
    print(f"      Q1 (25%): {cluster_df['recency'].quantile(0.25):.0f} dias")
    print(f"      Mediana: {cluster_df['recency'].median():.0f} dias")
    print(f"      Q3 (75%): {cluster_df['recency'].quantile(0.75):.0f} dias")
    print(f"      Max: {cluster_df['recency'].max():.0f} dias")
    
    print(f"\n   📊 Distribuição de Frequência:")
    print(f"      Min: {cluster_df['frequency'].min():.0f} pedidos")
    print(f"      Mediana: {cluster_df['frequency'].median():.0f} pedidos")
    print(f"      Max: {cluster_df['frequency'].max():.0f} pedidos")

# Criar resumo comparativo
print("\n" + "="*70)
print("📊 RESUMO COMPARATIVO (ordenado por score)")
print("="*70)

summary = df.groupby('cluster_id').agg({
    'recency': 'mean',
    'frequency': 'mean',
    'monetary': 'mean',
    'customer_id': 'count'
}).round(2)

summary.columns = ['Recência Média', 'Frequência Média', 'Valor Médio', 'Total Clientes']

# Calcular score
summary['Score RFM'] = (
    (1 / (summary['Recência Média'] + 1)) * 1000 +
    summary['Frequência Média'] * 10 +
    summary['Valor Médio'] / 100
)

# Ordenar por score (maior = melhor)
summary = summary.sort_values('Score RFM', ascending=False)

print(summary.to_string())

print("\n" + "="*70)
print("✅ INTERPRETAÇÃO CORRETA ESPERADA:")
print("="*70)
print("🏆 Cluster 0 (Campeões):  Recência BAIXA + Frequência ALTA + Valor ALTO")
print("💎 Cluster 1 (Fiéis):     Recência MÉDIA + Frequência BOA + Valor BOM")
print("⚠️  Cluster 2 (Em Risco):  Recência ALTA + Frequência MÉDIA + Valor MÉDIO")
print("💔 Cluster 3 (Perdidos):  Recência MUITO ALTA + Frequência BAIXA + Valor VARIADO")

print("\n" + "="*70)
print("🔍 DIAGNÓSTICO AUTOMÁTICO:")
print("="*70)

# Verificar se está correto
clusters_ordenados = summary.sort_values('Score RFM', ascending=False).index.tolist()

print(f"\n📊 Ordem atual dos clusters (do melhor pro pior): {clusters_ordenados}")

if clusters_ordenados == [0, 1, 2, 3]:
    print("\n✅ ✅ ✅ CLUSTERS ESTÃO CORRETOS! ✅ ✅ ✅")
else:
    print("\n🚨 🚨 🚨 CLUSTERS ESTÃO INVERTIDOS! 🚨 🚨 🚨")
    print("\n💡 Execute novamente: python ml_engine.py")

print("\n" + "="*70)