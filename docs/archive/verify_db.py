import asyncio
import asyncpg
import os
from dotenv import load_dotenv

async def verify():
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    if db_url.startswith("postgresql+asyncpg://"):
        db_url = db_url.replace("postgresql+asyncpg://", "postgresql://")
    
    print(f"Attempting to connect to: {db_url.split('@')[1] if '@' in db_url else db_url}")
    
    try:
        conn = await asyncpg.connect(db_url)
        print("Database Connection: SUCCESS")
        
        version = await conn.fetchval("SELECT version();")
        print(f"PostgreSQL Version: {version}")
        
        tables = await conn.fetch('''
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        ''')
        
        table_names = [t['table_name'] for t in tables]
        print("\nTables Found:")
        for t in table_names:
            print(f"- {t}")
            
        expected_tables = ['users', 'reports', 'audit_logs', 'functions', 'generated_tests']
        missing_tables = [t for t in expected_tables if t not in table_names]
        
        if missing_tables:
            print("\nMissing Tables:")
            for t in missing_tables:
                print(f"- {t}")
        else:
            print("\nAll expected tables found!")
            
        await conn.close()
    except Exception as e:
        print("Database Connection: FAILED")
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(verify())
