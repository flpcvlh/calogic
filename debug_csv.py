"""
debug_csv.py - Diagnostica o formato do CSV
"""

import pandas as pd

print("🔍 Analisando o CSV...")

df = pd.read_csv('data/mock_orders_for_rfm.csv', sep=';')

print(f"\n📊 Total de linhas: {len(df)}")
print(f"\n📋 Colunas: {list(df.columns)}")
print(f"\n🔍 Primeiras 5 linhas:")
print(df.head())

print(f"\n📊 Tipos de dados:")
print(df.dtypes)

print(f"\n🔍 Amostra da coluna totalAmount:")
print(df['totalAmount'].head(20))

print(f"\n📊 Valores únicos de totalAmount (primeiros 20):")
print(df['totalAmount'].unique()[:20])

print(f"\n✅ Valores não-nulos:")
print(df['totalAmount'].notna().sum())

print(f"\n❌ Valores nulos:")
print(df['totalAmount'].isna().sum())