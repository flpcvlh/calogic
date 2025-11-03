"""
setup_db.py - Script ETL para configuração do banco de dados
Lê o arquivo CSV e carrega os dados no PostgreSQL (Neon)
Execute uma vez antes de rodar o app
"""

import pandas as pd
from sqlalchemy import create_engine, text
import os
from pathlib import Path

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

def setup_database():
    """Configura o banco de dados e carrega os dados do CSV"""
    
    print("🚀 Iniciando configuração do banco de dados...")
    
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
    
    # Conexão com o banco Neon
    try:
        engine = create_engine(db_url)
        print("✅ Conexão com Neon estabelecida!")
    except Exception as e:
        print(f"❌ Erro ao conectar com o banco: {e}")
        return
    
    # Ler o arquivo CSV com separador correto (ponto e vírgula)
    try:
        df = pd.read_csv('data/mock_orders_for_rfm.csv', sep=';')
        print(f"✅ CSV carregado: {len(df)} registros encontrados")
        print(f"📊 Colunas: {list(df.columns)}")
        print(f"📋 Amostra dos dados brutos:")
        print(df.head(3))
    except Exception as e:
        print(f"❌ Erro ao ler CSV: {e}")
        return
    
    # Preparar DataFrame para inserção
    try:
        df_to_load = df.copy()
        
        # Renomear colunas para match com a tabela
        column_mapping = {
            'id': 'id',
            'customer': 'customer',
            'createdAt': 'created_at',
            'totalAmount': 'total_amount',
            'status': 'status',
            'salesChannel': 'sales_channel'
        }
        
        df_to_load = df_to_load.rename(columns=column_mapping)
        
        # CRÍTICO: Converter totalAmount (formato brasileiro com vírgula)
        print("\n🔧 Convertendo total_amount (formato BR: vírgula para ponto)...")
        df_to_load['total_amount'] = df_to_load['total_amount'].astype(str).str.replace(',', '.', regex=False)
        df_to_load['total_amount'] = pd.to_numeric(df_to_load['total_amount'], errors='coerce')
        
        print(f"  ✅ Valores convertidos: {df_to_load['total_amount'].notna().sum()}")
        print(f"  ❌ Valores nulos após conversão: {df_to_load['total_amount'].isna().sum()}")
        
        # Converter createdAt para datetime (formato DD/MM/YYYY HH:MM)
        print("\n🔧 Convertendo datas (formato DD/MM/YYYY)...")
        df_to_load['created_at'] = pd.to_datetime(
            df_to_load['created_at'], 
            format='%d/%m/%Y %H:%M',
            errors='coerce'
        )
        
        print(f"  ✅ Datas convertidas: {df_to_load['created_at'].notna().sum()}")
        print(f"  ❌ Datas nulas após conversão: {df_to_load['created_at'].isna().sum()}")
        
        print(f"\n📊 Estrutura final para inserção:")
        print(df_to_load.head(3))
        print(f"\n📋 Tipos de dados:")
        print(df_to_load.dtypes)
        
    except Exception as e:
        print(f"❌ Erro ao preparar dados: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Criar tabela orders (se não existir)
    with engine.connect() as conn:
        # Drop table if exists (para recriar)
        print("\n🗑️  Removendo tabela antiga (se existir)...")
        conn.execute(text("DROP TABLE IF EXISTS orders CASCADE"))
        conn.commit()
        
        # Criar tabela com estrutura correta baseada no CSV
        print("📦 Criando tabela 'orders'...")
        create_table_query = """
        CREATE TABLE orders (
            id VARCHAR(100) PRIMARY KEY,
            customer VARCHAR(100),
            created_at TIMESTAMP,
            total_amount DECIMAL(10, 2),
            status VARCHAR(50),
            sales_channel VARCHAR(50)
        )
        """
        conn.execute(text(create_table_query))
        conn.commit()
        print("✅ Tabela 'orders' criada com sucesso!")
    
    # Inserir dados no banco
    try:
        print(f"\n💾 Inserindo {len(df_to_load)} registros...")
        df_to_load.to_sql('orders', engine, if_exists='append', index=False)
        print(f"✅ {len(df_to_load)} registros inseridos na tabela 'orders'!")
        
    except Exception as e:
        print(f"❌ Erro ao inserir dados: {e}")
        print(f"\n🔍 Detalhes do DataFrame:")
        print(df_to_load.info())
        import traceback
        traceback.print_exc()
        return
    
    # Verificar dados inseridos
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) as total FROM orders"))
        total = result.fetchone()[0]
        print(f"\n✅ Total de registros na tabela: {total}")
        
        # Mostrar amostra
        result = conn.execute(text("SELECT * FROM orders LIMIT 5"))
        print("\n📋 Amostra dos dados inseridos:")
        for row in result:
            print(row)
        
        # Estatísticas por status
        result = conn.execute(text("""
            SELECT status, COUNT(*) as total 
            FROM orders 
            GROUP BY status 
            ORDER BY total DESC
        """))
        print("\n📊 Distribuição por Status:")
        for row in result:
            print(f"  {row[0]}: {row[1]} pedidos")
        
        # Verificar valores de total_amount
        result = conn.execute(text("""
            SELECT 
                COUNT(*) as total,
                COUNT(total_amount) as com_valor,
                SUM(CASE WHEN total_amount IS NULL THEN 1 ELSE 0 END) as nulos,
                AVG(total_amount) as media,
                MIN(total_amount) as minimo,
                MAX(total_amount) as maximo
            FROM orders
        """))
        row = result.fetchone()
        print("\n💰 Estatísticas de total_amount:")
        print(f"  Total de pedidos: {row[0]}")
        print(f"  Com valor: {row[1]}")
        print(f"  Nulos: {row[2]}")
        print(f"  Média: R$ {row[3]:.2f}" if row[3] else "  Média: N/A")
        print(f"  Mínimo: R$ {row[4]:.2f}" if row[4] else "  Mínimo: N/A")
        print(f"  Máximo: R$ {row[5]:.2f}" if row[5] else "  Máximo: N/A")
    
    print("\n" + "="*60)
    print("🎉 CONFIGURAÇÃO DO BANCO CONCLUÍDA COM SUCESSO!")
    print("="*60)
    print("\n💡 Próximo passo: Execute 'python ml_engine.py'\n")

if __name__ == "__main__":
    setup_database()