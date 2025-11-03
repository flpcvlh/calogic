"""
check_database.py - Verifica o estado do banco de dados
"""

from sqlalchemy import create_engine, inspect, text
import streamlit as st

def check_database():
    """Verifica quais tabelas existem no banco"""
    
    print("🔍 Verificando estado do banco de dados...")
    
    try:
        engine = create_engine(st.secrets["NEON_DB_URL"])
        print("✅ Conexão estabelecida!")
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return
    
    # Listar tabelas
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    print(f"\n📊 Tabelas encontradas no banco ({len(tables)}):")
    for table in tables:
        print(f"  ✅ {table}")
    
    # Verificar tabelas necessárias
    required_tables = ['orders', 'customer_segments', 'elbow_data']
    missing_tables = [table for table in required_tables if table not in tables]
    
    if missing_tables:
        print(f"\n❌ Tabelas FALTANDO ({len(missing_tables)}):")
        for table in missing_tables:
            print(f"  ❌ {table}")
        
        print("\n💡 Para criar as tabelas faltando:")
        if 'orders' in missing_tables:
            print("   1. Execute: python setup_db.py")
        if 'customer_segments' in missing_tables or 'elbow_data' in missing_tables:
            print("   2. Execute: python ml_engine.py")
    else:
        print("\n✅ Todas as tabelas necessárias existem!")
        
        # Contar registros
        with engine.connect() as conn:
            for table in required_tables:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.fetchone()[0]
                print(f"  📊 {table}: {count} registros")

if __name__ == "__main__":
    check_database()